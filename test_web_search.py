from research.web_search import web_search
from research.source_validator import validate_sources


query = "benefits and risks of multi-agent AI systems"

sources = web_search(query, max_results=5)

validated_sources = validate_sources(sources)

print("\n===== VALIDATED SOURCES =====\n")

for i, source in enumerate(validated_sources, start=1):
    print(f"{i}. {source['title']}")
    print(f"URL: {source['url']}")
    print(f"Valid: {source['valid']}")
    print()