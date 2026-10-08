from decision.confidence_threshold import ConfidenceThreshold
from decision.evidence_sufficiency import EvidenceSufficiency
from decision.risk_assessment import RiskAssessment
from decision.decision_guard import DecisionGuard


class SecureDecisionEngine:

    def __init__(self):

        self.confidence_checker = ConfidenceThreshold()
        self.evidence_checker = EvidenceSufficiency()
        self.risk_checker = RiskAssessment()
        self.guard = DecisionGuard()

    def evaluate(
        self,
        confidence_score,
        evidence_list
    ):

        # 1. Confidence classification
        confidence_level = (
            self.confidence_checker.classify(
                confidence_score
            )
        )

        # 2. Evidence sufficiency
        evidence_result = (
            self.evidence_checker.check(
                evidence_list
            )
        )

        # 3. Risk assessment
        risk_level = self.risk_checker.assess(
            confidence_score,
            evidence_list
        )

        # 4. Security guard
        guard_result = self.guard.evaluate(
            confidence_score=confidence_score,
            evidence_sufficient=evidence_result["sufficient"],
            risk_level=risk_level
        )

        return {
            "allowed": guard_result["allowed"],
            "status": guard_result["status"],
            "confidence_score": confidence_score,
            "confidence_level": confidence_level,
            "evidence_sufficient": evidence_result["sufficient"],
            "evidence_count": len(evidence_list),
            "risk_level": risk_level,
            "issues": guard_result["issues"]
        }