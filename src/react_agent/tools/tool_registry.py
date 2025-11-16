# src/react_agent/tools/tool_registry.py

from typing import Callable, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class RegisteredTool:
    name: str
    description: str
    runner: Callable[..., dict]


class ToolRegistry:
    """Central registry where any tool can be registered."""

    def __init__(self) -> None:
        self._tools: Dict[str, RegisteredTool] = {}

    def register(self, name: str, description: str, runner: Callable[..., dict]) -> None:
        self._tools[name] = RegisteredTool(name, description, runner)

    def get(self, name: str) -> Optional[RegisteredTool]:
        return self._tools.get(name)

    def list(self) -> List[RegisteredTool]:
        return list(self._tools.values())

    def names(self) -> List[str]:
        return list(self._tools.keys())


# default global registry
registry = ToolRegistry()


def register_tool(name: str, description: str, runner: Callable[..., dict]) -> None:
    """Convenience wrapper for global registry."""
    registry.register(name, description, runner)


def get_tool(name: str) -> Optional[RegisteredTool]:
    return registry.get(name)


def list_tools() -> List[RegisteredTool]:
    return registry.list()
