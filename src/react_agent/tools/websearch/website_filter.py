from __future__ import annotations

import json
from typing import Any, Dict

from react_agent.llm.llm_client import LLMClient
from react_agent.config.logging_config import log, vlog


def extract_relevant_info(
    subtask: str,
    extracted_text: str,
    model: str = "llama3.2:1b",
    max_chars: int = 12000,
) -> str:
    """
    Extract the most relevant information from extracted_text for the given subtask.

    - Uses only the provided extracted_text (no outside knowledge)
    - Returns concise bullet points + key quotes + missing info (if any)

    Returns a plain string that is safe to print.
    """

    if not extracted_text or not extracted_text.strip():
        return "No extracted text provided."

    # Cap context to avoid blowing up the model context window
    text = extracted_text.strip()
    if max_chars and len(text) > max_chars:
        text = text[:max_chars] + "\n...[TRUNCATED]..."

    client = LLMClient(model)

    system_prompt = (
        "You are an information extractor.\n"
        "Your job: extract only the information that is relevant to the user's subtask.\n"
        "Rules:\n"
        "- Use ONLY the provided text. Do not add outside facts.\n"
        "- Be concise and specific.\n"
        "- Prefer bullet points.\n"
        "- If important info is missing from the text, say what is missing.\n"
        "Return ONLY valid JSON with keys:\n"
        '{"relevant_points":[...], "key_quotes":[...], "missing_info":[...]}\n'
        "No markdown. No extra keys."
    )

    prompt = (
        f"{system_prompt}\n\n"
        f"SUBTASK:\n{subtask}\n\n"
        f"TEXT:\n{text}\n\n"
        "JSON:"
    )

    raw = client.chat(prompt)
    vlog(f"[RELEVANCE_EXTRACTOR] LLM raw output:\n{raw}")

    # Parse JSON safely; if it fails, just return raw
    try:
        data: Dict[str, Any] = json.loads(raw)
        points = data.get("relevant_points", [])
        quotes = data.get("key_quotes", [])
        missing = data.get("missing_info", [])

        # Normalize to strings
        points = [str(x).strip() for x in points if str(x).strip()]
        quotes = [str(x).strip() for x in quotes if str(x).strip()]
        missing = [str(x).strip() for x in missing if str(x).strip()]

        out_lines = []
        if points:
            out_lines.append("Relevant points:")
            out_lines.extend([f"- {p}" for p in points])

        if quotes:
            out_lines.append("")
            out_lines.append("Key quotes:")
            out_lines.extend([f'- "{q}"' for q in quotes])

        if missing:
            out_lines.append("")
            out_lines.append("Missing info:")
            out_lines.extend([f"- {m}" for m in missing])

        return "\n".join(out_lines).strip() or raw

    except Exception as e:
        log(f"[RELEVANCE_EXTRACTOR] Failed to parse JSON ({e}). Returning raw output.")
        return raw
