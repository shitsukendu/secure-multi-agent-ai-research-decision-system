from coordination.coordination_engine import CoordinationEngine
from coordination.coordination_audit import CoordinationAudit


engine = CoordinationEngine()
audit = CoordinationAudit()


# ---------------------------------
# 1. Register Agents
# ---------------------------------

engine.register_agent(
    agent_name="ResearchAgent",
    role="Research",
    description="Collects and analyzes evidence."
)

engine.register_agent(
    agent_name="ValidationAgent",
    role="Validation",
    description="Validates evidence quality."
)

engine.register_agent(
    agent_name="DecisionAgent",
    role="Decision",
    description="Produces secure decisions."
)


# ---------------------------------
# 2. Assign Tasks
# ---------------------------------

research_task = engine.assign_task(
    task_description="Research evidence for the given query.",
    agent_name="ResearchAgent",
    priority="high"
)

validation_task = engine.assign_task(
    task_description="Validate collected research evidence.",
    agent_name="ValidationAgent",
    priority="normal"
)

decision_task = engine.assign_task(
    task_description="Prepare an evidence-backed decision.",
    agent_name="DecisionAgent",
    priority="low"
)


tasks = [
    research_task,
    validation_task,
    decision_task
]


# ---------------------------------
# 3. Prioritize Tasks
# ---------------------------------

prioritized_tasks = engine.prioritize_tasks(
    tasks
)


print("\n================================")
print("MULTI-AGENT COORDINATION PIPELINE")
print("================================")


print("\n[1] Registered Agents")

for agent_name in [
    "ResearchAgent",
    "ValidationAgent",
    "DecisionAgent"
]:

    print(
        agent_name,
        "->",
        engine.registry.get_agent(agent_name)["role"]
    )


print("\n[2] Prioritized Tasks")

for task in prioritized_tasks:

    print(
        task["task_id"],
        "|",
        task["agent_name"],
        "|",
        task["priority"]
    )


# ---------------------------------
# 4. Research Agent Response
# ---------------------------------

research_response = engine.submit_response(
    task_id=research_task["task_id"],
    agent_name="ResearchAgent",
    status="completed",
    result={
        "finding": "Evidence collected successfully."
    }
)


print("\n[3] Research Agent Response")

print(
    "Agent:",
    research_response.agent_name
)

print(
    "Status:",
    research_response.status
)


# ---------------------------------
# 5. Validation Agent Response
# ---------------------------------

validation_response = engine.submit_response(
    task_id=validation_task["task_id"],
    agent_name="ValidationAgent",
    status="completed",
    result={
        "validation": "Evidence passed validation."
    }
)


print("\n[4] Validation Agent Response")

print(
    "Agent:",
    validation_response.agent_name
)

print(
    "Status:",
    validation_response.status
)


# ---------------------------------
# 6. Audit
# ---------------------------------

audit_entries = []

for task in tasks:

    entry = audit.record(
        action="task_assigned",
        agent_name=task["agent_name"],
        task_id=task["task_id"],
        details={
            "priority": task["priority"],
            "description": task["task_description"]
        }
    )

    audit_entries.append(entry)


print("\n[5] Coordination Audit")

print(
    "Audit Entries:",
    len(audit_entries)
)


# ---------------------------------
# 7. Final Verification
# ---------------------------------

if (
    engine.registry.exists("ResearchAgent")
    and engine.registry.exists("ValidationAgent")
    and engine.registry.exists("DecisionAgent")
    and prioritized_tasks[0]["priority"] == "high"
    and research_response.status == "completed"
    and validation_response.status == "completed"
    and len(audit_entries) == 3
):

    print("\n================================")
    print("MULTI-AGENT COORDINATION PIPELINE OK")
    print("================================")

else:

    print("\n================================")
    print("MULTI-AGENT COORDINATION PIPELINE FAILED")
    print("================================")