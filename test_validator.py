from evidence.evidence_schema import Evidence
from evidence.evidence_validator import EvidenceValidator


evidence = Evidence(
    evidence_id="EV-TEST001",
    source_title="Test Research Paper",
    source_type="research_paper",
    claim="AI systems should provide traceable evidence.",
    snippet="This is a test evidence snippet.",
    agent_name="ResearchAgent"
)


validator = EvidenceValidator()

result = validator.validate(evidence)

print("Validation Result:")
print(result)

print("\nUpdated Reliability Score:")
print(evidence.reliability_score)