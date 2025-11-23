from react_agent.logging_config import log, vlog

from typing import Callable, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class RegisteredTool:
    name: str
    description: str
    runner: Callable[..., dict]


class ToolRegistry:
    """
    Holds a set of tools by name.
    """
    def __init__(self) -> None:
        self._tools: Dict[str, RegisteredTool] = {}

    def register(self, name: str, description: str, runner: Callable[..., dict]) -> None:
        log(f"Registering tool: {name}")
        self._tools[name] = RegisteredTool(name=name, description=description, runner=runner)

    def get(self, name: str) -> Optional[RegisteredTool]:
        tool = self._tools.get(name)
        vlog(f"Getting tool '{name}': found={tool is not None}")
        return tool

    def list(self) -> List[RegisteredTool]:
        tools = list(self._tools.values())
        vlog(f"Listing tools: {[t.name for t in tools]}")
        return tools

    def names(self) -> List[str]:
        names = list(self._tools.keys())
        vlog(f"Tool names: {names}")
        return names



# default global registry
registry = ToolRegistry()


def register_tool(name: str, description: str, runner: Callable[..., dict]) -> None:
    """Convenience wrapper for global registry."""
    registry.register(name, description, runner)


def get_tool(name: str) -> Optional[RegisteredTool]:
    return registry.get(name)


def list_tools() -> List[RegisteredTool]:
    return registry.list()
