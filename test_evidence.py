from evidence.evidence_collector import EvidenceCollector


collector = EvidenceCollector()

evidence = collector.collect(
    source_title="Demo Research Paper",
    claim="AI systems should provide traceable evidence.",
    snippet="This is a test evidence snippet.",
    source_url="https://example.com",
    source_type="research_paper",
    agent_name="ResearchAgent"
)

print("Evidence stored successfully!")
print("Evidence ID:", evidence.evidence_id)
print("Reliability Score:", evidence.reliability_score)


second = collector.collect(
    source_title="Demo Research Paper",
    claim="AI systems should provide traceable evidence.",
    snippet="This is a test evidence snippet.",
    source_url="https://example.com",
    source_type="research_paper",
    agent_name="ResearchAgent"
)

print("Second evidence ID:", second.evidence_id)