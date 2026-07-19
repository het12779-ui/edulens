"""
Accepts a PDF/video file OR a YouTube URL, saves it, creates a record.
Background processing (transcription, LLM generation) gets wired in Hour 12 —
for now we just get the upload mechanics working end-to-end.
"""
import os
import uuid
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.config import get_settings
from app.models.schemas import UploadResponse
from app.db.supabase_client import save_content_record, get_content_record, list_content_records

router = APIRouter(prefix="/api", tags=["upload"])
settings = get_settings()


@router.post("/upload/file", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    content_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1].lower()

    if ext == ".pdf":
        source_type = "pdf"
    elif ext in (".mp4", ".mov", ".mkv", ".mp3", ".wav", ".m4a"):
        source_type = "video"
    else:
        raise HTTPException(400, "Unsupported file type. Upload PDF, MP4, MOV, MKV, MP3, WAV or M4A.")

    save_path = os.path.join(settings.upload_dir, f"{content_id}{ext}")
    with open(save_path, "wb") as f:
        f.write(await file.read())

    save_content_record(content_id, {
        "filename": file.filename,
        "source_type": source_type,
        "status": "queued",
    })

    return UploadResponse(content_id=content_id, filename=file.filename,
                           source_type=source_type, status="queued")


@router.post("/upload/youtube", response_model=UploadResponse)
async def upload_youtube(url: str = Form(...)):
    content_id = str(uuid.uuid4())

    save_content_record(content_id, {
        "filename": url,
        "source_type": "youtube",
        "status": "queued",
    })

    return UploadResponse(content_id=content_id, filename=url,
                           source_type="youtube", status="queued")


@router.get("/content/{content_id}")
async def get_content(content_id: str):
    record = get_content_record(content_id)
    if not record:
        raise HTTPException(404, "Content not found")
    return record


@router.get("/library")
async def library():
    return list_content_records()