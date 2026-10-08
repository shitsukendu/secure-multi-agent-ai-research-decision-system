from coordination.agent_priority import AgentPriority


priority = AgentPriority()


tasks = [
    {
        "task_id": "TASK-001",
        "priority": "low"
    },
    {
        "task_id": "TASK-002",
        "priority": "high"
    },
    {
        "task_id": "TASK-003",
        "priority": "normal"
    }
]


print("\n--- Agent Priority Test ---")


print(
    "HIGH Score:",
    priority.get_priority_score("high")
)

print(
    "NORMAL Score:",
    priority.get_priority_score("normal")
)

print(
    "LOW Score:",
    priority.get_priority_score("low")
)


sorted_tasks = priority.sort_tasks(tasks)


print("\nSorted Tasks:")

for task in sorted_tasks:

    print(
        task["task_id"],
        "| Priority:",
        task["priority"]
    )


if (
    sorted_tasks[0]["priority"] == "high"
    and sorted_tasks[1]["priority"] == "normal"
    and sorted_tasks[2]["priority"] == "low"
):

    print("\nAGENT PRIORITY TEST PASSED")

else:

    print("\nAGENT PRIORITY TEST FAILED")