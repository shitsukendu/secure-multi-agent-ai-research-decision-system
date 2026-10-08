from agents.analyst_agent import analyze_research


research_report = """
Multi-agent AI systems can improve problem-solving through
specialized agents, parallel processing, scalability,
and independent task execution.

However, multi-agent systems can also introduce security
risks, coordination problems, communication overhead,
unexpected behavior, and increased complexity.
"""


fact_check_report = """
CLAIM 1:
Status: Supported
Evidence: Specialized agents can divide complex tasks.
Source: Source 1

CLAIM 2:
Status: Supported
Evidence: Multi-agent systems can introduce coordination
and security risks.
Source: Source 2

CLAIM 3:
Status: Partially Supported
Evidence: Parallel execution can improve efficiency, but
the exact performance improvement depends on system design.
Source: Source 3
"""


result = analyze_research(
    research_report,
    fact_check_report,
)

print("\n===== ANALYST REPORT =====\n")
print(result)