from coordination.coordination_engine import CoordinationEngine
from workflow.workflow_state import WorkflowStateManager
from workflow.workflow_transition import WorkflowTransitionManager


class WorkflowOrchestrator:

    def __init__(self):

        self.coordination_engine = CoordinationEngine()

        self.state_manager = WorkflowStateManager()

        self.transition_manager = WorkflowTransitionManager(
            self.state_manager
        )

    def register_agents(self):

        self.coordination_engine.register_agent(
            agent_name="ResearchAgent",
            role="Research",
            description="Collects and analyzes evidence."
        )

        self.coordination_engine.register_agent(
            agent_name="ValidationAgent",
            role="Validation",
            description="Validates evidence quality."
        )

        self.coordination_engine.register_agent(
            agent_name="DecisionAgent",
            role="Decision",
            description="Produces secure decisions."
        )

    def create_workflow(self, workflow_id):

        return self.state_manager.create_workflow(
            workflow_id
        )

    def start_research(self, workflow_id, query):

        self.transition_manager.transition(
            workflow_id,
            "research"
        )

        self.state_manager.update_agent(
            workflow_id,
            "ResearchAgent"
        )

        self.state_manager.update_status(
            workflow_id,
            "running"
        )

        task = self.coordination_engine.assign_task(
            task_description=query,
            agent_name="ResearchAgent",
            priority="high"
        )

        return task

    def start_validation(self, workflow_id):

        self.transition_manager.transition(
            workflow_id,
            "validation"
        )

        self.state_manager.update_agent(
            workflow_id,
            "ValidationAgent"
        )

        task = self.coordination_engine.assign_task(
            task_description="Validate collected evidence.",
            agent_name="ValidationAgent",
            priority="normal"
        )

        return task

    def start_decision(self, workflow_id):

        self.transition_manager.transition(
            workflow_id,
            "decision"
        )

        self.state_manager.update_agent(
            workflow_id,
            "DecisionAgent"
        )

        task = self.coordination_engine.assign_task(
            task_description="Prepare secure evidence-based decision.",
            agent_name="DecisionAgent",
            priority="low"
        )

        return task

    def complete_workflow(self, workflow_id):

        result = self.transition_manager.transition(
            workflow_id,
            "completed"
        )

        if result["success"]:

            self.state_manager.update_status(
                workflow_id,
                "completed"
            )

            self.state_manager.update_agent(
                workflow_id,
                ""
            )

        return result

    def get_workflow_state(self, workflow_id):

        return self.state_manager.get_state(
            workflow_id
        )