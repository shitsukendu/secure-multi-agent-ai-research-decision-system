from langgraph.graph import StateGraph, START, END

from core.state import AgentState

from agents.research_agent import research_agent
from agents.fact_checker_agent import fact_check_claims
from agents.analyst_agent import analyze_research
from agents.decision_agent import make_decision

from security.input_guard import detect_prompt_injection
from security.input_validator import validate_user_query
from security.output_guard import validate_agent_output
from security.policy import security_decision


# =========================================================
# SECURITY NODE
# =========================================================

def security_node(state: AgentState):
    try:
        query = state.get("query", "")

        # -------------------------------------------------
        # Step 1: Validate user input
        # -------------------------------------------------

        input_validation = validate_user_query(query)

        if not input_validation["valid"]:
            return {
                "security_result": {
                    "is_suspicious": False,
                    "risk_level": "HIGH",
                    "reason": input_validation["reason"],
                },
                "status": "BLOCK",
                "error": input_validation["reason"],
            }

        # Use normalized query
        validated_query = input_validation["query"]

        # -------------------------------------------------
        # Step 2: Prompt injection detection
        # -------------------------------------------------

        security_result = detect_prompt_injection(
            validated_query
        )

        decision = security_decision(
            security_result.get("risk_level", "LOW")
        )

        # -------------------------------------------------
        # Security decision
        # -------------------------------------------------

        if decision == "BLOCK":
            return {
                "query": validated_query,
                "security_result": security_result,
                "status": "BLOCK",
                "error": (
                    "Request blocked by the security layer."
                ),
            }

        return {
            "query": validated_query,
            "security_result": security_result,
            "status": "ALLOW",
            "error": "",
        }

    except Exception:
        return {
            "security_result": {
                "is_suspicious": False,
                "risk_level": "ERROR",
                "reason": "Security check failed.",
            },
            "status": "ERROR",
            "error": "Security validation failed.",
        }


# =========================================================
# RESEARCH NODE
# =========================================================

def research_node(state: AgentState):
    try:
        query = state.get("query", "")

        if not query or not query.strip():
            return {
                "research_report": "",
                "status": "ERROR",
                "error": "Research query is empty.",
            }

        report = research_agent(query)

        validation = validate_agent_output(report)

        if not validation["safe"]:
            return {
                "research_report": "",
                "status": "ERROR",
                "error": (
                    "Research agent output failed validation: "
                    + validation["reason"]
                ),
            }

        return {
            "research_report": report,
            "status": "RESEARCH_COMPLETE",
            "error": "",
        }

    except Exception:
        return {
            "research_report": "",
            "status": "ERROR",
            "error": "Research service is currently unavailable.",
        }


# =========================================================
# FACT CHECKER NODE
# =========================================================

def fact_checker_node(state: AgentState):
    try:
        research_report = state.get(
            "research_report",
            ""
        )

        if not research_report.strip():
            return {
                "fact_check_report": "",
                "status": "ERROR",
                "error": (
                    "No research report available "
                    "for fact checking."
                ),
            }

        fact_check_report = fact_check_claims(
            research_report,
            research_report,
        )

        validation = validate_agent_output(
            fact_check_report
        )

        if not validation["safe"]:
            return {
                "fact_check_report": "",
                "status": "ERROR",
                "error": (
                    "Fact checker output failed validation: "
                    + validation["reason"]
                ),
            }

        return {
            "fact_check_report": fact_check_report,
            "status": "FACT_CHECK_COMPLETE",
            "error": "",
        }

    except Exception:
        return {
            "fact_check_report": "",
            "status": "ERROR",
            "error": (
                "Fact-checking service is currently "
                "unavailable."
            ),
        }


# =========================================================
# ANALYST NODE
# =========================================================

def analyst_node(state: AgentState):
    try:
        research_report = state.get(
            "research_report",
            ""
        )

        fact_check_report = state.get(
            "fact_check_report",
            ""
        )

        if not research_report.strip():
            return {
                "analyst_report": "",
                "status": "ERROR",
                "error": "Research report is missing.",
            }

        if not fact_check_report.strip():
            return {
                "analyst_report": "",
                "status": "ERROR",
                "error": "Fact-check report is missing.",
            }

        analyst_report = analyze_research(
            research_report,
            fact_check_report,
        )

        validation = validate_agent_output(
            analyst_report
        )

        if not validation["safe"]:
            return {
                "analyst_report": "",
                "status": "ERROR",
                "error": (
                    "Analyst output failed validation: "
                    + validation["reason"]
                ),
            }

        return {
            "analyst_report": analyst_report,
            "status": "ANALYSIS_COMPLETE",
            "error": "",
        }

    except Exception:
        return {
            "analyst_report": "",
            "status": "ERROR",
            "error": (
                "Analysis service is currently unavailable."
            ),
        }


# =========================================================
# DECISION NODE
# =========================================================

def decision_node(state: AgentState):
    try:
        research_report = state.get(
            "research_report",
            ""
        )

        fact_check_report = state.get(
            "fact_check_report",
            ""
        )

        analyst_report = state.get(
            "analyst_report",
            ""
        )

        if not research_report.strip():
            return {
                "decision": "",
                "status": "ERROR",
                "error": "Research report is missing.",
            }

        if not fact_check_report.strip():
            return {
                "decision": "",
                "status": "ERROR",
                "error": "Fact-check report is missing.",
            }

        if not analyst_report.strip():
            return {
                "decision": "",
                "status": "ERROR",
                "error": "Analyst report is missing.",
            }

        decision = make_decision(
            research_report,
            fact_check_report,
            analyst_report,
        )

        validation = validate_agent_output(
            decision
        )

        if not validation["safe"]:
            return {
                "decision": "",
                "status": "ERROR",
                "error": (
                    "Decision agent output failed validation: "
                    + validation["reason"]
                ),
            }

        return {
            "decision": decision,
            "status": "DECISION_COMPLETE",
            "error": "",
        }

    except Exception:
        return {
            "decision": "",
            "status": "ERROR",
            "error": (
                "Decision service is currently unavailable."
            ),
        }


# =========================================================
# ROUTERS
# =========================================================

def security_router(state: AgentState):

    status = state.get("status")

    if status == "BLOCK":
        return END

    if status == "ERROR":
        return END

    return "research"


def research_router(state: AgentState):

    if state.get("status") == "ERROR":
        return END

    return "fact_checker"


def fact_checker_router(state: AgentState):

    if state.get("status") == "ERROR":
        return END

    return "analyst"


def analyst_router(state: AgentState):

    if state.get("status") == "ERROR":
        return END

    return "decision"


# =========================================================
# BUILD WORKFLOW
# =========================================================

def build_workflow():

    graph = StateGraph(AgentState)

    graph.add_node(
        "security",
        security_node
    )

    graph.add_node(
        "research",
        research_node
    )

    graph.add_node(
        "fact_checker",
        fact_checker_node
    )

    graph.add_node(
        "analyst",
        analyst_node
    )

    graph.add_node(
        "decision",
        decision_node
    )

    graph.add_edge(
        START,
        "security"
    )

    graph.add_conditional_edges(
        "security",
        security_router,
        {
            "research": "research",
            END: END,
        },
    )

    graph.add_conditional_edges(
        "research",
        research_router,
        {
            "fact_checker": "fact_checker",
            END: END,
        },
    )

    graph.add_conditional_edges(
        "fact_checker",
        fact_checker_router,
        {
            "analyst": "analyst",
            END: END,
        },
    )

    graph.add_conditional_edges(
        "analyst",
        analyst_router,
        {
            "decision": "decision",
            END: END,
        },
    )

    graph.add_edge(
        "decision",
        END
    )

    return graph.compile()