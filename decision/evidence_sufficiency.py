class EvidenceSufficiency:

    def __init__(
        self,
        minimum_evidence=1,
        minimum_reliability=0.60
    ):
        self.minimum_evidence = minimum_evidence
        self.minimum_reliability = minimum_reliability

    def check(self, evidence_list):

        issues = []

        # Check evidence count
        if len(evidence_list) < self.minimum_evidence:
            issues.append(
                "Insufficient number of evidence items."
            )

        # Check reliability
        reliable_evidence = [
            evidence
            for evidence in evidence_list
            if evidence.get(
                "reliability_score",
                0.0
            ) >= self.minimum_reliability
        ]

        if len(reliable_evidence) < self.minimum_evidence:
            issues.append(
                "Insufficient reliable evidence."
            )

        return {
            "sufficient": len(issues) == 0,
            "evidence_count": len(evidence_list),
            "reliable_evidence_count": len(reliable_evidence),
            "issues": issues
        }