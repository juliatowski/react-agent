# Command to run this test:
# PYTHONPATH=src python tests/newtests/test_websearch.py

import time
from pathlib import Path

from react_agent.tools.websearch import WebSearch


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def slugify(text: str) -> str:
    return (
        text.lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("?", "")
        .replace(",", "")
    )


def run_query(ws: WebSearch, query: str):
    print("=" * 80)
    print(f"QUERY: {query}")
    start = time.time()

    result = ws.run(query)

    elapsed = time.time() - start
    print(f"TIME: {elapsed:.2f}s")
    print(f"OUTPUT LENGTH: {len(result)} chars\n")

    # Save full output to file
    filename = DATA_DIR / f"websearch_{slugify(query)[:60]}.txt"
    filename.write_text(result, encoding="utf-8")

    print(f"FULL OUTPUT SAVED TO: {filename}")

    # Print only a preview
    preview = result[:800]
    print("\nPREVIEW:")
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
