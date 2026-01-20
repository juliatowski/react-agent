from react_agent.adapters.wikipedia_adapter import WikipediaAdapter


def test_wikipedia_adapter_integration():
    adapter = WikipediaAdapter(model="qwen2.5")
    subtask = "Give me a short summary of GPT-3"
    result = adapter.run(subtask, sentences=1)

    assert isinstance(result, str)
    assert result.strip() != ""
    assert "GPT" in result or "Wikipedia error" in result

    print(f"\nSubtask: {subtask}\nResult: {result}")
