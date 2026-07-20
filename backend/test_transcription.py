from app.services.youtube import download_youtube_audio
from app.services.transcription import transcribe, segments_to_transcript_text

if __name__ == "__main__":
    path, title = download_youtube_audio("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    print(f"Downloaded: {title}")

    segments = transcribe(path)
    print(f"\nGot {len(segments)} segments\n")
    for s in segments[:5]:
        print(f"[{s['start']}s - {s['end']}s] {s['text']}")

    print("\nFull transcript preview:")
    print(segments_to_transcript_text(segments)[:300])