from workflow.workflow_state import WorkflowStateManager


class WorkflowTransitionManager:

    VALID_TRANSITIONS = {
        "initialized": ["research"],
        "research": ["validation"],
        "validation": ["decision"],
        "decision": ["completed"],
        "completed": []
    }

    def __init__(self, state_manager):

        self.state_manager = state_manager

    def transition(self, workflow_id, next_stage):

        state = self.state_manager.get_state(workflow_id)

        if not state:
            return {
                "success": False,
                "message": "Workflow not found."
            }

        current_stage = state.current_stage

        allowed_stages = self.VALID_TRANSITIONS.get(
            current_stage,
            []
        )

        if next_stage not in allowed_stages:

            return {
                "success": False,
                "message": (
                    f"Invalid transition: "
                    f"{current_stage} -> {next_stage}"
                )
            }

        self.state_manager.update_stage(
            workflow_id,
            next_stage
        )

        return {
            "success": True,
            "message": (
                f"Workflow transitioned: "
                f"{current_stage} -> {next_stage}"
            )
        }