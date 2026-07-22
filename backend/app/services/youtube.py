"""
Downloads audio-only stream from a YouTube URL so we can feed it straight
into the transcription service. Uses multiple fallback player clients since
YouTube's anti-bot restrictions change frequently and no single client works
100% of the time.
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

    # Try multiple player clients in order — if one gets blocked/restricted,
    # fall back to the next. This is the known workaround for YouTube's
    # frequently-changing anti-bot measures.
    client_attempts = [
        ["android"],
        ["ios"],
        ["web"],
        ["tv"],
    ]

    last_error = None
    for clients in client_attempts:
        try:
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
                "extractor_args": {"youtube": {"player_client": clients}},
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get("title", "Untitled YouTube Video")

            final_path = os.path.join(settings.upload_dir, f"{out_id}.mp3")
            if os.path.exists(final_path):
                return final_path, title
        except Exception as e:
            last_error = e
            continue

    raise RuntimeError(
        f"Could not download audio from this YouTube link after trying multiple methods. "
        f"This video may be restricted, private, or region-locked. "
        f"Try a different video, or upload a local file instead. (Last error: {last_error})"
    )