# src/react_agent/tools/__init__.py

from .tool_registry import registry, register_tool, get_tool, list_tools
from .registered_tools import register_default_tools

# Automatically register all default tools when importing this package
register_default_tools()

__all__ = [
    "registry",
    "register_tool",
    "get_tool",
    "list_tools",
]
