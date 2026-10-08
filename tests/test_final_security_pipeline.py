from evidence.evidence_collector import EvidenceCollector
from evidence.evidence_ranker import EvidenceRanker
from decision.secure_decision_engine import SecureDecisionEngine
from coordination.coordination_engine import CoordinationEngine
from workflow.workflow_orchestrator import WorkflowOrchestrator


print("\n==========================================")
print("FINAL END-TO-END SECURITY TEST")
print("==========================================")


# ==========================================
# 1. Evidence Collection
# ==========================================

collector = EvidenceCollector()

evidence = collector.collect(
    source_title="Secure AI Research",
    claim="Validated evidence supports secure AI decisions.",
    snippet="Reliable evidence should be validated before decision making.",
    source_type="research_paper",
    agent_name="ResearchAgent"
)

evidence_data = {
    "evidence_id": evidence.evidence_id,
    "source_title": evidence.source_title,
    "claim": evidence.claim,
    "snippet": evidence.snippet,
    "reliability_score": evidence.reliability_score
}


print("\n[1] Evidence Collection")
print("Evidence ID:", evidence.evidence_id)
print("Reliability:", evidence.reliability_score)


# ==========================================
# 2. Evidence Ranking
# ==========================================

ranker = EvidenceRanker()

ranked = ranker.top_k(
    [evidence_data],
    "secure AI evidence",
    k=1
)


print("\n[2] Evidence Ranking")
print("Ranked Evidence:", len(ranked))
print("Score:", ranked[0]["final_score"])


# ==========================================
# 3. Secure Decision
# ==========================================

decision_engine = SecureDecisionEngine()

decision = decision_engine.evaluate(
    confidence_score=0.90,
    evidence_list=ranked
)


print("\n[3] Secure Decision")
print("Status:", decision["status"])
print("Risk:", decision["risk_level"])
print("Confidence:", decision["confidence_level"])


# ==========================================
# 4. Multi-Agent Coordination
# ==========================================

coordination = CoordinationEngine()

coordination.register_agent(
    "ResearchAgent",
    "Research",
    "Collects research evidence."
)

coordination.register_agent(
    "ValidationAgent",
    "Validation",
    "Validates evidence."
)

coordination.register_agent(
    "DecisionAgent",
    "Decision",
    "Produces secure decisions."
)


research_task = coordination.assign_task(
    "Collect evidence.",
    "ResearchAgent",
    "high"
)

validation_task = coordination.assign_task(
    "Validate evidence.",
    "ValidationAgent",
    "normal"
)

decision_task = coordination.assign_task(
    "Prepare secure decision.",
    "DecisionAgent",
    "low"
)


print("\n[4] Multi-Agent Coordination")
print("Research:", research_task["agent_name"])
print("Validation:", validation_task["agent_name"])
print("Decision:", decision_task["agent_name"])


# ==========================================
# 5. Workflow Orchestration
# ==========================================

orchestrator = WorkflowOrchestrator()

orchestrator.register_agents()

workflow_id = "SECURITY-FINAL-001"

orchestrator.create_workflow(
    workflow_id
)

orchestrator.start_research(
    workflow_id,
    "Research secure AI evidence."
)

orchestrator.start_validation(
    workflow_id
)

orchestrator.start_decision(
    workflow_id
)

completion = orchestrator.complete_workflow(
    workflow_id
)

state = orchestrator.get_workflow_state(
    workflow_id
)


print("\n[5] Workflow")
print("Workflow ID:", state.workflow_id)
print("Final Stage:", state.current_stage)
print("Final Status:", state.status)


# ==========================================
# 6. Security Verification
# ==========================================

security_passed = (
    decision["allowed"]
    and decision["status"] == "APPROVED"
    and decision["risk_level"] == "LOW"
    and decision["confidence_level"] == "HIGH"
)


print("\n[6] Security Verification")
print("Security Passed:", security_passed)


# ==========================================
# 7. Final Verification
# ==========================================

if (
    evidence.reliability_score >= 0.90
    and len(ranked) == 1
    and decision["allowed"]
    and decision["status"] == "APPROVED"
    and decision["risk_level"] == "LOW"
    and research_task["agent_name"] == "ResearchAgent"
    and validation_task["agent_name"] == "ValidationAgent"
    and decision_task["agent_name"] == "DecisionAgent"
    and completion["success"]
    and state.current_stage == "completed"
    and state.status == "completed"
    and security_passed
):

    print("\n==========================================")
    print("FINAL END-TO-END SECURITY TEST OK")
    print("==========================================")

else:

    print("\n==========================================")
    print("FINAL END-TO-END SECURITY TEST FAILED")
    print("==========================================")