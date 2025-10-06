from react_agent.tools.websearch import WebSearch


def test_websearch_tool_integration():
    tool = WebSearch()
    queries = [
        "OpenAI GPT models",
        "latest SpaceX rocket launch",
        "Python 3.12 new features",
        "UEFA Champions League 2025 results",
        "climate change news 2025",
    ]

    for query in queries:
        results = tool.run(query, k=2)

        assert isinstance(results, str)
        assert results.strip() != ""
        assert "http" in results or "No results" in results

        print(f"\n Query: {query}\n Results:\n{results}\n{'-'*80}")
