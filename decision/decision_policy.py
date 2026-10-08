class DecisionPolicy:

    def __init__(
        self,
        minimum_confidence=0.70,
        minimum_evidence=1,
        minimum_reliability=0.60
    ):

        self.minimum_confidence = minimum_confidence
        self.minimum_evidence = minimum_evidence
        self.minimum_reliability = minimum_reliability

    def evaluate(
        self,
        confidence_score,
        evidence_list
    ):

        issues = []

        # Confidence check
        if confidence_score < self.minimum_confidence:
            issues.append(
                "Confidence score is below the required threshold."
            )

        # Evidence count check
        if len(evidence_list) < self.minimum_evidence:
            issues.append(
                "Insufficient evidence for decision."
            )

        # Evidence reliability check
        for evidence in evidence_list:

            reliability = evidence.get(
                "reliability_score",
                0.0
            )

            if reliability < self.minimum_reliability:

                issues.append(
                    f"Low reliability evidence: "
                    f"{evidence.get('evidence_id')}"
                )

        approved = len(issues) == 0

        return {
            "approved": approved,
            "issues": issues,
            "confidence_score": confidence_score,
            "evidence_count": len(evidence_list)
        }