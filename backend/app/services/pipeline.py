"""
Glues every service together into one function that runs as a FastAPI
BackgroundTask. This IS "the pipeline" your architecture diagram shows:

  raw file/url -> transcript/text -> outline (LLM)
                                   -> flashcards (LLM)
                                   -> saved to DB, status flipped to "ready"

NOTE ON SCALE: today this runs inside the API process via BackgroundTasks.
The next infra step (documented, not built, in the 36h scope) is to move
this function's body into a Celery task so long videos don't tie up a web
worker — mention this explicitly in your report as the production upgrade path.
"""
from app.db.supabase_client import save_content_record
from app.services import transcription, pdf_extract, youtube, ai_generate


def process_content(content_id: str, path_or_url: str, source_type: str):
    try:
        save_content_record(content_id, {"status": "processing"})

        if source_type == "youtube":
            audio_path, title = youtube.download_youtube_audio(path_or_url)
            segments = transcription.transcribe(audio_path)
            full_text = transcription.segments_to_transcript_text(segments)
            is_video = True
            filename = title
        elif source_type == "video":
            segments = transcription.transcribe(path_or_url)
            full_text = transcription.segments_to_transcript_text(segments)
            is_video = True
            filename = None
        else:  # pdf
            pages = pdf_extract.extract_pdf_pages(path_or_url)
            full_text = pdf_extract.pages_to_full_text(pages)
            is_video = False
            filename = None

        # --- AI generation (outline, flashcards) ---
        outline_raw = ai_generate.generate_outline(full_text, is_video)
        flashcards_raw = ai_generate.generate_flashcards(full_text)

        outline = [{
            "title": o.get("title", ""),
            "summary": o.get("summary", ""),
            "timestamp_seconds": o.get("ref") if is_video else None,
            "page_number": o.get("ref") if not is_video else None,
        } for o in outline_raw]

        update = {
            "status": "ready",
            "transcript_preview": full_text[:500],
            "outline": outline,
            "flashcards": flashcards_raw,
        }
        if filename:
            update["filename"] = filename

        save_content_record(content_id, update)
        print(f"[pipeline] content {content_id} ready")

    except Exception as e:
        save_content_record(content_id, {"status": "failed", "error": str(e)})
        print(f"[pipeline] content {content_id} FAILED: {e}")
        raise