"""Orchestrator Use Case Module."""

from app.core.entities.agent import Agent
from app.core.entities.message import Message
from app.use_cases.ports import LlmPort, MemoryPort


class AgentOrchestrator:
    """Coordinates interaction between multiple autonomous agents, memory, and LLMs.

    Implements Clean Architecture use case layer: orchestrates domain logic.
    """

    def __init__(self, llm_port: LlmPort, memory_port: MemoryPort) -> None:
        """Initialize the Orchestrator with required outbound ports.

        Args:
            llm_port: Implemented adapter for Large Language Models.
            memory_port: Implemented adapter for Vector DB or key-value storage.
        """
        self._llm = llm_port
        self._memory = memory_port

    def execute_session(self, session_id: str, agents: list[Agent], prompt: str) -> Message | None:
        """Execute a coordinated chat session using memory context and LLMs.

        Args:
            session_id: Active session identifier.
            agents: List of participating agents.
            prompt: Input query or task command.

        Returns:
            The final resolved Message, or None.
        """
        # Architectural Decision: Use Cases coordinate but do not implement concrete APIs.
        # This will query memory_port, route to the correct agent, compile prompts,
        # invoke the llm_port, and store results back to memory.
        raise NotImplementedError("Use case execute_session not implemented.")
