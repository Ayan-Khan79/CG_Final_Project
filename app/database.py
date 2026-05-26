# ========================================================
# FILE: database.py
# Purpose: AuraStream AI Cloud MongoDB Atlas & Native Vector RAG Engine
# ========================================================

import os
import joblib
import certifi
from pymongo import MongoClient
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, Any, List

# 1. Inject variables from the local hidden .env file into runtime memory
load_dotenv()

# 2. Extract configuration tokens safely from system environment memory
db_user = os.getenv("MONGO_USER")
db_password = os.getenv("MONGO_PASSWORD")
db_cluster = os.getenv("MONGO_CLUSTER_URL")
db_app_name = os.getenv("MONGO_APP_NAME")

# 3. Dynamically compile your secure connection string URI
MONGO_URI = f"mongodb+srv://{db_user}:{db_password}@{db_cluster}/?retryWrites=true&w=majority&appName={db_app_name}"

# 4. Establish safe, encrypted cloud cluster connection boundaries
try:
    # tlsCAFile=certifi.where() ensures secure root SSL authorities resolve perfectly on local machines
    mongo_client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    
    # Mount our centralized logical data workspace
    db = mongo_client["AuraStream_RetailDB"]
    
    # Expose collection endpoints across the platform application maps
    transactions_collection = db["staged_transactions"]  # Connected to Ingestion (API 1)
    forecast_collection = db["forecast_history"]         # Connected to Predictions (API 2)
    sessions_collection = db["agent_sessions"]           # Connected to Chat Memory (API 4)
    
    # Test network routing via diagnostic administrative ping
    mongo_client.admin.command('ping')
    print("MongoDB Atlas Cloud Status: Secure Link Active via .env parameters.")

except Exception as conn_fault:
    print(f"Database Connectivity Fault: Network connection refused. Details:\n{str(conn_fault)}")


# =====================================================================
# NATIVE VECTOR STORAGE INTERFACE (GenAI / RAG Pipeline Core)
# =====================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAG_MODEL_PATH = os.path.join(BASE_DIR, "models", "native_vector_rag.pkl")

class ProductionVectorStoreRAG:
    """
    Production-grade Vector Store Interface executing native matrix similarity 
    calculations completely offline without remote network dependencies.
    """
    def __init__(self, file_path=RAG_MODEL_PATH):
        if os.path.exists(file_path):
            self.bundle = joblib.load(file_path)
            self.active = True
            print(f"GenAI Layer: Native Vector Index loaded. Registered Chunks: {len(self.bundle['documents'])}")
        else:
            self.active = False
            print("GenAI Layer Warning: 'native_vector_rag.pkl' missing! Please execute 'seed_vector_db.py' first.")

    def search_similarity(self, user_query: str, top_k: int = 1) -> List[Dict[str, Any]]:
        """Executes high-performance local Cosine Similarity lookups over document matrices."""
        if not self.active:
            return [{"doc_id": "fallback", "content": "Baseline Operational Guideline: Review parameters manually."}]

        # Extract pre-compiled matrix artifacts from our serialized bundle file
        vectorizer = self.bundle["vectorizer"]
        tfidf_matrix = self.bundle["matrix"]
        documents = self.bundle["documents"]
        ids = self.bundle["ids"]

        # 1. Mathematical Feature Transformation: Vectorize the live string query 
        query_vector = vectorizer.transform([user_query])

        # 2. Similarity Metric Processing: Calculate angular spatial closeness instantly
        similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()
        
        # 3. Extraction Routing: Pull the exact document index location matching highest value score
        best_match_idx = similarity_scores.argmax()
        
        return [{
            "doc_id": ids[best_match_idx],
            "content": documents[best_match_idx]
        }]

# Instantiate the global operational shared singleton handles
rag_engine = ProductionVectorStoreRAG()