from app.services.transcription import transcribe, segments_to_transcript_text

if __name__ == "__main__":
    path = "./storage/uploads/test.mp3"  # your earlier local test file
    segments = transcribe(path)
    print(f"Got {len(segments)} segments")
    for s in segments:
        print(f"[{s['start']}s - {s['end']}s] {s['text']}")