from security.output_guard import validate_agent_output


safe_output = "AI can improve cybersecurity through automated threat detection."

sensitive_output = "API_KEY=demo_secret_value_12345"


print("SAFE OUTPUT:")
print(validate_agent_output(safe_output))

print("\nSENSITIVE OUTPUT:")
print(validate_agent_output(sensitive_output))