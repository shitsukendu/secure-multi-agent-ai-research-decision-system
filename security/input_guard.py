import re
from security.audit_logger import log_security_event


# =========================================================
# PROMPT INJECTION PATTERNS
# =========================================================

SUSPICIOUS_PATTERNS = [
    # Instruction override
    r"ignore\s+(all|any|the|your)?\s*(previous|prior|above|earlier)?\s*instructions",
    r"disregard\s+(all|any|the|your)?\s*(previous|prior|above|earlier)?\s*instructions",

    # System / developer prompt extraction
    r"reveal\s+(your|the)\s+(system|developer)\s+(prompt|instructions)",
    r"show\s+(me\s+)?(your|the)\s+(system|developer)\s+(prompt|instructions)",
    r"print\s+(your|the)\s+(system|developer)\s+(prompt|instructions)",
    r"tell\s+me\s+(your|the)\s+(system|developer)\s+(prompt|instructions)",

    # Security bypass
    r"bypass\s+(your\s+)?security",
    r"disable\s+(your\s+)?safety",
    r"override\s+(your\s+)?instructions",
    r"bypass\s+(the\s+)?safety\s+rules",

    # Role manipulation
    r"you\s+are\s+now\s+",
    r"act\s+as\s+if\s+you\s+are",
    r"pretend\s+that\s+you\s+are",

    # Previous instruction manipulation
    r"forget\s+(all|any|the|your)\s+(previous|prior|earlier)?\s*instructions",
    r"forget\s+everything\s+above",

    # Hidden instruction requests
    r"follow\s+these\s+instructions\s+instead",
    r"new\s+instructions\s*:",
]


# =========================================================
# TEXT NORMALIZATION
# =========================================================

def normalize_input(text: str) -> str:
    """
    Normalize user input before security analysis.
    """

    text = text.lower()

    # Replace repeated whitespace with a single space
    text = re.sub(r"\s+", " ", text)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text


# =========================================================
# PROMPT INJECTION DETECTION
# =========================================================

def detect_prompt_injection(text: str) -> dict:
    """
    Detect common prompt-injection patterns.
    """

    # Empty input
    if not text or not text.strip():
        return {
            "is_suspicious": False,
            "risk_level": "LOW",
            "reason": "Empty or missing input.",
            "matched_patterns": [],
        }

    normalized_text = normalize_input(text)

    detected_patterns = []

    for pattern in SUSPICIOUS_PATTERNS:

        if re.search(
            pattern,
            normalized_text,
            re.IGNORECASE,
        ):
            detected_patterns.append(pattern)

    # High-risk input
    if detected_patterns:
        log_security_event(
            "PROMPT_INJECTION_DETECTED",
            f"risk=HIGH | pattern_count={len(detected_patterns)}"
        )

        return {
            "is_suspicious": True,
            "risk_level": "HIGH",
            "reason": "Potential prompt injection detected.",
            "matched_patterns": detected_patterns,
        }

    # Safe input
    return {
        "is_suspicious": False,
        "risk_level": "LOW",
        "reason": "No known prompt-injection pattern detected.",
        "matched_patterns": [],
    }