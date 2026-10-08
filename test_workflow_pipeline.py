from workflow.workflow_orchestrator import WorkflowOrchestrator


orchestrator = WorkflowOrchestrator()


# ---------------------------------
# 1. Register Agents
# ---------------------------------

orchestrator.register_agents()


# ---------------------------------
# 2. Create Workflow
# ---------------------------------

workflow_id = "WF-004"

orchestrator.create_workflow(
    workflow_id
)


# ---------------------------------
# 3. Research Stage
# ---------------------------------

research_task = orchestrator.start_research(
    workflow_id,
    "Research evidence for secure AI decision making."
)


# ---------------------------------
# 4. Validation Stage
# ---------------------------------

validation_task = orchestrator.start_validation(
    workflow_id
)


# ---------------------------------
# 5. Decision Stage
# ---------------------------------

decision_task = orchestrator.start_decision(
    workflow_id
)


# ---------------------------------
# 6. Complete Workflow
# ---------------------------------

completion = orchestrator.complete_workflow(
    workflow_id
)


# ---------------------------------
# 7. Get Final State
# ---------------------------------

state = orchestrator.get_workflow_state(
    workflow_id
)


# ---------------------------------
# 8. Display Results
# ---------------------------------

print("\n======================================")
print("END-TO-END WORKFLOW PIPELINE")
print("======================================")


print("\nWorkflow ID:")
print(state.workflow_id)


print("\nResearch Agent:")
print(research_task["agent_name"])


print("\nValidation Agent:")
print(validation_task["agent_name"])


print("\nDecision Agent:")
print(decision_task["agent_name"])


print("\nFinal Stage:")
print(state.current_stage)


print("\nFinal Status:")
print(state.status)


print("\nCompletion Result:")
print(completion)


# ---------------------------------
# 9. Final Verification
# ---------------------------------

if (
    state.workflow_id == workflow_id
    and research_task["agent_name"] == "ResearchAgent"
    and validation_task["agent_name"] == "ValidationAgent"
    and decision_task["agent_name"] == "DecisionAgent"
    and completion["success"]
    and state.current_stage == "completed"
    and state.status == "completed"
):

    print("\n======================================")
    print("END-TO-END WORKFLOW PIPELINE OK")
    print("======================================")

else:

    print("\n======================================")
    print("END-TO-END WORKFLOW PIPELINE FAILED")
    print("======================================")