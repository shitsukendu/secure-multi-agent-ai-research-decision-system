from decision.secure_decision_engine import SecureDecisionEngine
from decision.decision_audit import DecisionAudit


engine = SecureDecisionEngine()
auditor = DecisionAudit()


# ---------------------------------
# 1. Evidence
# ---------------------------------

evidence = [
    {
        "evidence_id": "EV-PIPE-001",
        "reliability_score": 0.95
    },
    {
        "evidence_id": "EV-PIPE-002",
        "reliability_score": 0.90
    }
]


# ---------------------------------
# 2. Secure Decision Evaluation
# ---------------------------------

result = engine.evaluate(
    confidence_score=0.92,
    evidence_list=evidence
)


print("\n================================")
print("FINAL SECURE DECISION PIPELINE")
print("================================")


print("\n[1] Decision Evaluation")

print("Status:", result["status"])
print("Allowed:", result["allowed"])
print(
    "Confidence:",
    result["confidence_score"]
)
print(
    "Confidence Level:",
    result["confidence_level"]
)
print(
    "Evidence Sufficient:",
    result["evidence_sufficient"]
)
print(
    "Evidence Count:",
    result["evidence_count"]
)
print(
    "Risk Level:",
    result["risk_level"]
)
print(
    "Issues:",
    result["issues"]
)


# ---------------------------------
# 3. Audit
# ---------------------------------

audit_entry = auditor.record_decision(
    decision_id="DEC-PIPELINE-001",
    agent_name="DecisionAgent",
    evidence_ids=[
        evidence[0]["evidence_id"],
        evidence[1]["evidence_id"]
    ],
    decision_result=result
)


print("\n[2] Audit Record")

print(
    "Action:",
    audit_entry["action"]
)

print(
    "Decision ID:",
    audit_entry["decision_id"]
)

print(
    "Evidence IDs:",
    audit_entry["evidence_ids"]
)


# ---------------------------------
# 4. Final Verification
# ---------------------------------

if (
    result["allowed"]
    and result["status"] == "APPROVED"
    and result["confidence_level"] == "HIGH"
    and result["evidence_sufficient"]
    and result["risk_level"] == "LOW"
    and audit_entry["action"]
    == "secure_decision_evaluated"
):

    print("\n================================")
    print("SECURE DECISION PIPELINE OK")
    print("================================")

else:

    print("\n================================")
    print("SECURE DECISION PIPELINE FAILED")
    print("================================")