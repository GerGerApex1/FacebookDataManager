"""
rename_images.py
----------------
Renames (or copies-and-renames) media files referenced inside a Facebook
data export by reading all ``message_*.json`` files recursively, extracting
every media URI together with its creation timestamp, sorting everything
chronologically, and writing new named files to the destination directory.

Public API
----------
RenameImagesWorker(QThread)
    Background worker that scans a Facebook export root for JSON message
    files, collects photo/video/gif/audio URIs with timestamps, and produces
    chronologically-named renames or copies.

    Signals
    -------
    progress(int)                   overall 0–100 progress value
    log(str)                        human-readable status / error line
    stats_updated(int, int, int)    (processed, renamed, errors) running totals
    finished()                      emitted when done or cancelled
    error(str)                      emitted on a fatal, unrecoverable error

    Usage
    -----
    worker = RenameImagesWorker(
        src_dir="/path/to/facebook-export-root",
        dest_dir="/path/to/output",
        prefix="photo_",
        start_index=1,
        padding=4,
        copy_mode=True,   # False = rename in-place
    )
    worker.progress.connect(progress_bar.setValue)
    worker.log.connect(log_widget.append)
    worker.stats_updated.connect(lambda p, r, e: ...)
    worker.finished.connect(on_done)
    worker.start()

    # To stop early:
    worker.cancel()
"""

from __future__ import annotations

import json
import logging
import os
import re
import shutil
import sys
import threading
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

from PySide6.QtCore import QThread, Signal

logger = logging.getLogger(__name__)


class RenameImagesWorker(QThread):
    """Background thread that reads Facebook JSON files, collects media URIs
    with timestamps, sorts them chronologically, and renames/copies the
    original files with sequential timeline-based names.

    Parameters
    ----------
    src_dir:
        Root of the Facebook data export (the folder that contains
        ``your_facebook_activity/`` or ``messages/``).  All
        ``message_*.json`` files under this tree are scanned.
    dest_dir:
        Directory where renamed/copied files are written.  Created
        automatically if it does not exist.
    prefix:
        Optional string prepended to every output filename.
    start_index:
        Numeric counter value for the first file (default 1).
    padding:
        Zero-padding width for the sequential counter (e.g. 4 → ``0001``).
    copy_mode:
        When ``True`` the original file is *copied* to ``dest_dir`` with the
        new name; the original is preserved.  When ``False`` the file is
        *renamed* (moved) to ``dest_dir``.
    """

    # --- Signals ---
    progress      = Signal(int)             # 0 – 100
    log           = Signal(str)             # one log line
    stats_updated = Signal(int, int, int)   # processed, renamed, errors
    finished      = Signal()
    error         = Signal(str)             # fatal error message

    # Keys in a message object that may contain media item lists
    _MEDIA_KEYS: tuple[str, ...] = ("photos", "videos", "gifs", "audio_files")

    def __init__(
        self,
        src_dir: str,
        dest_dir: str,
        json_dir: str = "",
        prefix: str = "",
        start_index: int = 1,
        padding: int = 4,
        copy_mode: bool = False,
        name_template: str = "",
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.src_dir     = Path(src_dir)
        self.dest_dir    = Path(dest_dir)
        # If a separate JSON directory is given use it; otherwise fall back to src_dir
        self.json_dir    = Path(json_dir) if json_dir.strip() else self.src_dir
        self.prefix      = prefix
        self.start_index = max(0, start_index)
        self.padding     = max(1, padding)
        self.copy_mode   = copy_mode
        self.name_template = name_template.strip() or "${PREFIX}${DATE_TIME}_${THREAD_NAME}"

        self._cancel_event = threading.Event()

    # ------------------------------------------------------------------
    # Public control
    # ------------------------------------------------------------------

    def cancel(self) -> None:
        """Ask the worker to stop after the current file finishes."""
        self._cancel_event.set()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _set_file_timestamps(self, path: Path, ts: int) -> None:
        """Set the file's access/modification time to *ts* (Unix seconds).

        On Windows the creation timestamp is also updated via the Win32
        ``SetFileTime`` API so Explorer and other tools show the correct date.
        Does nothing when *ts* is 0 (unknown timestamp).
        """
        if ts == 0:
            return
        try:
            os.utime(path, (ts, ts))
        except OSError as exc:
            logger.debug("Could not set utime on %s: %s", path.name, exc)
            return

        if sys.platform != "win32":
            return

        # Windows: also update the creation timestamp via SetFileTime
        try:
            import ctypes
            import ctypes.wintypes

            class _FILETIME(ctypes.Structure):
                _fields_ = [
                    ("dwLowDateTime",  ctypes.wintypes.DWORD),
                    ("dwHighDateTime", ctypes.wintypes.DWORD),
                ]

            # Unix epoch → Windows FILETIME (100-ns ticks since 1601-01-01)
            _EPOCH_DIFF = 116_444_736_000_000_000
            ft_val = int(ts * 10_000_000) + _EPOCH_DIFF
            ft = _FILETIME(ft_val & 0xFFFFFFFF, ft_val >> 32)

            handle = ctypes.windll.kernel32.CreateFileW(
                str(path), 0x100, 0, None, 3, 0, None  # FILE_WRITE_ATTRIBUTES, OPEN_EXISTING
            )
            if handle != -1:
                ctypes.windll.kernel32.SetFileTime(handle, ctypes.byref(ft), None, None)
                ctypes.windll.kernel32.CloseHandle(handle)
        except Exception as exc:
            logger.debug("Could not set creation time on %s: %s", path.name, exc)

    def _load_json(self, path: Path) -> dict | None:
        """Load a JSON file, tolerating Facebook's mojibake encoding.

        Facebook encodes multi-byte UTF-8 characters as sequences of
        latin-1 escape characters inside otherwise valid JSON.  This method
        tries standard UTF-8 first and falls back to ``raw_unicode_escape``
        decoding to recover the original text.
        """
        try:
            with open(path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except (UnicodeDecodeError, json.JSONDecodeError):
            pass

        try:
            with open(path, "rb") as fh:
                raw = fh.read()
            text = raw.decode("raw_unicode_escape")
            return json.loads(text)
        except Exception as exc:
            msg = f"[WARN] Cannot parse {path.name}: {exc}"
            logger.warning("Cannot parse %s: %s", path.name, exc)
            self.log.emit(msg)
            return None

    def _sanitize_thread_name(self, name: str) -> str:
        """Return an ASCII-safe, filesystem-friendly version of a thread title.

        Steps:
        1. Fix Facebook's mojibake (UTF-8 bytes stored as latin-1 codepoints).
        2. NFKD-normalise so accented letters decompose to base + combining.
        3. Drop every non-ASCII codepoint (strips emoji, CJK, etc.).
        4. Keep only alphanumeric characters, spaces, and hyphens.
        5. Collapse whitespace / hyphens into single underscores.
        6. Return ``"unknown"`` if nothing remains.
        """
        # Step 1 — undo Facebook mojibake
        try:
            name = name.encode("latin-1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass

        # Step 2 — decompose accented letters
        name = unicodedata.normalize("NFKD", name)

        # Step 3 — drop non-ASCII
        name = name.encode("ascii", errors="ignore").decode("ascii")

        # Step 4 — strip anything that is not alphanumeric, space, or hyphen
        name = re.sub(r"[^A-Za-z0-9 \-]", "", name)

        # Step 5 — collapse runs of spaces/hyphens into a single underscore
        name = re.sub(r"[\s\-]+", "_", name)
        name = re.sub(r"_+", "_", name).strip("_")

        return name or "unknown"

    def _collect_entries(
        self,
        json_files: list[Path],
        file_index: dict[str, list[Path]] | None = None,
    ) -> list[tuple[int, Path, str]]:
        """Parse every JSON file and return ``(timestamp_seconds, abs_path, thread_name)``
        triples for every media item found, sorted oldest-first.

        ``timestamp_seconds`` comes from ``creation_timestamp`` on the media
        item when available, otherwise falls back to ``timestamp_ms`` (÷1000)
        on the enclosing message.  ``thread_name`` is the sanitized
        conversation ``title`` from the same JSON file.

        When *file_index* is supplied and the URI-derived path does not exist
        on disk, the method falls back to locating the file by its bare
        filename inside *src_dir* (e.g. a flat export where all images live
        directly in the source folder rather than mirroring the URI tree).
        """
        entries: list[tuple[int, Path, str]] = []

        for jf in json_files:
            if self._cancel_event.is_set():
                break

            data = self._load_json(jf)
            if data is None:
                continue

            messages = data.get("messages")
            if not isinstance(messages, list):
                continue

            # Extract and sanitize the conversation title once per file
            raw_title = data.get("title") or jf.parent.name
            thread_name = self._sanitize_thread_name(str(raw_title))

            for msg in messages:
                if not isinstance(msg, dict):
                    continue

                # Fallback timestamp from the message envelope (ms → s)
                msg_ts_ms = msg.get("timestamp_ms", 0)
                msg_ts = (msg_ts_ms // 1000) if msg_ts_ms else 0

                for key in self._MEDIA_KEYS:
                    media_list = msg.get(key)
                    if not isinstance(media_list, list):
                        continue

                    for item in media_list:
                        if not isinstance(item, dict):
                            continue

                        uri = item.get("uri", "").strip()
                        if not uri:
                            continue

                        # Prefer item-level timestamp, fall back to message ts
                        ts = int(item.get("creation_timestamp") or msg_ts or 0)

                        # Resolve the URI relative to the export root
                        rel = Path(uri.replace("\\", "/"))
                        abs_path = (self.src_dir / rel).resolve()

                        # Fallback: if the full path doesn't exist, search by
                        # bare filename in the file index built from src_dir.
                        if not abs_path.is_file() and file_index:
                            candidates = file_index.get(rel.name, [])
                            if candidates:
                                abs_path = candidates[0]

                        entries.append((ts, abs_path, thread_name))

        # Sort chronologically — oldest first
        entries.sort(key=lambda e: e[0])
        return entries

    def _build_file_index(self) -> dict[str, list[Path]]:
        """Recursively scan *src_dir* and return a ``{filename: [abs_path, ...]``
        mapping so that media items can be located by bare filename alone when
        the full URI path does not exist on disk.
        """
        index: dict[str, list[Path]] = {}
        try:
            for p in self.src_dir.rglob("*"):
                if p.is_file():
                    index.setdefault(p.name, []).append(p)
        except OSError as exc:
            logger.warning("Could not fully index src_dir: %s", exc)
        return index

    def _apply_template(self, index: int, date_str: str, thread_name: str) -> str:
        """Expand self.name_template by substituting all known variables."""
        s = self.name_template
        s = s.replace("${PREFIX}", self.prefix)
        s = s.replace("${INDEX}", str(index).zfill(self.padding))
        s = s.replace("${DATE_TIME}", date_str)
        s = s.replace("${THREAD_NAME}", thread_name)
        return s

    def _unique_dest(self, dest_dir: Path, new_name: str, suffix: str) -> Path:
        """Return a destination Path that does not already exist.

        If ``dest_dir / new_name`` is already taken, an integer suffix is
        appended before the extension until a free name is found.
        """
        candidate = dest_dir / new_name
        if not candidate.exists():
            return candidate

        stem = new_name[: -len(suffix)] if new_name.endswith(suffix) else new_name
        collision = 1
        while True:
            candidate = dest_dir / f"{stem}_{collision}{suffix}"
            if not candidate.exists():
                return candidate
            collision += 1

    # ------------------------------------------------------------------
    # QThread entry point
    # ------------------------------------------------------------------

    def run(self) -> None:  # noqa: C901
        self._cancel_event.clear()

        # 1. Discover all message JSON files
        try:
            json_files: list[Path] = sorted(self.json_dir.rglob("message_*.json"))
        except OSError as exc:
            logger.error("Cannot scan JSON directory: %s", exc)
            self.error.emit(f"Cannot scan JSON directory: {exc}")
            return

        if not json_files:
            msg = f"No message_*.json files found in: {self.json_dir}"
            logger.warning(msg)
            self.log.emit(msg)
            self.finished.emit()
            return

        msg = f"Found {len(json_files)} JSON file(s) — parsing media entries…"
        logger.info(msg)
        self.log.emit(msg)

        # 2a. Build a filename index for fallback path resolution
        self.log.emit("Indexing source directory for filename-based fallback…")
        file_index = self._build_file_index()
        self.log.emit(
            f"File index ready — {len(file_index)} unique filename(s) found in source directory."
        )

        # 2b. Collect URIs and timestamps from every message
        entries = self._collect_entries(json_files, file_index)

        if not entries:
            msg = "No media entries found across all JSON files."
            logger.warning(msg)
            self.log.emit(msg)
            self.finished.emit()
            return

        msg = (
            f"Collected {len(entries)} media entry/entries — "
            f"{'copying' if self.copy_mode else 'renaming'}…"
        )
        logger.info(msg)
        self.log.emit(msg)

        # 3. Ensure destination directory exists
        try:
            self.dest_dir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            logger.error("Cannot create destination directory: %s", exc)
            self.error.emit(f"Cannot create destination directory: {exc}")
            return

        total    = len(entries)
        renamed  = 0
        errors   = 0
        skipped  = 0
        rename_map: list[dict] = []  # [{original, renamed}] written to JSON at end

        for idx_offset, (ts, src_path, thread_name) in enumerate(entries):
            if self._cancel_event.is_set():
                msg = "Cancelled by user."
                logger.info(msg)
                self.log.emit(msg)
                break

            # Build the new chronological filename from the naming template
            dt       = datetime.fromtimestamp(ts, tz=timezone.utc) if ts else None
            date_str = dt.strftime("%Y_%m_%d_%H_%M_%S") if dt else "0000_00_00_00_00_00"
            suffix   = src_path.suffix.lower()
            index    = self.start_index + idx_offset
            new_name = self._apply_template(index, date_str, thread_name) + suffix

            dest_path = self._unique_dest(self.dest_dir, new_name, suffix)

            if not src_path.is_file():
                msg = f"[SKIP] File not found on disk: {src_path}"
                logger.warning(msg)
                self.log.emit(msg)
                skipped += 1
            else:
                try:
                    if self.copy_mode:
                        shutil.copy2(src_path, dest_path)
                        self._set_file_timestamps(dest_path, ts)
                        msg = f"Copied  → {dest_path.name}  (source: {src_path.name})"
                        logger.info(msg)
                        self.log.emit(msg)
                    else:
                        src_path.rename(dest_path)
                        self._set_file_timestamps(dest_path, ts)
                        msg = f"Renamed → {dest_path.name}  (was: {src_path.name})"
                        logger.info(msg)
                        self.log.emit(msg)
                    renamed += 1
                    rename_map.append({
                        "original": src_path.name,
                        "renamed":  dest_path.name,
                    })
                except OSError as exc:
                    msg = f"[ERR] {src_path.name}: {exc}"
                    logger.error(msg)
                    self.log.emit(msg)
                    errors += 1

            processed = idx_offset + 1
            self.stats_updated.emit(processed, renamed, errors)
            self.progress.emit(int(processed / total * 100))

        summary = (
            f"Done — {renamed} {'copied' if self.copy_mode else 'renamed'}, "
            f"{skipped} skipped (not found on disk), {errors} error(s)."
        )
        logger.info(summary)
        self.log.emit(summary)

        # Write rename map JSON to destination directory
        if rename_map:
            map_path = self.dest_dir / "rename_map.json"
            try:
                with open(map_path, "w", encoding="utf-8") as fh:
                    json.dump(rename_map, fh, indent=2, ensure_ascii=False)
                msg = f"Rename map written → {map_path.name} ({len(rename_map)} entries)"
                logger.info(msg)
                self.log.emit(msg)
            except OSError as exc:
                msg = f"[WARN] Could not write rename map: {exc}"
                logger.warning(msg)
                self.log.emit(msg)

        self.finished.emit()
 