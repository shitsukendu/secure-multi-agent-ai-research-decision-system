import uuid


class TaskAssignment:

    def __init__(self):
        self.tasks = {}

    def assign(
        self,
        task_description,
        agent_name,
        priority="normal"
    ):

        task_id = f"TASK-{uuid.uuid4().hex[:8].upper()}"

        task = {
            "task_id": task_id,
            "task_description": task_description,
            "agent_name": agent_name,
            "priority": priority,
            "status": "assigned"
        }

        self.tasks[task_id] = task

        return task

    def get_task(self, task_id):

        return self.tasks.get(task_id)

    def update_status(
        self,
        task_id,
        status
    ):

        if task_id not in self.tasks:
            return False

        self.tasks[task_id]["status"] = status

        return True

    def get_agent_tasks(self, agent_name):

        return [
            task
            for task in self.tasks.values()
            if task["agent_name"] == agent_name
        ]