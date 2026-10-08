class RiskAssessment:

    def assess(
        self,
        confidence_score,
        evidence_list
    ):

        if not evidence_list:
            return "HIGH"

        average_reliability = sum(
            evidence.get("reliability_score", 0.0)
            for evidence in evidence_list
        ) / len(evidence_list)

        if (
            confidence_score >= 0.85
            and average_reliability >= 0.80
        ):
            return "LOW"

        elif (
            confidence_score >= 0.70
            and average_reliability >= 0.60
        ):
            return "MEDIUM"

        else:
            return "HIGH"