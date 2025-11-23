from __future__ import annotations
from ddgs import DDGS
from react_agent.logging_config import log, vlog  

#Crawler could be added

class WebSearch:
    name = "web_search"
    description = "Search the web for the latest information and current events."

    def run(self, query: str, k: int = 5) -> str:
        vlog(f"WebSearch query: {query}")
        try:
            results = []
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=k):
                    results.append(r)

            if not results:
                log(f"WebSearch: no results for query='{query}'")
                return f"No results found for query: {query!r}"

            formatted = []
            for r in results[:k]:
                title = r.get("title", "").strip()
                link = r.get("href", "").strip()
                snippet = r.get("body", "").strip()
                formatted.append(f"- {title}\n  {link}\n  {snippet}")

            out = "\n\n".join(formatted)
            vlog(f"WebSearch returned {len(results)} results")
            return out

        except Exception as e:
            log(f"WebSearch error for query='{query}': {e}")
            return f"Web search error: {e}"
