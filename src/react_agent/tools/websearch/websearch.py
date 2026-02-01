from ddgs import DDGS
from react_agent.config.logging_config import vlog


class WebSearch:
    name = "web_search"
    description = "Search the web using DuckDuckGo"

    def __init__(
        self,
        max_results: int = 5,
        max_pages_to_fetch: int = 3,
        max_chars_per_page: int = 3000,
        timeout_s: int = 12,
        sleep_s: float = 0.3,
    ):
        self.max_results = max_results
        self.max_pages_to_fetch = max_pages_to_fetch
        self.max_chars_per_page = max_chars_per_page
        self.timeout_s = timeout_s
        self.sleep_s = sleep_s

    def run(self, query: str, k: int | None = None) -> str:
        vlog(f"[DDG] Searching for: {query}")

        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=k or self.max_results):
                results.append(
                    f"- {r.get('title')}\n"
                    f"  URL: {r.get('href')}\n"
                    f"  Snippet: {r.get('body')}"
                )

        return "\n\n".join(results) if results else f"No results for {query!r}"
