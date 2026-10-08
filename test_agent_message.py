from coordination.agent_message import AgentMessage


message = AgentMessage(
    message_id="MSG-001",
    sender="ResearchAgent",
    receiver="DecisionAgent",
    message_type="evidence_result",
    content={
        "claim": "AI systems require evidence-based decisions."
    },
    task_id="TASK-001",
    priority="high"
)


print("\n--- Agent Message Test ---")

print("Message ID:", message.message_id)
print("Sender:", message.sender)
print("Receiver:", message.receiver)
print("Message Type:", message.message_type)
print("Task ID:", message.task_id)
print("Priority:", message.priority)
print("Content:", message.content)
print("Timestamp:", message.timestamp)


if (
    message.message_id == "MSG-001"
    and message.sender == "ResearchAgent"
    and message.receiver == "DecisionAgent"
    and message.task_id == "TASK-001"
):

    print("\nAGENT MESSAGE TEST PASSED")

else:

    print("\nAGENT MESSAGE TEST FAILED")