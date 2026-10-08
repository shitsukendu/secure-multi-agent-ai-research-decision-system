from agents.research_agent import research_agent


query = "What are the major benefits and risks of multi-agent AI systems?"

result = research_agent(query)

print("\n===== SOURCE-BACKED RESEARCH REPORT =====\n")
print(result)