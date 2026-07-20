from app.services.pdf_extract import extract_pdf_pages
from app.services.vectorstore import chunk_segments, index_content, retrieve

if __name__ == "__main__":
    pages = extract_pdf_pages("./storage/uploads/test.pdf")
    segments = [{"page": p["page"], "text": p["text"]} for p in pages]

    chunks = chunk_segments(segments)
    print(f"Created {len(chunks)} chunks")
    for c in chunks[:2]:
        print(f"[ref: {c['source_ref']}] {c['text'][:100]}...")

    test_id = "test-content-123"
    index_content(test_id, chunks)
    print(f"\nIndexed {len(chunks)} chunks under content_id={test_id}")

    results = retrieve("What is this document about?", [test_id], k=3)
    print(f"\nRetrieved {len(results)} relevant chunks:")
    for r in results:
        print(f"[ref: {r['source_ref']}] {r['text'][:150]}...")