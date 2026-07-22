"""
Turns audio/video into timestamped transcript segments using openai-whisper.
(Switched from faster-whisper due to a persistent MKL memory allocator
conflict on this machine's CPU/BLAS configuration — openai-whisper uses
PyTorch's memory management instead, which is more reliable on Windows.)
"""
import os
import whisper
from app.config import get_settings
from functools import lru_cache

settings = get_settings()


@lru_cache
def _get_model():
    return whisper.load_model(settings.whisper_model_size)


def transcribe(file_path: str) -> list[dict]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    model = _get_model()
    output = model.transcribe(file_path, fp16=False)

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