from decision.decision_guard import DecisionGuard


guard = DecisionGuard()


print("\n--- Decision Guard Test ---")


# Safe decision
safe_result = guard.evaluate(
    confidence_score=0.90,
    evidence_sufficient=True,
    risk_level="LOW"
)

print("\nSafe Decision:")
print("Allowed:", safe_result["allowed"])
print("Status:", safe_result["status"])
print("Issues:", safe_result["issues"])


# Low confidence
low_confidence_result = guard.evaluate(
    confidence_score=0.50,
    evidence_sufficient=True,
    risk_level="LOW"
)

print("\nLow Confidence Decision:")
print("Allowed:", low_confidence_result["allowed"])
print("Status:", low_confidence_result["status"])
print("Issues:", low_confidence_result["issues"])


# Insufficient evidence
insufficient_result = guard.evaluate(
    confidence_score=0.80,
    evidence_sufficient=False,
    risk_level="MEDIUM"
)

print("\nInsufficient Evidence:")
print("Allowed:", insufficient_result["allowed"])
print("Status:", insufficient_result["status"])
print("Issues:", insufficient_result["issues"])


# High risk
high_risk_result = guard.evaluate(
    confidence_score=0.90,
    evidence_sufficient=True,
    risk_level="HIGH"
)

print("\nHigh Risk Decision:")
print("Allowed:", high_risk_result["allowed"])
print("Status:", high_risk_result["status"])
print("Issues:", high_risk_result["issues"])


if (
    safe_result["allowed"]
    and not low_confidence_result["allowed"]
    and not insufficient_result["allowed"]
    and not high_risk_result["allowed"]
):

    print("\nDECISION GUARD TEST PASSED")

else:

    print("\nDECISION GUARD TEST FAILED")