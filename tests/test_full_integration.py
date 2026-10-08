from evidence.evidence_collector import EvidenceCollector
from evidence.evidence_ranker import EvidenceRanker
from decision.secure_decision_engine import SecureDecisionEngine
from coordination.coordination_engine import CoordinationEngine
from workflow.workflow_orchestrator import WorkflowOrchestrator


print("\n======================================")
print("FULL SYSTEM INTEGRATION TEST")
print("======================================")


# =====================================
# 1. Evidence Layer
# =====================================

collector = EvidenceCollector()

evidence = collector.collect(
    source_title="AI Security Research Paper",
    claim="Secure AI systems should use validated evidence.",
    snippet="Validated evidence improves decision reliability.",
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

print("\n[1] Evidence Layer")

print(
    "Evidence:",
    evidence_data["evidence_id"]
)

print(
    "Reliability:",
    evidence_data["reliability_score"]
)


# =====================================
# 2. Evidence Ranking
# =====================================

ranker = EvidenceRanker()

ranked_evidence = ranker.top_k(
    [evidence_data],
    "secure AI evidence",
    k=1
)

print("\n[2] Evidence Ranking")

print(
    "Top Evidence:",
    ranked_evidence[0]["evidence_id"]
)

print(
    "Final Score:",
    ranked_evidence[0]["final_score"]
)


# =====================================
# 3. Secure Decision Layer
# =====================================

decision_engine = SecureDecisionEngine()

decision_result = decision_engine.evaluate(
    confidence_score=0.90,
    evidence_list=ranked_evidence
)

print("\n[3] Secure Decision Layer")

print(
    "Status:",
    decision_result["status"]
)

print(
    "Risk:",
    decision_result["risk_level"]
)


# =====================================
# 4. Multi-Agent Coordination
# =====================================

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
    "Prepare decision.",
    "DecisionAgent",
    "low"
)

print("\n[4] Multi-Agent Coordination")

print(
    "Research Task:",
    research_task["task_id"]
)

print(
    "Validation Task:",
    validation_task["task_id"]
)

print(
    "Decision Task:",
    decision_task["task_id"]
)


# =====================================
# 5. Workflow Orchestration
# =====================================

orchestrator = WorkflowOrchestrator()

orchestrator.register_agents()

workflow_id = "INTEGRATION-001"

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

print("\n[5] Workflow Orchestration")

print(
    "Workflow:",
    state.workflow_id
)

print(
    "Final Stage:",
    state.current_stage
)

print(
    "Final Status:",
    state.status
)


# =====================================
# 6. Final Verification
# =====================================

if (
    evidence_data["reliability_score"] >= 0.90
    and len(ranked_evidence) == 1
    and decision_result["status"] == "APPROVED"
    and decision_result["risk_level"] == "LOW"
    and research_task["agent_name"] == "ResearchAgent"
    and validation_task["agent_name"] == "ValidationAgent"
    and decision_task["agent_name"] == "DecisionAgent"
    and completion["success"]
    and state.current_stage == "completed"
    and state.status == "completed"
):

    print("\n======================================")
    print("FULL SYSTEM INTEGRATION TEST OK")
    print("======================================")

else:

    print("\n======================================")
    print("FULL SYSTEM INTEGRATION TEST FAILED")
    print("======================================")