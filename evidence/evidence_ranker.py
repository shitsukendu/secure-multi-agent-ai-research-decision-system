class EvidenceRanker:

    def calculate_relevance(self, evidence, query):
        query_words = set(query.lower().split())

        text = " ".join([
            str(evidence.get("source_title", "")),
            str(evidence.get("claim", "")),
            str(evidence.get("snippet", ""))
        ]).lower()

        text_words = set(text.split())

        if not query_words:
            return 0.0

        matched_words = query_words.intersection(text_words)

        return len(matched_words) / len(query_words)

    def calculate_final_score(self, evidence, query):
        reliability = evidence.get(
            "reliability_score",
            0.0
        )

        relevance = self.calculate_relevance(
            evidence,
            query
        )

        final_score = (
            0.6 * reliability
            +
            0.4 * relevance
        )

        return round(final_score, 4)

    def rank(self, evidence_list, query):

        ranked = []

        for evidence in evidence_list:

            relevance = self.calculate_relevance(
                evidence,
                query
            )

            final_score = self.calculate_final_score(
                evidence,
                query
            )

            item = evidence.copy()

            item["relevance_score"] = round(
                relevance,
                4
            )

            item["final_score"] = final_score

            ranked.append(item)

        ranked.sort(
            key=lambda x: x["final_score"],
            reverse=True
        )

        return ranked

    def top_k(self, evidence_list, query, k=5):

        ranked_results = self.rank(
            evidence_list,
            query
        )

        return ranked_results[:k]