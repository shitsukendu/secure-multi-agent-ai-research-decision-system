from workflow.workflow_state import WorkflowStateManager
from workflow.workflow_transition import WorkflowTransitionManager


state_manager = WorkflowStateManager()

transition_manager = WorkflowTransitionManager(
    state_manager
)


# Create workflow
state_manager.create_workflow(
    "WF-002"
)


print("\n==============================")
print("WORKFLOW TRANSITION TEST")
print("==============================")


# initialized -> research

result1 = transition_manager.transition(
    "WF-002",
    "research"
)

print("\nTransition 1:")
print(result1)


# research -> validation

result2 = transition_manager.transition(
    "WF-002",
    "validation"
)

print("\nTransition 2:")
print(result2)


# validation -> decision

result3 = transition_manager.transition(
    "WF-002",
    "decision"
)

print("\nTransition 3:")
print(result3)


# decision -> completed

result4 = transition_manager.transition(
    "WF-002",
    "completed"
)

print("\nTransition 4:")
print(result4)


# Test invalid transition

invalid_result = transition_manager.transition(
    "WF-002",
    "research"
)

print("\nInvalid Transition Test:")
print(invalid_result)


# Final state

final_state = state_manager.get_state(
    "WF-002"
)


print("\nFinal Stage:")
print(final_state.current_stage)


if (
    result1["success"]
    and result2["success"]
    and result3["success"]
    and result4["success"]
    and not invalid_result["success"]
    and final_state.current_stage == "completed"
):

    print("\n==============================")
    print("WORKFLOW TRANSITION TEST OK")
    print("==============================")

else:

    print("\n==============================")
    print("WORKFLOW TRANSITION TEST FAILED")
    print("==============================")