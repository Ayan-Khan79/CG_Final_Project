# =====================================================================
# FILE: app/main.py
# Purpose: Unified Core FastAPI Routing App Node Engine (Fixed Cloud Layout)
# =====================================================================

import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import IngestionPayload, PredictionPayload, SearchPayload, AgentPayload
from app.database import rag_engine

app = FastAPI(
    title="Smart Retail Assistant Multi-Agent Platform",
    description="Production-ready backend orchestrating ML models, separate agent files, and data streams.",
    version="1.0.0"
)

# 🛡️ FIX 1: ABSOLUTE CORS MIDDLEWARE FOR AZURE GATEWAY HANDSHAKE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 👑 FIX 2: Dynamic Paths matching both Local Machine & Linux Docker Containers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "demand_forecast_model.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "models", "model_features.pkl")

model = None
model_features = None

@app.on_event("startup")
def pre_load_ml_pipeline():
    global model, model_features
    if os.path.exists(MODEL_PATH) and os.path.exists(FEATURES_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            model_features = joblib.load(FEATURES_PATH)
            print("🚀 Success: Random Forest Regressor cached from Cloud Sync. Platform Live.")
        except Exception as load_err:
            print(f"⚠️ Passive Startup Notice: Model files exist but parsing failed: {str(load_err)}")
    else:
        print("ℹ️ System Notice: Prediction binaries not detected yet. Waiting for Azure Blob runtime sync trigger.")

# --- API 1: DATA INGESTION PIPELINE ---
@app.post("/api/ingest", tags=["Data Engineering Pipeline"])
async def ingest_retail_stream(payload: IngestionPayload, background_tasks: BackgroundTasks):
    if not payload.records:
        raise HTTPException(status_code=400, detail="Transaction logs batch is completely empty.")
    
    def async_cloud_database_commit(data_list):
        try:
            from app.database import transactions_collection
            import datetime
            
            raw_records = [rec.dict(by_alias=True) for rec in data_list]
            
            for record in raw_records:
                record["ingested_at"] = datetime.datetime.utcnow().isoformat() + "Z"
                record["data_pipeline_origin"] = "AuraStream_ADF_Pipeline"
            
            result = transactions_collection.insert_many(raw_records)
            print(f"📦 MongoDB Atlas Sync: Successfully committed {len(result.inserted_ids)} records down to cloud storage.")
        except Exception as write_err:
            print(f"❌ Cloud Write Failure: Failed to stream metrics to Atlas. Reason: {str(write_err)}")

    background_tasks.add_task(async_cloud_database_commit, payload.records)
    return {"status": "success", "message": f"Successfully queued {len(payload.records)} streaming records for cloud persistence."}

# --- API 2: ML Demand Forecast Inference ---
@app.post("/api/predict-demand", tags=["Machine Learning Core"])
async def run_demand_inference(payload: PredictionPayload):
    global model, model_features
    
    # Check if loaded, else dynamic fallback loading via absolute-relative path
    if model is None or model_features is None:
        if os.path.exists(MODEL_PATH) and os.path.exists(FEATURES_PATH):
            model = joblib.load(MODEL_PATH)
            model_features = joblib.load(FEATURES_PATH)
            print("⚡ [Runtime Hot-Reload]: Random Forest Model successfully forced into memory cache.")
            
    if model is None or model_features is None:
        raise HTTPException(
            status_code=503, 
            detail="Predictive model engine is unmounted or offline. Please check if your .pkl files exist in app/models/"
        )
        
    try:
        raw_payload = payload.dict(by_alias=True)
        input_vector = {}
        for key, val in raw_payload.items():
            if not isinstance(val, dict):
                input_vector[key] = val
                
        input_vector.update(payload.category_flags)
        input_vector.update(payload.region_flags)
        input_vector.update(payload.weather_flags)
        input_vector.update(payload.seasonality_flags)
        
        df_input = pd.DataFrame([input_vector])
        for col in model_features:
            if col not in df_input.columns:
                df_input[col] = 0
        df_aligned = df_input[model_features]
        
        prediction = model.predict(df_aligned)[0]
        return {"status": "success", "predicted_units_sold": round(float(prediction), 2)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference pipeline crash: {str(e)}")

# --- API 3: Document Knowledge Search (RAG Router) ---
@app.post("/api/search-knowledge", tags=["GenAI & Vector Stores"])
async def query_knowledge_base(payload: SearchPayload):
    matched = rag_engine.search_similarity(payload.query, top_k=payload.top_k)
    return {"query": payload.query, "matched_chunks": matched}

# --- API 4: COGNITIVE MULTI-AGENT CHAT ORCHESTRATOR ---
@app.post("/api/agent/chat", tags=["Multi-Agent Orchestration Framework"])
async def route_agent_workflow(payload: AgentPayload):
    try:
        from app.agents.orchestrator import run_autonomous_orchestration
        orchestration_result = await run_autonomous_orchestration(payload.user_query)
        
        return {
            "session_id": payload.session_id,
            "active_handler": orchestration_result["handler"],  
            "agent_response": orchestration_result["output"],   
            "orchestration_status": "workflow_resolved"
        }
    except Exception as crew_fault:
        raise HTTPException(status_code=500, detail=f"CrewAI Workspace Fault: {str(crew_fault)}")