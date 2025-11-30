from react_agent.adapters.vectorsearch_adapter import VectorSearchAdapter


def test_vectorsearch_adapter_integration():
    adapter = VectorSearchAdapter(model="qwen2.5", data_file="data/ai_research.txt")
    subtask = "What are the main AI research areas in Vienna?"
    results = adapter.run(subtask, k=2)

    assert isinstance(results, str)
    assert results.strip() != ""
    print(f"\nSubtask: {subtask}\nResults:\n{results}")
