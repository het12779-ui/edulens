"""
Record store. Currently in-memory — Hour 11 will swap this for real Supabase
calls behind the SAME function signatures, so nothing else in the app changes.
"""
_memory_db: dict[str, dict] = {}


def save_content_record(content_id: str, record: dict):
    existing = _memory_db.get(content_id, {})
    _memory_db[content_id] = {**existing, **record, "id": content_id}


def get_content_record(content_id: str) -> dict | None:
    return _memory_db.get(content_id)


def list_content_records() -> list[dict]:
    return list(_memory_db.values())