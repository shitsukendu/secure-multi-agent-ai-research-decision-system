import uuid

from evidence.evidence_schema import Evidence
from evidence.evidence_store import EvidenceStore
from evidence.evidence_validator import EvidenceValidator


class EvidenceCollector:

    def __init__(self):
        self.store = EvidenceStore()
        self.validator = EvidenceValidator()

    def collect(
        self,
        source_title,
        claim,
        snippet,
        source_url=None,
        source_type="unknown",
        agent_name=None,
        metadata=None
    ):
        evidence_id = f"EV-{uuid.uuid4().hex[:8].upper()}"

        evidence = Evidence(
            evidence_id=evidence_id,
            source_title=source_title,
            source_url=source_url,
            source_type=source_type,
            claim=claim,
            snippet=snippet,
            agent_name=agent_name,
            metadata=metadata or {}
        )

        validation_result = self.validator.validate(evidence)

        if not validation_result["valid"]:
            raise ValueError(
                f"Invalid evidence: {validation_result['issues']}"
            )

        self.store.add_evidence(evidence)

        return evidence