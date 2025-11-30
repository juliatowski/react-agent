from react_agent.steps.subtask_excecutor import execute_single_subtask
from react_agent.logging_config import set_logging

MODEL = "qwen2.5"

def test_executor(subtasks, tools):
    for subtask, tool in zip(subtasks, tools):
        print(f"\n--- Executing subtask: {subtask} (tool={tool}) ---")
        result = execute_single_subtask(subtask, tool_name=tool, model=MODEL)
        print(result)


if __name__ == "__main__":
    set_logging(2)   # enable verbose logs

    subtasks = [
        "add two numbers",
        "who is einstein",
        "find similar research papers about AI",
        "what is the capital of france",
        "summarize wikipedia page about Alan Turing"
    ]

    # tools MUST match length of subtasks
    # Here you can test different behaviors:
    tools = [
        "calculator",
        "wikipedia",
        "vector_search",
        "wikipedia",
        None,            # fallback to LLM
    ]

    test_executor(subtasks, tools)