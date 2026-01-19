import time

from react_agent.tools.websearch import WebSearch


def run_query(ws: WebSearch, query: str):
    print("=" * 80)
    print(f"QUERY: {query}")
    start = time.time()

    result = ws.run(query)

    elapsed = time.time() - start
    print(f"TIME: {elapsed:.2f}s")
    print(f"OUTPUT LENGTH: {len(result)} chars\n")

    # Print only the first ~800 chars so
    #  your terminal doesn't explode
    preview = result[:800]
    print("PREVIEW:")
    print(preview)
    print("\n")


if __name__ == "__main__":
    ws = WebSearch(
        max_results=5,
        max_pages_to_fetch=3,
        max_chars_per_page=3000,
        timeout_s=12,
        sleep_s=0.3,
    )

    queries = [
        "machine learning consulting market Europe trends",
        "EU AI Act requirements for AI consulting companies",
        "GDPR compliance machine learning services",
    ]

    for q in queries:
        run_query(ws, q)
