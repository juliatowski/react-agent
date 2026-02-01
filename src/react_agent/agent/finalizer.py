import json
from typing import List
from react_agent.llm.llm_client import LLMClient
from react_agent.config.logging_config import log, vlog, time_block


def synthesize_final_answer(original_prompt: str, results: List[dict], model: str) -> str:
    """
    Generate the final answer using the LLM.
    The LLM sees:
      - the original question
      - the JSON results of all subtasks
    """

    with time_block("FINAL_ANSWER"):
        client = LLMClient(model)
        json_blob = json.dumps(results, indent=2)

        vlog(f"FINAL_ANSWER sees results: {json_blob}")

        prompt = f"""
The user asked:
"{original_prompt}"

Here are the subtask results in JSON:
{json_blob}

Synthesize a clear and concise final answer.
Do NOT repeat the JSON.
Do NOT list subtasks.
Just answer the user's question using the information.
"""

        response = client.chat(prompt)

        return response.strip()
