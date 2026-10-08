from security.audit_logger import log_security_event

# =========================================================
# TOOL ACCESS POLICY
# =========================================================

ALLOWED_TOOLS = {
    "web_search",
}


# =========================================================
# CHECK TOOL ACCESS
# =========================================================

def is_tool_allowed(tool_name: str) -> bool:
    """
    Check whether a tool is allowed to be used
    by the multi-agent system.
    """

    if not tool_name:
        return False

    return tool_name in ALLOWED_TOOLS


# =========================================================
# TOOL ACCESS DECISION
# =========================================================

def check_tool_access(tool_name: str) -> dict:
    """
    Return a structured security decision for a tool.
    """

    if not tool_name:
        return {
            "allowed": False,
            "risk_level": "HIGH",
            "reason": "Tool name is missing.",
        }

    if not is_tool_allowed(tool_name):
        log_security_event(
            "UNAUTHORIZED_TOOL_ACCESS",
            f"risk=HIGH | tool={tool_name}"
        )

        return {
            "allowed": False,
            "risk_level": "HIGH",
            "reason": (
                f"Tool '{tool_name}' is not "
                "authorized by the security policy."
            ),
        }

    log_security_event(
        "AUTHORIZED_TOOL_ACCESS",
        f"risk=LOW | tool={tool_name}"
    )

    return {
        "allowed": True,
        "risk_level": "LOW",
        "reason": (
            f"Tool '{tool_name}' is authorized."
        ),
    }