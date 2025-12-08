import json
from pathlib import Path

from react_agent.logging_config import set_logging
from react_agent.steps.pipeline import react_pipeline


def main():
    # 0 = no logging, 1 = normal logging, 2 = verbose logging
    set_logging(2)

    path = Path("src/data/test_prompts.json")

    if not path.exists():
        print(f"ERROR: Prompt file not found: {path}")
        return

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    prompts = data.get("prompts", [])
    if not prompts:
        print(f"No prompts found in {path}")
        return

    print(f"Running {len(prompts)} prompts...\n")

    for entry in prompts:
        pid = entry.get("id", "<no-id>")
        task = entry.get("task", "")

        print("=" * 80)
        print(f"ID:   {pid}")
        print(f"Task: {task}\n")

        answer = react_pipeline(task, model="llama3.2:1b")

        print("Answer:")
        print(answer)
        print()


if __name__ == "__main__":
    main()
