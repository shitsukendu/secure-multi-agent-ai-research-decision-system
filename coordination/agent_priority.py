class AgentPriority:

    PRIORITY_LEVELS = {
        "high": 3,
        "normal": 2,
        "low": 1
    }

    def get_priority_score(self, priority):

        priority = priority.lower().strip()

        return self.PRIORITY_LEVELS.get(
            priority,
            self.PRIORITY_LEVELS["normal"]
        )

    def compare(self, priority_a, priority_b):

        score_a = self.get_priority_score(
            priority_a
        )

        score_b = self.get_priority_score(
            priority_b
        )

        if score_a > score_b:
            return 1

        elif score_a < score_b:
            return -1

        return 0

    def sort_tasks(self, tasks):

        return sorted(
            tasks,
            key=lambda task: self.get_priority_score(
                task.get("priority", "normal")
            ),
            reverse=True
        )