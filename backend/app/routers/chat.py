"""
The chat-with-document endpoint: retrieval (ChromaDB) + generation (LLM),
with sources cited so the frontend can show "jump to this part of the video/PDF".
"""
from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse, ChatSource
from app.services import vectorstore, ai_generate

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest):
    retrieved = vectorstore.retrieve(req.question, [req.content_id], k=8)

    # --- DEBUG: temporary, remove once retrieval quality is confirmed good ---
    print(f"\n[chat debug] question={req.question!r}")
    print(f"[chat debug] retrieved {len(retrieved)} chunks for content_id={req.content_id}")
    for r in retrieved:
        print(f"  ref={r['source_ref']!r}  text={r['text'][:120]!r}")
    print("[chat debug] ---end---\n")
    # --- END DEBUG ---

    answer = ai_generate.answer_with_context(req.question, retrieved)

    sources = [
        ChatSource(
            content_id=r["content_id"],
            excerpt=r["text"][:200],
            timestamp_seconds=float(r["source_ref"]) if _is_number(r["source_ref"]) else None,
            page_number=int(float(r["source_ref"])) if _is_number(r["source_ref"]) else None,
        )
        for r in retrieved
    ]
    return ChatResponse(answer=answer, sources=sources)


def _is_number(val) -> bool:
    try:
        float(val)
        return True
    except (ValueError, TypeError):
        return False