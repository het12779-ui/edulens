"""
Shared request/response schemas — the contract between frontend and backend.
"""
from pydantic import BaseModel
from typing import List, Optional, Literal


class UploadResponse(BaseModel):
    content_id: str
    filename: str
    source_type: Literal["pdf", "video", "youtube"]
    status: Literal["queued", "processing", "ready", "failed"]


class OutlineItem(BaseModel):
    title: str
    timestamp_seconds: Optional[float] = None   # for video
    page_number: Optional[int] = None           # for pdf
    summary: str


class Flashcard(BaseModel):
    term: str
    definition: str
    source_ref: Optional[str] = None


class ProcessResult(BaseModel):
    content_id: str
    status: Literal["processing", "ready", "failed"]
    transcript_preview: Optional[str] = None
    outline: List[OutlineItem] = []
    flashcards: List[Flashcard] = []