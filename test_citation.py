from evidence.evidence_store import EvidenceStore
from evidence.evidence_ranker import EvidenceRanker
from evidence.evidence_citation import CitationBuilder


store = EvidenceStore()
ranker = EvidenceRanker()
builder = CitationBuilder()


evidence_list = store.get_all()

query = "AI evidence"

top_results = ranker.top_k(
    evidence_list,
    query,
    k=1
)


print("\n--- Evidence Citation ---")

for evidence in top_results:

    citation = builder.build(evidence)

    print("Citation Label:", citation.citation_label)
    print("Evidence ID:", citation.evidence_id)
    print("Source:", citation.source_title)
    print("Claim:", citation.claim)
    print("Reliability:", citation.reliability_score)
    print("Relevance:", citation.relevance_score)
    print("Final Score:", citation.final_score)