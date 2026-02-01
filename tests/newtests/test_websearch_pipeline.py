# Command to run:
# PYTHONPATH=src python tests/newtests/test_websearch_pipeline.py

from pathlib import Path
import time

from react_agent.logging_config import set_logging
from react_agent.tools.websearch_pipeline import enrich_subtask_with_web


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


SUBTASKS = [
    "Summarize EU AI Act requirements relevant for AI consulting companies.",
    "List key compliance deadlines and enforcement timeline mentioned in sources about the EU AI Act.",
    "Extract concrete compliance action items/checklist steps for companies offering AI services in the EU.",
]


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
    # 0 = no logs, 1 = normal, 2 = verbose
    set_logging(2)

    llm_model = "llama3.2:1b"
    max_urls = 3

    print(f"Running {len(SUBTASKS)} subtasks with llm_model={llm_model}, max_urls={max_urls}\n")

    for i, subtask in enumerate(SUBTASKS, start=1):
        print("=" * 90)
        print(f"SUBTASK {i}/{len(SUBTASKS)}:")
        print(subtask)
        print()

        start = time.time()
        result = enrich_subtask_with_web(
            subtask=subtask,
            llm_model=llm_model,
            max_urls=max_urls,
            extract_max_chars_per_page=8000,
        )
        elapsed = time.time() - start

        # Save full output
        out_path = DATA_DIR / f"web_enrich_{i:02d}__{slugify(subtask)[:60]}.txt"
        content = []
        content.append(f"SUBTASK:\n{subtask}\n")
        content.append(f"TIME: {elapsed:.2f}s\n")
        content.append("URLS USED:")
        for u in result.get("urls", []):
            content.append(f"- {u}")
        content.append("\nFILTERED RESULT:\n")
        content.append(result.get("filtered", ""))

        out_path.write_text("\n".join(content), encoding="utf-8")

        print(f"TIME: {elapsed:.2f}s")
        print(f"SAVED: {out_path}")
        print("\nPREVIEW:\n")
        print(result.get("filtered", "")[:800])
        print()

    print("Done.")


if __name__ == "__main__":
    main()
