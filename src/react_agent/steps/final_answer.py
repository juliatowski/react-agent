import json
from react_agent.llm_client import LLMClient


def synthesize_final_answer(original_prompt: str, subtask_results: dict[str, str], model: str = "qwen2.5") -> str:
    """
    Combine subtask results into a final coherent answer to the original prompt.
    """
    client = LLMClient(model)

    prompt = f"""
    You are a reasoning assistant.

    The user asked: "{original_prompt}"

    You decomposed this into subtasks, and here are the results:
    {subtask_results}

    Now, synthesize a final answer for the user.
    Be concise, clear, and directly answer the original prompt.
    """

    raw = client.chat(prompt)

    # Minimal cleanup: ensure string output
    if not isinstance(raw, str):
        try:
            raw = json.dumps(raw)
        except Exception:
            raw = str(raw)

    return raw.strip()
