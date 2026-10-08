import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


def create_analyst():
    """Create the Gemini-powered analyst agent."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file.")

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1,
        google_api_key=api_key,
    )


def analyze_research(
    research_report: str,
    fact_check_report: str,
) -> str:
    """
    Analyze research findings and fact-check results.
    """

    if not research_report.strip():
        return "Research report is empty."

    if not fact_check_report.strip():
        return "Fact-check report is empty."

    llm = create_analyst()

    prompt = f"""
You are the Analyst Agent in a Secure Multi-Agent AI
Research and Decision System.

Your task is to analyze the research report together with
the independent fact-checking report.

IMPORTANT RULES:

1. Give priority to fact-checked information.
2. Do not introduce facts that are not present in the
   supplied reports.
3. Clearly separate evidence from interpretation.
4. Highlight conflicting or uncertain information.
5. Identify the most important findings.
6. Identify major risks and opportunities.
7. Do not make the final decision for the user.
8. Do not invent sources or citations.

RESEARCH REPORT:
{research_report}

FACT-CHECK REPORT:
{fact_check_report}

Return the analysis using exactly this structure:

KEY FINDINGS:
- Finding 1
- Finding 2
- Finding 3

EVIDENCE QUALITY:
- Strong:
- Moderate:
- Weak or Uncertain:

MAJOR RISKS:
- Risk 1
- Risk 2
- Risk 3

OPPORTUNITIES:
- Opportunity 1
- Opportunity 2
- Opportunity 3

CONFLICTS OR UNCERTAINTIES:
- ...

ANALYST SUMMARY:
...
"""

    response = llm.invoke(prompt)

    return response.content