import json
import os
from datetime import datetime


class CoordinationAudit:

    def __init__(
        self,
        file_path="logs/coordination_audit.json"
    ):

        self.file_path = file_path

        self._ensure_file()

    def _ensure_file(self):

        os.makedirs(
            os.path.dirname(self.file_path),
            exist_ok=True
        )

        if not os.path.exists(self.file_path):

            with open(
                self.file_path,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump([], f, indent=4)

    def record(
        self,
        action,
        agent_name=None,
        task_id=None,
        details=None
    ):

        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "agent_name": agent_name,
            "task_id": task_id,
            "details": details or {}
        }

        with open(
            self.file_path,
            "r",
            encoding="utf-8"
        ) as f:

            logs = json.load(f)

        logs.append(entry)

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                logs,
                f,
                indent=4
            )

        return entry

    def get_all(self):

        with open(
            self.file_path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)