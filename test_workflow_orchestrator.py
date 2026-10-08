from workflow.workflow_orchestrator import WorkflowOrchestrator


orchestrator = WorkflowOrchestrator()


# ---------------------------------
# 1. Register Agents
# ---------------------------------

orchestrator.register_agents()


# ---------------------------------
# 2. Create Workflow
# ---------------------------------

workflow_id = "WF-003"

orchestrator.create_workflow(
    workflow_id
)


# ---------------------------------
# 3. Start Research
# ---------------------------------

research_task = orchestrator.start_research(
    workflow_id,
    "Research evidence for AI security."
)


# ---------------------------------
# 4. Start Validation
# ---------------------------------

validation_task = orchestrator.start_validation(
    workflow_id
)


# ---------------------------------
# 5. Start Decision
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
# 7. Final State
# ---------------------------------

state = orchestrator.get_workflow_state(
    workflow_id
)


print("\n================================")
print("WORKFLOW ORCHESTRATOR TEST")
print("================================")


print("\nWorkflow ID:")
print(state.workflow_id)


print("\nResearch Task:")
print(research_task["task_id"])


print("\nValidation Task:")
print(validation_task["task_id"])


print("\nDecision Task:")
print(decision_task["task_id"])


print("\nFinal Stage:")
print(state.current_stage)


print("\nFinal Status:")
print(state.status)


print("\nCurrent Agent:")
print(state.current_agent)


# ---------------------------------
# 8. Final Verification
# ---------------------------------

if (
    research_task["agent_name"] == "ResearchAgent"
    and validation_task["agent_name"] == "ValidationAgent"
    and decision_task["agent_name"] == "DecisionAgent"
    and completion["success"]
    and state.current_stage == "completed"
    and state.status == "completed"
):

    print("\n================================")
    print("WORKFLOW ORCHESTRATOR TEST OK")
    print("================================")

else:

    print("\n================================")
    print("WORKFLOW ORCHESTRATOR TEST FAILED")
    print("================================")