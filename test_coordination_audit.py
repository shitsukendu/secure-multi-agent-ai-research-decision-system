from coordination.coordination_audit import CoordinationAudit


audit = CoordinationAudit()


entry = audit.record(
    action="task_assigned",
    agent_name="ResearchAgent",
    task_id="TASK-AUDIT-001",
    details={
        "priority": "high",
        "description": "Research AI evidence."
    }
)


print("\n--- Coordination Audit Test ---")

print("Action:", entry["action"])
print("Agent:", entry["agent_name"])
print("Task ID:", entry["task_id"])
print("Details:", entry["details"])
print("Timestamp:", entry["timestamp"])


all_logs = audit.get_all()


print("\nTotal Coordination Logs:")
print(len(all_logs))


if (
    entry["action"] == "task_assigned"
    and entry["agent_name"] == "ResearchAgent"
    and entry["task_id"] == "TASK-AUDIT-001"
    and len(all_logs) >= 1
):

    print("\nCOORDINATION AUDIT TEST PASSED")

else:

    print("\nCOORDINATION AUDIT TEST FAILED")