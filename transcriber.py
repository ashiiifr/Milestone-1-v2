"""
transcriber.py
--------------
Wraps OpenAI Whisper to transcribe audio files and return structured results.
"""

import whisper
import os
import shutil
from pathlib import Path


# Available Whisper model sizes (smallest → largest / fastest → most accurate)
WHISPER_MODELS = ["tiny", "base", "small", "medium", "large"]


def _ensure_ffmpeg() -> str:
    """
    Locate ffmpeg and return its full executable path.

    Priority:
    1. Already on system PATH  → return 'ffmpeg' (let the OS resolve it).
    2. Bundled via imageio-ffmpeg  → return the absolute path to the binary.
    3. Neither found  → raise a clear RuntimeError.

    Also monkey-patches whisper.audio so it uses the resolved path directly
    instead of relying on PATH resolution at subprocess spawn time.
    """
    import whisper.audio as _waudio
    import subprocess

    # Check system PATH first
    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        return system_ffmpeg

    # Fall back to imageio-ffmpeg bundled binary
    try:
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        raise RuntimeError(
            "ffmpeg not found. Install it from https://ffmpeg.org or run:\n"
            "  pip install imageio[ffmpeg]"
        )

    # Monkey-patch whisper.audio.load_audio to use the full path
    import inspect, types

    _orig_source = inspect.getsource(_waudio.load_audio)

    def load_audio(file: str, sr: int = _waudio.SAMPLE_RATE):
        cmd = [
            ffmpeg_exe,        # ← full path instead of bare "ffmpeg"
            "-nostdin",
            "-threads", "0",
            "-i", file,
            "-f", "s16le",
            "-ac", "1",
            "-acodec", "pcm_s16le",
            "-ar", str(sr),
            "-",
        ]
        try:
            from subprocess import run, CalledProcessError
            import numpy as np
            out = run(cmd, capture_output=True, check=True).stdout
        except Exception as e:  # CalledProcessError
            raise RuntimeError(f"Failed to load audio: {e}") from e
        import numpy as np
        return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

    _waudio.load_audio = load_audio
    return ffmpeg_exe


# Patch ffmpeg as soon as this module is imported
_FFMPEG_EXE = _ensure_ffmpeg()


def load_model(model_size: str = "base") -> whisper.Whisper:
    """
    Load a Whisper model by size.

    Args:
        model_size: One of 'tiny', 'base', 'small', 'medium', 'large'.

    Returns:
        Loaded Whisper model instance.
    """
    if model_size not in WHISPER_MODELS:
        raise ValueError(
            f"Invalid model size '{model_size}'. Choose from: {WHISPER_MODELS}"
        )
    return whisper.load_model(model_size)


def transcribe_audio(audio_path: str, model_size: str = "base") -> dict:
    """
    Transcribe an audio file using Whisper.

    Args:
        audio_path: Absolute path to the audio/video file.
        model_size: Whisper model size to use.

    Returns:
        dict with keys:
            - 'text'     : full transcript string
            - 'segments' : list of timed segments (start, end, text)
            - 'language' : detected language code
            - 'model'    : model size used
            - 'file'     : original filename

    Raises:
        FileNotFoundError: if audio_path does not exist.
        RuntimeError: if Whisper transcription fails.
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    model = load_model(model_size)

    result = model.transcribe(audio_path, fp16=False)

    return {
        "text": result.get("text", "").strip(),
        "segments": result.get("segments", []),
        "language": result.get("language", "unknown"),
        "model": model_size,
        "file": Path(audio_path).name,
    }


def save_transcript(transcript_text: str, output_path: str) -> str:
    """
    Save a transcript string to a .txt file.

    Args:
        transcript_text: The full transcript.
        output_path: Destination .txt file path.

    Returns:
        Absolute path to the saved file.
    """
    output_path = os.path.abspath(output_path)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(transcript_text)
    return output_path
