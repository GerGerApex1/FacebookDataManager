"""
file_transfer.py
----------------
Copies media files from a Facebook data-export inbox to a destination
directory, filtering conversation folders by ID and files by type and MD5
hash to avoid duplicates.

Public API
----------
transfer_files(source_dir, dest_dir, ids, progress_callback, include_types, is_cancelled=None)
    Pure-function entry point.  Resolves ``<source_dir>/messages/inbox/``,
    keeps only folders whose name contains at least one of the provided
    conversation IDs, then recursively copies qualifying files.

FileTransferWorker(QThread)
    Qt background thread that wraps :func:`transfer_files` and exposes
    results via signals so the GUI thread can update the progress bar, log,
    and counters without blocking.

    Signals
    -------
    progress(int)                            running count of files copied
    log(str)                                 one human-readable status line
    stats_updated(int, int, int, int, int)   (images, videos, gifs, json, duplicates)
    finished(dict)                           result dict from transfer_files
    error(str)                               fatal / unrecoverable error message

    Usage
    -----
    worker = FileTransferWorker(
        src_dir="/path/to/facebook-export",
        dest_dir="/path/to/output",
        ids=["123456789", "987654321"],
        include_types={".jpg", ".jpeg", ".png", ".mp4", ".gif"},
        parent=self,
    )
    worker.progress.connect(progress_bar.setValue)
    worker.log.connect(log_widget.append)
    worker.stats_updated.connect(lambda img, vid, gif, js, dup: ...)
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
from pathlib import Path
from typing import Callable

from PySide6.QtCore import QThread, Signal

logger = logging.getLogger(__name__)

# Extension → stat-key mapping
_IMAGE_EXTS = frozenset({".jpg", ".jpeg", ".png"})
_VIDEO_EXTS = frozenset({".mp4"})
_GIF_EXTS   = frozenset({".gif"})
_JSON_EXTS  = frozenset({".json"})


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


def _unique_dest(dest_dir: Path, filename: str) -> Path:
    """Return a destination Path that does not already exist.

    If *dest_dir / filename* is taken, an integer suffix is appended before
    the extension (``photo_1.jpg``, ``photo_2.jpg``, …) until a free slot is
    found.
    """
    candidate = dest_dir / filename
    if not candidate.exists():
        return candidate
    stem   = Path(filename).stem
    suffix = Path(filename).suffix
    counter = 1
    while True:
        candidate = dest_dir / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def _copy_recursive(
    folder: Path,
    dest_dir: Path,
    include_types: frozenset[str] | set[str],
    processed_hashes: set[str],
    stats: dict[str, int],
    progress_callback: Callable[[int, str, str], None],
    is_cancelled: Callable[[], bool] | None,
) -> None:
    """Recursively walk *folder*, copying every qualifying file to *dest_dir*.

    A file is skipped when any of the following is true:

    * Its extension is not in *include_types*.
    * Its MD5 hash is already in *processed_hashes* (duplicate).
    * *is_cancelled* returns ``True``.

    Qualifying files are copied with :func:`shutil.copyfile` and their hash
    is added to *processed_hashes*.  Stat counters are incremented in *stats*.
    Folder structure is preserved during copying.
    """
    try:
        for item in folder.rglob("*"):
            if is_cancelled and is_cancelled():
                return
            if not item.is_file():
                continue

            suffix = item.suffix.lower()
            if suffix not in include_types:
                continue

            # --- MD5 duplicate detection ---
            try:
                digest = _md5(item)
            except OSError as exc:
                progress_callback(-1, f"[ERR] Cannot hash {item.name}: {exc}", "count")
                continue

            if digest in processed_hashes:
                stats["duplicates"] += 1
                progress_callback(-1, f"[DUP] {item.name}", "count")
                continue

            # --- Preserve folder structure ---
            relative_path = item.relative_to(folder)
            dest_subdir = dest_dir / relative_path.parent
            try:
                dest_subdir.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                progress_callback(-1, f"[ERR] Cannot create folder structure: {exc}", "count")
                continue

            # --- Copy to unique destination with folder structure ---
            dest_path = _unique_dest(dest_subdir, item.name)
            try:
                shutil.copyfile(item, dest_path)
                processed_hashes.add(digest)
            except OSError as exc:
                progress_callback(-1, f"[ERR] {item.name}: {exc}", "count")
                continue

            # --- Increment correct stat counter ---
            if suffix in _IMAGE_EXTS:
                stats["images"] += 1
            elif suffix in _VIDEO_EXTS:
                stats["videos"] += 1
            elif suffix in _GIF_EXTS:
                stats["gifs"] += 1
            elif suffix in _JSON_EXTS:
                stats["json"] += 1

            progress_callback(
                -1,
                f"Copied  → {dest_path.name}  (source: {item.name})",
                "count",
            )

    except OSError as exc:
        progress_callback(-1, f"[ERR] Walking {folder.name}: {exc}", "count")


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def transfer_files(
    source_dir: str,
    dest_dir: str,
    ids: list[str],
    progress_callback: Callable[[int, str, str], None],
    include_types: set[str] | frozenset[str],
    is_cancelled: Callable[[], bool] | None = None,
) -> dict:
    """Copy media files from a Facebook export's inbox to *dest_dir*.

    Parameters
    ----------
    source_dir:
        Root of the Facebook data export.  The inbox is resolved as
        ``<source_dir>/messages/inbox/``.
    dest_dir:
        Output directory.  Created automatically if it does not exist.
    ids:
        List of numeric conversation IDs (strings).  Only inbox folders
        whose name contains at least one of these IDs are processed.
        Pass an empty list to process *all* inbox folders.
    progress_callback:
        Called after each significant file operation as
        ``callback(value, message, kind)``.
        *value* is ``-1`` for incremental (count-based) updates.
        *message* is a human-readable status line.
        *kind* is always ``"count"`` in this implementation.
    include_types:
        Set of lowercase file extensions to allow, e.g.
        ``{".jpg", ".jpeg", ".png", ".mp4", ".gif"}``.
    is_cancelled:
        Optional zero-arg callable that returns ``True`` when the caller
        requests an early abort.  Checked before processing each file.

    Returns
    -------
    dict
        On success::

            {
                "success": True,
                "stats": {
                    "images": N, "videos": N, "gifs": N,
                    "json": N, "duplicates": N
                }
            }

        On failure::

            {"success": False, "error": "<reason>"}
    """
    src   = Path(source_dir)
    dst   = Path(dest_dir)
    inbox = src / "messages" / "inbox"

    if not inbox.is_dir():
        return {"success": False, "error": f"Inbox directory not found: {inbox}"}

    # --- Discover and filter inbox folders ---
    try:
        all_folders = [f for f in inbox.iterdir() if f.is_dir()]
    except OSError as exc:
        return {"success": False, "error": f"Cannot list inbox directory: {exc}"}

    if ids:
        matching = [f for f in all_folders if any(cid in f.name for cid in ids)]
    else:
        matching = all_folders

    if not matching:
        progress_callback(-1, "No matching conversation folders found.", "count")
        return {
            "success": True,
            "stats": {"images": 0, "videos": 0, "gifs": 0, "json": 0, "duplicates": 0},
        }

    # --- Prepare destination ---
    try:
        dst.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return {"success": False, "error": f"Cannot create destination directory: {exc}"}

    processed_hashes: set[str] = set()
    stats: dict[str, int] = {
        "images": 0, "videos": 0, "gifs": 0, "json": 0, "duplicates": 0
    }

    for folder in matching:
        if is_cancelled and is_cancelled():
            progress_callback(-1, "Cancelled by user.", "count")
            break
        progress_callback(-1, f"Processing folder: {folder.name}", "count")
        
        # Create a folder for this conversation
        conv_dest = dst / folder.name
        try:
            conv_dest.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            progress_callback(-1, f"[ERR] Cannot create conversation folder: {exc}", "count")
            continue
        
        _copy_recursive(
            folder, conv_dest, include_types, processed_hashes,
            stats, progress_callback, is_cancelled,
        )

    return {"success": True, "stats": stats}


# ---------------------------------------------------------------------------
# Qt worker thread
# ---------------------------------------------------------------------------

class FileTransferWorker(QThread):
    """Background thread that wraps :func:`transfer_files` with Qt signals.

    Parameters
    ----------
    src_dir:
        Root of the Facebook data export.
    dest_dir:
        Directory where files are written.  Created automatically.
    ids:
        Conversation IDs to filter by (empty list = all conversations).
    include_types:
        Lowercase file extensions to copy (e.g. ``{".jpg", ".mp4", ".gif"}``).
    """

    # --- Signals ---
    progress      = Signal(int)                    # running count of files copied
    log           = Signal(str)                    # one log line
    stats_updated = Signal(int, int, int, int, int)  # images, videos, gifs, json, duplicates
    finished      = Signal(dict)                   # result dict
    error         = Signal(str)                    # fatal error message

    def __init__(
        self,
        src_dir: str,
        dest_dir: str,
        ids: list[str],
        include_types: set[str],
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.src_dir       = src_dir
        self.dest_dir      = dest_dir
        self.ids           = ids
        self.include_types = include_types
        self._cancel_event = threading.Event()

    def cancel(self) -> None:
        """Ask the worker to stop after the current file finishes."""
        self._cancel_event.set()

    def run(self) -> None:
        self._cancel_event.clear()
        copied_count = [0]

        def _callback(value: int, message: str, kind: str) -> None:
            self.log.emit(message)
            if value == -1:
                copied_count[0] += 1
                self.progress.emit(copied_count[0])
            else:
                self.progress.emit(value)

        result = transfer_files(
            source_dir        = self.src_dir,
            dest_dir          = self.dest_dir,
            ids               = self.ids,
            progress_callback = _callback,
            include_types     = self.include_types,
            is_cancelled      = self._cancel_event.is_set,
        )

        if not result["success"]:
            self.error.emit(result.get("error", "Unknown error"))
        else:
            s = result["stats"]
            self.stats_updated.emit(
                s["images"], s["videos"], s["gifs"], s["json"], s["duplicates"]
            )
            summary = (
                f"Done — {s['images']} image(s), {s['videos']} video(s), "
                f"{s['gifs']} GIF(s), {s['json']} JSON file(s) copied; "
                f"{s['duplicates']} duplicate(s) skipped."
            )
            logger.info(summary)
            self.log.emit(summary)

        self.finished.emit(result)
