def security_decision(risk_level: str) -> str:
    """
    Convert risk level into a security action.
    """

    risk_level = risk_level.upper()

    if risk_level == "HIGH":
        return "BLOCK"

    if risk_level == "MEDIUM":
        return "REVIEW"

    return "ALLOW"