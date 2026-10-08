from typing import TypedDict


class AgentState(TypedDict, total=False):
    # User input
    query: str

    # Security
    security_result: dict

    # Research
    research_report: str
    sources: list[dict]

    # Fact checking
    fact_check_report: str

    # Analysis
    analyst_report: str

    # Final decision
    decision: str

    # Final workflow status
    status: str
    error: str