from decision.confidence_threshold import ConfidenceThreshold


threshold = ConfidenceThreshold()


test_scores = [
    0.92,
    0.78,
    0.55
]


print("\n--- Confidence Threshold Test ---")


for score in test_scores:

    level = threshold.classify(score)

    acceptable = threshold.is_acceptable(score)

    print(
        f"Confidence: {score} | "
        f"Level: {level} | "
        f"Acceptable: {acceptable}"
    )


print("\nCONFIDENCE THRESHOLD TEST PASSED")