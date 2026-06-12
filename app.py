import streamlit as st
import time

st.set_page_config(page_title="Agent PRIDE Blueprint", page_icon="🤖", layout="centered")
st.title("🤖 Agent PRIDE Blueprint Live Prototype")
st.caption("CrewAI Multi-Agent Pipeline · Simulated Execution · No API Key Required")

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.header("🔑 System Configuration")
st.sidebar.info("✨ Running on Free-Tier Simulated Pipeline (No API Key Required)")

st.sidebar.header("📦 Transaction Payload")
trader_id = st.sidebar.text_input("Trader Identifier", "Aurelia_Trader_01")
amount    = st.sidebar.number_input("Requested Value / Variance Amount", value=75000)
profile   = st.sidebar.selectbox("HUNT Variance Profile", ["Standard", "High Variance", "Critical"])

# ── Simulated agent outputs ───────────────────────────────────────────────────
def get_agent_outputs(trader_id, amount, profile):
    risk_level = {"Standard": "LOW", "High Variance": "ELEVATED", "Critical": "HIGH"}[profile]
    hold = profile in ("High Variance", "Critical")
    guard_result = "PASS" if profile == "Standard" else "PASS WITH CONDITIONS" if profile == "High Variance" else "HOLD — MANUAL REVIEW REQUIRED"

    return [
        {
            "label": "🔍 Scout Agent",
            "role": "Payload Ingestion & Normalisation",
            "output": (
                f"TRANSACTION SUMMARY\n"
                f"───────────────────────────────\n"
                f"Trader ID   : {trader_id}\n"
                f"Amount      : ${amount:,.2f}\n"
                f"Profile     : {profile}\n"
                f"Risk Level  : {risk_level}\n"
                f"Status      : NORMALISED ✓\n"
                f"Timestamp   : {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}"
            ),
        },
        {
            "label": "📊 HUNT Router Agent",
            "role": "Risk Profiling & Routing",
            "output": (
                f"ROUTING DIRECTIVE\n"
                f"───────────────────────────────\n"
                f"Profile Flag  : {profile}\n"
                f"Risk Score    : {risk_level}\n"
                f"Threshold     : {'WITHIN BOUNDS' if profile == 'Standard' else 'THRESHOLD BREACHED'}\n"
                f"Next Action   : {'Standard clearance queue' if profile == 'Standard' else 'Escalate to PRIDE Loop for validation hold'}\n"
                f"Milestone     : HUNT_ROUTE_{risk_level}_{'OK' if profile == 'Standard' else 'FLAGGED'}"
            ),
        },
        {
            "label": "🔄 PRIDE Loop Agent",
            "role": "Human-in-the-Loop Checkpoint",
            "output": (
                f"CHECKPOINT AUDIT BLOCK\n"
                f"───────────────────────────────\n"
                f"Hold Triggered  : {'YES — Awaiting manual sign-off' if hold else 'NO — Auto-cleared'}\n"
                f"Validation      : {'PENDING OVERSIGHT' if hold else 'CLEARED'}\n"
                f"Compliance Flag : {'RAISED' if hold else 'NONE'}\n"
                f"Checkpoint ID   : PRIDE-{trader_id[:6].upper()}-{int(amount) % 9999:04d}\n"
                f"Status          : {'⚠ HOLD' if hold else '✓ PASSED'}"
            ),
        },
        {
            "label": "🛡️ GUARD Interceptor Agent",
            "role": "Final Integrity & Safety Check",
            "output": (
                f"FINAL VALIDATION LOG\n"
                f"───────────────────────────────\n"
                f"Integrity Check : COMPLETE\n"
                f"Safety Rules    : ALL EVALUATED\n"
                f"Decision        : {guard_result}\n"
                f"Pipeline ID     : GUARD-{abs(hash(trader_id)) % 99999:05d}\n"
                f"Execution       : {'✅ CLEARED FOR PROCESSING' if profile == 'Standard' else '⚠ CONDITIONS APPLY — SEE PRIDE LOG' if profile == 'High Variance' else '🛑 BLOCKED — ESCALATE TO COMPLIANCE'}"
            ),
        },
    ]

# ── Run pipeline ──────────────────────────────────────────────────────────────
if st.sidebar.button("▶ Execute Agent Pipeline", use_container_width=True):
    st.subheader("🤖 Live Pipeline Execution Logs")

    agents = get_agent_outputs(trader_id, amount, profile)
    progress = st.progress(0)

    for i, agent in enumerate(agents):
        with st.spinner(f"Running {agent['label']}…"):
            time.sleep(0.8)  # simulates processing time

        with st.expander(f"{agent['label']} — {agent['role']}", expanded=True):
            st.code(agent["output"], language=None)

        progress.progress((i + 1) * 25)

    st.success("✅ Pipeline Execution Complete")

    # Combined summary
    st.subheader("🗂️ Full Pipeline Output")
    full_output = "\n\n".join(
        f"{'='*40}\n{a['label']} | {a['role']}\n{'='*40}\n{a['output']}"
        for a in agents
    )
    st.text_area("Agent Communication Output", value=full_output, height=320, label_visibility="collapsed")
