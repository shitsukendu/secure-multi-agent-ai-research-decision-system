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
# STEP 3 — EVIDENCE & CONFIDENCE HELPERS
# =========================================================

def _first_present(mapping, keys, default=None):
    """Return the first non-empty value found for any key."""
    if not isinstance(mapping, dict):
        return default

    for key in keys:
        value = mapping.get(key)
        if value not in (None, "", [], {}):
            return value

    return default


def extract_evidence(result):
    """
    Read evidence/source information from the workflow result without
    changing the backend. Supports several common result key names so
    the UI remains compatible with the existing orchestrator.
    """
    candidates = [
        result.get("evidence"),
        result.get("evidence_list"),
        result.get("sources"),
        result.get("citations"),
        result.get("evidence_items"),
        result.get("source_evidence"),
    ]

    raw = next(
        (item for item in candidates if item not in (None, "", [], {})),
        [],
    )

    if isinstance(raw, dict):
        # Common wrappers such as {"items": [...]} or {"sources": [...]}
        raw = _first_present(
            raw,
            ["items", "evidence", "sources", "citations", "results"],
            [],
        )

    if isinstance(raw, str):
        return [{
            "title": "Evidence",
            "claim": raw,
            "snippet": raw,
        }]

    if not isinstance(raw, list):
        return []

    normalized = []

    for index, item in enumerate(raw, start=1):
        if isinstance(item, str):
            normalized.append({
                "title": f"Source {index}",
                "claim": item,
                "snippet": item,
                "url": "",
                "reliability": None,
                "score": None,
            })
            continue

        if not isinstance(item, dict):
            continue

        title = _first_present(
            item,
            ["source_title", "title", "source", "name", "source_name"],
            f"Source {index}",
        )

        claim = _first_present(
            item,
            ["claim", "statement", "description", "summary"],
            "",
        )

        snippet = _first_present(
            item,
            ["snippet", "text", "excerpt", "content"],
            "",
        )

        url = _first_present(
            item,
            ["source_url", "url", "link"],
            "",
        )

        reliability = _first_present(
            item,
            ["reliability_score", "reliability", "source_reliability"],
            None,
        )

        score = _first_present(
            item,
            ["final_score", "relevance_score", "score"],
            None,
        )

        normalized.append({
            "title": str(title),
            "claim": str(claim),
            "snippet": str(snippet),
            "url": str(url),
            "reliability": reliability,
            "score": score,
        })

    return normalized


def parse_confidence(decision_text, result):
    """Convert the workflow confidence into a stable numeric score."""
    decision_text = str(decision_text or "")

    numeric = _first_present(
        result,
        ["confidence_score", "decision_confidence", "confidence"],
        None,
    )

    if isinstance(numeric, (int, float)):
        value = float(numeric)
        if value > 1:
            value = value / 100
        return max(0.0, min(1.0, value)), (
            "HIGH" if value >= 0.85 else
            "MEDIUM" if value >= 0.70 else
            "LOW"
        )

    match = re.search(
        r"CONFIDENCE(?:\s*SCORE)?\s*[:=-]\s*([0-9]+(?:\.[0-9]+)?)\s*%?",
        decision_text,
        re.IGNORECASE,
    )

    if match:
        value = float(match.group(1))
        if value > 1:
            value /= 100
        level = (
            "HIGH" if value >= 0.85 else
            "MEDIUM" if value >= 0.70 else
            "LOW"
        )
        return max(0.0, min(1.0, value)), level

    match = re.search(
        r"CONFIDENCE\s*[:=-]\s*(HIGH|MEDIUM|LOW)",
        decision_text,
        re.IGNORECASE,
    )

    if match:
        level = match.group(1).upper()
        value = {
            "HIGH": 0.90,
            "MEDIUM": 0.75,
            "LOW": 0.40,
        }[level]
        return value, level

    # Optional backend security result.
    security = result.get("security_result", {})
    security_confidence = _first_present(
        security,
        ["confidence_score", "confidence"],
        None,
    )

    if isinstance(security_confidence, (int, float)):
        value = float(security_confidence)
        if value > 1:
            value /= 100
        level = (
            "HIGH" if value >= 0.85 else
            "MEDIUM" if value >= 0.70 else
            "LOW"
        )
        return max(0.0, min(1.0, value)), level

    return None, "NOT SPECIFIED"


def confidence_color(level):
    if level == "HIGH":
        return "var(--green)"
    if level == "MEDIUM":
        return "var(--amber)"
    if level == "LOW":
        return "#ef4444"
    return "var(--text-muted)"


def confidence_description(level):
    descriptions = {
        "HIGH": "Strong confidence based on the available analysis.",
        "MEDIUM": "Moderate confidence — review supporting evidence.",
        "LOW": "Low confidence — additional verification is recommended.",
        "NOT SPECIFIED": "The workflow did not return a numeric confidence score.",
    }
    return descriptions.get(level, descriptions["NOT SPECIFIED"])


def evidence_count_text(evidence):
    count = len(evidence)
    if count == 0:
        return "No structured evidence returned by the workflow."
    return f"{count} evidence item(s) available for review."




# =========================================================
# STEP 4 — ADVANCED DECISION DASHBOARD HELPERS
# =========================================================

def get_security_result(result):
    security = result.get("security_result", {})
    return security if isinstance(security, dict) else {}


def normalize_percent(value):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None

    if number <= 1:
        number *= 100

    return max(0.0, min(100.0, number))


def get_risk_level(result):
    security = get_security_result(result)

    risk = _first_present(
        security,
        ["risk_level", "risk", "risk_status"],
        None,
    )

    if risk is None:
        risk = _first_present(
            result,
            ["risk_level", "risk", "risk_status"],
            None,
        )

    return str(risk).upper() if risk else "NOT SPECIFIED"


def risk_visual(level):
    level = str(level).upper()

    if level == "LOW":
        return (
            "LOW",
            "var(--green)",
            25,
            "Risk controls indicate a low-risk decision.",
        )

    if level == "MEDIUM":
        return (
            "MEDIUM",
            "var(--amber)",
            60,
            "Moderate risk detected — review the supporting evidence.",
        )

    if level == "HIGH":
        return (
            "HIGH",
            "#ef4444",
            90,
            "High risk detected — additional verification is recommended.",
        )

    return (
        "NOT SPECIFIED",
        "var(--text-muted)",
        0,
        "The workflow did not return a structured risk level.",
    )


def get_security_status(result):
    security = get_security_result(result)

    status = _first_present(
        security,
        ["status", "security_status", "guard_status"],
        None,
    )

    allowed = _first_present(
        security,
        ["allowed", "approved"],
        None,
    )

    if isinstance(allowed, bool):
        return "SECURE" if allowed else "BLOCKED"

    if status:
        status = str(status).upper()

        if status in {
            "APPROVED",
            "ALLOWED",
            "SECURE",
            "PASS",
            "PASSED",
        }:
            return "SECURE"

        if status in {
            "BLOCKED",
            "DENIED",
            "FAIL",
            "FAILED",
        }:
            return "BLOCKED"

        return status

    return "ACTIVE"


def security_visual(status):
    status = str(status).upper()

    if status in {
        "SECURE",
        "APPROVED",
        "ALLOWED",
        "PASS",
        "PASSED",
        "ACTIVE",
    }:
        return "SECURE", "var(--green)"

    if status in {"BLOCKED", "DENIED", "FAIL", "FAILED"}:
        return "BLOCKED", "#ef4444"

    return status, "var(--amber)"


def calculate_reliability_percent(evidence_items):
    values = []

    for item in evidence_items:
        value = item.get("reliability")

        if isinstance(value, (int, float)):
            normalized = normalize_percent(value)

            if normalized is not None:
                values.append(normalized)

        elif isinstance(value, str):
            try:
                normalized = normalize_percent(
                    float(value.strip().replace("%", ""))
                )

                if normalized is not None:
                    values.append(normalized)

            except ValueError:
                pass

    if not values:
        return None

    return sum(values) / len(values)


def get_agent_activity(result):
    candidates = [
        result.get("agents"),
        result.get("agent_status"),
        result.get("agent_states"),
        result.get("agent_activity"),
    ]

    raw = next(
        (
            item
            for item in candidates
            if item not in (None, "", [], {})
        ),
        None,
    )

    default_agents = [
        ("Security Agent", "READY"),
        ("Research Agent", "READY"),
        ("Fact Checker", "READY"),
        ("Analyst Agent", "READY"),
        ("Decision Agent", "READY"),
    ]

    if raw is None:
        return default_agents

    if isinstance(raw, dict):
        items = []

        for name, value in raw.items():
            if isinstance(value, dict):
                status = _first_present(
                    value,
                    ["status", "state", "activity"],
                    "READY",
                )
            else:
                status = value

            items.append((str(name), str(status).upper()))

        return items or default_agents

    if isinstance(raw, list):
        items = []

        for item in raw:
            if isinstance(item, dict):
                name = _first_present(
                    item,
                    ["agent_name", "name", "agent"],
                    "Agent",
                )

                status = _first_present(
                    item,
                    ["status", "state", "activity"],
                    "READY",
                )

                items.append((str(name), str(status).upper()))

        return items or default_agents

    return default_agents


def activity_color(status):
    status = str(status).upper()

    if status in {
        "READY",
        "ACTIVE",
        "RUNNING",
        "COMPLETED",
        "DONE",
        "SUCCESS",
        "PASSED",
    }:
        return "var(--green)"

    if status in {"BLOCKED", "FAILED", "ERROR"}:
        return "#ef4444"

    return "var(--amber)"


def calculate_system_health(
    security_status,
    confidence_value,
    risk_level,
    evidence_items,
):
    points = 0.0
    total = 4.0

    security = str(security_status).upper()

    if security in {
        "SECURE",
        "APPROVED",
        "ALLOWED",
        "ACTIVE",
    }:
        points += 1
    elif security not in {"BLOCKED", "DENIED"}:
        points += 0.5

    if confidence_value is not None:
        points += 1 if confidence_value >= 0.70 else 0.5

    if evidence_items:
        points += 1

    risk = str(risk_level).upper()

    if risk == "LOW":
        points += 1
    elif risk == "MEDIUM":
        points += 0.5

    return round((points / total) * 100)


def health_visual(score):
    if score >= 85:
        return "HEALTHY", "var(--green)"

    if score >= 65:
        return "STABLE", "var(--amber)"

    return "REVIEW", "#ef4444"


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
       STEP 3 — EVIDENCE & CONFIDENCE
       ===================================================== */

    .evidence-summary {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 14px;
        margin: 1rem 0 1.2rem;
    }

    .evidence-card {
        padding: 1.15rem 1.25rem;
        border-radius: 18px;
        background: var(--surface);
        border: 1px solid var(--border);
        box-shadow: 0 8px 25px var(--shadow);
    }

    .evidence-title {
        color: var(--text);
        font-size: 0.96rem;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .evidence-meta {
        color: var(--text-muted);
        font-size: 0.72rem;
        line-height: 1.55;
    }

    .evidence-score {
        color: var(--indigo);
        font-size: 0.78rem;
        font-weight: 800;
        margin-top: 8px;
    }

    .source-link {
        color: var(--blue);
        font-size: 0.74rem;
        font-weight: 700;
        word-break: break-all;
        text-decoration: none;
    }

    .confidence-panel {
        padding: 1.45rem 1.5rem;
        border-radius: 20px;
        background:
            linear-gradient(
                135deg,
                rgba(37,99,235,0.09),
                rgba(124,58,237,0.08)
            );
        border: 1px solid var(--border);
        box-shadow: 0 12px 32px var(--shadow);
    }

    .confidence-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 10px;
    }

    .confidence-level {
        font-size: 1rem;
        font-weight: 850;
        letter-spacing: 0.4px;
    }

    .confidence-percent {
        color: var(--text);
        font-size: 1.35rem;
        font-weight: 850;
    }

    .confidence-track {
        width: 100%;
        height: 11px;
        overflow: hidden;
        border-radius: 999px;
        background: var(--surface-soft);
        border: 1px solid var(--border);
    }

    .confidence-fill {
        height: 100%;
        border-radius: 999px;
        background:
            linear-gradient(
                90deg,
                var(--blue),
                var(--violet)
            );
        box-shadow: 0 0 16px rgba(99,102,241,0.20);
    }

    .confidence-description {
        color: var(--text-secondary);
        font-size: 0.78rem;
        margin-top: 9px;
        line-height: 1.55;
    }

    .evidence-empty {
        padding: 1.1rem 1.2rem;
        border-radius: 15px;
        background: var(--surface-soft);
        border: 1px dashed var(--border);
        color: var(--text-secondary);
        font-size: 0.82rem;
        line-height: 1.55;
    }

    @media (max-width: 900px) {
        .evidence-summary {
            grid-template-columns: 1fr;
        }
    }



    /* =====================================================
       STEP 4 — ADVANCED DECISION DASHBOARD
       ===================================================== */

    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 16px;
        margin: 1rem 0 1.4rem;
    }

    .dashboard-panel {
        padding: 1.35rem;
        border-radius: 20px;
        background: var(--surface);
        border: 1px solid var(--border);
        box-shadow: 0 10px 30px var(--shadow);
    }

    .dashboard-panel-wide {
        grid-column: 1 / -1;
    }

    .dashboard-panel-title {
        color: var(--text);
        font-size: 0.96rem;
        font-weight: 820;
        margin-bottom: 4px;
    }

    .dashboard-panel-subtitle {
        color: var(--text-muted);
        font-size: 0.73rem;
        line-height: 1.5;
        margin-bottom: 14px;
    }

    .risk-header,
    .health-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
    }

    .risk-level,
    .health-level {
        font-size: 1.08rem;
        font-weight: 850;
        letter-spacing: 0.4px;
    }

    .risk-percent,
    .health-percent {
        color: var(--text);
        font-size: 1.15rem;
        font-weight: 850;
    }

    .dashboard-track {
        width: 100%;
        height: 10px;
        margin-top: 10px;
        overflow: hidden;
        border-radius: 999px;
        background: var(--surface-soft);
        border: 1px solid var(--border);
    }

    .dashboard-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(
            90deg,
            var(--blue),
            var(--violet)
        );
    }

    .dashboard-description {
        color: var(--text-secondary);
        font-size: 0.76rem;
        line-height: 1.55;
        margin-top: 9px;
    }

    .security-status {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 12px 14px;
        border-radius: 14px;
        background: var(--surface-soft);
        border: 1px solid var(--border);
    }

    .status-orb {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        flex: 0 0 auto;
        box-shadow: 0 0 12px currentColor;
    }

    .security-status-text {
        color: var(--text);
        font-size: 0.84rem;
        font-weight: 800;
    }

    .security-status-note {
        color: var(--text-muted);
        font-size: 0.71rem;
        margin-top: 2px;
    }

    .agent-activity-grid {
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: 10px;
        margin-top: 10px;
    }

    .agent-activity-card {
        padding: 12px 10px;
        border-radius: 15px;
        background: var(--surface-soft);
        border: 1px solid var(--border);
        text-align: center;
    }

    .agent-activity-name {
        color: var(--text);
        font-size: 0.68rem;
        font-weight: 760;
        line-height: 1.35;
        min-height: 30px;
    }

    .agent-activity-status {
        margin-top: 7px;
        font-size: 0.63rem;
        font-weight: 850;
        letter-spacing: 0.35px;
    }

    .reliability-note {
        color: var(--text-secondary);
        font-size: 0.76rem;
        line-height: 1.55;
        padding: 12px;
        border-radius: 14px;
        background: var(--surface-soft);
        border: 1px dashed var(--border);
    }

    @media (max-width: 950px) {
        .dashboard-grid {
            grid-template-columns: 1fr;
        }

        .dashboard-panel-wide {
            grid-column: auto;
        }

        .agent-activity-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }

    @media (max-width: 550px) {
        .agent-activity-grid {
            grid-template-columns: 1fr;
        }
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

            tab_research, tab_fact, tab_analysis, tab_evidence = st.tabs(
                [
                    "🔎 Research",
                    "✓ Fact Check",
                    "◈ Analysis",
                    "📚 Evidence & Sources",
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


            with tab_evidence:

                evidence_items = extract_evidence(result)

                st.html(
                    """
                    <div class="section-header">
                        <div class="section-icon">◈</div>
                        <div class="section-text">
                            Evidence Summary
                        </div>
                    </div>
                    """
                )

                if evidence_items:

                    reliable_count = 0

                    for item in evidence_items:
                        reliability = item.get("reliability")

                        if isinstance(reliability, (int, float)):
                            if reliability >= 0.60:
                                reliable_count += 1
                        elif isinstance(reliability, str):
                            try:
                                numeric_reliability = float(
                                    reliability.replace("%", "")
                                )
                                if numeric_reliability > 1:
                                    numeric_reliability /= 100
                                if numeric_reliability >= 0.60:
                                    reliable_count += 1
                            except ValueError:
                                pass

                    st.html(
                        f"""
                        <div class="evidence-summary">

                            <div class="evidence-card">
                                <div class="metric-label">
                                    Evidence Items
                                </div>
                                <div class="overview-value">
                                    {len(evidence_items)}
                                </div>
                                <div class="evidence-meta">
                                    Collected from the workflow
                                </div>
                            </div>

                            <div class="evidence-card">
                                <div class="metric-label">
                                    Reliable Evidence
                                </div>
                                <div class="overview-value">
                                    {reliable_count}
                                </div>
                                <div class="evidence-meta">
                                    Reliability ≥ 0.60 when available
                                </div>
                            </div>

                            <div class="evidence-card">
                                <div class="metric-label">
                                    Evidence Layer
                                </div>
                                <div class="overview-value">
                                    ACTIVE
                                </div>
                                <div class="evidence-meta">
                                    Source review &amp; verification
                                </div>
                            </div>

                        </div>
                        """
                    )

                    for index, item in enumerate(evidence_items, start=1):

                        title = html.escape(
                            str(item.get("title", f"Source {index}"))
                        )

                        claim = html.escape(
                            str(item.get("claim", "")).strip()
                        )

                        snippet = html.escape(
                            str(item.get("snippet", "")).strip()
                        )

                        url = str(item.get("url", "")).strip()

                        reliability = item.get("reliability")
                        score = item.get("score")

                        reliability_text = "Not provided"
                        if isinstance(reliability, (int, float)):
                            reliability_value = float(reliability)
                            if reliability_value <= 1:
                                reliability_value *= 100
                            reliability_text = (
                                f"{reliability_value:.0f}%"
                            )
                        elif reliability not in (None, ""):
                            reliability_text = html.escape(
                                str(reliability)
                            )

                        score_text = ""
                        if isinstance(score, (int, float)):
                            score_value = float(score)
                            if score_value <= 1:
                                score_value *= 100
                            score_text = (
                                f"Relevance / Final Score: "
                                f"{score_value:.0f}%"
                            )
                        elif score not in (None, ""):
                            score_text = (
                                "Score: " +
                                html.escape(str(score))
                            )

                        source_html = ""
                        if url.startswith(("http://", "https://")):
                            safe_url = html.escape(url, quote=True)
                            source_html = (
                                f'<a class="source-link" '
                                f'href="{safe_url}" target="_blank">'
                                f'{safe_url}</a>'
                            )

                        st.html(
                            f"""
                            <div class="evidence-card"
                                 style="margin-bottom: 12px;">

                                <div class="evidence-title">
                                    {index}. {title}
                                </div>

                                <div class="evidence-meta">
                                    Reliability: {reliability_text}
                                </div>

                                {
                                    f'<div class="evidence-score">'
                                    f'{html.escape(score_text)}'
                                    f'</div>'
                                    if score_text else ''
                                }

                                {
                                    f'<div style="margin-top:10px; '
                                    f'color:var(--text); '
                                    f'font-size:0.80rem; '
                                    f'line-height:1.6;">'
                                    f'<b>Claim:</b> {claim}</div>'
                                    if claim else ''
                                }

                                {
                                    f'<div style="margin-top:8px; '
                                    f'color:var(--text-secondary); '
                                    f'font-size:0.78rem; '
                                    f'line-height:1.6;">'
                                    f'<b>Snippet:</b> {snippet}</div>'
                                    if snippet else ''
                                }

                                {
                                    f'<div style="margin-top:9px;">'
                                    f'{source_html}</div>'
                                    if source_html else ''
                                }

                            </div>
                            """
                        )

                else:

                    st.html(
                        """
                        <div class="evidence-empty">
                            No structured evidence objects were returned
                            by the current workflow result. The existing
                            Research and Fact Check reports are still
                            available in their respective tabs.
                        </div>
                        """
                    )

            # =================================================
            # STEP 4 — ADVANCED DECISION DASHBOARD
            # =================================================

            dashboard_decision = result.get(
                "decision",
                "No final decision available.",
            )

            evidence_items_dashboard = extract_evidence(result)

            confidence_value_dashboard, confidence_level_dashboard = (
                parse_confidence(
                    dashboard_decision,
                    result,
                )
            )

            risk_level_dashboard = get_risk_level(result)

            (
                risk_label,
                risk_color,
                risk_width,
                risk_description,
            ) = risk_visual(risk_level_dashboard)

            security_status_raw = get_security_status(result)

            (
                security_label,
                security_color,
            ) = security_visual(security_status_raw)

            reliability_average = calculate_reliability_percent(
                evidence_items_dashboard
            )

            system_health_score = calculate_system_health(
                security_status_raw,
                confidence_value_dashboard,
                risk_level_dashboard,
                evidence_items_dashboard,
            )

            health_label, health_color = health_visual(
                system_health_score
            )

            agent_activity = get_agent_activity(result)

            if reliability_average is not None:
                reliability_html = f"""
                    <div class="risk-header">
                        <div class="risk-level"
                             style="color:var(--green);">
                            VERIFIED DATA
                        </div>

                        <div class="risk-percent">
                            {reliability_average:.0f}%
                        </div>
                    </div>

                    <div class="dashboard-track">
                        <div class="dashboard-fill"
                             style="width:{reliability_average:.0f}%;
                                    background:linear-gradient(
                                        90deg,
                                        var(--green),
                                        var(--blue)
                                    );">
                        </div>
                    </div>
                """
            else:
                reliability_html = """
                    <div class="reliability-note">
                        Reliability scores were not returned by the
                        current workflow result.
                    </div>
                """

            agent_html = ""

            for name, status in agent_activity:
                safe_name = html.escape(str(name))
                safe_status = html.escape(str(status))
                color = activity_color(status)

                agent_html += f"""
                    <div class="agent-activity-card">

                        <div class="agent-activity-name">
                            {safe_name}
                        </div>

                        <div
                            class="agent-activity-status"
                            style="color:{color};"
                        >
                            ● {safe_status}
                        </div>

                    </div>
                """

            st.html(
                """
                <div class="section-header">
                    <div class="section-icon">◈</div>
                    <div class="section-text">
                        Advanced Decision Dashboard
                    </div>
                </div>
                """
            )

            st.html(
                f"""
                <div class="dashboard-grid">

                    <div class="dashboard-panel">

                        <div class="dashboard-panel-title">
                            🛡️ Security Status
                        </div>

                        <div class="dashboard-panel-subtitle">
                            Current security guard state returned by
                            the workflow.
                        </div>

                        <div class="security-status">

                            <div
                                class="status-orb"
                                style="color:{security_color};
                                       background:{security_color};"
                            ></div>

                            <div>
                                <div class="security-status-text">
                                    {html.escape(security_label)}
                                </div>

                                <div class="security-status-note">
                                    Decision security layer
                                </div>
                            </div>

                        </div>

                    </div>


                    <div class="dashboard-panel">

                        <div class="dashboard-panel-title">
                            ⚠️ Decision Risk Meter
                        </div>

                        <div class="dashboard-panel-subtitle">
                            Risk level derived from the workflow's
                            security result.
                        </div>

                        <div class="risk-header">

                            <div
                                class="risk-level"
                                style="color:{risk_color};"
                            >
                                {html.escape(risk_label)}
                            </div>

                            <div class="risk-percent">
                                {risk_width}%
                            </div>

                        </div>

                        <div class="dashboard-track">

                            <div
                                class="dashboard-fill"
                                style="width:{risk_width}%;
                                       background:{risk_color};"
                            ></div>

                        </div>

                        <div class="dashboard-description">
                            {html.escape(risk_description)}
                        </div>

                    </div>


                    <div class="dashboard-panel">

                        <div class="dashboard-panel-title">
                            📊 Evidence Reliability
                        </div>

                        <div class="dashboard-panel-subtitle">
                            Average reliability of evidence items when
                            scores are available.
                        </div>

                        {reliability_html}

                    </div>


                    <div class="dashboard-panel">

                        <div class="dashboard-panel-title">
                            ❤️ Overall System Health
                        </div>

                        <div class="dashboard-panel-subtitle">
                            Visual monitoring summary using security,
                            confidence, risk and evidence signals.
                        </div>

                        <div class="health-header">

                            <div
                                class="health-level"
                                style="color:{health_color};"
                            >
                                {html.escape(health_label)}
                            </div>

                            <div class="health-percent">
                                {system_health_score}%
                            </div>

                        </div>

                        <div class="dashboard-track">

                            <div
                                class="dashboard-fill"
                                style="width:{system_health_score}%;
                                       background:{health_color};"
                            ></div>

                        </div>

                        <div class="dashboard-description">
                            This is a UI monitoring indicator and does not
                            override the backend decision guard.
                        </div>

                    </div>


                    <div class="dashboard-panel dashboard-panel-wide">

                        <div class="dashboard-panel-title">
                            🤖 Agent Activity
                        </div>

                        <div class="dashboard-panel-subtitle">
                            Current multi-agent pipeline status.
                        </div>

                        <div class="agent-activity-grid">
                            {agent_html}
                        </div>

                    </div>

                </div>
                """
            )

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

            confidence_value, confidence = parse_confidence(
                decision,
                result,
            )

            confidence_style = confidence_color(confidence)

            if confidence_value is None:
                confidence_percent = 0
                confidence_display = "N/A"
            else:
                confidence_percent = round(
                    confidence_value * 100
                )
                confidence_display = f"{confidence_percent}%"

            confidence_width = confidence_percent

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

                </div>
                """
            )

            st.html(
                f"""
                <div class="section-header">
                    <div class="section-icon">◎</div>
                    <div class="section-text">
                        Decision Confidence
                    </div>
                </div>

                <div class="confidence-panel">

                    <div class="confidence-header">

                        <div
                            class="confidence-level"
                            style="color:{confidence_style};"
                        >
                            {html.escape(confidence)}
                        </div>

                        <div class="confidence-percent">
                            {confidence_display}
                        </div>

                    </div>

                    <div class="confidence-track">

                        <div
                            class="confidence-fill"
                            style="width:{confidence_width}%;"
                        ></div>

                    </div>

                    <div class="confidence-description">
                        {html.escape(
                            confidence_description(confidence)
                        )}
                    </div>

                </div>
                """
            )


            # =================================================
            # SAVE TO HISTORY
            # =================================================

            save_history_entry(
                query=query,
                result={
                    **result,
                    "confidence_score": confidence_value,
                    "confidence_level": confidence,
                    "evidence_count": len(extract_evidence(result)),
                },
                decision=decision,
            )

            st.info(
                "🕘 This research result has been saved to History."
            )
