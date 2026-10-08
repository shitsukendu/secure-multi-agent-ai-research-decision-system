from decision.risk_assessment import RiskAssessment


risk_checker = RiskAssessment()


high_quality_evidence = [
    {
        "evidence_id": "EV-001",
        "reliability_score": 0.90
    },
    {
        "evidence_id": "EV-002",
        "reliability_score": 0.85
    }
]


medium_quality_evidence = [
    {
        "evidence_id": "EV-003",
        "reliability_score": 0.65
    },
    {
        "evidence_id": "EV-004",
        "reliability_score": 0.70
    }
]


low_quality_evidence = [
    {
        "evidence_id": "EV-005",
        "reliability_score": 0.30
    }
]


print("\n--- Risk Assessment Test ---")


low_risk = risk_checker.assess(
    confidence_score=0.90,
    evidence_list=high_quality_evidence
)

print(
    "High Quality Evidence:",
    low_risk
)


medium_risk = risk_checker.assess(
    confidence_score=0.75,
    evidence_list=medium_quality_evidence
)

print(
    "Medium Quality Evidence:",
    medium_risk
)


high_risk = risk_checker.assess(
    confidence_score=0.50,
    evidence_list=low_quality_evidence
)

print(
    "Low Quality Evidence:",
    high_risk
)


empty_risk = risk_checker.assess(
    confidence_score=0.90,
    evidence_list=[]
)

print(
    "No Evidence:",
    empty_risk
)


if (
    low_risk == "LOW"
    and medium_risk == "MEDIUM"
    and high_risk == "HIGH"
    and empty_risk == "HIGH"
):

    print("\nRISK ASSESSMENT TEST PASSED")

else:

    print("\nRISK ASSESSMENT TEST FAILED")