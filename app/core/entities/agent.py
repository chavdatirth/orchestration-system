"""Agent Entity Module."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Agent:
    """Represents an autonomous agent within the JARVIS orchestration OS.

    Attributes:
        id: Unique identifier for the agent.
        name: Human-readable name of the agent.
        role: The functional role or persona of the agent (e.g., Researcher, Coder).
        system_prompt: The core directives guiding this agent's LLM generation.
        metadata: Extensible configuration settings or context flags.
        tags: Categorization tags for discoverability and routing.
    """

    id: str
    name: str
    role: str
    system_prompt: str
    metadata: dict[str, str] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
