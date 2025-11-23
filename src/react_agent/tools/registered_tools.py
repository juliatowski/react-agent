
from react_agent.tools.tool_registry import register_tool
from react_agent.tools.calculator import Calculator
from react_agent.tools.websearch import WebSearch
from react_agent.tools.wikipedia import WikipediaTool
from react_agent.tools.vectorsearch import VectorSearch
from react_agent.logging_config import log, vlog

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


    register_tool(
        name="calculator",
        description="Perform arithmetic calculations.",
        runner=Calculator().run,
    )

    register_tool(
        name="web_search",
        description="Search the web for current information.",
        runner=WebSearch().run,
    )

    register_tool(
        name="wikipedia",
        description="Retrieve summaries and facts from Wikipedia.",
        runner=WikipediaTool().run,
    )

    register_tool(
        name="vector_search",
        description="Search a local AI research corpus.",
        runner=VectorSearch(model=model).run,
    )

    # Developers can add more tools here:
    # register_tool("my_tool", "description", MyTool().run)
