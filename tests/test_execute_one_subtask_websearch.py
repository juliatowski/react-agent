import pytest
from react_agent.steps.subtask_handler import execute_one_subtask


def test_execute_one_subtask_chained_websearch():
    previous_results = {}

    # Step 1: Find breakthroughs
    subtask1 = "Find the latest AI breakthroughs in healthcare"
    result1, score1, ok1 = execute_one_subtask(
        subtask=subtask1,
        tool_name="web_search",
        previous_results=previous_results,
        model="qwen2.5",
        threshold=0.5,
    )
    previous_results[subtask1] = result1

    print(f"\n Step 1: {subtask1}\n➡️ Result:\n{result1}\n✅ Score: {score1}, Correct: {ok1}")

    assert isinstance(result1, str)
    assert result1.strip() != ""
    assert "http" in result1 or "No results" in result1 or "Web search error" in result1

    # Step 2: Use Step 1 as context
    subtask2 = "Explain the potential impact of these AI breakthroughs on patient outcomes"
    result2, score2, ok2 = execute_one_subtask(
        subtask=subtask2,
        tool_name="web_search",
        previous_results=previous_results,
        model="qwen2.5",
        threshold=0.5,
    )
    previous_results[subtask2] = result2

    print(f"\n Step 2: {subtask2}\n➡️ Result:\n{result2}\n Score: {score2}, Correct: {ok2}")

    assert isinstance(result2, str)
    assert result2.strip() != ""

    # Step 3: Narrow it down
    subtask3 = "Find recent news on AI use for cancer diagnosis"
    result3, score3, ok3 = execute_one_subtask(
        subtask=subtask3,
        tool_name="web_search",
        previous_results=previous_results,
        model="qwen2.5",
        threshold=0.5,
    )

    print(f"\n Step 3: {subtask3}\n➡️ Result:\n{result3}\n Score: {score3}, Correct: {ok3}")

    assert isinstance(result3, str)
    assert result3.strip() != ""
