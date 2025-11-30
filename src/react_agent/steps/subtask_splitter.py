import json
from react_agent.llm_client import LLMClient
from react_agent.logging_config import log, vlog, time_block


def split_into_subtasks(goal: str, model: str = "qwen2.5", max_subtasks: int = 5) -> str:

    """
    Step 1: A task is being split into subtasks for the model to solve the parts individually using the best model for each sutask. 
    Maximum number of subtasks returned can be controlled.
    
    Returns:
        JSON string: {"subtasks": [...]}
    """

    with time_block("SUBTASK_SPLITTER"):
        
        client = LLMClient(model)

        system_prompt = (
            f"You break a user goal into a small number of LLM-solvable subtasks. "
            f"Each subtask must be: atomic, self-contained, actionable, and directly solvable by an LLM. "
            f"Do not produce high-level advice, explanations, or planning instructions. "
            f"Do not include steps like 'research' or 'choose'. "
            f"Instead, convert them into concrete LLM tasks such as 'List...', 'Summarize...', 'Gather...', 'Generate...', etc. "
            f"Return between 1 and {max_subtasks} subtasks. "
            f"Output only a numbered list of subtasks with no additional text."
        )


        raw = client.chat(f"{system_prompt}\n\nGoal: {goal}\n\nSubtasks:")

        steps = []
        for line in raw.splitlines():
            line = line.strip(" \t-•")
            if not line:
                continue
            if line[0].isdigit():
                # Remove leading "1.", "2)" etc.
                line = line.split(".", 1)[-1] if "." in line[:3] else line
                line = line.split(")", 1)[-1] if ")" in line[:3] else line
            steps.append(line.strip())

        steps = steps[:max_subtasks]

        # JSON output
        result = json.dumps({"subtasks": steps})
        vlog(f"SUBTASK_SPLITTER output: {result}")
        return result
