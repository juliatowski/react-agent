from react_agent.steps.subtask_splitter import split_into_subtasks

MODEL = "llama3.2:1b"
def test_splitter(prompt):
    out = split_into_subtasks(prompt, model=MODEL)
    print(out)

if __name__ == "__main__":
    test_splitter("plan me a 3 day itenary for a trip to Paris")
