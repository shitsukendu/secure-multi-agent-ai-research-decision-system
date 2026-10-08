from decision.secure_decision_engine import SecureDecisionEngine


engine = SecureDecisionEngine()


print("\n======================================")
print("SECURITY VALIDATION TEST")
print("======================================")


# =====================================
# 1. Safe Decision
# =====================================

safe_evidence = [
    {
        "evidence_id": "EV-SAFE-001",
        "reliability_score": 0.95
    }
]

safe_result = engine.evaluate(
    confidence_score=0.90,
    evidence_list=safe_evidence
)

print("\n[1] Safe Decision")
print("Status:", safe_result["status"])
print("Risk:", safe_result["risk_level"])


# =====================================
# 2. Low Confidence
# =====================================

low_confidence_result = engine.evaluate(
    confidence_score=0.40,
    evidence_list=safe_evidence
)

print("\n[2] Low Confidence")
print("Status:", low_confidence_result["status"])
print("Allowed:", low_confidence_result["allowed"])


# =====================================
# 3. No Evidence
# =====================================

no_evidence_result = engine.evaluate(
    confidence_score=0.90,
    evidence_list=[]
)

print("\n[3] No Evidence")
print("Status:", no_evidence_result["status"])
print("Allowed:", no_evidence_result["allowed"])


# =====================================
# 4. Low Reliability Evidence
# =====================================

low_reliability_evidence = [
    {
        "evidence_id": "EV-LOW-001",
        "reliability_score": 0.30
    }
]

low_reliability_result = engine.evaluate(
    confidence_score=0.90,
    evidence_list=low_reliability_evidence
)

print("\n[4] Low Reliability Evidence")
print("Status:", low_reliability_result["status"])
print("Risk:", low_reliability_result["risk_level"])


# =====================================
# 5. Final Verification
# =====================================

if (
    safe_result["status"] == "APPROVED"
    and safe_result["allowed"]
    and low_confidence_result["status"] == "BLOCKED"
    and not low_confidence_result["allowed"]
    and no_evidence_result["status"] == "BLOCKED"
    and not no_evidence_result["allowed"]
    and low_reliability_result["status"] == "BLOCKED"
    and not low_reliability_result["allowed"]
):

    print("\n======================================")
    print("SECURITY VALIDATION TEST OK")
    print("======================================")

else:

    print("\n======================================")
    print("SECURITY VALIDATION TEST FAILED")
    print("======================================")