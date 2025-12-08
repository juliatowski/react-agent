from react_agent.steps.subtask_splitter import split_into_subtasks

MODEL = "llama3.2:1b"

# List of prompts you want to test the splitter with
TEST_PROMPTS = [
    "Plan me a 3-day itinerary for a trip to Paris.",
    "Write a step-by-step guide on how to start a YouTube channel.",
    "Analyze the causes of the 2008 financial crisis.",
    "Explain how neural networks learn in simple terms.",
    "Break down the process of cooking a lasagna.",
    "Help me prepare for a junior software engineering interview.",
    "Outline the main points for an essay about climate change.",
    "Give me instructions for assembling IKEA furniture.",
]


def test_splitter(prompt):
    print("=" * 80)
    print(f"Prompt:\n{prompt}\n")
    out = split_into_subtasks(prompt, model=MODEL)
    print("Splitter Output:")
    print(out)
    print()


if __name__ == "__main__":
    print(f"Testing subtask splitter with model: {MODEL}\n")

    for p in TEST_PROMPTS:
        test_splitter(p)
