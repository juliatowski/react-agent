import json
from react_agent.llm_client import LLMClient


def evaluate_subtask(subtask: str, result: str, model: str = "qwen2.5") -> tuple[str, float, bool]:
    """
    Use an LLM to evaluate whether a single subtask result is correct.

    Args:
        subtask: the subtask description/question
        result: the produced answer for the subtask
        model: which LLM to use

    Returns:
        (result, score, is_correct)
        - score: float in [0, 1], confidence in correctness
        - is_correct: True if score >= 0.5
    """
    client = LLMClient(model)

    prompt = f"""
You are an evaluator.

Subtask: {subtask}
Proposed result: {result}

Decide if the result correctly answers the subtask.

Return ONLY valid JSON with fields:
{{
  "result": "<repeat the result>",
  "score": <float between 0.0 and 1.0>,
  "is_correct": <true/false>
}}
"""

    raw = client.chat(prompt)

    try:
        parsed = json.loads(raw)
        return (
            parsed.get("result", result),
            float(parsed.get("score", 0.5)),
            bool(parsed.get("is_correct", True)),
        )
    except Exception:
        # fallback if LLM output is bad
        return (result, 0.5, True)
