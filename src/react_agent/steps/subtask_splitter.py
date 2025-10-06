from react_agent.llm_client import LLMClient


def split_into_subtasks(goal: str, model: str = "qwen2.5", max_subtasks: int = 5) -> list[str]:
    """
    Step 1: Given a goal, ask the LLM to split it into sequential subtasks.
    Maximum number of subtasks returned can be controlled.
    """
    client = LLMClient(model)

    system_prompt = (
        f"You are an AI assistant that splits user goals into a logical sequence of subtasks. "
        f"Each subtask should be clear, short, and actionable. "
        f"Return no more than {max_subtasks} subtasks, as a numbered list."
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

    # Ensure we don't exceed max_subtasks
    return steps[:max_subtasks]
