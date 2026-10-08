class EvidenceValidator:

    SOURCE_RELIABILITY = {
        "official_document": 0.95,
        "government": 0.95,
        "research_paper": 0.90,
        "academic": 0.90,
        "trusted_news": 0.80,
        "web": 0.60,
        "blog": 0.50,
        "social_media": 0.30,
        "unknown": 0.20
    }

    def calculate_reliability(self, source_type):

        source_type = source_type.lower().strip()

        return self.SOURCE_RELIABILITY.get(
            source_type,
            self.SOURCE_RELIABILITY["unknown"]
        )

    def validate(self, evidence):

        issues = []

        if not evidence.source_title:
            issues.append("Missing source title")

        if not evidence.claim:
            issues.append("Missing claim")

        if not evidence.snippet:
            issues.append("Missing evidence snippet")

        score = self.calculate_reliability(
            evidence.source_type
        )

        evidence.reliability_score = score

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "reliability_score": score
        }