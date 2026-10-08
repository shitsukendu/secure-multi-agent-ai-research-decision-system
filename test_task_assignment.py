from coordination.task_assignment import TaskAssignment


assignment = TaskAssignment()


task = assignment.assign(
    task_description="Research AI evidence sources.",
    agent_name="ResearchAgent",
    priority="high"
)


print("\n--- Task Assignment Test ---")

print("Task ID:", task["task_id"])
print("Task:", task["task_description"])
print("Agent:", task["agent_name"])
print("Priority:", task["priority"])
print("Status:", task["status"])


assignment.update_status(
    task["task_id"],
    "in_progress"
)


updated_task = assignment.get_task(
    task["task_id"]
)


print("\nUpdated Status:")
print(updated_task["status"])


agent_tasks = assignment.get_agent_tasks(
    "ResearchAgent"
)


print("\nResearchAgent Tasks:")
print(agent_tasks)


if (
    task["agent_name"] == "ResearchAgent"
    and task["priority"] == "high"
    and updated_task["status"] == "in_progress"
    and len(agent_tasks) == 1
):

    print("\nTASK ASSIGNMENT TEST PASSED")

else:

    print("\nTASK ASSIGNMENT TEST FAILED")