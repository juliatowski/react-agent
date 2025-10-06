import pytest
from react_agent.steps.final_answer import synthesize_final_answer


@pytest.mark.integration
def test_final_answer():
    """Integration test: actually calls the LLM to synthesize final answer."""
    original = "What is 12 * 7 and when was GPT-3 released?"
    subtask_results = {
        "Calculate 12 * 7": "84",
        "Look up GPT-3 release date": "GPT-3 was released in June 2020.",
    }

    result = synthesize_final_answer(original, subtask_results, model="qwen2.5")

    # Print result for inspection
    print("\nSynthesized final answer:\n", result)

    # LLM outputs vary in wording, so only check for key facts
    assert isinstance(result, str)
    assert "84" in result
    assert "2020" in result
    assert "GPT-3" in result
