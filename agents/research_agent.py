import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from research.web_search import web_search
from research.source_validator import validate_sources


load_dotenv()


def create_research_agent():
    """Create the Gemini-powered research agent."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file.")

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2,
        google_api_key=api_key,
    )


def research_agent(query: str) -> str:
    """Perform web research and generate a source-backed analysis."""

    if not query or not query.strip():
        return "Please provide a valid research query."

    # Step 1: Search the web
    sources = web_search(query, max_results=5)

    # Step 2: Validate sources
    validated_sources = validate_sources(sources)

    if not validated_sources:
        return "No valid research sources were found."

    # Step 3: Prepare source context
    source_context = ""

    for i, source in enumerate(validated_sources, start=1):
        source_context += f"""
SOURCE {i}
Title: {source["title"]}
URL: {source["url"]}
Content:
{source["content"]}

"""

    # Step 4: Ask Gemini to analyze the sources
    llm = create_research_agent()

    prompt = f"""
You are the Research Agent in a Secure Multi-Agent AI
Research and Decision System.

Analyze the user's research question using ONLY the
validated web sources provided below.

Rules:
1. Do not invent facts.
2. Do not create fake citations.
3. Clearly distinguish facts from interpretation.
4. Mention uncertainty when the sources do not provide
   enough evidence.
5. Cite sources using [Source 1], [Source 2], etc.
6. Provide a concise but useful research analysis.
7. Do not make the final decision for the user.

User Research Query:
{query}

Validated Web Sources:
{source_context}
"""

    response = llm.invoke(prompt)

    return response.content