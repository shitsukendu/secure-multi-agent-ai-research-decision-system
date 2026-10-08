import re
from security.audit_logger import log_security_event


# =========================================================
# SENSITIVE DATA PATTERNS
# =========================================================

SENSITIVE_PATTERNS = [

    # API keys / tokens
    r"api[_\s-]?key\s*[:=]\s*\S+",
    r"access[_\s-]?token\s*[:=]\s*\S+",
    r"secret[_\s-]?key\s*[:=]\s*\S+",

    # Passwords
    r"password\s*[:=]\s*\S+",
    r"passwd\s*[:=]\s*\S+",

    # Common private key indicators
    r"-----BEGIN\s+(RSA|EC|OPENSSH|PRIVATE)\s+KEY-----",

    # Bearer token
    r"bearer\s+[A-Za-z0-9\-._~+/]+=*",

]


# =========================================================
# DETECT SENSITIVE INFORMATION
# =========================================================

def detect_sensitive_information(output: str) -> dict:
    """
    Detect common sensitive-information patterns
    in an AI agent output.
    """

    if not output or not output.strip():
        return {
            "detected": False,
            "risk_level": "LOW",
            "reason": "Output is empty.",
            "matched_patterns": [],
        }

    detected_patterns = []

    for pattern in SENSITIVE_PATTERNS:

        if re.search(
            pattern,
            output,
            re.IGNORECASE,
        ):
            detected_patterns.append(pattern)

    if detected_patterns:
        log_security_event(
            "SENSITIVE_OUTPUT_DETECTED",
            f"risk=HIGH | pattern_count={len(detected_patterns)}"
        )

        return {
            "detected": True,
            "risk_level": "HIGH",
            "reason": (
                "Potential sensitive information "
                "detected in agent output."
            ),
            "matched_patterns": detected_patterns,
        }

    return {
        "detected": False,
        "risk_level": "LOW",
        "reason": (
            "No known sensitive-information "
            "pattern detected."
        ),
        "matched_patterns": [],
    }


# =========================================================
# VALIDATE AGENT OUTPUT
# =========================================================

def validate_agent_output(output: str) -> dict:
    """
    Validate output returned by an AI agent.
    """

    # -----------------------------------------------------
    # Empty output
    # -----------------------------------------------------

    if not output or not output.strip():
        return {
            "safe": False,
            "risk_level": "HIGH",
            "reason": "Agent returned an empty output.",
        }

    # -----------------------------------------------------
    # Extremely large output
    # -----------------------------------------------------

    if len(output) > 50000:
        return {
            "safe": False,
            "risk_level": "MEDIUM",
            "reason": "Agent output is unusually large.",
        }

    # -----------------------------------------------------
    # Sensitive information check
    # -----------------------------------------------------

    sensitive_check = detect_sensitive_information(
        output
    )

    if sensitive_check["detected"]:
        return {
            "safe": False,
            "risk_level": "HIGH",
            "reason": sensitive_check["reason"],
        }

    # -----------------------------------------------------
    # Safe output
    # -----------------------------------------------------

    return {
        "safe": True,
        "risk_level": "LOW",
        "reason": (
            "Agent output passed security validation."
        ),
    }