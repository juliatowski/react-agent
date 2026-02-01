# Command to run:
# PYTHONPATH=src python tests/newtests/test_website_filter.py

from pathlib import Path
import time

from react_agent.logging_config import set_logging
from react_agent.tools.website_filter import extract_relevant_info


def slugify(text: str) -> str:
    return (
        text.lower()
        .strip()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("?", "")
        .replace(",", "")
        .replace(":", "")
        .replace(";", "")
        .replace("&", "and")
    )


def main():
    # 0 = no logging, 1 = normal, 2 = verbose
    set_logging(2)

    data_dir = Path("data")
    if not data_dir.exists():
        print("ERROR: data/ folder not found. Run your URL extraction test first.")
        return

    # Pick extracted files. Adjust the glob if your naming differs.
    extracted_files = sorted(data_dir.glob("extracted_*.txt"))
    if not extracted_files:
        print("ERROR: No extracted_*.txt files found in data/.")
        print("Hint: create them with your URL extraction script first.")
        return

    # Subtasks to test relevance extraction with
    subtasks = [
        "Extract the key compliance requirements relevant for AI consulting companies under the EU AI Act.",
        "Extract any mentioned dates, enforcement timelines, and obligations (with exact wording if present).",
        "Extract concrete action items or checklists suggested by the text.",
    ]

    model = "llama3.2:1b"

    print(f"Found {len(extracted_files)} extracted files in data/")
    print(f"Using model: {model}\n")

    for fpath in extracted_files:
        text = fpath.read_text(encoding="utf-8", errors="ignore").strip()
        if not text:
            print(f"Skipping empty file: {fpath.name}")
            continue

        print("=" * 90)
        print(f"SOURCE FILE: {fpath.name}")
        print(f"TEXT LENGTH: {len(text)} chars\n")

        for subtask in subtasks:
            print("-" * 90)
            print(f"SUBTASK: {subtask}")

            start = time.time()
            out = extract_relevant_info(subtask, text, model=model, max_chars=12000)
            elapsed = time.time() - start

            out_name = f"relevant_{fpath.stem}__{slugify(subtask)[:60]}.txt"
            out_path = data_dir / out_name
            out_path.write_text(out, encoding="utf-8")

            print(f"Saved: {out_path}")
            print(f"TIME: {elapsed:.2f}s | OUTPUT LENGTH: {len(out)} chars")
            print("\nPREVIEW:")
            print(out[:700])
            print()

    print("\nDone.")


if __name__ == "__main__":
    main()
