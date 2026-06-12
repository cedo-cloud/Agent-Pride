import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_community.llms import FakeListLLM
import os

# Set dummy env strings so CrewAI doesn't throw standard missing-key errors
os.environ["OPENAI_API_KEY"] = "DA-FAKE-KEY"
os.environ["OPENAI_MODEL_NAME"] = "mock-model"

st.set_page_config(page_title="Agent PRIDE Blueprint", page_icon="🤖", layout="centered")

st.title("🤖 Agent PRIDE Blueprint Live Prototype")
st.caption("Option B: CrewAI Multi-Agent Team running live via Streamlit")

# -----------------------------------------------------------------------------
# SIDEBAR CONFIGURATION
# -----------------------------------------------------------------------------
st.sidebar.header("🔑 System Configuration")
st.sidebar.info("✨ Running on Free-Tier Mock LLM (No API Key Required)")

st.sidebar.header("📦 Transaction Payload")
trader_id = st.sidebar.text_input("Trader Identifier", "Aurelia_Trader_01")
amount = st.sidebar.number_input("Requested Value / Variance Amount", value=75000)
profile = st.sidebar.selectbox("HUNT Variance Profile", ["Standard", "High Variance", "Critical"])

# -----------------------------------------------------------------------------
# MOCK LLM ENGINE SETUP (Bypasses paid API restrictions)
# -----------------------------------------------------------------------------
fake_responses = [
    f"[Scout Agent]: Ingested transaction payload for {trader_id}. Parameters normalized. Passing to HUNT Router.",
    f"[HUNT Router]: Evaluation complete. Profile flag is set to '{profile}'. Calibrating RANK constraints and routing accordingly.",
    f"[PRIDE Loop]: Analyzing pipeline flags. Action: Simulated Human-in-the-loop pause point cleared. Milestone logging updated.",
    f"[GUARD Interceptor]: Final structural integrity checks validated. Security protocols signed off. Pipeline complete."
]
mock_llm = FakeListLLM(responses=fake_responses)

# -----------------------------------------------------------------------------
# PIPELINE EXECUTION
# -----------------------------------------------------------------------------
if st.sidebar.button("Execute Agent Pipeline"):
    st.subheader("🤖 Live Pipeline Execution Logs")
    
    # 1. Agent Definitions with local mock LLM assigned
    scout_agent = Agent(
        role='Scout Agent',
        goal='Ingest incoming system data payloads and normalize parameters.',
        backstory='Data validation specialist responsible for filtering transaction logs.',
        llm=mock_llm,
        verbose=True
    )
    hunt_router = Agent(
        role='HUNT Router Agent',
        goal='Evaluate variances and profile financial risk profiles.',
        backstory='Risk modeling analyst that checks incoming metrics against structural rules.',
        llm=mock_llm,
        verbose=True
    )
    pride_loop_agent = Agent(
        role='PRIDE Loop Verification Agent',
        goal='Enforce human-in-the-loop pause points for high-variance data.',
        backstory='Compliance manager who ensures data is held until verified by manual oversight.',
        llm=mock_llm,
        verbose=True
    )
    guard_interceptor = Agent(
        role='GUARD Interceptor Agent',
        goal='Perform final system sanity logs and execute strict structural safety guardrails.',
        backstory='Automated gatekeeper blocking payload processing if constraints fail.',
        llm=mock_llm,
        verbose=True
    )

    # 2. Task Definitions
    task_scout = Task(
        description=f"Ingest payload: Trader={trader_id}, Amount={amount}, Profile={profile}.",
        expected_output="Structured transaction summary.",
        agent=scout_agent
    )
    task_hunt = Task(
        description=f"Analyze summary. Target profile is {profile}. Assign specific routing directives.",
        expected_output="Risk routing profile mapping out next critical milestones.",
        agent=hunt_router
    )
    task_pride = Task(
        description="Evaluate HUNT Router output. Simulate PRIDE Loop validation constraints if flagged.",
        expected_output="Audit block confirming checkpoint processing status.",
        agent=pride_loop_agent
    )
    task_guard = Task(
        description="Perform final structural integrity rules and output clear validation logs.",
        expected_output="Final pipeline validation log confirming execution clearance.",
        agent=guard_interceptor
    )

    # 3. Running the Crew
    crew = Crew(
        agents=[scout_agent, hunt_router, pride_loop_agent, guard_interceptor],
        tasks=[task_scout, task_hunt, task_pride, task_guard],
        process=Process.sequential
    )

    with st.spinner("Agents are coordinating..."):
        output = crew.kickoff()
        
    st.success("✓ Pipeline Execution Finished")
    st.text_area("Agent Communication Output", value=str(output), height=250)
