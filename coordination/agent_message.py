from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from datetime import datetime


@dataclass
class AgentMessage:

    message_id: str

    sender: str

    receiver: str

    message_type: str

    content: Any

    task_id: Optional[str] = None

    priority: str = "normal"

    timestamp: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )