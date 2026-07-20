from app.services.llm import ask_llm, ask_llm_json

if __name__ == "__main__":
    # Plain text test
    answer = ask_llm("Explain what a hash table is in exactly 2 sentences.")
    print("Plain answer:\n", answer)

    # JSON mode test
    data = ask_llm_json(
        "List 3 programming languages with their release year. "
        'Return JSON like {"languages": [{"name": "...", "year": ...}]}'
    )
    print("\nJSON answer:\n", data)