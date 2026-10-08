from dataclasses import dataclass, field
from typing import Dict, Any
from datetime import datetime


@dataclass
class WorkflowState:

    workflow_id: str

    current_stage: str = "initialized"

    current_agent: str = ""

    status: str = "pending"

    evidence_collected: bool = False

    evidence_validated: bool = False

    decision_created: bool = False

    decision_approved: bool = False

    metadata: Dict[str, Any] = field(default_factory=dict)

    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    updated_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )


class WorkflowStateManager:

    def __init__(self):

        self.states = {}


    def create_workflow(self, workflow_id):

        state = WorkflowState(
            workflow_id=workflow_id
        )

        self.states[workflow_id] = state

        return state


    def get_state(self, workflow_id):

        return self.states.get(workflow_id)


    def update_stage(self, workflow_id, stage):

        state = self.get_state(workflow_id)

        if not state:
            return False

        state.current_stage = stage

        state.updated_at = datetime.utcnow().isoformat()

        return True


    def update_agent(self, workflow_id, agent_name):

        state = self.get_state(workflow_id)

        if not state:
            return False

        state.current_agent = agent_name

        state.updated_at = datetime.utcnow().isoformat()

        return True


    def update_status(self, workflow_id, status):

        state = self.get_state(workflow_id)

        if not state:
            return False

        state.status = status

        state.updated_at = datetime.utcnow().isoformat()

        return True


    def mark_evidence_collected(self, workflow_id):

        state = self.get_state(workflow_id)

        if not state:
            return False

        state.evidence_collected = True

        state.updated_at = datetime.utcnow().isoformat()

        return True


    def mark_evidence_validated(self, workflow_id):

        state = self.get_state(workflow_id)

        if not state:
            return False

        state.evidence_validated = True

        state.updated_at = datetime.utcnow().isoformat()

        return True


    def mark_decision_created(self, workflow_id):

        state = self.get_state(workflow_id)

        if not state:
            return False

        state.decision_created = True

        state.updated_at = datetime.utcnow().isoformat()

        return True


    def mark_decision_approved(self, workflow_id):

        state = self.get_state(workflow_id)

        if not state:
            return False

        state.decision_approved = True

        state.updated_at = datetime.utcnow().isoformat()

        return True