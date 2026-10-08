from workflow.workflow_state import WorkflowStateManager


manager = WorkflowStateManager()


# Create workflow
state = manager.create_workflow(
    "WF-001"
)


# Update workflow
manager.update_stage(
    "WF-001",
    "research"
)

manager.update_agent(
    "WF-001",
    "ResearchAgent"
)

manager.update_status(
    "WF-001",
    "running"
)

manager.mark_evidence_collected(
    "WF-001"
)


# Get state
current_state = manager.get_state(
    "WF-001"
)


print("\n==============================")
print("WORKFLOW STATE TEST")
print("==============================")


print(
    "Workflow ID:",
    current_state.workflow_id
)

print(
    "Stage:",
    current_state.current_stage
)

print(
    "Agent:",
    current_state.current_agent
)

print(
    "Status:",
    current_state.status
)

print(
    "Evidence Collected:",
    current_state.evidence_collected
)


if (
    current_state.workflow_id == "WF-001"
    and current_state.current_stage == "research"
    and current_state.current_agent == "ResearchAgent"
    and current_state.status == "running"
    and current_state.evidence_collected
):

    print("\n==============================")
    print("WORKFLOW STATE TEST OK")
    print("==============================")

else:

    print("\n==============================")
    print("WORKFLOW STATE TEST FAILED")
    print("==============================")