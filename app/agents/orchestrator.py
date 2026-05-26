# =====================================================================
# FILE: app/agents/orchestrator.py
# Purpose: Master Autonomous Swarm Orchestrator (Multi-Task Async Engine)
# =====================================================================

import os
from crewai import Crew, Process, Task, LLM

# Import your isolated agent files natively from your package folder
from agents.anomaly_agent import anomaly_agent
from agents.forecasting_agent import forecasting_agent
from agents.support_agent import document_agent

# Bring in your decoupled cloud asset utility manager
from azure_storage import AzureBlobManager

# Configure the Native CrewAI Azure LLM Wrapper Explicitly
crew_azure_llm = LLM(
    model=f"azure/{os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', 'gpt-4o')}",
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
    temperature=0.2
)


async def run_autonomous_orchestration(user_query: str) -> dict:
    """
    An advanced cognitive multi-agent router with runtime cloud-native asset syncing.
    """
    print(" [Cloud Asset Audit]: User query received. Checking dynamic target binaries on Azure Blob...")
    
    try:
        blob_sync_engine = AzureBlobManager()
        # Direct cloud fetch safely locked into the scoped execution flow
        blob_sync_engine.sync_asset_from_cloud(
            blob_name="forecasting_model.pkl", 
            local_target_path=r"C:\Users\hp\Desktop\CG_Final_Project\models\demand_forecast_model.pkl"
        )
        blob_sync_engine.sync_asset_from_cloud(
            blob_name="warehouse_compliance.txt", 
            local_target_path=r"C:\Users\hp\Desktop\CG_Final_Project\app\data\warehouse_compliance.txt"
        )
    except Exception as sync_err:
        print(f" Non-blocking Sync Exception: {str(sync_err)}. Falling back to local cached files.")

    # 1. Bind stable Azure LLM to all sub-agents
    document_assistant = document_agent
    document_assistant.llm = crew_azure_llm
    forecasting_expert = forecasting_agent
    forecasting_expert.llm = crew_azure_llm
    anomaly_supervisor = anomaly_agent
    anomaly_supervisor.llm = crew_azure_llm

    #  Step 2: COGNITIVE INTENT GATEKEEPER (Azure Powered)
    gatekeeper_prompt = (
        f"You are the security gatekeeper for an enterprise retail intelligence platform.\n"
        f"Analyze the incoming user request: '{user_query}'\n\n"
        f"Classify the request into EXACTLY one of these three token strings:\n"
        f"1. LOCAL_SWARM -> If the query specifically asks about internal warehouse safety protocols, "
        f"compliance manuals, or numeric sales demand curve projections/calculations.\n"
        f"2. GENERAL_RETAIL -> If the query is related to the retail industry, supply chain management, "
        f"marketing, e-commerce, or business strategies in general, but does NOT ask for local specs or metrics.\n"
        f"3. BLOCK -> If the query is entirely unrelated to retail, commerce, or logistics (e.g., sports, general science, coding, video games).\n\n"
        f"Output ONLY the token string. Do not include formatting, markdown, or extra words."
    )
    
    gatekeeper_decision = str(await crew_azure_llm.acall(gatekeeper_prompt)).strip()
    print(f"[Gatekeeper Evaluation]: Query classified as -> {gatekeeper_decision}")

    # --- PATH A: Completely Off-Topic -> Strict Rejection ---
    if "BLOCK" in gatekeeper_decision:
        print("[Guardrail Active]: Non-retail query blocked immediately.")
        return {
            "handler": "AuraStream Enterprise Guardrail Boundary",
            "output": (
                " Access Denied: The requested query falls outside the operational domain of this system. "
                "This Multi-Agent framework is strictly restricted to Retail Logistics, Warehouse Compliance, "
                "and Demand Forecasting analytics. Please submit an industry-relevant prompt."
            )
        }

    # --- PATH B: Valid Retail Industry Question, but No Local Docs ---
    if "GENERAL_RETAIL" in gatekeeper_decision:
        print("[Routing Core]: Valid retail query outside local data scope. Answering via Azure Cloud Core...")
        fallback_response = await crew_azure_llm.acall(
            f"You are an expert retail industry management consultant. Provide a highly detailed, professional, "
            f"and analytical response to this industry query: {user_query}"
        )
        return {
            "handler": "Azure AI Foundry Retail Knowledge Core",
            "output": str(fallback_response).strip()
        }

    # --- PATH C: Specific Local Data Requests -> Run the Crew Swarm ---
    print("[Routing Core]: Local specifications requested. Launching internal CrewAI Swarm Pipeline...")
    
    task_policy = Task(
        description=f"Search the local compliance documents using your RAG tool to address this aspect of the query: '{user_query}'",
        expected_output="Extracted warehouse safety regulations or compliance protocols relevant to the query.",
        agent=document_assistant
    )

    task_forecast = Task(
        description=f"Execute your forecasting tool to analyze inventory metrics or product turnover velocities for: '{user_query}'",
        expected_output="Numeric demand prediction results and analytical model outputs.",
        agent=forecasting_expert
    )

    task_synthesis = Task(
        description=(
            f"Review the policy insights collected by the Compliance Auditor and the numeric data from the Data Scientist.\n\n"
            f"Synthesize their outputs into a final, highly professional corporate report that fully answers the user's prompt: '{user_query}'\n\n"
            f"CRITICAL FORMATTING REQUIREMENT:\n"
            f"You MUST explicitly attribute the sections of your answer to the agent that provided the data. "
            f"Use the exact markdown header format below for each section:\n"
            f"### Answered by: Document Assistant Agent\n"
            f"[Insert compliance/RAG insights here]\n\n"
            f"### Answered by: ML Expert / Forecasting Agent\n"
            f"[Insert machine learning demand predictions here]\n\n"
            f"### Answered by: Supply Chain Risk Supervisor\n"
            f"[Insert your synthesized risk analysis and operational recommendations here]"
        ),
        expected_output="A cohesive operational summary cleanly segmented by the specific agent that generated the insight.",
        agent=anomaly_supervisor
    )

    retail_swarm = Crew(
        agents=[document_assistant, forecasting_expert, anomaly_supervisor],
        tasks=[task_policy, task_forecast, task_synthesis],
        process=Process.sequential,
        verbose=True
    )

    crew_output_object = await retail_swarm.kickoff_async()
    return {
        "handler": "CrewAI Autonomous Swarm Matrix",
        "output": str(crew_output_object).strip()
    }