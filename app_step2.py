import html
import re
import json
import os
from datetime import datetime

import streamlit as st

from core.orchestrator import build_workflow


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Secure Multi-Agent AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# HISTORY CONFIG
# =========================================================

HISTORY_FILE = "data/history.json"


def ensure_history_file():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)


def load_history():
    ensure_history_file()

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            return data

        return []

    except (json.JSONDecodeError, OSError):
        return []


def save_history_entry(query, result, decision=""):
    history = load_history()

    security = result.get("security_result", {})
    risk = security.get("risk_level", "UNKNOWN")
    workflow_status = result.get("status", "UNKNOWN")
    workflow_id = result.get("workflow_id", "N/A")

    confidence_match = re.search(
        r"CONFIDENCE:\s*(HIGH|MEDIUM|LOW)",
        str(decision),
        re.IGNORECASE,
    )

    if confidence_match:
        confidence = confidence_match.group(1).upper()
    else:
        confidence = "NOT SPECIFIED"

    history_entry = {
        "history_id": f"HIST-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "status": workflow_status,
        "risk_level": risk,
        "confidence": confidence,
        "workflow_id": workflow_id,
        "decision": str(decision),
    }

    history.insert(0, history_entry)
    history = history[:50]

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

    return history_entry


def clear_history():
    ensure_history_file()

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, indent=4)


# =========================================================
# PREMIUM RESPONSIVE THEME
# =========================================================

st.html(
    """
    <style>

    /* =====================================================
       THEME VARIABLES
       ===================================================== */

    :root {
        --bg: #f6f7fb;
        --surface: rgba(255,255,255,0.88);
        --surface-solid: #ffffff;
        --surface-soft: #f0f2f8;

        --text: #172033;
        --text-secondary: #5f697b;
        --text-muted: #7b8495;

        --border: rgba(79,70,229,0.13);

        --indigo: #4f46e5;
        --violet: #7c3aed;
        --blue: #2563eb;
        --green: #059669;
        --amber: #d97706;

        --shadow: rgba(15,23,42,0.08);
    }


    /* =====================================================
       DARK MODE
       ===================================================== */

    @media (prefers-color-scheme: dark) {

        :root {
            --bg: #111827;
            --surface: rgba(23,28,42,0.90);
            --surface-solid: #171c2a;
            --surface-soft: #202638;

            --text: #f1f5f9;
            --text-secondary: #c3ccda;
            --text-muted: #929daf;

            --border: rgba(129,140,248,0.18);

            --indigo: #818cf8;
            --violet: #a78bfa;
            --blue: #60a5fa;
            --green: #34d399;
            --amber: #fbbf24;

            --shadow: rgba(0,0,0,0.28);
        }
    }


    /* =====================================================
       APP BACKGROUND
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 8% 8%,
                rgba(37,99,235,0.22),
                transparent 30%
            ),
            radial-gradient(
                circle at 92% 12%,
                rgba(124,58,237,0.20),
                transparent 32%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(79,70,229,0.14),
                transparent 38%
            ),
            var(--bg) !important;
    }


    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(
                circle at 8% 8%,
                rgba(37,99,235,0.22),
                transparent 30%
            ),
            radial-gradient(
                circle at 92% 12%,
                rgba(124,58,237,0.20),
                transparent 32%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(79,70,229,0.14),
                transparent 38%
            ),
            var(--bg) !important;
    }


    [data-testid="stMain"] {
        background: transparent !important;
    }


    [data-testid="stHeader"] {
        background: transparent !important;
    }


    .block-container {
        max-width: 1280px;
        padding-top: 1.8rem;
        padding-bottom: 4rem;
    }


    /* =====================================================
       HERO
       ===================================================== */

    .premium-hero {
        position: relative;
        overflow: hidden;

        padding: 2.7rem 2.8rem;

        border-radius: 28px;

        background:
            linear-gradient(
                115deg,
                rgba(30,27,75,0.98) 0%,
                rgba(67,56,202,0.94) 46%,
                rgba(124,58,237,0.80) 100%
            );

        border: 1px solid rgba(255,255,255,0.14);

        box-shadow:
            0 22px 55px rgba(49,46,129,0.20);

        margin-bottom: 1.7rem;
    }


    .premium-hero::before {
        content: "";

        position: absolute;

        width: 420px;
        height: 420px;

        right: -170px;
        top: -220px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(255,255,255,0.14),
                transparent 68%
            );

        pointer-events: none;
    }


    .hero-badge {
        display: inline-block;

        padding: 6px 12px;

        border-radius: 999px;

        background: rgba(255,255,255,0.11);

        border: 1px solid rgba(255,255,255,0.18);

        color: rgba(255,255,255,0.90);

        font-size: 0.72rem;

        font-weight: 700;

        letter-spacing: 0.7px;
    }


    .hero-title {
        margin-top: 14px;

        color: #ffffff;

        font-size: 2.7rem;

        line-height: 1.08;

        font-weight: 850;

        letter-spacing: -1.3px;
    }


    .hero-title-gradient {
        background:
            linear-gradient(
                90deg,
                #ffffff 0%,
                #e0e7ff 48%,
                #ddd6fe 100%
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }


    .hero-description {
        margin-top: 13px;

        max-width: 850px;

        color: rgba(255,255,255,0.78);

        font-size: 0.98rem;

        line-height: 1.65;
    }


    /* =====================================================
       PIPELINE
       ===================================================== */

    .pipeline-wrap {
        display: flex;

        align-items: center;

        justify-content: center;

        gap: 8px;

        margin: 1.2rem 0 2rem;

        flex-wrap: wrap;
    }


    .pipeline-node {
        display: flex;

        align-items: center;

        gap: 7px;

        padding: 8px 13px;

        border-radius: 999px;

        background: var(--surface);

        border: 1px solid var(--border);

        box-shadow: 0 5px 16px var(--shadow);

        color: var(--text);

        font-size: 0.78rem;

        font-weight: 700;
    }


    .pipeline-dot {
        width: 8px;
        height: 8px;

        border-radius: 50%;

        background:
            linear-gradient(
                135deg,
                var(--indigo),
                var(--violet)
            );
    }


    .pipeline-arrow {
        color: var(--text-muted);

        font-size: 0.75rem;
    }


    /* =====================================================
       SECTION HEADER
       ===================================================== */

    .section-header {
        display: flex;

        align-items: center;

        gap: 9px;

        margin-top: 1.4rem;

        margin-bottom: 0.65rem;
    }


    .section-icon {
        color: var(--indigo);

        font-size: 1.1rem;
    }


    .section-text {
        color: var(--text);

        font-size: 1.18rem;

        font-weight: 780;
    }


    /* =====================================================
       STATUS CARDS
       ===================================================== */

    .metric-card {
        padding: 1.15rem 1.3rem;

        border-radius: 17px;

        background: var(--surface);

        border: 1px solid var(--border);

        box-shadow:
            0 8px 25px var(--shadow);
    }


    .metric-label {
        color: var(--text-muted);

        font-size: 0.70rem;

        font-weight: 750;

        letter-spacing: 0.65px;

        text-transform: uppercase;
    }


    .metric-value {
        color: var(--text);

        font-size: 1.05rem;

        font-weight: 800;

        margin-top: 5px;
    }


    /* =====================================================
       SYSTEM OVERVIEW
       ===================================================== */

    .overview-grid {
        display: grid;

        grid-template-columns:
            repeat(4, minmax(0, 1fr));

        gap: 14px;

        margin:
            1.2rem 0 1.8rem;
    }


    .overview-card {
        padding: 1.15rem 1.25rem;

        border-radius: 18px;

        background: var(--surface);

        border: 1px solid var(--border);

        box-shadow:
            0 8px 25px var(--shadow);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }


    .overview-card:hover {
        transform: translateY(-2px);

        box-shadow:
            0 13px 30px var(--shadow);
    }


    .overview-label {
        color: var(--text-muted);

        font-size: 0.68rem;

        font-weight: 800;

        letter-spacing: 0.65px;

        text-transform: uppercase;
    }


    .overview-value {
        color: var(--text);

        font-size: 1.25rem;

        font-weight: 850;

        margin-top: 5px;
    }


    .overview-subtitle {
        color: var(--text-secondary);

        font-size: 0.72rem;

        margin-top: 3px;
    }


    @media (max-width: 900px) {

        .overview-grid {
            grid-template-columns:
                repeat(2, minmax(0, 1fr));
        }
    }


    @media (max-width: 550px) {

        .overview-grid {
            grid-template-columns:
                1fr;
        }
    }


    /* =====================================================
       DECISION CARD
       ===================================================== */

    .final-card {
        position: relative;

        overflow: hidden;

        padding: 1.7rem;

        border-radius: 22px;

        background:
            linear-gradient(
                135deg,
                rgba(99,102,241,0.13),
                rgba(139,92,246,0.08)
            );

        border: 1px solid rgba(99,102,241,0.23);

        box-shadow:
            0 14px 38px var(--shadow);
    }


    .final-card::after {
        content: "";

        position: absolute;

        width: 180px;
        height: 180px;

        right: -80px;
        bottom: -100px;

        border-radius: 50%;

        background:
            rgba(139,92,246,0.09);

        pointer-events: none;
    }


    .final-label {
        color: var(--indigo);

        font-size: 0.74rem;

        font-weight: 800;

        letter-spacing: 0.7px;

        text-transform: uppercase;
    }


    .final-title {
        color: var(--text);

        font-size: 1.22rem;

        font-weight: 800;

        margin-top: 4px;

        margin-bottom: 12px;
    }


    .final-content {
        color: var(--text);

        line-height: 1.72;

        font-size: 0.96rem;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    [data-testid="stSidebar"] {
        background: var(--surface-solid);

        border-right: 1px solid var(--border);
    }


    [data-testid="stSidebar"] * {
        color: var(--text);
    }


    .side-brand {
        font-size: 1.12rem;

        font-weight: 800;

        color: var(--text);
    }


    .side-description {
        margin-top: 5px;

        color: var(--text-secondary);

        font-size: 0.82rem;

        line-height: 1.5;
    }


    .side-arrow {
        text-align: center;

        color: var(--text-muted);

        font-size: 0.7rem;
    }


    .stack-title {
        color: var(--text);

        font-size: 0.78rem;

        font-weight: 750;

        text-transform: uppercase;

        letter-spacing: 0.6px;
    }


    .stack-text {
        margin-top: 8px;

        color: var(--text-secondary);

        font-size: 0.79rem;

        line-height: 1.8;
    }


    /* =====================================================
       AGENT STATUS
       ===================================================== */

    .agent-status {
        display: flex;

        align-items: center;

        justify-content: space-between;

        gap: 10px;

        padding: 9px 11px;

        margin: 6px 0;

        border-radius: 11px;

        background: var(--surface-soft);

        border: 1px solid var(--border);
    }


    .agent-name {
        display: flex;

        align-items: center;

        gap: 8px;

        color: var(--text);

        font-size: 0.82rem;

        font-weight: 650;
    }


    .agent-status-badge {
        padding: 3px 8px;

        border-radius: 999px;

        background: rgba(5,150,105,0.12);

        border: 1px solid rgba(5,150,105,0.20);

        color: var(--green);

        font-size: 0.62rem;

        font-weight: 800;

        letter-spacing: 0.4px;
    }


    .agent-status-dot {
        width: 7px;
        height: 7px;

        border-radius: 50%;

        background: var(--green);

        box-shadow:
            0 0 0 3px rgba(5,150,105,0.10);
    }


    /* =====================================================
       INPUT
       ===================================================== */

    textarea {
        background: var(--surface-solid) !important;

        color: var(--text) !important;

        border: 1px solid var(--border) !important;

        border-radius: 15px !important;
    }


    textarea::placeholder {
        color: var(--text-muted) !important;
    }


    /* =====================================================
       BUTTON
       ===================================================== */

    .stButton > button {
        min-height: 46px;

        border: none;

        border-radius: 13px;

        background:
            linear-gradient(
                90deg,
                #4f46e5,
                #7c3aed
            );

        color: #ffffff;

        font-weight: 750;

        box-shadow:
            0 9px 25px rgba(79,70,229,0.20);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }


    .stButton > button:hover {
        transform: translateY(-1px);

        box-shadow:
            0 13px 30px rgba(79,70,229,0.28);
    }


    /* =====================================================
       TABS
       ===================================================== */

    button[data-baseweb="tab"] {
        color: var(--text-secondary);
        font-weight: 650;
    }


    button[data-baseweb="tab"][aria-selected="true"] {
        color: var(--indigo);
    }


    /* =====================================================
       EXPANDER
       ===================================================== */

    [data-testid="stExpander"] {
        background: var(--surface);

        border: 1px solid var(--border);

        border-radius: 15px;

        overflow: hidden;
    }

    </style>
    """
)


# =========================================================
# HERO
# =========================================================

st.html(
    """
    <div class="premium-hero">

        <div class="hero-badge">
            ✦ AI RESEARCH • VERIFICATION • DECISION
        </div>

        <div class="hero-title">
            Secure Multi-Agent AI<br>
            <span class="hero-title-gradient">
                Research &amp; Decision System
            </span>
        </div>

        <div class="hero-description">
            An evidence-driven multi-agent intelligence pipeline
            designed to research, verify, analyze and support
            informed decisions.
        </div>

    </div>
    """
)


# =========================================================
# VISUAL PIPELINE
# =========================================================

st.html(
    """
    <div class="pipeline-wrap">

        <div class="pipeline-node">
            <span class="pipeline-dot"></span>
            Security
        </div>

        <div class="pipeline-arrow">→</div>

        <div class="pipeline-node">
            <span class="pipeline-dot"></span>
            Research
        </div>

        <div class="pipeline-arrow">→</div>

        <div class="pipeline-node">
            <span class="pipeline-dot"></span>
            Fact Check
        </div>

        <div class="pipeline-arrow">→</div>

        <div class="pipeline-node">
            <span class="pipeline-dot"></span>
            Analysis
        </div>

        <div class="pipeline-arrow">→</div>

        <div class="pipeline-node">
            <span class="pipeline-dot"></span>
            Decision
        </div>

    </div>
    """
)


# =========================================================
# SYSTEM OVERVIEW
# =========================================================

st.html(
    """
    <div class="section-header">
        <div class="section-icon">◈</div>
        <div class="section-text">
            System Overview
        </div>
    </div>
    """
)


st.html(
    """
    <div class="overview-grid">

        <div class="overview-card">

            <div class="overview-label">
                AI Agents
            </div>

            <div class="overview-value">
                5
            </div>

            <div class="overview-subtitle">
                Multi-Agent Pipeline
            </div>

        </div>


        <div class="overview-card">

            <div class="overview-label">
                Evidence Layer
            </div>

            <div class="overview-value">
                READY
            </div>

            <div class="overview-subtitle">
                Source Verification
            </div>

        </div>


        <div class="overview-card">

            <div class="overview-label">
                Decision Engine
            </div>

            <div class="overview-value">
                ACTIVE
            </div>

            <div class="overview-subtitle">
                Secure Decision Guard
            </div>

        </div>


        <div class="overview-card">

            <div class="overview-label">
                Audit System
            </div>

            <div class="overview-value">
                ACTIVE
            </div>

            <div class="overview-subtitle">
                Trace &amp; Logging
            </div>

        </div>

    </div>
    """
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.html(
        """
        <div class="side-brand">
            ✦ AI Control Center
        </div>

        <div class="side-description">
            Secure multi-agent workflow and system architecture.
        </div>
        """
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🔍 New Research",
            "🕘 History",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    agents = [
        ("🛡️", "Security Agent"),
        ("🔎", "Research Agent"),
        ("✅", "Fact Checker"),
        ("📊", "Analyst Agent"),
        ("🧠", "Decision Agent"),
    ]

    for index, (icon, agent_name) in enumerate(agents):

        st.html(
            f"""
            <div class="agent-status">

                <div class="agent-name">

                    <span class="agent-status-dot"></span>

                    <span>
                        {icon} {agent_name}
                    </span>

                </div>

                <div class="agent-status-badge">
                    READY
                </div>

            </div>
            """
        )

        if index < len(agents) - 1:
            st.html(
                '<div class="side-arrow">↓</div>'
            )

    st.divider()

    st.html(
        """
        <div class="stack-title">
            Technology Stack
        </div>

        <div class="stack-text">
            Gemini 2.5 Flash<br>
            LangGraph<br>
            LangChain<br>
            Tavily Search<br>
            Streamlit
        </div>
        """
    )


# =========================================================
# HISTORY PAGE
# =========================================================

if page == "🕘 History":

    st.html(
        """
        <div class="section-header">
            <div class="section-icon">◷</div>
            <div class="section-text">
                Research History
            </div>
        </div>
        """
    )

    history = load_history()

    if not history:

        st.info(
            "No research history available yet. "
            "Run a research query first."
        )

    else:

        st.write(
            f"Showing the latest {len(history)} research record(s)."
        )

        history_labels = []

        for item in history:

            timestamp = item.get(
                "timestamp",
                "Unknown time",
            )

            query_text = item.get(
                "query",
                "Unknown query",
            )

            history_labels.append(
                f"{timestamp[:19].replace('T', ' ')}  —  "
                f"{query_text[:70]}"
            )

        selected_index = st.selectbox(
            "Select a research record",
            range(len(history)),
            format_func=lambda index: history_labels[index],
        )

        selected = history[selected_index]

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:

            st.html(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        Workflow Status
                    </div>

                    <div class="metric-value">
                        {html.escape(
                            str(
                                selected.get(
                                    "status",
                                    "UNKNOWN"
                                )
                            )
                        )}
                    </div>

                </div>
                """
            )

        with col2:

            st.html(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        Risk Level
                    </div>

                    <div class="metric-value">
                        {html.escape(
                            str(
                                selected.get(
                                    "risk_level",
                                    "UNKNOWN"
                                )
                            )
                        )}
                    </div>

                </div>
                """
            )

        with col3:

            st.html(
                f"""
                <div class="metric-card">

                    <div class="metric-label">
                        Confidence
                    </div>

                    <div class="metric-value">
                        {html.escape(
                            str(
                                selected.get(
                                    "confidence",
                                    "UNKNOWN"
                                )
                            )
                        )}
                    </div>

                </div>
                """
            )

        st.html(
            """
            <div class="section-header">
                <div class="section-icon">⌕</div>
                <div class="section-text">
                    Research Query
                </div>
            </div>
            """
        )

        st.markdown(
            f"**{html.escape(str(selected.get('query', '')))}**"
        )

        st.html(
            """
            <div class="section-header">
                <div class="section-icon">◈</div>
                <div class="section-text">
                    Workflow Information
                </div>
            </div>
            """
        )

        workflow_id = selected.get(
            "workflow_id",
            "N/A",
        )

        timestamp = selected.get(
            "timestamp",
            "N/A",
        )

        st.write(f"**Workflow ID:** {workflow_id}")
        st.write(f"**Executed:** {timestamp}")

        st.html(
            """
            <div class="section-header">
                <div class="section-icon">✦</div>
                <div class="section-text">
                    Final Decision
                </div>
            </div>
            """
        )

        decision = selected.get(
            "decision",
            "No decision available.",
        )

        st.markdown(decision)

        st.divider()

        st.html(
            """
            <div class="section-header">
                <div class="section-icon">⚙</div>
                <div class="section-text">
                    History Management
                </div>
            </div>
            """
        )

        if st.button(
            "🗑️ Clear All History",
            use_container_width=True,
        ):

            clear_history()

            st.success(
                "Research history cleared successfully."
            )

            st.rerun()


# =========================================================
# NEW RESEARCH PAGE
# =========================================================

else:

    st.html(
        """
        <div class="section-header">
            <div class="section-icon">⌕</div>
            <div class="section-text">
                Research Query
            </div>
        </div>
        """
    )


    query = st.text_area(
        "Research question",
        placeholder=(
            "Ask a research question, for example: "
            "What are the major benefits and risks of "
            "multi-agent AI systems in business?"
        ),
        height=125,
        label_visibility="collapsed",
    )


    run_button = st.button(
        "✦  Run Multi-Agent Research",
        use_container_width=True,
    )


    # =====================================================
    # EXECUTE WORKFLOW
    # =====================================================

    if run_button:

        if not query.strip():

            st.warning(
                "Please enter a research question first."
            )

        else:

            with st.spinner(
                "Running Security → Research → "
                "Fact Check → Analysis → Decision..."
            ):

                workflow = build_workflow()

                initial_state = {
                    "query": query,
                    "status": "STARTED",
                    "error": "",
                }

                try:

                    result = workflow.invoke(
                        initial_state
                    )

                except Exception:

                    st.error(
                        "⚠️ The AI workflow could not be completed."
                    )

                    st.info(
                        "Please check your API configuration "
                        "or try again later."
                    )

                    st.stop()

            if result.get("status") == "ERROR":

                st.error(
                    "⚠️ Workflow stopped safely."
                )

                error_message = result.get(
                    "error",
                    "An unexpected error occurred.",
                )

                st.warning(error_message)

                save_history_entry(
                    query=query,
                    result=result,
                    decision=error_message,
                )

                st.stop()


            if result.get("status") == "BLOCK":

                st.warning(
                    "🛡️ Request blocked by the security layer."
                )

            else:

                st.success(
                    "✓ Multi-Agent workflow completed successfully."
                )


            # =================================================
            # STATUS
            # =================================================

            st.html(
                """
                <div class="section-header">
                    <div class="section-icon">◈</div>
                    <div class="section-text">
                        System Status
                    </div>
                </div>
                """
            )

            security = result.get(
                "security_result",
                {},
            )

            risk = security.get(
                "risk_level",
                "UNKNOWN",
            )

            workflow_status = result.get(
                "status",
                "UNKNOWN",
            )

            col1, col2 = st.columns(2)

            with col1:

                st.html(
                    f"""
                    <div class="metric-card">

                        <div class="metric-label">
                            Security Risk
                        </div>

                        <div class="metric-value">
                            {html.escape(str(risk))}
                        </div>

                    </div>
                    """
                )

            with col2:

                st.html(
                    f"""
                    <div class="metric-card">

                        <div class="metric-label">
                            Workflow Status
                        </div>

                        <div class="metric-value">
                            {html.escape(
                                str(workflow_status)
                            )}
                        </div>

                    </div>
                    """
                )


            # =================================================
            # AGENT OUTPUT TABS
            # =================================================

            st.html(
                """
                <div class="section-header">
                    <div class="section-icon">◇</div>
                    <div class="section-text">
                        Agent Intelligence
                    </div>
                </div>
                """
            )

            tab_research, tab_fact, tab_analysis = st.tabs(
                [
                    "🔎 Research",
                    "✓ Fact Check",
                    "◈ Analysis",
                ]
            )


            with tab_research:

                research_report = result.get(
                    "research_report",
                    "No research report available.",
                )

                st.markdown(research_report)


            with tab_fact:

                fact_check = result.get(
                    "fact_check_report",
                    "No fact-check report available.",
                )

                st.markdown(fact_check)


            with tab_analysis:

                analyst = result.get(
                    "analyst_report",
                    "No analyst report available.",
                )

                st.markdown(analyst)


            # =================================================
            # FINAL DECISION
            # =================================================

            st.html(
                """
                <div class="section-header">
                    <div class="section-icon">✦</div>
                    <div class="section-text">
                        Final Decision
                    </div>
                </div>
                """
            )

            decision = result.get(
                "decision",
                "No final decision available.",
            )

            safe_decision = (
                html.escape(str(decision))
                .replace("\n", "<br>")
            )

            confidence_match = re.search(
                r"CONFIDENCE:\s*(HIGH|MEDIUM|LOW)",
                str(decision),
                re.IGNORECASE,
            )

            if confidence_match:

                confidence = (
                    confidence_match.group(1)
                    .upper()
                )

            else:

                confidence = "NOT SPECIFIED"


            st.html(
                f"""
                <div class="final-card">

                    <div class="final-label">
                        ✦ AI DECISION
                    </div>

                    <div class="final-title">
                        Evidence-Based Recommendation
                    </div>

                    <div class="final-content">
                        {safe_decision}
                    </div>

                    <br>

                    <div class="metric-label">
                        Confidence
                    </div>

                    <div class="metric-value">
                        {html.escape(confidence)}
                    </div>

                </div>
                """
            )


            # =================================================
            # SAVE TO HISTORY
            # =================================================

            save_history_entry(
                query=query,
                result=result,
                decision=decision,
            )

            st.info(
                "🕘 This research result has been saved to History."
            )
