# Command to run:
# PYTHONPATH=src python tests/newtests/test_extract_urls.py

from pathlib import Path
import time

from react_agent.logging_config import set_logging
from react_agent.tools.url_extractor import extract_text_from_url


# enable normal logging (set to 2 for verbose)
set_logging(1)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


URLS = [
    "https://mkdev.me/b/consulting/eu-ai-act",
    "https://consulting.tuv.com/en/eu-ai-act",
    "https://rhymetec.com/eu-ai-act-compliance/",
    "https://www.mondaq.com/unitedstates/new-technology/1443370/the-eu-ai-act-and-obligations-for-companies-operating-in-the-european-union",
]


def slugify(url: str) -> str:
    return (
        url.replace("https://", "")
        .replace("http://", "")
        .replace("/", "_")
        .replace("?", "")
        .replace("&", "")
        .replace("=", "")
    )


def run_extract(url: str):
    print("=" * 80)
    print(f"URL: {url}")
    start = time.time()

    text = extract_text_from_url(
        url,
        timeout_s=12,
        max_chars=None,  # save FULL text
    )

    elapsed = time.time() - start
    print(f"TIME: {elapsed:.2f}s")
    print(f"TEXT LENGTH: {len(text)} chars")

    if not text:
        print("⚠️  No text extracted\n")
        return

    filename = DATA_DIR / f"extracted_{slugify(url)}.txt"
    filename.write_text(text, encoding="utf-8")

    print(f"SAVED TO: {filename}")

    print("\nPREVIEW:")
    print(text[:800])
    print("\n")


if __name__ == "__main__":
    for url in URLS:
        run_extract(url)
