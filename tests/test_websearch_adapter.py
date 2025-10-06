from react_agent.adapters.websearch_adapter import WebSearchAdapter


def test_websearch_adapter_integration():
    adapter = WebSearchAdapter(model="qwen2.5:7b")
    subtasks = [
        "Find the latest AI breakthroughs in healthcare",
        "What are the newest SpaceX rocket launches?",
        "Summarize climate change policies in 2025",
    ]

    for subtask in subtasks:
        results = adapter.run(subtask, k=2)

        #sanity checks
        assert isinstance(results, str)
        assert results.strip() != ""
        assert "http" in results or "No results" in results

        #log for debugging
        print(f"\n Subtask: {subtask}\n Results:\n{results}\n{'-'*80}")
