import pytest
from react_agent.steps.tool_excecutor import execute_subtasks


@pytest.mark.integration
def test_execute_subtasks_integration():
    """Integration test: run real tools + evaluator in the retry loop."""
    subtasks = [
        "Calculate 12 * 7",
        "Look up GPT-3 release date"
    ]
    tool_mapping = {
        "Calculate 12 * 7": "calculator",
        "Look up GPT-3 release date": "wikipedia",
    }

    results = execute_subtasks(
        subtasks,
        tool_mapping,
        model="qwen2.5",
        threshold=0.7,
        max_retries=1,
    )

    # Print results so we can inspect the flow
    print("\n--- Execute Subtasks Integration ---")
    for sub, res in results.items():
        print(f"{sub} -> {res}")
    print("------------------------------------\n")

    # Assertions
    assert isinstance(results, dict)
    assert "Calculate 12 * 7" in results
    assert "Look up GPT-3 release date" in results

    # Calculator task should yield "84" with high confidence
    assert "84" in results["Calculate 12 * 7"]

    # Wikipedia task: wording may vary, but should mention "GPT-3" and a year
    assert "GPT-3" in results["Look up GPT-3 release date"]
    assert any(year in results["Look up GPT-3 release date"] for year in ["2020", "2021"])
