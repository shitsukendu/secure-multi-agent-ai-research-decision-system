class DecisionGuard:

    def evaluate(
        self,
        confidence_score,
        evidence_sufficient,
        risk_level
    ):

        issues = []

        # Confidence check
        if confidence_score < 0.70:
            issues.append(
                "Decision confidence is too low."
            )

        # Evidence check
        if not evidence_sufficient:
            issues.append(
                "Decision does not have sufficient evidence."
            )

        # Risk check
        if risk_level == "HIGH":
            issues.append(
                "Decision has a high risk level."
            )

        if issues:

            return {
                "allowed": False,
                "status": "BLOCKED",
                "issues": issues
            }

        return {
            "allowed": True,
            "status": "APPROVED",
            "issues": []
        }