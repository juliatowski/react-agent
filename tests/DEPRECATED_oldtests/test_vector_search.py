from react_agent.tools.vectorsearch import VectorSearch

def test_vector_search_integration():
    vs = VectorSearch(model="qwen2.5", data_file="data/ai_research.txt")
    query = "AI research in Europe"
    results = vs.run(query, k=2)

    assert isinstance(results, str)
    assert results.strip() != ""
    print(f"\nQuery: {query}\nResults:\n{results}")
