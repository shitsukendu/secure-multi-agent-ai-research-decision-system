from agents.decision_agent import make_decision


research_report = """
Multi-agent AI systems can improve task decomposition,
parallel processing, and specialized reasoning.

However, they may introduce additional complexity,
coordination problems, security risks, and higher
computational costs.
"""

fact_check_report = """
CLAIM 1:
Claim: Multi-agent systems can improve task decomposition.
Status: Supported.
Evidence: The research sources describe specialized
agents working on different subtasks.
Source: Source 1

CLAIM 2:
Claim: Multi-agent systems can introduce security risks.
Status: Supported.
Evidence: The sources identify prompt injection,
tool misuse, and coordination risks.
Source: Source 2
"""

analyst_report = """
KEY FINDINGS:
- Multi-agent systems can improve task specialization.
- Security and coordination are important concerns.
- The benefits depend on proper system design.

EVIDENCE QUALITY:
- Strong: Task specialization benefits.
- Moderate: Security considerations.
- Weak or Uncertain: Exact performance improvements.

MAJOR RISKS:
- Prompt injection.
- Tool misuse.
- Increased system complexity.

OPPORTUNITIES:
- Better task decomposition.
- Specialized agent workflows.
- Evidence-based decision support.

CONFLICTS OR UNCERTAINTIES:
- Performance improvements vary by implementation.

ANALYST SUMMARY:
Multi-agent AI can provide meaningful benefits when
specialized agents are coordinated with appropriate
security controls and evidence validation.
"""


result = make_decision(
    research_report,
    fact_check_report,
    analyst_report,
)

print("\n===== FINAL DECISION =====\n")
print(result)