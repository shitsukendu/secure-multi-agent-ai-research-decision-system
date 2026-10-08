import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def create_decision_agent():
    """Create the Gemini-powered decision agent."""
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file.")

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.0,
        google_api_key=api_key,
    )


def make_decision(
    research_report: str,
    fact_check_report: str,
    analyst_report: str,
) -> str:
    """Generate a final evidence-based decision."""

    if not research_report.strip():
        return "Research report is empty."

    if not fact_check_report.strip():
        return "Fact-check report is empty."

    if not analyst_report.strip():
        return "Analyst report is empty."

    llm = create_decision_agent()

    prompt = f"""
You are the Decision Agent in a Secure Multi-Agent AI
Research and Decision System.

Your job is to produce a final evidence-based decision using
ONLY the outputs provided by the Research Agent, Fact Checker
Agent, and Analyst Agent.

IMPORTANT RULES:

1. Do not use raw user input.
2. Do not introduce new facts.
3. Give priority to fact-checked evidence.
4. Consider the analyst's identified risks, opportunities,
   conflicts, and uncertainties.
5. Do not invent sources or citations.
6. If evidence is weak or conflicting, reduce confidence.
7. Clearly explain the reasoning behind the decision.
8. Mention important limitations.
9. The decision must be evidence-based, not speculative.
10. Do not claim certainty when the evidence does not support it.

RESEARCH REPORT:
{research_report}

FACT-CHECK REPORT:
{fact_check_report}

ANALYST REPORT:
{analyst_report}

Return the final decision using exactly this structure:

FINAL DECISION:
...

CONFIDENCE:
HIGH / MEDIUM / LOW

KEY EVIDENCE:
- Evidence 1
- Evidence 2
- Evidence 3

MAJOR RISKS:
- Risk 1
- Risk 2
- Risk 3

REASONING:
...

LIMITATIONS:
...
"""

    response = llm.invoke(prompt)

    return response.content