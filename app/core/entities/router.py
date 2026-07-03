"""Router Entity Module."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RoutingRule:
    """Represents a rule used to match input queries with appropriate target agents.

    Attributes:
        rule_id: Unique identifier for the rule.
        keywords: Keywords or phrases triggering this rule.
        target_agent_id: The ID of the agent that should handle the input if matched.
        priority: Execution priority order (higher priority rules evaluate first).
    """

    rule_id: str
    keywords: list[str]
    target_agent_id: str
    priority: int = 0


@dataclass(frozen=True)
class Router:
    """Represents a routing engine configuration that decides query targets.

    Attributes:
        router_id: Unique identifier for this router configuration.
        rules: Available matching rules.
        default_target_agent_id: The fallback agent ID if no rule matches.
    """

    router_id: str
    rules: list[RoutingRule] = field(default_factory=list)
    default_target_agent_id: str = "default_agent"
