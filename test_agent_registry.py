from coordination.agent_registry import AgentRegistry


registry = AgentRegistry()


registry.register(
    agent_name="ResearchAgent",
    role="Research",
    description="Collects and analyzes research evidence."
)


registry.register(
    agent_name="ValidationAgent",
    role="Validation",
    description="Validates evidence quality and reliability."
)


registry.register(
    agent_name="DecisionAgent",
    role="Decision",
    description="Produces secure evidence-based decisions."
)


print("\n--- Agent Registry Test ---")

print(
    "ResearchAgent Exists:",
    registry.exists("ResearchAgent")
)

print(
    "ValidationAgent Exists:",
    registry.exists("ValidationAgent")
)

print(
    "DecisionAgent Exists:",
    registry.exists("DecisionAgent")
)


print("\nRegistered Agents:")

for agent in registry.get_active_agents():

    print(
        agent["agent_name"],
        "| Role:",
        agent["role"]
    )


print("\nAgent Details:")

print(
    registry.get_agent("ResearchAgent")
)


if (
    registry.exists("ResearchAgent")
    and registry.exists("ValidationAgent")
    and registry.exists("DecisionAgent")
    and len(registry.get_active_agents()) == 3
):

    print("\nAGENT REGISTRY TEST PASSED")

else:

    print("\nAGENT REGISTRY TEST FAILED")