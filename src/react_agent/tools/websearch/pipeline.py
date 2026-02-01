from __future__ import annotations

import re
from typing import List, Dict, Any

from react_agent.config.logging_config import log, vlog, time_block
from react_agent.tools.websearch import WebSearch
from react_agent.tools.websearch.url_extractor import extract_text_from_url
from react_agent.tools.websearch.website_filter import extract_relevant_info


_URL_RE = re.compile(r"URL:\s*(https?://\S+)")


def _urls_from_websearch_output(text: str, max_urls: int) -> List[str]:
    """Extract URLs from the formatted WebSearch output."""
    urls = _URL_RE.findall(text or "")
    out: List[str] = []
    seen = set()
    for u in urls:
        if u not in seen:
            out.append(u)
            seen.add(u)
        if len(out) >= max_urls:
            break
    return out


def enrich_subtask_with_web(
    subtask: str,
    search: WebSearch | None = None,
    llm_model: str = "llama3.2:1b",
    max_urls: int = 3,
    extract_max_chars_per_page: int = 8000,
) -> Dict[str, Any]:
    """
    Given a subtask, do:
      1) web search (DDG)
      2) extract top URLs
      3) fetch + extract page text for each URL
      4) LLM extracts the most relevant info for THIS subtask

    Returns a dict with the final filtered result and metadata.
    """
    subtask = (subtask or "").strip()
    if not subtask:
        return {"subtask": subtask, "urls": [], "filtered": "Empty subtask."}

    search = search or WebSearch(max_results=5, max_pages_to_fetch=max_urls)

    with time_block("ENRICH_SUBTASK_WITH_WEB"):
        # 1) Search
        vlog(f"[ENRICH] Searching for subtask: {subtask}")
        search_output = search.run(subtask)
        vlog(f"[ENRICH] Search output (first 800 chars):\n{search_output[:800]}")

        # 2) Parse URLs
        urls = _urls_from_websearch_output(search_output, max_urls=max_urls)
        if not urls:
            return {"subtask": subtask, "urls": [], "filtered": "No URLs found from web search output."}

        log(f"[ENRICH] Using {len(urls)} URL(s) for extraction")

        # 3) Extract page text
        extracted_blocks: List[str] = []
        for url in urls:
            text = extract_text_from_url(url, max_chars=extract_max_chars_per_page)
            if not text:
                continue
            extracted_blocks.append(f"URL: {url}\n{text}")

        combined_text = "\n\n---\n\n".join(extracted_blocks)
        if not combined_text.strip():
            return {"subtask": subtask, "urls": urls, "filtered": "Failed to extract any usable text from URLs."}

        # 4) LLM relevance filter
        filtered = extract_relevant_info(
            subtask=subtask,
            extracted_text=combined_text,
            model=llm_model,
            max_chars=12000,
        )

        return {
            "subtask": subtask,
            "urls": urls,
            "filtered": filtered,
        }
