import json
import os
from dataclasses import asdict

from evidence.evidence_schema import Evidence


class EvidenceStore:

    def __init__(self, file_path="evidence/evidence.json"):
        self.file_path = file_path
        self._ensure_file()

    def _ensure_file(self):
        os.makedirs(
            os.path.dirname(self.file_path),
            exist_ok=True
        )

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)

    def add_evidence(self, evidence: Evidence):

        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Duplicate check
        for item in data:
            if (
                item.get("source_url") == evidence.source_url
                and item.get("claim") == evidence.claim
                and item.get("snippet") == evidence.snippet
            ):
                return False

        data.append(asdict(evidence))

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        return True

    def get_all(self):

        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_by_agent(self, agent_name):

        evidence = self.get_all()

        return [
            item
            for item in evidence
            if item.get("agent_name") == agent_name
        ]

    def get_by_source_type(self, source_type):

        evidence = self.get_all()

        return [
            item
            for item in evidence
            if item.get("source_type") == source_type
        ]

    def get_by_min_reliability(self, minimum_score):

        evidence = self.get_all()

        return [
            item
            for item in evidence
            if item.get("reliability_score", 0) >= minimum_score
        ]

    def search(self, keyword):

        keyword = keyword.lower()

        evidence = self.get_all()

        results = []

        for item in evidence:

            searchable_text = " ".join([
                str(item.get("source_title", "")),
                str(item.get("claim", "")),
                str(item.get("snippet", ""))
            ]).lower()

            if keyword in searchable_text:
                results.append(item)

        return results