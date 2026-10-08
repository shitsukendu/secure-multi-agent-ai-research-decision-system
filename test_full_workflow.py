from core.orchestrator import build_workflow


workflow = build_workflow()


query = """
What are the major benefits and risks of using multi-agent
AI systems in business decision-making?
"""


initial_state = {
    "query": query,
    "status": "STARTED",
}


print("\n===== STARTING MULTI-AGENT WORKFLOW =====\n")

result = workflow.invoke(initial_state)


print("\n===== WORKFLOW COMPLETED =====\n")

print("STATUS:")
print(result.get("status"))

print("\n===== SECURITY RESULT =====")
print(result.get("security_result"))

print("\n===== RESEARCH REPORT =====")
print(result.get("research_report"))

print("\n===== FACT CHECK REPORT =====")
print(result.get("fact_check_report"))

print("\n===== ANALYST REPORT =====")
print(result.get("analyst_report"))

print("\n===== FINAL DECISION =====")
print(result.get("decision"))