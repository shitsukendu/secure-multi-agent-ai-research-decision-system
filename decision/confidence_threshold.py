class ConfidenceThreshold:

    def __init__(
        self,
        high_threshold=0.85,
        medium_threshold=0.70
    ):
        self.high_threshold = high_threshold
        self.medium_threshold = medium_threshold

    def classify(self, confidence_score):

        if confidence_score >= self.high_threshold:
            return "HIGH"

        elif confidence_score >= self.medium_threshold:
            return "MEDIUM"

        else:
            return "LOW"

    def is_acceptable(self, confidence_score):

        return confidence_score >= self.medium_threshold