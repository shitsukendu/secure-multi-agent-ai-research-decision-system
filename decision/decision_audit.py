from evidence.evidence_audit import EvidenceAuditLog


class DecisionAudit:

    def __init__(self):

        self.audit_log = EvidenceAuditLog()

    def record_decision(
        self,
        decision_id,
        agent_name,
        evidence_ids,
        decision_result
    ):

        return self.audit_log.record(
            action="secure_decision_evaluated",
            evidence_ids=evidence_ids,
            agent_name=agent_name,
            decision_id=decision_id,
            details={
                "status": decision_result["status"],
                "allowed": decision_result["allowed"],
                "confidence_score": decision_result[
                    "confidence_score"
                ],
                "confidence_level": decision_result[
                    "confidence_level"
                ],
                "evidence_sufficient": decision_result[
                    "evidence_sufficient"
                ],
                "evidence_count": decision_result[
                    "evidence_count"
                ],
                "risk_level": decision_result[
                    "risk_level"
                ],
                "issues": decision_result[
                    "issues"
                ]
            }
        )