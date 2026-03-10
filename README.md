# FacebookDataManager

A desktop GUI application for organizing and managing Facebook data exports. Built with PySide6 (Qt), it provides four tools in a tabbed interface for processing media files from your Facebook archive.
### its crazy how you can vibe-code an app with claude 
## Features

### Face Detection
Scans a directory of images, detects faces using MTCNN (via `facenet-pytorch`), and copies qualifying images to a destination folder.
- Set a minimum face count threshold (1–20)
- GPU (CUDA) acceleration with automatic CPU fallback
- Configurable thread count for parallel CPU processing
- MD5-based duplicate prevention across runs

### File Transfer
Copies media files directly from a Facebook data export (`messages/inbox/`), filtered by conversation ID and file type.
- Filter by images, videos, and/or GIFs
- Manage a list of conversation IDs to include
- Skips duplicate files via MD5 hashing
- Reports counts of images, videos, GIFs, JSON files, and duplicates skipped

### Rename Images
Reads all `message_*.json` files from a Facebook export, extracts photo/video/GIF/audio URIs with their creation timestamps, and produces chronologically-named output files.
- Configurable filename prefix, start index, and zero-padding
- Copy mode (preserves originals) or rename-in-place mode

### Rename Videos
Same as Rename Images but scoped to video files only.

## Requirements

- Python 3.10+
- An NVIDIA GPU with CUDA drivers is optional but recommended for face detection

Install dependencies:

```bash
pip install -r requirements.txt
```

> **Note:** For GPU acceleration, install the CUDA-enabled PyTorch wheel matching your driver from [pytorch.org](https://pytorch.org/get-started/locally/) before running the above command.

## Usage

```bash
python main.py
```

## Project Structure

```
FacebookDataManager/
├── main.py               # Application entry point and GUI layout
├── main.ui               # Qt Designer source file
├── requirements.txt
└── modules/
    ├── face_detection.py  # MTCNN face detection worker thread
    ├── file_transfer.py   # Facebook inbox media transfer worker
    ├── rename_images.py   # Chronological image rename worker
    └── rename_videos.py   # Chronological video rename worker
```

## Dependencies

| Package | Purpose |
|---|---|
| `pyside6` | GUI framework (Qt bindings) |
| `torch` / `torchvision` | Deep learning backend for face detection |
| `facenet-pytorch` | MTCNN face detection model |
| `opencv-python` | Image processing utilities |
| `Pillow` | Image loading and manipulation |
| `numpy` | Numerical operations |

