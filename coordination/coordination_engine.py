from coordination.agent_registry import AgentRegistry
from coordination.task_assignment import TaskAssignment
from coordination.agent_response import AgentResponseHandler
from coordination.agent_priority import AgentPriority


class CoordinationEngine:

    def __init__(self):

        self.registry = AgentRegistry()

        self.assignment = TaskAssignment()

        self.response_handler = AgentResponseHandler()

        self.priority = AgentPriority()

    def register_agent(
        self,
        agent_name,
        role,
        description=""
    ):

        self.registry.register(
            agent_name=agent_name,
            role=role,
            description=description
        )

    def assign_task(
        self,
        task_description,
        agent_name,
        priority="normal"
    ):

        if not self.registry.exists(agent_name):

            raise ValueError(
                f"Agent not registered: {agent_name}"
            )

        return self.assignment.assign(
            task_description=task_description,
            agent_name=agent_name,
            priority=priority
        )

    def submit_response(
        self,
        task_id,
        agent_name,
        status,
        result,
        metadata=None
    ):

        return self.response_handler.record_response(
            task_id=task_id,
            agent_name=agent_name,
            status=status,
            result=result,
            metadata=metadata
        )

    def get_task(self, task_id):

        return self.assignment.get_task(
            task_id
        )

    def get_response(self, task_id):

        return self.response_handler.get_response(
            task_id
        )

    def prioritize_tasks(self, tasks):

        return self.priority.sort_tasks(
            tasks
        )