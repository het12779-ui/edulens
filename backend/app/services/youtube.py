"""
Downloads audio-only stream from a YouTube URL so we can feed it straight
into the transcription service (Hour 6).
"""
import os
import uuid
import yt_dlp
from app.config import get_settings

settings = get_settings()


def download_youtube_audio(url: str) -> tuple[str, str]:
    """
    Returns (file_path, video_title).
    """
    out_id = str(uuid.uuid4())
    out_template = os.path.join(settings.upload_dir, f"{out_id}.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": out_template,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title", "Untitled YouTube Video")

    final_path = os.path.join(settings.upload_dir, f"{out_id}.mp3")
    return final_path, title