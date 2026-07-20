"""
Turns audio/video into timestamped transcript segments.
Uses faster-whisper if memory allows, falls back to openai-whisper otherwise.
"""
from functools import lru_cache
import os

# Try faster-whisper first
try:
    from faster_whisper import WhisperModel
    FASTER_AVAILABLE = True
except ImportError:
    FASTER_AVAILABLE = False

# Fallback to openai-whisper
if not FASTER_AVAILABLE:
    import whisper as openai_whisper

from app.config import get_settings

settings = get_settings()


@lru_cache
def _get_model():
    if FASTER_AVAILABLE:
        try:
            return WhisperModel(
                settings.whisper_model_size,
                device="cpu",
                compute_type="int8",
                cpu_threads=2,
            )
        except Exception:
            # Memory allocation failed — fall back
            # Use a helper to avoid global declaration issues
            return _fallback_model()
    else:
        return openai_whisper.load_model(settings.whisper_model_size)


def _fallback_model():
    """Load openai-whisper model when faster-whisper fails."""
    global FASTER_AVAILABLE
    FASTER_AVAILABLE = False
    return openai_whisper.load_model(settings.whisper_model_size)


def transcribe(file_path: str) -> list[dict]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    model = _get_model()

    if FASTER_AVAILABLE:
        segments, _info = model.transcribe(file_path, beam_size=1, vad_filter=False)
        result = []
        for seg in segments:
            result.append({
                "start": round(seg.start, 2),
                "end": round(seg.end, 2),
                "text": seg.text.strip(),
            })
        return result
    else:
        # openai-whisper path
        output = model.transcribe(file_path)
        return [
            {
                "start": round(seg["start"], 2),
                "end": round(seg["end"], 2),
                "text": seg["text"].strip(),
            }
            for seg in output.get("segments", [])
        ]


def segments_to_transcript_text(segments: list[dict]) -> str:
    return " ".join(s["text"] for s in segments)