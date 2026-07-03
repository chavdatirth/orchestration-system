"""Planner Use Case Module."""

from app.core.entities.plan import Plan
from app.use_cases.ports import LlmPort


class TaskPlanner:
    """Generates execution plans and decomposes complex goals into steps.

    Uses an LLM via LlmPort to dynamically plan paths to achieve goals.
    """

    def __init__(self, llm_port: LlmPort) -> None:
        """Initialize the TaskPlanner use case.

        Args:
            llm_port: Interface for model reasoning.
        """
        self._llm = llm_port

    def generate_plan(self, goal: str) -> Plan:
        """Decompose a complex objective into sequential tasks.

        Args:
            goal: Detailed task request description.

        Returns:
            A generated Plan object containing plan steps.
        """
        raise NotImplementedError("Use case generate_plan not implemented.")
