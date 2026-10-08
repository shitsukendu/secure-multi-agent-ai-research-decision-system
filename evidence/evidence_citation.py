from dataclasses import dataclass
from typing import Optional


@dataclass
class EvidenceCitation:

    evidence_id: str
    source_title: str

    claim: str

    source_url: Optional[str] = None

    relevance_score: float = 0.0
    reliability_score: float = 0.0
    final_score: float = 0.0

    citation_label: str = ""


class CitationBuilder:

    def build(self, evidence):

        citation_label = (
            f"[{evidence['evidence_id']}] "
            f"{evidence['source_title']}"
        )

        return EvidenceCitation(
            evidence_id=evidence["evidence_id"],
            source_title=evidence["source_title"],
            claim=evidence.get("claim", ""),
            source_url=evidence.get("source_url"),
            relevance_score=evidence.get(
                "relevance_score",
                0.0
            ),
            reliability_score=evidence.get(
                "reliability_score",
                0.0
            ),
            final_score=evidence.get(
                "final_score",
                0.0
            ),
            citation_label=citation_label
        )