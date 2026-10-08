from decision.secure_decision_engine import SecureDecisionEngine


engine = SecureDecisionEngine()


strong_evidence = [
    {
        "evidence_id": "EV-001",
        "reliability_score": 0.90
    },
    {
        "evidence_id": "EV-002",
        "reliability_score": 0.85
    }
]


weak_evidence = [
    {
        "evidence_id": "EV-003",
        "reliability_score": 0.30
    }
]


print("\n--- Secure Decision Engine Test ---")


# Safe decision
safe_result = engine.evaluate(
    confidence_score=0.90,
    evidence_list=strong_evidence
)

print("\nSafe Decision:")
print(safe_result)


# Weak decision
weak_result = engine.evaluate(
    confidence_score=0.50,
    evidence_list=weak_evidence
)

print("\nWeak Decision:")
print(weak_result)


if (
    safe_result["allowed"]
    and safe_result["status"] == "APPROVED"
    and not weak_result["allowed"]
    and weak_result["status"] == "BLOCKED"
):

    print("\nSECURE DECISION ENGINE TEST PASSED")

else:

    print("\nSECURE DECISION ENGINE TEST FAILED")