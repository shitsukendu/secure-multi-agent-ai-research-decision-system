from evidence.evidence_store import EvidenceStore
from evidence.evidence_ranker import EvidenceRanker
from evidence.decision_trace import DecisionTraceBuilder


store = EvidenceStore()
ranker = EvidenceRanker()
builder = DecisionTraceBuilder()


evidence_list = store.get_all()

query = "AI evidence"

top_results = ranker.top_k(
    evidence_list,
    query,
    k=2
)


trace = builder.build(
    decision_id="DEC-001",
    decision="Use evidence-backed AI research.",
    evidence_list=top_results,
    reasoning="The decision is supported by the highest-ranked available evidence."
)


print("\n--- Decision Trace ---")

print("Decision ID:", trace.decision_id)
print("Decision:", trace.decision)
print("Evidence IDs:", trace.evidence_ids)
print("Confidence Score:", trace.confidence_score)
print("Reasoning:", trace.reasoning)