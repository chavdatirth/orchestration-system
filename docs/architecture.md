# JARVIS Architecture Details

This document explains the software architecture of **JARVIS**, an AI Orchestration Operating System.

## Architecture Patterns

JARVIS is built using **Clean Architecture**, **SOLID principles**, and **Dependency Injection**. The main objective is to keep the core orchestration logic decoupled from external systems such as LLM providers, database systems, vector search backends, and user interfaces (CLI/Web).

### 1. Layer Separation and Dependencies

Dependencies point strictly inwards. Outer circles represent mechanisms, inner circles represent policies.

```text
                  +-----------------------------------+
                  | Infrastructure & Drivers          |
                  | (FastAPI, Click CLI, Loggers)     |
                  |      +---------------------+      |
                  |      | Interface Adapters  |      |
                  |      | (LLM SDKs, VectorDB)|      |
                  |      |      +--------------+      |
                  |      |      | Use Cases    |      |
                  |      |      | (Pipelines)  |      |
                  |      |      |      +-------+      |
                  |      |      |      | Domain|      |
                  |      |      |      |Core   |      |
                  +------+------+------+-------+------+
```

*   **Domain Core (`app.core`)**: Contains plain Python domain entities. These models represent primary AI orchestrator elements (e.g., `Agent`, `Tool`, `Message`, `Plan`, `Memory`).
*   **Use Cases (`app.use_cases`)**: The operational logic of JARVIS. Examples include initiating an agent, executing a planned task sequence, or selecting the best LLM via a routing rule. Use Cases define interface structures (abstract base classes) for any external systems they need.
*   **Interface Adapters (`app.adapters`)**: Adapts outer elements to use-case interfaces. For instance, an `LlmAdapter` implements the abstract client class defined in the Use Cases layer using a specific provider (like Gemini SDK).
*   **Infrastructure (`app.infrastructure`)**: The entry-points and configuration wiring. Examples include the command-line parser, dependency injection container, settings loader, and logging handlers.

### 2. Dependency Injection & Inversion

To ensure testability and compliance with the Dependency Inversion Principle, all use cases and adapters are injected with their dependencies.

For example, a use case coordinating agent communication is not responsible for creating LLM clients or databases:

```python
class RunOrchestrationUseCase:
    def __init__(self, llm_adapter: LlmAdapterPort, memory_adapter: MemoryAdapterPort) -> None:
        self._llm = llm_adapter
        self._memory = memory_adapter
```

A dependency injection container binds concrete implementations (e.g. `GeminiAdapter`, `ChromaDbAdapter`) to these ports during application startup.

### 3. Testing Strategy

*   **Unit Tests (`tests/unit`)**: Fast and isolated tests. All outer adapters and external services are mocked. Tests verify core domain logic and individual use cases.
*   **Integration Tests (`tests/integration`)**: Verify that adapters correctly integrate with actual external resources (e.g., test vector DB operations, live LLM API calls).
