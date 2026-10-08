import re


# =========================================================
# INPUT VALIDATION SETTINGS
# =========================================================

MAX_QUERY_LENGTH = 5000
MIN_QUERY_LENGTH = 3


# =========================================================
# VALIDATE USER QUERY
# =========================================================

def validate_user_query(query: str) -> dict:
    """
    Validate and normalize a user research query
    before it enters the multi-agent workflow.
    """

    # -----------------------------------------------------
    # Type validation
    # -----------------------------------------------------

    if not isinstance(query, str):
        return {
            "valid": False,
            "reason": "Research query must be text.",
            "query": "",
        }

    # -----------------------------------------------------
    # Remove unnecessary whitespace
    # -----------------------------------------------------

    normalized_query = re.sub(
        r"\s+",
        " ",
        query
    ).strip()

    # -----------------------------------------------------
    # Empty query
    # -----------------------------------------------------

    if not normalized_query:
        return {
            "valid": False,
            "reason": "Research query cannot be empty.",
            "query": "",
        }

    # -----------------------------------------------------
    # Minimum length
    # -----------------------------------------------------

    if len(normalized_query) < MIN_QUERY_LENGTH:
        return {
            "valid": False,
            "reason": "Research query is too short.",
            "query": "",
        }

    # -----------------------------------------------------
    # Maximum length
    # -----------------------------------------------------

    if len(normalized_query) > MAX_QUERY_LENGTH:
        return {
            "valid": False,
            "reason": (
                "Research query is too long. "
                f"Maximum length is {MAX_QUERY_LENGTH} characters."
            ),
            "query": "",
        }

    # -----------------------------------------------------
    # Control-character check
    # -----------------------------------------------------

    if any(ord(char) < 32 and char not in "\n\t" for char in query):
        return {
            "valid": False,
            "reason": "Research query contains invalid characters.",
            "query": "",
        }

    # -----------------------------------------------------
    # Valid input
    # -----------------------------------------------------

    return {
        "valid": True,
        "reason": "Research query passed input validation.",
        "query": normalized_query,
    }