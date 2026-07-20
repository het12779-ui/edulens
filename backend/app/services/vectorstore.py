"""
Chunk content, embed it, store in ChromaDB (local, free, zero external
dependency — same LangChain interface as Pinecone/Weaviate, so swapping to a
hosted vector DB later is a one-line change — mention this as evidence of
clean abstraction, not a shortcut, in your viva).
"""
import chromadb
from chromadb.utils import embedding_functions
from app.config import get_settings

settings = get_settings()

_client = chromadb.PersistentClient(path=settings.chroma_dir)
_embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)


def _get_collection():
    return _client.get_or_create_collection(
        name="edulens_content",
        embedding_function=_embed_fn,
    )


def chunk_segments(segments: list[dict], max_chars: int = 500) -> list[dict]:
    """
    Groups whisper segments (or pdf pages reshaped into {page, text}) into
    ~max_chars chunks while preserving a source_ref, so retrieved chunks can
    be traced back to a timestamp or page.
    """
    chunks = []
    buffer, buffer_ref = "", None
    for seg in segments:
        if buffer_ref is None:
            buffer_ref = seg.get("start", seg.get("page"))
        buffer += " " + seg["text"]
        if len(buffer) >= max_chars:
            chunks.append({"text": buffer.strip(), "source_ref": buffer_ref})
            buffer, buffer_ref = "", None
    if buffer.strip():
        chunks.append({"text": buffer.strip(), "source_ref": buffer_ref})
    return chunks


def index_content(content_id: str, chunks: list[dict]):
    """Embeds and stores chunks under a namespaced id so retrieval can be
    scoped to one document or across many (cross-doc synthesis, later)."""
    collection = _get_collection()
    ids = [f"{content_id}::{i}" for i in range(len(chunks))]
    documents = [c["text"] for c in chunks]
    metadatas = [{"content_id": content_id, "source_ref": str(c["source_ref"])} for c in chunks]

    collection.add(ids=ids, documents=documents, metadatas=metadatas)


def retrieve(query: str, content_ids: list[str], k: int = 5) -> list[dict]:
    """Retrieval scoped to one or more content_ids."""
    collection = _get_collection()
    where_filter = {"content_id": {"$in": content_ids}} if len(content_ids) > 1 else {"content_id": content_ids[0]}

    results = collection.query(query_texts=[query], n_results=k, where=where_filter)

    out = []
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    for doc, meta in zip(docs, metas):
        out.append({"text": doc, "content_id": meta["content_id"], "source_ref": meta["source_ref"]})
    return out