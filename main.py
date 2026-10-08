from evidence.evidence_collector import EvidenceCollector
from evidence.evidence_ranker import EvidenceRanker
from decision.secure_decision_engine import SecureDecisionEngine
from workflow.workflow_orchestrator import WorkflowOrchestrator


def run_system(query):

    print("\n==========================================")
    print("SECURE MULTI-AGENT AI SYSTEM")
    print("==========================================")

    # --------------------------------------
    # 1. Evidence Collection
    # --------------------------------------

    collector = EvidenceCollector()

    evidence = collector.collect(
        source_title="Secure AI Research Source",
        claim="Validated evidence supports reliable AI decisions.",
        snippet="Reliable evidence should be collected and validated before decision making.",
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

    print("\n[Evidence]")
    print("Evidence ID:", evidence.evidence_id)
    print("Reliability:", evidence.reliability_score)

    # --------------------------------------
    # 2. Evidence Ranking
    # --------------------------------------

    ranker = EvidenceRanker()

    ranked_evidence = ranker.top_k(
        [evidence_data],
        query,
        k=1
    )

    print("\n[Ranking]")
    print("Top Evidence:", ranked_evidence[0]["evidence_id"])
    print("Score:", ranked_evidence[0]["final_score"])

    # --------------------------------------
    # 3. Secure Decision
    # --------------------------------------

    decision_engine = SecureDecisionEngine()

    decision = decision_engine.evaluate(
        confidence_score=0.90,
        evidence_list=ranked_evidence
    )

    print("\n[Secure Decision]")
    print("Status:", decision["status"])
    print("Confidence:", decision["confidence_level"])
    print("Risk:", decision["risk_level"])

    # --------------------------------------
    # 4. Multi-Agent Workflow
    # --------------------------------------

    orchestrator = WorkflowOrchestrator()

    orchestrator.register_agents()

    workflow_id = "MAIN-WORKFLOW-001"

    orchestrator.create_workflow(
        workflow_id
    )

    orchestrator.start_research(
        workflow_id,
        query
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

    print("\n[Workflow]")
    print("Workflow ID:", state.workflow_id)
    print("Final Stage:", state.current_stage)
    print("Final Status:", state.status)

    # --------------------------------------
    # 5. Final Result
    # --------------------------------------

    print("\n==========================================")

    if (
        decision["allowed"]
        and completion["success"]
        and state.current_stage == "completed"
    ):

        print("FINAL RESULT: APPROVED")
        print("System completed successfully.")

    else:

        print("FINAL RESULT: BLOCKED")
        print("System stopped for safety reasons.")

    print("==========================================")

    return {
        "workflow_id": workflow_id,
        "decision": decision,
        "workflow_state": state,
        "completion": completion
    }


if __name__ == "__main__":

    user_query = input(
        "\nEnter your research query: "
    )

    if not user_query.strip():

        print(
            "\nQuery cannot be empty."
        )

    else:

        run_system(
            user_query
        )