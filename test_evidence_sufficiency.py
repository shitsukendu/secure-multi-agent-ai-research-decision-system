from decision.evidence_sufficiency import EvidenceSufficiency


checker = EvidenceSufficiency()


good_evidence = [
    {
        "evidence_id": "EV-001",
        "reliability_score": 0.90
    },
    {
        "evidence_id": "EV-002",
        "reliability_score": 0.85
    }
]


bad_evidence = []


print("\n--- Evidence Sufficiency Test ---")


result_good = checker.check(good_evidence)

print("\nGood Evidence:")
print("Sufficient:", result_good["sufficient"])
print("Evidence Count:", result_good["evidence_count"])
print(
    "Reliable Evidence:",
    result_good["reliable_evidence_count"]
)
print("Issues:", result_good["issues"])


result_bad = checker.check(bad_evidence)

print("\nEmpty Evidence:")
print("Sufficient:", result_bad["sufficient"])
print("Evidence Count:", result_bad["evidence_count"])
print("Issues:", result_bad["issues"])


if result_good["sufficient"] and not result_bad["sufficient"]:
    print("\nEVIDENCE SUFFICIENCY TEST PASSED")
else:
    print("\nEVIDENCE SUFFICIENCY TEST FAILED")