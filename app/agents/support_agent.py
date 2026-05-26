# =====================================================================
# FILE: app/agents/support_agent.py
# Purpose: Cosmos DB Cloud NoSQL Vector RAG Powered Compliance Agent
# =====================================================================

import os
import numpy as np
import joblib
from azure.cosmos import CosmosClient
from sklearn.metrics.pairwise import cosine_similarity
from crewai import Agent
from crewai.tools import tool


# 1. Standalone Native Azure Cosmos DB RAG Tool Definition
@tool("Warehouse Policy RAG Search Tool")
def execute_rag_tool(query: str) -> str:
    """
    Useful when you need to look up corporate compliance manuals, 
    warehouse regulations, or logistics safety protocols from the Azure Cloud.
    """
    # Configuration parameters load out of .env layer
    cosmos_endpoint = os.getenv("AZURE_COSMOS_ENDPOINT")
    cosmos_key = os.getenv("AZURE_COSMOS_KEY")
    database_name = "RetailLogisticsDB"
    container_name = "KnowledgeBase"
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    vectorizer_path = os.path.join(BASE_DIR, "models", "cosmos_vectorizer.pkl")

    if not cosmos_endpoint or not cosmos_key:
        return "Tool Error: Azure Cosmos DB network credentials are missing from .env configuration."

    try:
        # Connect dynamically to the active Azure Cosmos DB instance
        client = CosmosClient(cosmos_endpoint, cosmos_key)
        database = client.get_database_client(database_name)
        container = database.get_container_client(container_name)
        
        # Pull the complete list of vectorized chunks from the NoSQL container
        items = list(container.read_all_items())
        if not items:
            return "Tool Notice: The cloud repository container is currently empty."

        # Load the transformation mapping file to shape the user search query
        if not os.path.exists(vectorizer_path):
            return f"Tool Error: Local model file missing at '{vectorizer_path}' path."
            
        vectorizer = joblib.load(vectorizer_path)
        query_vector = vectorizer.transform([query]).toarray()

        # In-Memory Cosine Similarity Calculation Loop
        best_score = -1
        best_match_text = "No exact matching administrative safety policy or protocol identified for this query context."

        for item in items:
            if "vector_values" not in item:
                continue
                
            # Convert python structure back into structural numerical array
            doc_vector = np.array([item["vector_values"]])
            similarity = cosine_similarity(query_vector, doc_vector)[0][0]
            
            # Mathematical threshold gate checking
            if similarity > best_score and similarity > 0.05:
                best_score = similarity
                best_match_text = item["text"]

        return f"[Cloud Matrix Search Confidence Score: {round(float(best_score), 4)}]\nMatched Context Chunk: '{best_match_text}'"

    except Exception as err:
        return f"Tool execution failed unexpectedly: {str(err)}"


# 2. Agent Wrapper and Export Lifecycle Block
class DocumentAssistantAgent:
    """Agent #2: Searches unstructured operational text files via Azure Cosmos DB RAG framework."""
    def __init__(self):
        self.name = "Document Assistant Agent"

    def get_agent(self) -> Agent:
        return Agent(
            role="Corporate Policy Compliance Auditor",
            goal="Extract accurate, verified operational guidelines from unstructured warehouse manuals.",
            backstory=(
                "You are a meticulous supply chain legal expert. You use your cloud-native "
                "Cosmos DB RAG search tool to pull operational regulatory metrics and match them against logs."
            ),
            tools=[execute_rag_tool],
            verbose=True
        )

# Instantiate the single export object for the orchestrator to keep imports clean
document_agent = DocumentAssistantAgent().get_agent()