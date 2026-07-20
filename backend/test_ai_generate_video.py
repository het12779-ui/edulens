# test_ai_generate_video.py
from app.services.youtube import download_youtube_audio
from app.services.transcription import transcribe, segments_to_transcript_text
from app.services.ai_generate import generate_outline, generate_flashcards

if __name__ == "__main__":
    # Always re-download to get the correct path
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    path, title = download_youtube_audio(url)
    print(f"Downloaded: {title}")
    print(f"File path: {path}")

    segments = transcribe(path)
    full_text = segments_to_transcript_text(segments)

    print("\nGenerating outline from VIDEO transcript...")
    outline = generate_outline(full_text, is_video=True)
    for item in outline:
        print(f"- [{item.get('ref')}s] {item.get('title')}: {item.get('summary')}")

    print("\nGenerating flashcards...")
    flashcards = generate_flashcards(full_text)
    for card in flashcards:
        print(f"- {card.get('term')}: {card.get('definition')}")