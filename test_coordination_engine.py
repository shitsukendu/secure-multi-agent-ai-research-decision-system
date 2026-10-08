from coordination.coordination_engine import CoordinationEngine


engine = CoordinationEngine()


# ---------------------------------
# 1. Register Agents
# ---------------------------------

engine.register_agent(
    agent_name="ResearchAgent",
    role="Research",
    description="Collects research evidence."
)

engine.register_agent(
    agent_name="ValidationAgent",
    role="Validation",
    description="Validates evidence."
)

engine.register_agent(
    agent_name="DecisionAgent",
    role="Decision",
    description="Produces secure decisions."
)


# ---------------------------------
# 2. Assign Tasks
# ---------------------------------

task1 = engine.assign_task(
    task_description="Research AI evidence.",
    agent_name="ResearchAgent",
    priority="high"
)

task2 = engine.assign_task(
    task_description="Validate collected evidence.",
    agent_name="ValidationAgent",
    priority="normal"
)

task3 = engine.assign_task(
    task_description="Prepare final decision.",
    agent_name="DecisionAgent",
    priority="low"
)


print("\n--- Coordination Engine Test ---")

print("\nAssigned Tasks:")

print(task1)
print(task2)
print(task3)


# ---------------------------------
# 3. Prioritize Tasks
# ---------------------------------

tasks = [
    task1,
    task2,
    task3
]

sorted_tasks = engine.prioritize_tasks(
    tasks
)


print("\nPrioritized Tasks:")

for task in sorted_tasks:

    print(
        task["task_id"],
        "|",
        task["agent_name"],
        "|",
        task["priority"]
    )


# ---------------------------------
# 4. Submit Agent Response
# ---------------------------------

response = engine.submit_response(
    task_id=task1["task_id"],
    agent_name="ResearchAgent",
    status="completed",
    result={
        "finding": "Evidence collected successfully."
    }
)


print("\nAgent Response:")

print(
    response
)


# ---------------------------------
# 5. Verify
# ---------------------------------

stored_response = engine.get_response(
    task1["task_id"]
)


if (
    engine.registry.exists("ResearchAgent")
    and engine.registry.exists("ValidationAgent")
    and engine.registry.exists("DecisionAgent")
    and sorted_tasks[0]["priority"] == "high"
    and stored_response is not None
    and stored_response.status == "completed"
):

    print("\nCOORDINATION ENGINE TEST PASSED")

else:

    print("\nCOORDINATION ENGINE TEST FAILED")