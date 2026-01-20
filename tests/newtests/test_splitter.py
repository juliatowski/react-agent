#Command to run this test:
# PYTHONPATH=src python tests/newtests/test_splitter.py

from react_agent.steps.subtask_splitter import split_into_subtasks

MODEL = "llama3.2:1b"

TEST_PROMPTS = [
    (
        "I’m planning a 7-day trip to Japan for the first time. I want to visit Tokyo and Kyoto, "
        "experience local food, avoid tourist traps as much as possible, and keep the budget under €2,000. "
        "Please help me plan the trip, including a rough daily itinerary, transport tips, and food recommendations."
    ),

    (
        "I want to start a YouTube channel focused on software engineering interview preparation. "
        "I already have some coding experience but no audience. Help me figure out what content to create first, "
        "how often to post, what tools I’ll need, and how to grow the channel in the first 6 months."
    ),

    (
        "Explain the 2008 financial crisis to someone with no economics background, but also include enough detail "
        "that a university student could use it for an exam. Cover the main causes, key events, and long-term consequences."
    ),

    (
        "I’m trying to understand how neural networks learn, but I keep getting confused by math-heavy explanations. "
        "Please explain the intuition behind training neural networks, including loss functions and backpropagation, "
        "using simple examples and analogies."
    ),

    (
        "I’ve never cooked lasagna before, but I want to make one from scratch for a dinner with friends. "
        "Please break down the process step by step, including ingredients, preparation order, timing, "
        "and common mistakes beginners make."
    ),
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
