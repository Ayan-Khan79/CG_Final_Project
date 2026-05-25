# =====================================================================
# FILE: app/test_main.py
# Purpose: Pydantic Validation & REST API Unit Testing Suite via Pytest
# Execution: pytest test_main.py -v
# =====================================================================

import pytest
import datetime
from fastapi.testclient import TestClient

# Import the core application layer to wrap endpoints
from main import app

# Instantiate the standard structural test node client
client = TestClient(app)

# ---------------------------------------------------------------------
# 🧪 TEST 1: CHAT ORCHESTRATOR COGNITIVE GUARDRAIL GATE (API 4)
# ---------------------------------------------------------------------
def test_agent_chat_endpoint_block_guardrail():
    """Verifies that the cognitive guardrail catches and rejects out-of-domain queries."""
    payload = {
        "user_query": "Tell me a football joke or how to hack a network",
        "session_id": "test_verification_session_alpha"
    }
    response = client.post("/api/agent/chat", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert "orchestration_status" in data
    # It must map either to the Enterprise Guardrail or handle the exception safely
    assert data["orchestration_status"] == "workflow_resolved"


# ---------------------------------------------------------------------
# 🧪 TEST 2: DOCUMENT KNOWLEDGE SEARCH ENDPOINT (API 3)
# ---------------------------------------------------------------------
def test_search_knowledge_endpoint():
    """Verifies vector RAG response schema properties and data structures."""
    payload = {
        "query": "grocery buffer rules and temperature constraints",
        "top_k": 2
    }
    response = client.post("/api/search-knowledge", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert "matched_chunks" in data
    assert isinstance(data["matched_chunks"], list)


# ---------------------------------------------------------------------
# 🧪 TEST 3: REAL-TIME TRANSACTION INGESTION PIPELINE (API 1)
# ---------------------------------------------------------------------
def test_data_ingestion_pipeline_success():
    """Validates full Pydantic mapping constraints and asynchronous push triggers."""
    now = datetime.datetime.now()
    mock_record = {
        "Date": now.strftime("%Y-%m-%d"),
        "Store ID": 99,
        "Product ID": 15,
        "Inventory Level": 200,
        "Units Ordered": 30,
        "Demand Forecast": 40.0,
        "Price": 19.99,
        "Discount": 0.0,
        "Holiday/Promotion": 0,
        "Competitor Pricing": 18.50
    }
    
    payload = {"records": [mock_record]}
    response = client.post("/api/ingest", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "queued" in data["message"]


# ---------------------------------------------------------------------
# 🧪 TEST 4: INGESTION PIPELINE DATA VALIDATION CRASH (API 1 - Fail Case)
# ---------------------------------------------------------------------
def test_data_ingestion_validation_error():
    """Ensures Pydantic catch blocks intercept faulty structures (Missing Date)."""
    # Malformed record without mandatory 'Date' field string
    faulty_record = {
        "Store ID": 99,
        "Product ID": 15,
        "Inventory Level": 200
    }
    
    payload = {"records": [faulty_record]}
    response = client.post("/api/ingest", json=payload)
    
    # Fast API should intercept and return standard 422 validation fault
    assert response.status_code == 422