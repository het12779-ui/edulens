from app.services.pdf_extract import extract_pdf_pages, pages_to_full_text

if __name__ == "__main__":
    path = r"C:\Users\hetpa\Downloads\test.pdf"   # note the r"" prefix — needed for Windows backslashes

    pages = extract_pdf_pages(path)
    print(f"Extracted {len(pages)} pages\n")

    for p in pages[:2]:
        print(f"--- Page {p['page']} ---")
        print(p["text"][:300])
        print()

    full_text = pages_to_full_text(pages)
    print(f"Total extracted text length: {len(full_text)} characters")