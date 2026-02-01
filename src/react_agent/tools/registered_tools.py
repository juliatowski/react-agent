from react_agent.tools.tool_registry import register_tool
from react_agent.tools.calculator import Calculator
from react_agent.tools.websearch import WebSearch
from react_agent.tools.wikipedia import WikipediaTool
from react_agent.tools.vectorsearch import VectorSearch
from react_agent.config.logging_config import log, vlog

"""
This file is the ONLY place where tools are registered.

- internal tools
- external tools
- 3rd-party tools
- user-defined tools
"""

def register_default_tools(model: str = "qwen2.5"):
    log(f"Registering default tools (model={model})")
    """Register all default tools into the global registry."""
    vlog("Default tools registered.")

    # ------------------------------------------------------------
    # CALCULATOR (Math, Algebra, Equations, Expressions)
    # ------------------------------------------------------------
    register_tool(
        name="calculator",
        description=(
            "A mathematical computation tool for evaluating numeric and symbolic expressions. "
            "Use this tool when the subtask requires: arithmetic (+, -, *, /), exponentiation, "
            "fractions, algebra, solving equations, trigonometry (sin, cos, tan), square roots, "
            "logarithms, or constants like pi. Input must be a valid math expression such as: "
            "'2 + 3*4', 'sin(pi/2)', 'sqrt(16)', or 'solve(x**2 - 4, x)'. "
            "Do NOT use this tool for general knowledge, summaries, text processing, or searching the web. "
            "This tool cannot read external data — it only computes math."
        ),
        runner=Calculator().run,
    )

    # ------------------------------------------------------------
    # WEB SEARCH (Real-time internet search)
    # ------------------------------------------------------------
    register_tool(
        name="web_search",
        description=(
            "A real-time internet search tool. Use this when you need up-to-date or live information "
            "such as news, current events, price comparisons, live statistics, or any question requiring "
            "fresh online data. Examples: 'today's weather', 'current inflation rate', "
            "'latest AI research news', 'compare iPhone 15 vs Samsung S24'. "
            "Not suitable for math, offline documents, or stable historical facts that Wikipedia already covers."
        ),
        runner=WebSearch().run,
    )

    # ------------------------------------------------------------
    # WIKIPEDIA (General Knowledge & Encyclopedic Summaries)
    # ------------------------------------------------------------
    register_tool(
        name="wikipedia",
        description=(
            "A tool for retrieving concise summaries, explanations, and factual encyclopedic information "
            "from Wikipedia. Best for subtasks involving: biographies (e.g., Ada Lovelace, Einstein), "
            "historical events, scientific concepts, definitions, geography, cultural topics, and general knowledge. "
            "Examples: 'Summarize the life of Alan Turing', 'Explain quantum entanglement', "
            "'What is the capital of France?'. "
            "Not suitable for math computation, real-time information, or internet searches."
        ),
        runner=WikipediaTool().run,
    )

    # ------------------------------------------------------------
    # VECTOR SEARCH (Semantic search in local AI research corpus)
    # ------------------------------------------------------------
    register_tool(
        name="vector_search",
        description=(
            "A semantic search tool over a *local* AI research text corpus using embeddings. "
            "Use this tool when the subtask requires retrieving related paragraphs, exploring AI concepts, "
            "finding similar research topics, or answering questions tied to the local dataset. "
            "Examples: 'find text about reinforcement learning', 'retrieve similar paragraphs on neural networks', "
            "'search the knowledge base for LLM safety topics'. "
            "This tool does NOT access the internet or Wikipedia. It only searches the local FAISS vector index built "
            "from the ai_research.txt file."
        ),
        runner=VectorSearch(model=model).run,
    )

    # Developers can add more tools here:
    # register_tool("my_tool", "description", MyTool().run)
