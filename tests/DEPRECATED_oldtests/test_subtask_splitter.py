from react_agent.steps import subtask_splitter


def test_split_into_subtasks_integration():
    goal = "Compare Vienna and Berlin for AI research opportunities."
    subtasks = subtask_splitter.split_into_subtasks(goal, model="qwen2.5", max_subtasks=5)

    # Basic checks
    assert isinstance(subtasks, list)
    assert len(subtasks) > 0
    assert all(isinstance(s, str) and s.strip() for s in subtasks)

    # Log results so you can see what the model produced
    print("\nGoal:", goal)
    print("\nSequential subtasks:")
    for i, task in enumerate(subtasks, 1):
        print(f"{i}. {task}")
