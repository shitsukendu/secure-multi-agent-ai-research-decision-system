from evidence.evidence_store import EvidenceStore
from evidence.evidence_ranker import EvidenceRanker


store = EvidenceStore()
ranker = EvidenceRanker()

evidence_list = store.get_all()

query = "AI evidence"

ranked_results = ranker.rank(
    evidence_list,
    query
)

print("\n--- Ranked Evidence ---")

for item in ranked_results:

    print("\nEvidence ID:", item["evidence_id"])
    print("Source:", item["source_title"])
    print("Reliability:", item["reliability_score"])
    print("Relevance:", item["relevance_score"])
    print("Final Score:", item["final_score"])



top_results = ranker.top_k(
    evidence_list,
    query,
    k=1
)

print("\n--- Top 1 Evidence ---")

for item in top_results:

    print("Evidence ID:", item["evidence_id"])
    print("Source:", item["source_title"])
    print("Final Score:", item["final_score"])