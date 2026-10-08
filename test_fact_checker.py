from agents.fact_checker_agent import fact_check_claims


claims = """
Multi-agent AI systems can improve reliability through
specialized agents and peer verification.

Multi-agent systems can also introduce coordination,
security, and communication risks.
"""


sources = """
SOURCE 1:
Multi-agent systems can divide complex tasks among
specialized agents and allow independent verification.

SOURCE 2:
Multi-agent systems may experience coordination failures,
communication overhead, and security vulnerabilities.

SOURCE 3:
Multiple interacting AI agents can produce unexpected
behaviors and require additional safeguards.
"""


result = fact_check_claims(claims, sources)

print("\n===== FACT CHECKER REPORT =====\n")
print(result)