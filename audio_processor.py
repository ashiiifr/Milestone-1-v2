"""
audio_processor.py
------------------
Handles audio file validation and preprocessing before transcription.
Supports: mp3, wav, m4a, mp4, ogg, flac, webm
"""

import os
import tempfile
from pathlib import Path

# Supported audio/video formats
SUPPORTED_FORMATS = {".mp3", ".wav", ".m4a", ".mp4", ".ogg", ".flac", ".webm"}
MAX_FILE_SIZE_MB = 500  # maximum upload size in MB


def validate_audio_file(uploaded_file) -> tuple[bool, str]:
    """
    Validate an uploaded Streamlit file object.

    Returns:
        (is_valid: bool, message: str)
    """
    if uploaded_file is None:
        return False, "No file provided."

    # Check extension
    ext = Path(uploaded_file.name).suffix.lower()
    if ext not in SUPPORTED_FORMATS:
        return (
            False,
            f"Unsupported file format '{ext}'. "
            f"Supported formats: {', '.join(sorted(SUPPORTED_FORMATS))}",
        )

    # Check file size
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        return (
            False,
            f"File too large ({file_size_mb:.1f} MB). Maximum allowed size is {MAX_FILE_SIZE_MB} MB.",
        )

    return True, f"File '{uploaded_file.name}' is valid ({file_size_mb:.2f} MB)."


def save_uploaded_file(uploaded_file) -> str:
    """
    Save a Streamlit UploadedFile to a temporary file on disk.

    Returns:
        Path to the saved temporary file.
    """
    ext = Path(uploaded_file.name).suffix.lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(uploaded_file.read())
        return tmp.name


def cleanup_temp_file(file_path: str) -> None:
    """Remove a temporary file if it exists."""
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
    except OSError:
        pass  # non-critical cleanup failure
