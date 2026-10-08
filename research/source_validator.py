from urllib.parse import urlparse


def validate_sources(sources: list[dict]) -> list[dict]:
    """
    Basic validation of collected web sources.
    """

    validated = []

    for source in sources:
        url = source.get("url", "").strip()
        title = source.get("title", "").strip()
        content = source.get("content", "").strip()

        if not url or not content:
            continue

        parsed = urlparse(url)

        if parsed.scheme not in {"http", "https"}:
            continue

        validated.append(
            {
                "title": title,
                "url": url,
                "content": content,
                "valid": True,
            }
        )

    return validated