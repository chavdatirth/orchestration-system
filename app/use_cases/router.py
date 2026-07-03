"""Router Use Case Module."""

from app.core.entities.router import Router
from app.use_cases.ports import LlmPort


class AgentRouterUseCase:
    """Routes an incoming goal or query to the most capable agent."""

    def __init__(self, llm_port: LlmPort) -> None:
        """Initialize the router use case.

        Args:
            llm_port: LLM interface used for semantic classification if rules fail.
        """
        self._llm = llm_port

    def route_request(self, router_config: Router, query: str) -> str:
        """Evaluate matching rules or prompt the LLM to identify the target agent ID.

        Args:
            router_config: Available rules and default routing parameters.
            query: The user input prompt.

        Returns:
            The matched agent ID.
        """
        raise NotImplementedError("Use case route_request not implemented.")
