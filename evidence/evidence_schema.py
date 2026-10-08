from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime


@dataclass
class Evidence:
    evidence_id: str
    source_title: str
    source_url: Optional[str] = None
    source_type: str = "unknown"

    claim: str = ""
    snippet: str = ""

    agent_name: Optional[str] = None

    reliability_score: float = 0.0

    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    metadata: dict = field(default_factory=dict)