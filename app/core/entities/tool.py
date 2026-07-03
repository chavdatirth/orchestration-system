"""Tool Entity Module."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Tool:
    """Represents a tool definition that can be executed by agents.

    Attributes:
        name: Name of the tool, matching standard LLM tool schema formatting.
        description: Verbose documentation describing when and how to call the tool.
        parameters: JSON schema of arguments expected by the tool.
        metadata: Custom configurations or runtime settings for tool execution.
    """

    name: str
    description: str
    parameters: dict[str, Any]
    metadata: dict[str, Any] = field(default_factory=dict)
