import pytest
from react_agent.steps.subtask_evaluator import evaluate_subtask

@pytest.mark.integration
def test_evaluate_subtask_with_llm():
    """Integration test: actually calls the LLM to evaluate correctness."""
    subtask = "Calculate 12 * 7"
    result = "84"

    evaluated_result, score, is_correct = evaluate_subtask(subtask, result, model="qwen2.5")

    # Print so pytest -s shows the evaluation
    print("\n--- LLM Evaluation ---")
    print(f"Subtask: {subtask}")
    print(f"Result: {result}")
    print(f"Evaluated result: {evaluated_result}")
    print(f"Score: {score}")
    print(f"Is correct: {is_correct}")
    print("----------------------\n")

    # Assertions
    assert isinstance(evaluated_result, str)
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0
    assert isinstance(is_correct, bool)

    # Since this is a correct answer, we expect score to be reasonably high
    assert score >= 0.5
    assert is_correct is True
