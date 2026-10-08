from evidence.evidence_audit import EvidenceAuditLog


audit = EvidenceAuditLog()


entry = audit.record(
    action="decision_created",
    evidence_ids=[
        "EV-81A4649F",
        "EV-1275EC7A"
    ],
    agent_name="DecisionAgent",
    decision_id="DEC-001",
    details={
        "reason": "Decision supported by ranked evidence."
    }
)


print("\n--- Audit Log Entry ---")

print("Timestamp:", entry["timestamp"])
print("Action:", entry["action"])
print("Evidence IDs:", entry["evidence_ids"])
print("Agent:", entry["agent_name"])
print("Decision ID:", entry["decision_id"])
print("Details:", entry["details"])


print("\n--- All Audit Logs ---")

print(audit.get_all())