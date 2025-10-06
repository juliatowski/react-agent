from __future__ import annotations
from ddgs import DDGS

#Crawler could be added

class WebSearch:
    """A tool that runs DuckDuckGo searches and returns formatted results."""

    name = "web_search"
    description = "Search the web for the latest information and current events."

    def run(self, query: str, k: int = 5) -> str:
        """
        Run a DuckDuckGo search and return up to k results (title + link + snippet).
        """
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=k))

            if not results:
                return f"No results found for query: {query!r}"

            formatted = []
            for r in results[:k]:
                title = r.get("title", "").strip()
                link = r.get("href", "").strip()
                snippet = r.get("body", "").strip()
                formatted.append(f"- {title}\n  {link}\n  {snippet}")

            return "\n\n".join(formatted)

        except Exception as e:
            return f"Web search error: {e}"
