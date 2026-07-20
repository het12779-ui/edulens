from app.db.supabase_client import save_content_record, get_content_record, list_content_records
import uuid

if __name__ == "__main__":
    test_id = str(uuid.uuid4())
    save_content_record(test_id, {
        "filename": "test-connection.pdf",
        "source_type": "pdf",
        "status": "queued",
    })

    record = get_content_record(test_id)
    print("Saved record:", record)

    all_records = list_content_records()
    print(f"\nTotal records in DB: {len(all_records)}")