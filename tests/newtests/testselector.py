from react_agent.steps.tool_selector import assign_tools_to_subtasks
from react_agent.logging_config import set_logging

MODEL = "qwen2.5"

def test_tool_selector(subtasks):
    result = assign_tools_to_subtasks(subtasks, model=MODEL)
    print("\nFinal mapping:")
    print(result)


if __name__ == "__main__":
    set_logging(2)

    prompts = [
        "add two numbers",
        "who is einstein",
        "find similar research papers about AI",
        "what is the capital of france",
        "summarize wikipedia page about Alan Turing"
    ]

    test_tool_selector(prompts)
