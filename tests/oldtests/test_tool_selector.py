from react_agent.steps import tool_selector


def test_assign_tools_to_subtasks_integration():
    subtasks = [
        "Calculate 12 * 7",
        "Look up GPT-3 on Wikipedia",
        "Search latest AI news on the web",
    ]

    mapping = tool_selector.assign_tools_to_subtasks(subtasks, model="qwen2.5")

    assert isinstance(mapping, dict)
    assert all(s in mapping for s in subtasks)

    print("\nSubtasks and assigned tools:")
    for sub, tool in mapping.items():
        print(f"- {sub} -> {tool}")
