import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_community.chat_models.fake import FakeListChatModel
import os

os.environ["OPENAI_API_KEY"] = "DA-FAKE-KEY"
os.environ["OPENAI_MODEL_NAME"] = "mock-model"

st.set_page_config(page_title="Agent PRIDE Blueprint", page_icon="🤖", layout="centered")
st.title("🤖 Agent PRIDE Blueprint Live Prototype")
st.caption("Option B: CrewAI Multi-Agent Team running live via Streamlit")

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.header("🔑 System Configuration")
st.sidebar.info("✨ Running on Free-Tier Mock LLM (No API Key Required)")

st.sidebar.header("📦 Transaction Payload")
trader_id = st.sidebar.text_input("Trader Identifier", "Aurelia_Trader_01")
amount    = st.sidebar.number_input("Requested Value / Variance Amount", value=75000)
profile   = st.sidebar.selectbox("HUNT Variance Profile", ["Standard", "High Variance", "Critical"])

# ── Mock LLM (chat-model interface — compatible with CrewAI's Pydantic checks) ─
fake_responses = [
    f"Final Answer: [Scout Agent] Ingested transaction for {trader_id}. Amount {amount} normalised. Profile '{profile}' confirmed. Passing to HUNT Router.",
    f"Final Answer: [HUNT Router] Evaluation complete. Profile '{profile}' flagged. Routing directives assigned. Risk thresholds within bounds.",
    f"Final Answer: [PRIDE Loop] Human-in-the-loop checkpoint cleared. Milestone logging updated. No holds raised.",
    f"Final Answer: [GUARD Interceptor] Final structural integrity checks passed. Security protocols signed off. Pipeline CLEARED.",
]
mock_llm = FakeListChatModel(responses=fake_responses)

# ── Pipeline execution ────────────────────────────────────────────────────────
if st.sidebar.button("Execute Agent Pipeline"):
    st.subheader("🤖 Live Pipeline Execution Logs")

    scout_agent = Agent(
        role="Scout Agent",
        goal="Ingest incoming system data payloads and normalize parameters.",
        backstory="Data validation specialist responsible for filtering transaction logs.",
        llm=mock_llm,
        verbose=False,
    )
    hunt_router = Agent(
        role="HUNT Router Agent",
        goal="Evaluate variances and profile financial risk profiles.",
        backstory="Risk modeling analyst that checks incoming metrics against structural rules.",
        llm=mock_llm,
        verbose=False,
    )
    pride_loop_agent = Agent(
        role="PRIDE Loop Verification Agent",
        goal="Enforce human-in-the-loop pause points for high-variance data.",
        backstory="Compliance manager who ensures data is held until verified by manual oversight.",
        llm=mock_llm,
        verbose=False,
    )
    guard_interceptor = Agent(
        role="GUARD Interceptor Agent",
        goal="Perform final system sanity logs and execute strict structural safety guardrails.",
        backstory="Automated gatekeeper blocking payload processing if constraints fail.",
        llm=mock_llm,
        verbose=False,
    )

    task_scout = Task(
        description=f"Ingest payload: Trader={trader_id}, Amount={amount}, Profile={profile}.",
        expected_output="Structured transaction summary.",
        agent=scout_agent,
    )
    task_hunt = Task(
        description=f"Analyze summary. Target profile is {profile}. Assign specific routing directives.",
        expected_output="Risk routing profile mapping out next critical milestones.",
        agent=hunt_router,
    )
    task_pride = Task(
        description="Evaluate HUNT Router output. Simulate PRIDE Loop validation constraints if flagged.",
        expected_output="Audit block confirming checkpoint processing status.",
        agent=pride_loop_agent,
    )
    task_guard = Task(
        description="Perform final structural integrity rules and output clear validation logs.",
        expected_output="Final pipeline validation log confirming execution clearance.",
        agent=guard_interceptor,
    )

    crew = Crew(
        agents=[scout_agent, hunt_router, pride_loop_agent, guard_interceptor],
        tasks=[task_scout, task_hunt, task_pride, task_guard],
        process=Process.sequential,
        verbose=False,
    )

    with st.spinner("Agents coordinating…"):
        try:
            output = crew.kickoff()
            st.success("✓ Pipeline Execution Finished")
            final_text = output.raw if hasattr(output, "raw") else str(output)
            st.text_area("Agent Communication Output", value=final_text, height=280)
        except Exception as e:
            st.error(f"Pipeline failed: {e}")
            import traceback
            with st.expander("🐛 Full traceback"):
                st.code(traceback.format_exc())
