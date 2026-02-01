import json
from react_agent.llm.llm_client import LLMClient
from react_agent.config.logging_config import log, vlog, time_block


def evaluate_subtask(subtask: str, result: str, model: str = "qwen2.5") -> str:
    """
    Use an LLM to evaluate whether a single subtask result is correct.
    Returns a JSON string.
    """

    with time_block("SUBTASK_EVALUATOR"):
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
            result_value = parsed.get("result", result)
            score_value = float(parsed.get("score", 0.5))
            correct_value = bool(parsed.get("is_correct", True))

        except Exception:
            # fallback if LLM output is invalid
            result_value = result
            score_value = 0.5
            correct_value = True

        out = json.dumps({
            "result": result_value,
            "score": score_value,
            "is_correct": correct_value
        })
        vlog(f"SUBTASK_EVALUATOR output: {out}")
        return out
