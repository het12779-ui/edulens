"""
Every place we ask the LLM to produce something structured about the content
lives here — outline, flashcards, and (this hour) chat answers grounded in
retrieved context.
"""
from app.services.llm import ask_llm, ask_llm_json


def generate_outline(full_text: str, is_video: bool) -> list[dict]:
    ref_kind = "timestamp_seconds (number)" if is_video else "page_number (integer)"
    prompt = f"""
You are analyzing educational content to build a chapter outline.
Break the content below into 5-10 logical chapters/topics.

For each chapter return: title, a 1-2 sentence summary, and {ref_kind}
approximating where that chapter begins in the source (best estimate is fine).

Return ONLY valid JSON in this exact shape:
{{"outline": [{{"title": "...", "summary": "...", "ref": <number>}}]}}

CONTENT:
{full_text[:12000]}
"""
    data = ask_llm_json(prompt, system="You are a precise educational content analyst.")
    return data.get("outline", [])


def generate_flashcards(full_text: str) -> list[dict]:
    prompt = f"""
Extract the 5 most important technical terms/concepts from the content below
and write a clear, exam-ready definition for each, in your own words.

Return ONLY valid JSON:
{{"flashcards": [{{"term": "...", "definition": "..."}}]}}

CONTENT:
{full_text[:12000]}
"""
    data = ask_llm_json(prompt, system="You are an expert tutor creating study flashcards.")
    return data.get("flashcards", [])


def answer_with_context(question: str, retrieved_chunks: list[dict]) -> str:
    context = "\n\n".join(
        f"[Source ref: {c['source_ref']}] {c['text']}" for c in retrieved_chunks
    )
    prompt = f"""
Answer the question using ONLY the context below. Cite the source ref(s) you
used inline like (ref: 123.4). If the answer isn't in the context, say so.

CONTEXT:
{context}

QUESTION: {question}
"""
    return ask_llm(prompt, system="You are a helpful study assistant that answers strictly from provided context.")