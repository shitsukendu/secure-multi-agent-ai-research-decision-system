from dataclasses import dataclass, field
from typing import Any, Dict
from datetime import datetime


@dataclass
class AgentResponse:

    task_id: str

    agent_name: str

    status: str

    result: Any

    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )


class AgentResponseHandler:

    def __init__(self):
        self.responses = {}

    def record_response(
        self,
        task_id,
        agent_name,
        status,
        result,
        metadata=None
    ):

        response = AgentResponse(
            task_id=task_id,
            agent_name=agent_name,
            status=status,
            result=result,
            metadata=metadata or {}
        )

        self.responses[task_id] = response

        return response

    def get_response(self, task_id):

        return self.responses.get(task_id)

    def has_response(self, task_id):

        return task_id in self.responses