import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import os
import traceback

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Agent PRIDE Blueprint",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Agent PRIDE Blueprint")
st.caption("CrewAI Multi-Agent Pipeline · Sequential Execution")

# ── Sidebar: credentials + payload ───────────────────────────────────────────
with st.sidebar:
    st.header("🔑 API Configuration")
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        placeholder="sk-...",
        help="Required for agents to reason. Not stored beyond this session.",
    )
    model_name = st.selectbox(
        "Model",
        ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
        index=1,          # default to cheaper model
    )

    st.divider()
    st.header("📦 Transaction Payload")
    trader_id = st.text_input("Trader Identifier", "Aurelia_Trader_01")
    amount = st.number_input("Requested Value / Variance Amount", value=75_000, step=1_000)
    profile = st.selectbox(
        "HUNT Variance Profile", ["Standard", "High Variance", "Critical"]
    )

    run_button = st.button("▶ Execute Agent Pipeline", use_container_width=True)

# ── Guard: require API key before running ────────────────────────────────────
if run_button:
    if not api_key or len(api_key.strip()) < 20:
        st.error("Please enter your OpenAI API key in the sidebar before running.")
        st.stop()

    os.environ["OPENAI_API_KEY"] = api_key

    # Build a shared LLM object so every agent uses the chosen model
    llm = ChatOpenAI(model=model_name, temperature=0.2, openai_api_key=api_key)

    st.subheader("📋 Pipeline Execution")

    # ── Agent definitions ─────────────────────────────────────────────────────
    scout_agent = Agent(
        role="Scout Agent",
        goal="Ingest incoming system data payloads and normalise parameters.",
        backstory="Data validation specialist responsible for filtering transaction logs.",
        llm=llm,
        verbose=False,   # verbose=True sends to stdout, not Streamlit
    )
    hunt_router = Agent(
        role="HUNT Router Agent",
        goal="Evaluate variances and profile financial risk levels.",
        backstory="Risk modelling analyst that checks metrics against structural rules.",
        llm=llm,
        verbose=False,
    )
    pride_loop_agent = Agent(
        role="PRIDE Loop Verification Agent",
        goal="Enforce human-in-the-loop pause points for high-variance data.",
        backstory=(
            "Compliance manager who ensures data is held until verified "
            "by manual oversight."
        ),
        llm=llm,
        verbose=False,
    )
    guard_interceptor = Agent(
        role="GUARD Interceptor Agent",
        goal="Perform final sanity checks and enforce strict structural safety guardrails.",
        backstory="Automated gatekeeper that blocks processing if constraints fail.",
        llm=llm,
        verbose=False,
    )

    # ── Task definitions ──────────────────────────────────────────────────────
    task_scout = Task(
        description=(
            f"Ingest payload — Trader: {trader_id}, "
            f"Amount: {amount:,}, Profile: {profile}. "
            "Validate and return a structured transaction summary."
        ),
        expected_output="Structured transaction summary with validated fields.",
        agent=scout_agent,
    )
    task_hunt = Task(
        description=(
            f"Analyse the transaction summary. The variance profile is '{profile}'. "
            "Assign routing directives and flag any risk thresholds breached."
        ),
        expected_output="Risk routing profile with next critical milestones and flags.",
        agent=hunt_router,
    )
    task_pride = Task(
        description=(
            "Evaluate the HUNT Router output. "
            "If the profile is 'High Variance' or 'Critical', simulate a PRIDE Loop "
            "validation pause and document the checkpoint status."
        ),
        expected_output="Audit block confirming checkpoint processing status.",
        agent=pride_loop_agent,
    )
    task_guard = Task(
        description=(
            "Run final structural integrity checks against all prior outputs. "
            "Produce a concise validation log with a clear PASS or FAIL decision."
        ),
        expected_output="Final pipeline validation log with PASS/FAIL and reasoning.",
        agent=guard_interceptor,
    )

    # ── Crew assembly & execution ─────────────────────────────────────────────
    crew = Crew(
        agents=[scout_agent, hunt_router, pride_loop_agent, guard_interceptor],
        tasks=[task_scout, task_hunt, task_pride, task_guard],
        process=Process.sequential,
        verbose=False,
    )

    # Show per-task progress while the crew runs
    task_labels = [
        ("🔍 Scout Agent — ingesting payload", task_scout),
        ("📊 HUNT Router — risk profiling", task_hunt),
        ("🔄 PRIDE Loop — checkpoint validation", task_pride),
        ("🛡️ GUARD Interceptor — final integrity check", task_guard),
    ]

    progress_bar = st.progress(0)
    status_area = st.empty()
    log_expander = st.expander("📄 Per-task outputs", expanded=False)

    try:
        with st.spinner("Agents coordinating…"):
            result = crew.kickoff()

        progress_bar.progress(100)
        st.success("✅ Pipeline execution complete")

        # Show final output
        st.subheader("🗂️ Final Agent Output")
        final_text = (
            result.raw
            if hasattr(result, "raw")
            else str(result)
        )
        st.text_area("Output", value=final_text, height=320, label_visibility="collapsed")

        # Show individual task outputs if available
        with log_expander:
            tasks_output = getattr(result, "tasks_output", None)
            if tasks_output:
                for i, (label, _) in enumerate(task_labels):
                    st.markdown(f"**{label}**")
                    task_out = tasks_output[i] if i < len(tasks_output) else None
                    if task_out:
                        st.write(
                            task_out.raw
                            if hasattr(task_out, "raw")
                            else str(task_out)
                        )
                    st.divider()
            else:
                st.info("Individual task logs not available for this CrewAI version.")

    except Exception as exc:
        progress_bar.empty()
        st.error(f"Pipeline failed: {exc}")
        with st.expander("🐛 Full traceback"):
            st.code(traceback.format_exc())
