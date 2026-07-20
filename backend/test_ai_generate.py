from app.services.pdf_extract import extract_pdf_pages, pages_to_full_text
from app.services.ai_generate import generate_outline, generate_flashcards

if __name__ == "__main__":
    pages = extract_pdf_pages("./storage/uploads/test.pdf")
    full_text = pages_to_full_text(pages)

    print("Generating outline...")
    outline = generate_outline(full_text, is_video=False)
    for item in outline:
        print(f"- [{item.get('ref')}] {item.get('title')}: {item.get('summary')}")

    print("\nGenerating flashcards...")
    flashcards = generate_flashcards(full_text)
    for card in flashcards:
        print(f"- {card.get('term')}: {card.get('definition')}")