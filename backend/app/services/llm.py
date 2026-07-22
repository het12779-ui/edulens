"""
Single abstraction over the LLM provider so the rest of the app never cares
whether we're calling Groq, OpenAI, or Gemini. Swapping providers is a
one-line config change.
"""
import json
from app.config import get_settings

settings = get_settings()


def _call_groq(prompt: str, system: str = "", json_mode: bool = False) -> str:
    from groq import Groq
    client = Groq(api_key=settings.groq_api_key)
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    kwargs = {}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile", messages=messages, temperature=0.2, **kwargs,
    )
    return resp.choices[0].message.content


def _call_openai(prompt: str, system: str = "", json_mode: bool = False) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=settings.openai_api_key)
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    kwargs = {}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    resp = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages, temperature=0.2, **kwargs,
    )
    return resp.choices[0].message.content


def _call_gemini(prompt: str, system: str = "", json_mode: bool = False) -> str:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=settings.gemini_api_key)

    config = types.GenerateContentConfig(
        temperature=0.2,
        system_instruction=system if system else None,
        response_mime_type="application/json" if json_mode else "text/plain",
    )

    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=config,
    )
    return resp.text


def ask_llm(prompt: str, system: str = "", json_mode: bool = False) -> str:
    """Single entry point every other service should use."""
    if settings.llm_provider == "openai":
        return _call_openai(prompt, system, json_mode)
    if settings.llm_provider == "gemini":
        return _call_gemini(prompt, system, json_mode)
    return _call_groq(prompt, system, json_mode)


def ask_llm_json(prompt: str, system: str = "") -> dict:
    """Convenience wrapper that parses JSON and retries once on failure."""
    raw = ask_llm(prompt, system=system, json_mode=True)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        fixed = ask_llm(
            f"The following is supposed to be valid JSON but failed to parse. "
            f"Return ONLY corrected valid JSON, nothing else:\n\n{raw}",
            json_mode=True,
        )
        return json.loads(fixed)