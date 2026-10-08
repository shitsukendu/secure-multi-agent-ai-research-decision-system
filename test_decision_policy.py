from decision.decision_policy import DecisionPolicy


policy = DecisionPolicy()


evidence = [
    {
        "evidence_id": "EV-001",
        "reliability_score": 0.90
    },
    {
        "evidence_id": "EV-002",
        "reliability_score": 0.85
    }
]


result = policy.evaluate(
    confidence_score=0.88,
    evidence_list=evidence
)


print("\n--- Decision Policy Test ---")

print("Approved:", result["approved"])
print("Confidence:", result["confidence_score"])
print("Evidence Count:", result["evidence_count"])
print("Issues:", result["issues"])


if result["approved"]:

    print("\nDECISION POLICY PASSED")

else:

    print("\nDECISION POLICY BLOCKED")