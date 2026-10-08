import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


def create_fact_checker():
    """Create the Gemini-powered fact checker."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file.")

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.0,
        google_api_key=api_key,
    )


def fact_check_claims(claims: str, sources: str) -> str:
    """
    Verify research claims against the provided sources.
    """

    if not claims.strip():
        return "No claims were provided."

    if not sources.strip():
        return "No sources were provided."

    llm = create_fact_checker()

    prompt = f"""
You are the Fact Checker Agent in a Secure Multi-Agent AI
Research and Decision System.

Your task is to verify research claims against the supplied
web sources.

IMPORTANT RULES:

1. Use ONLY the provided sources.
2. Do not use your own external knowledge.
3. Do not invent evidence.
4. Identify whether each claim is supported, partially
   supported, or unsupported.
5. Explain the reason for each classification.
6. Mention the relevant source number.
7. If evidence is insufficient, clearly say so.
8. Do not make a final decision for the user.

Research Claims:
{claims}

Available Sources:
{sources}

Return the result using this structure:

CLAIM 1:
Claim:
Status:
Evidence:
Source:

CLAIM 2:
Claim:
Status:
Evidence:
Source:

Overall Verification:
"""

    response = llm.invoke(prompt)

    return response.content