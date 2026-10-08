from dataclasses import dataclass, field
from typing import List


@dataclass
class DecisionTrace:

    decision_id: str
    decision: str

    evidence_ids: List[str] = field(
        default_factory=list
    )

    confidence_score: float = 0.0

    reasoning: str = ""

class DecisionTraceBuilder:

    def build(
        self,
        decision_id,
        decision,
        evidence_list,
        reasoning="",
    ):

        evidence_ids = [
            evidence["evidence_id"]
            for evidence in evidence_list
        ]

        if evidence_list:

            confidence_score = sum(
                evidence.get("final_score", 0.0)
                for evidence in evidence_list
            ) / len(evidence_list)

        else:
            confidence_score = 0.0

        return DecisionTrace(
            decision_id=decision_id,
            decision=decision,
            evidence_ids=evidence_ids,
            confidence_score=round(
                confidence_score,
                4
            ),
            reasoning=reasoning
        )