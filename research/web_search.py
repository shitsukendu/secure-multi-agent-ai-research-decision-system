import os

from dotenv import load_dotenv
from tavily import TavilyClient

from security.tool_policy import check_tool_access


load_dotenv()


# =========================================================
# WEB SEARCH TOOL
# =========================================================

def web_search(query: str, max_results: int = 5) -> list[dict]:
    """
    Perform a web search only if the tool is
    authorized by the security policy.
    """

    # -----------------------------------------------------
    # Tool authorization
    # -----------------------------------------------------

    tool_check = check_tool_access("web_search")

    if not tool_check["allowed"]:
        raise PermissionError(
            tool_check["reason"]
        )

    # -----------------------------------------------------
    # API key validation
    # -----------------------------------------------------

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise ValueError(
            "TAVILY_API_KEY not found in .env file."
        )

    # -----------------------------------------------------
    # Query validation
    # -----------------------------------------------------

    if not query or not query.strip():
        return []

    # -----------------------------------------------------
    # Tavily client
    # -----------------------------------------------------

    client = TavilyClient(
        api_key=api_key
    )

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results,
    )

    # -----------------------------------------------------
    # Format results
    # -----------------------------------------------------

    results = []

    for item in response.get("results", []):

        results.append(
            {
                "title": item.get(
                    "title",
                    ""
                ),
                "url": item.get(
                    "url",
                    ""
                ),
                "content": item.get(
                    "content",
                    ""
                ),
            }
        )

    return results