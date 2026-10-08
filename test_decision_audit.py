from decision.decision_audit import DecisionAudit


auditor = DecisionAudit()


decision_result = {
    "allowed": True,
    "status": "APPROVED",
    "confidence_score": 0.90,
    "confidence_level": "HIGH",
    "evidence_sufficient": True,
    "evidence_count": 2,
    "risk_level": "LOW",
    "issues": []
}


entry = auditor.record_decision(
    decision_id="DEC-SECURE-001",
    agent_name="DecisionAgent",
    evidence_ids=[
        "EV-001",
        "EV-002"
    ],
    decision_result=decision_result
)


print("\n--- Decision Audit Test ---")

print("Action:", entry["action"])
print("Decision ID:", entry["decision_id"])
print("Agent:", entry["agent_name"])
print("Evidence IDs:", entry["evidence_ids"])

print("\nDecision Details:")
print(
    "Status:",
    entry["details"]["status"]
)

print(
    "Confidence:",
    entry["details"]["confidence_score"]
)

print(
    "Risk Level:",
    entry["details"]["risk_level"]
)

print(
    "Evidence Sufficient:",
    entry["details"]["evidence_sufficient"]
)


if (
    entry["action"] == "secure_decision_evaluated"
    and entry["decision_id"] == "DEC-SECURE-001"
    and entry["details"]["status"] == "APPROVED"
):

    print("\nDECISION AUDIT TEST PASSED")

else:

    print("\nDECISION AUDIT TEST FAILED")