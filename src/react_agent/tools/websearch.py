from ddgs import DDGS
from react_agent.logging_config import vlog

class WebSearch:
    name = "web_search"
    description = "Search the web using DuckDuckGo (no API key)."

    def run(self, query: str, k: int = 5) -> str:
        vlog(f"[DDG] Searching for: {query}")
        items = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=k):
                items.append(
                    f"- {r.get('title')}\n"
                    f"  URL: {r.get('href')}\n"
                    f"  Snippet: {r.get('body')}"
                )
        return "\n\n".join(items) if items else f"No results for {query!r}"
