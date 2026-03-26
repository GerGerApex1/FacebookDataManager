"""
face_detection.py
-----------------
Provides GPU/CPU face detection and image-copying logic for the
FacebookDataManager application.

Public API
----------
is_gpu_available() -> bool
    Module-level helper — call this from any other class to know whether
    CUDA processing is available before constructing FaceDetectionWorker.

get_cuda_unavailable_reason() -> str
    Returns a human-readable string explaining *why* CUDA is unavailable,
    or an empty string if CUDA is available.

FaceDetectionWorker(QThread)
    Background worker that scans a source directory recursively, counts
    detected faces in every image using MTCNN (facenet-pytorch), and copies
    qualifying images (face_count >= min_faces) to a destination directory.

    Signals
    -------
    progress(int)               overall 0-100 progress value
    log(str)                    human-readable status / error line
    stats_updated(int, int, int) (processed, copied, errors) running totals
    finished()                  emitted when the run is complete or cancelled
    error(str)                  emitted on a fatal, unrecoverable error

    Usage
    -----
    worker = FaceDetectionWorker(
        src_dir="/photos/raw",
        dest_dir="/photos/with_faces",
        min_faces=1,
        threads=8,
        use_gpu=True,           # falls back to CPU if CUDA is unavailable
        prevent_duplicates=True,
        confidence_level=0.7,   # 0.0 (lenient) to 1.0 (strict)
    )
    worker.progress.connect(progress_bar.setValue)
    worker.log.connect(log_widget.append)
    worker.stats_updated.connect(lambda p, c, e: ...)
    worker.finished.connect(on_done)
    worker.start()

    # To stop early:
    worker.cancel()
"""

from __future__ import annotations

import hashlib
import logging
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import cv2
import torch
from uniface.detection import RetinaFace
from PIL import Image
from PySide6.QtCore import QThread, Signal

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Module-level GPU helper (importable by any other class / module)
# ---------------------------------------------------------------------------

def is_gpu_available() -> bool:
    """Return ``True`` if a CUDA-capable GPU is present and usable by PyTorch.

    This function can be called from any other class to decide whether to
    offer GPU processing as an option before constructing a
    :class:`FaceDetectionWorker`.

    Example::

        from modules.face_detection import is_gpu_available

        if is_gpu_available():
            label.setText("GPU (CUDA)")
        else:
            label.setText("CPU only")
    """
    return torch.cuda.is_available()


def get_cuda_unavailable_reason() -> str:
    """Return a human-readable explanation of why CUDA is not available.

    Returns an empty string if CUDA *is* available, so callers can do::

        reason = get_cuda_unavailable_reason()
        if reason:
            label.setText(f"GPU unavailable: {reason}")

    Possible reasons diagnosed
    --------------------------
    * PyTorch was installed as a CPU-only build (no CUDA compiled in).
    * No CUDA-capable NVIDIA GPU was detected by the driver.
    * CUDA is compiled in but the driver / runtime is incompatible.
    """
    if torch.cuda.is_available():
        return ""

    if torch.version.cuda is None:
        return (
            "PyTorch was installed without CUDA support (CPU-only build). "
            "Reinstall PyTorch with a CUDA-enabled wheel from https://pytorch.org/get-started/locally/."
        )

    if torch.cuda.device_count() == 0:
        return (
            f"PyTorch was built with CUDA {torch.version.cuda}, but no CUDA-capable "
            "GPU was detected. Ensure an NVIDIA GPU is present and that the correct "
            "driver is installed."
        )

    return (
        f"PyTorch was built with CUDA {torch.version.cuda}, but CUDA is still not "
        "usable. Your NVIDIA driver may be outdated or incompatible with this CUDA "
        "version. Try updating the driver from https://www.nvidia.com/drivers."
    )


# ---------------------------------------------------------------------------
# Worker thread
# ---------------------------------------------------------------------------

class FaceDetectionWorker(QThread):
    """Background thread that detects faces and copies matching images.

    Parameters
    ----------
    src_dir:
        Root directory to scan recursively for image files.
    dest_dir:
        Directory where qualifying images are copied.  Created automatically.
    min_faces:
        Minimum number of detected faces required to copy an image (≥ 1).
    max_faces:
        Maximum number of detected faces allowed to copy an image.
        Set to 0 for unlimited. If set, only images with faces in the range
        [min_faces, max_faces] are copied. Default is 0 (unlimited).
    threads:
        Number of parallel worker threads for CPU mode.  Ignored in GPU mode
        (GPU mode always uses a single thread to avoid CUDA context races).
    use_gpu:
        Request GPU (CUDA) acceleration.  If CUDA is not available the worker
        silently falls back to CPU and logs a notice.
    prevent_duplicates:
        When ``True`` an MD5 hash is computed for each qualifying image and
        files identical to one already copied are skipped.
    confidence_level:
        Detection confidence threshold (0.0–1.0). Higher values are stricter,
        resulting in fewer but more confident face detections. Default is 0.7.
    """

    # --- Signals ---
    progress      = Signal(int)        # 0 – 100
    log           = Signal(str)        # one log line
    stats_updated = Signal(int, int, int)  # processed, copied, errors
    finished      = Signal()
    error         = Signal(str)        # fatal error message

    _IMAGE_EXTENSIONS: frozenset[str] = frozenset(
        {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff", ".tif"}
    )

    def __init__(
        self,
        src_dir: str,
        dest_dir: str,
        min_faces: int = 1,
        max_faces: int = 0,
        threads: int = 4,
        use_gpu: bool = False,
        prevent_duplicates: bool = True,
        confidence_level: float = 0.7,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.src_dir  = Path(src_dir)
        self.dest_dir = Path(dest_dir)
        self.min_faces = max(1, min_faces)
        self.max_faces = max(0, max_faces)  # 0 means unlimited
        self.threads   = max(1, threads)
        self.prevent_duplicates = prevent_duplicates
        # Clamp confidence level to 0.0-1.0 range
        self.confidence_level = max(0.0, min(1.0, confidence_level))

        # Resolve GPU availability at construction time
        if use_gpu and not is_gpu_available():
            self._device = "cpu"
            self._gpu_requested_but_unavailable = True
        else:
            self._device = "cuda" if use_gpu else "cpu"
            self._gpu_requested_but_unavailable = False

        self._cancel_event = threading.Event()

    # ------------------------------------------------------------------
    # Public control
    # ------------------------------------------------------------------

    def cancel(self) -> None:
        """Ask the worker to stop after the current image finishes."""
        self._cancel_event.set()

    @property
    def using_gpu(self) -> bool:
        """``True`` when this worker is running on a CUDA device."""
        return self._device == "cuda"

    # ------------------------------------------------------------------
    # QThread entry point
    # ------------------------------------------------------------------

    def run(self) -> None:  # noqa: C901  (complexity is justified here)
        self._cancel_event.clear()

        # --- Warn if GPU was requested but unavailable ---
        if self._gpu_requested_but_unavailable:
            msg = "[WARN] CUDA not available — falling back to CPU processing."
            logger.warning("CUDA not available — falling back to CPU processing.")
            self.log.emit(msg)

        device = self._device

        # --- Collect image paths ---
        try:
            image_files: list[Path] = [
                p
                for p in self.src_dir.rglob("*")
                if p.is_file() and p.suffix.lower() in self._IMAGE_EXTENSIONS
            ]
        except OSError as exc:
            logger.error("Cannot scan source directory: %s", exc)
            self.error.emit(f"Cannot scan source directory: {exc}")
            return

        total = len(image_files)
        if total == 0:
            logger.warning("No image files found in source directory.")
            self.log.emit("No image files found in source directory.")
            self.finished.emit()
            return

        # --- Prepare destination ---
        try:
            self.dest_dir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            logger.error("Cannot create destination directory: %s", exc)
            self.error.emit(f"Cannot create destination directory: {exc}")
            return

        max_faces_str = f"max={self.max_faces}" if self.max_faces > 0 else "no limit"
        msg = (
            f"Found {total} image(s) | device={device.upper()} | "
            f"faces={self.min_faces}-{max_faces_str} | threads={self.threads} | "
            f"confidence={self.confidence_level:.2f}"
        )
        logger.info(msg)
        self.log.emit(msg)

        # --- Shared mutable state (all guarded by _lock) ---
        _lock            = threading.Lock()
        _processed       = [0]
        _copied          = [0]
        _errors          = [0]
        _seen_hashes:  set[str] = set()   # MD5 digests of copied files
        _reserved_paths: set[str] = set() # destination paths already claimed

        # --- Pre-seed hashes from files already in the destination ---
        # This prevents re-copying files from a previous run.
        if self.prevent_duplicates:
            existing = [
                p
                for p in self.dest_dir.rglob("*")
                if p.is_file() and p.suffix.lower() in self._IMAGE_EXTENSIONS
            ]
            if existing:
                msg = (
                    f"Hashing {len(existing)} existing file(s) in destination "
                    f"to skip already-processed images…"
                )
                logger.info(msg)
                self.log.emit(msg)
                for p in existing:
                    if self._cancel_event.is_set():
                        self.finished.emit()
                        return
                    try:
                        _seen_hashes.add(_md5(p))
                        _reserved_paths.add(str(p))
                    except OSError as exc:
                        msg = f"[WARN] Cannot hash existing file {p.name}: {exc}"
                        logger.warning("Cannot hash existing file %s: %s", p.name, exc)
                        self.log.emit(msg)
                msg = f"Pre-scan complete — {len(_seen_hashes)} unique hash(es) loaded."
                logger.info(msg)
                self.log.emit(msg)

        # --- Thread-local RetinaFace instances (one detector per OS thread) ---
        # Using thread-local detectors avoids CUDA context races on multiple
        # GPU threads and avoids the GIL serialising CPU inference.
        _thread_local = threading.local()

        def _get_detector() -> RetinaFace:
            if not hasattr(_thread_local, "detector"):
                # Determine execution providers based on device
                if device == "cuda":
                    providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
                else:
                    providers = ["CPUExecutionProvider"]
                
                _thread_local.detector = RetinaFace(providers=providers)
            return _thread_local.detector

        # --- Unique destination path (must be called under _lock) ---
        def _claim_dest(src_path: Path) -> Path:
            candidate = self.dest_dir / src_path.name
            counter   = 1
            while candidate.exists() or str(candidate) in _reserved_paths:
                candidate = (
                    self.dest_dir / f"{src_path.stem}_{counter}{src_path.suffix}"
                )
                counter += 1
            _reserved_paths.add(str(candidate))
            return candidate

        # --- Per-image processing function ---
        def _process(img_path: Path) -> None:
            if self._cancel_event.is_set():
                return

            # 1. Detect faces
            try:
                # RetinaFace expects BGR format from OpenCV
                img_cv = cv2.imread(str(img_path))
                if img_cv is None:
                    raise ValueError(f"Failed to load image: {img_path.name}")
                
                # Calculate detection threshold based on confidence level
                # confidence_level ranges from 0.0 (lenient) to 1.0 (strict)
                # Map to detection threshold: 0.5–1.0 range (RetinaFace's natural range)
                det_thresh = 0.5 + (self.confidence_level * 0.5)  # 0.5-1.0 range
                
                detector = _get_detector()
                faces = detector.detect(img_cv)
                
                # Filter faces by confidence threshold
                confident_faces = [
                    f for f in faces
                    if hasattr(f, "confidence") and f.confidence >= det_thresh
                ]
                face_count = len(confident_faces)
            except Exception as exc:
                with _lock:
                    _errors[0] += 1
                    stats = (_processed[0], _copied[0], _errors[0])
                msg = f"[ERROR]  {img_path.name}: {exc}"
                logger.error("Face detection error on %s: %s", img_path.name, exc)
                self.log.emit(msg)
                self.stats_updated.emit(*stats)
                return

            # 2. Check face count range
            in_range = face_count >= self.min_faces
            if self.max_faces > 0:
                in_range = in_range and face_count <= self.max_faces
            
            if not in_range:
                max_faces_str = f"-{self.max_faces}" if self.max_faces > 0 else "+"
                msg = f"[SKIP]   {img_path.name}  ({face_count} face(s), want {self.min_faces}{max_faces_str})"
                logger.debug(msg)
                self.log.emit(msg)
                with _lock:
                    _processed[0] += 1
                    stats = (_processed[0], _copied[0], _errors[0])
                self.progress.emit(int(_processed[0] / total * 100))
                self.stats_updated.emit(*stats)
                return

            # 3. Duplicate check (hash computed outside the lock to avoid I/O
            #    stalls while holding it, then validated inside the lock)
            if self.prevent_duplicates:
                try:
                    digest = _md5(img_path)
                except OSError as exc:
                    with _lock:
                        _errors[0] += 1
                    msg = f"[ERROR]  Cannot hash {img_path.name}: {exc}"
                    logger.error("Cannot hash %s: %s", img_path.name, exc)
                    self.log.emit(msg)
                    return

                with _lock:
                    if digest in _seen_hashes:
                        msg = f"[SKIP-DUP] {img_path.name}"
                        logger.debug(msg)
                        self.log.emit(msg)
                        _processed[0] += 1
                        stats = (_processed[0], _copied[0], _errors[0])
                        self.progress.emit(int(_processed[0] / total * 100))
                        self.stats_updated.emit(*stats)
                        return
                    _seen_hashes.add(digest)

            # 4. Claim a unique destination path (under lock) then copy outside
            with _lock:
                dest_path = _claim_dest(img_path)

            try:
                shutil.copy2(img_path, dest_path)
            except OSError as exc:
                with _lock:
                    _errors[0] += 1
                    _reserved_paths.discard(str(dest_path))  # release claim
                msg = f"[ERROR]  Copy failed {img_path.name}: {exc}"
                logger.error("Copy failed %s: %s", img_path.name, exc)
                self.log.emit(msg)
                return

            with _lock:
                _copied[0]    += 1
                _processed[0] += 1
                stats = (_processed[0], _copied[0], _errors[0])

            msg = (
                f"[COPIED] {img_path.name}  ({face_count} face(s))"
                f"  →  {dest_path.name}"
            )
            logger.info(msg)
            self.log.emit(msg)
            self.progress.emit(int(_processed[0] / total * 100))
            self.stats_updated.emit(*stats)

        # --- Execute ---
        # GPU: single thread — CUDA is already internally parallel and
        #      sharing an MTCNN across threads risks context errors.
        # CPU: use the configured thread count for I/O + inference overlap.
        effective_threads = 1 if self._device == "cuda" else self.threads

        with ThreadPoolExecutor(max_workers=effective_threads) as executor:
            future_map = {executor.submit(_process, p): p for p in image_files}
            for future in as_completed(future_map):
                if self._cancel_event.is_set():
                    for pending in future_map:
                        pending.cancel()
                    logger.info("Processing cancelled by user.")
                    self.log.emit("Processing cancelled by user.")
                    break
                try:
                    future.result()   # re-raise any unhandled exception
                except Exception as exc:
                    img_path = future_map[future]
                    msg = f"[UNHANDLED] {img_path.name}: {exc}"
                    logger.exception("Unhandled error processing %s", img_path.name)
                    self.log.emit(msg)

        with _lock:
            p, c, e = _processed[0], _copied[0], _errors[0]

        if not self._cancel_event.is_set():
            msg = f"Completed — Processed: {p} | Copied: {c} | Errors: {e}"
            logger.info(msg)
            self.log.emit(msg)
        self.finished.emit()


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _md5(path: Path) -> str:
    """Return the hex MD5 digest of *path* using buffered reads."""
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65_536), b""):
            h.update(chunk)
    return h.hexdigest()
