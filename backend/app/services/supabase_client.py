"""
Supabase-backed content store, with an in-memory fallback so the app still
runs even before Supabase credentials are configured.
"""
from app.config import get_settings

settings = get_settings()

_memory_db: dict[str, dict] = {}  # fallback store: content_id -> record


def _has_supabase() -> bool:
    return bool(settings.supabase_url and settings.supabase_key)


def _client():
    from supabase import create_client
    return create_client(settings.supabase_url, settings.supabase_key)


def save_content_record(content_id: str, record: dict):
    existing = _memory_db.get(content_id, {})
    merged = {**existing, **record, "id": content_id}

    if _has_supabase():
        _client().table("content").upsert(merged).execute()
    else:
        _memory_db[content_id] = merged


def get_content_record(content_id: str) -> dict | None:
    if _has_supabase():
        res = _client().table("content").select("*").eq("id", content_id).execute()
        return res.data[0] if res.data else None
    return _memory_db.get(content_id)


def list_content_records() -> list[dict]:
    if _has_supabase():
        res = _client().table("content").select("*").order("created_at", desc=True).execute()
        return res.data
    return list(_memory_db.values())