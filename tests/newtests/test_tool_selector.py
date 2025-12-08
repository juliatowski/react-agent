from react_agent.steps.tool_selector import assign_tools_to_subtasks
from react_agent.logging_config import set_logging

# Turn on full logging
set_logging(2)

TEST_SUBTASKS = [
    "Search for the population of Germany.",
    "Calculate 25 * 18.",
    "Find recent research about transformer attention mechanisms.",
    "Explain how photosynthesis works.",
    "Translate 'good morning' to French.",
]

def run_test():
    print("\n=== Running Tool Selector Test (No Mocking) ===\n")

    print("Subtasks to evaluate:")
    for t in TEST_SUBTASKS:
        print(" •", t)
    print()

    mapping = assign_tools_to_subtasks(TEST_SUBTASKS, model="qwen2.5")

    print("\n=== Tool Selector Output ===")
    for subtask, tool in mapping.items():
        print(f"\nSubtask: {subtask}")
        print(f"Chosen Tool: {tool}")

    print("\nDone.\n")


if __name__ == "__main__":
    run_test()
