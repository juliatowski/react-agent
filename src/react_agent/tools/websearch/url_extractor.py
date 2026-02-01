import requests
import trafilatura
from react_agent.config.logging_config import log


def extract_text_from_url(
    url: str,
    timeout_s: int = 12,
    max_chars: int | None = 8000,
    user_agent: str = "Mozilla/5.0 (compatible; WebExtractor/1.0)",
) -> str:
    """
    Fetches a URL and extracts the main article/page text.

    Returns:
        Extracted plain text (possibly truncated), or an empty string on failure.
    """

    try:
        resp = requests.get(
            url,
            headers={"User-Agent": user_agent},
            timeout=timeout_s,
        )
        resp.raise_for_status()
    except Exception as e:
        log(f"[WEB_EXTRACT] Failed to fetch {url}: {e}")
        return ""

    content_type = resp.headers.get("content-type", "").lower()
    if "text/html" not in content_type:
        log(f"[WEB_EXTRACT] Skipping non-HTML content: {url}")
        return ""

    html = resp.text

    text = trafilatura.extract(
        html,
        include_comments=False,
        include_tables=False,
        favor_recall=False,
    )

    if not text:
        log(f"[WEB_EXTRACT] No extractable text found for {url}")
        return ""

    # Normalize whitespace
    text = " ".join(text.split())

    # Optional truncation
    if max_chars and len(text) > max_chars:
        text = text[:max_chars] + "…"

    return text
