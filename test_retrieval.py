from evidence.evidence_store import EvidenceStore


store = EvidenceStore()

print("\n--- All Evidence ---")
print(store.get_all())


print("\n--- ResearchAgent Evidence ---")
print(
    store.get_by_agent("ResearchAgent")
)


print("\n--- Research Paper Evidence ---")
print(
    store.get_by_source_type("research_paper")
)


print("\n--- High Reliability Evidence ---")
print(
    store.get_by_min_reliability(0.80)
)


print("\n--- Search: AI ---")
print(
    store.search("AI")
)