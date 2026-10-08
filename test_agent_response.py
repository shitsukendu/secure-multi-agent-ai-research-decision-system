from coordination.agent_response import AgentResponseHandler


handler = AgentResponseHandler()


response = handler.record_response(
    task_id="TASK-001",
    agent_name="ResearchAgent",
    status="completed",
    result={
        "finding": "AI systems require traceable evidence."
    },
    metadata={
        "source_count": 5
    }
)


print("\n--- Agent Response Test ---")

print("Task ID:", response.task_id)
print("Agent:", response.agent_name)
print("Status:", response.status)
print("Result:", response.result)
print("Metadata:", response.metadata)
print("Timestamp:", response.timestamp)


stored_response = handler.get_response(
    "TASK-001"
)


print("\nStored Response:")
print(stored_response)


if (
    response.task_id == "TASK-001"
    and response.agent_name == "ResearchAgent"
    and response.status == "completed"
    and handler.has_response("TASK-001")
):

    print("\nAGENT RESPONSE TEST PASSED")

else:

    print("\nAGENT RESPONSE TEST FAILED")