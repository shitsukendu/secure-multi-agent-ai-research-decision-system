from coordination.coordination_engine import CoordinationEngine
from workflow.workflow_state import WorkflowStateManager
from workflow.workflow_transition import WorkflowTransitionManager
from decision.secure_decision_engine import SecureDecisionEngine


print("\n======================================")
print("FAILURE & EDGE CASE TEST")
print("======================================")


# =====================================
# 1. Unregistered Agent
# =====================================

coordination = CoordinationEngine()

try:

    coordination.assign_task(
        task_description="Test invalid agent.",
        agent_name="UnknownAgent",
        priority="high"
    )

    unregistered_agent_result = False

except ValueError:

    unregistered_agent_result = True


print("\n[1] Unregistered Agent")
print(
    "Handled:",
    unregistered_agent_result
)


# =====================================
# 2. Missing Workflow
# =====================================

state_manager = WorkflowStateManager()

missing_state = state_manager.get_state(
    "UNKNOWN-WORKFLOW"
)

missing_workflow_result = (
    missing_state is None
)

print("\n[2] Missing Workflow")
print(
    "Handled:",
    missing_workflow_result
)


# =====================================
# 3. Invalid Workflow Transition
# =====================================

state_manager.create_workflow(
    "WF-EDGE-001"
)

transition_manager = WorkflowTransitionManager(
    state_manager
)

invalid_transition = transition_manager.transition(
    "WF-EDGE-001",
    "decision"
)

invalid_transition_result = (
    invalid_transition["success"] is False
)

print("\n[3] Invalid Workflow Transition")
print(
    "Handled:",
    invalid_transition_result
)


# =====================================
# 4. Empty Evidence
# =====================================

decision_engine = SecureDecisionEngine()

empty_evidence_result = decision_engine.evaluate(
    confidence_score=0.90,
    evidence_list=[]
)

empty_evidence_handled = (
    empty_evidence_result["status"] == "BLOCKED"
    and not empty_evidence_result["allowed"]
)

print("\n[4] Empty Evidence")
print(
    "Handled:",
    empty_evidence_handled
)


# =====================================
# 5. Very Low Confidence
# =====================================

low_confidence_result = decision_engine.evaluate(
    confidence_score=0.10,
    evidence_list=[]
)

low_confidence_handled = (
    low_confidence_result["status"] == "BLOCKED"
    and not low_confidence_result["allowed"]
)

print("\n[5] Very Low Confidence")
print(
    "Handled:",
    low_confidence_handled
)


# =====================================
# 6. Final Verification
# =====================================

if (
    unregistered_agent_result
    and missing_workflow_result
    and invalid_transition_result
    and empty_evidence_handled
    and low_confidence_handled
):

    print("\n======================================")
    print("FAILURE & EDGE CASE TEST OK")
    print("======================================")

else:

    print("\n======================================")
    print("FAILURE & EDGE CASE TEST FAILED")
    print("======================================")