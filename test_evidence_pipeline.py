from evidence.evidence_collector import EvidenceCollector
from evidence.evidence_store import EvidenceStore
from evidence.evidence_ranker import EvidenceRanker
from evidence.evidence_citation import CitationBuilder
from evidence.decision_trace import DecisionTraceBuilder
from evidence.evidence_audit import EvidenceAuditLog


# 1. Initialize components

collector = EvidenceCollector()
store = EvidenceStore()
ranker = EvidenceRanker()
citation_builder = CitationBuilder()
trace_builder = DecisionTraceBuilder()
audit = EvidenceAuditLog()


# 2. Collect evidence

evidence = collector.collect(
    source_title="Integration Test Research Paper",
    claim="AI systems require evidence-based decisions.",
    snippet="Evidence helps improve transparency and traceability.",
    source_url="https://example.com/integration-test",
    source_type="research_paper",
    agent_name="ResearchAgent"
)

print("\n[1] Evidence Collected")
print("Evidence ID:", evidence.evidence_id)
print("Reliability:", evidence.reliability_score)


# 3. Retrieve evidence

all_evidence = store.get_all()

print("\n[2] Evidence Retrieved")
print("Total Evidence:", len(all_evidence))


# 4. Rank evidence

query = "AI evidence"

ranked = ranker.rank(
    all_evidence,
    query
)

top_results = ranked[:2]

print("\n[3] Evidence Ranked")

for item in top_results:
    print(
        item["evidence_id"],
        "Score:",
        item["final_score"]
    )


# 5. Build citations

print("\n[4] Evidence Citations")

citations = []

for item in top_results:

    citation = citation_builder.build(item)

    citations.append(citation)

    print(
        citation.citation_label
    )


# 6. Create decision trace

trace = trace_builder.build(
    decision_id="DEC-INTEGRATION-001",
    decision="Use evidence-backed AI decision making.",
    evidence_list=top_results,
    reasoning="Decision generated from the highest-ranked available evidence."
)

print("\n[5] Decision Trace")

print("Decision ID:", trace.decision_id)
print("Evidence IDs:", trace.evidence_ids)
print("Confidence:", trace.confidence_score)


# 7. Create audit log

audit_entry = audit.record(
    action="decision_created",
    evidence_ids=trace.evidence_ids,
    agent_name="DecisionAgent",
    decision_id=trace.decision_id,
    details={
        "confidence_score": trace.confidence_score,
        "reason": trace.reasoning
    }
)

print("\n[6] Audit Log")

print("Action:", audit_entry["action"])
print("Decision ID:", audit_entry["decision_id"])
print("Evidence IDs:", audit_entry["evidence_ids"])


print("\n================================")
print("SOURCE & EVIDENCE PIPELINE OK")
print("================================")