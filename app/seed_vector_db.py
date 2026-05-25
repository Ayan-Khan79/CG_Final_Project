# =====================================================================
# FILE: seed_cosmos_rag.py
# Purpose: Dynamic Azure Cosmos DB RAG Seeder using External TXT File
# =====================================================================

import os
import numpy as np
import joblib
from azure.cosmos import CosmosClient, PartitionKey
from sklearn.feature_extraction.text import TfidfVectorizer
from dotenv import load_dotenv

load_dotenv()

# 🟦 1. Credentials Configuration
COSMOS_ENDPOINT = os.getenv("AZURE_COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("AZURE_COSMOS_KEY")
DATABASE_NAME = "RetailLogisticsDB"
CONTAINER_NAME = "KnowledgeBase"

def load_and_chunk_txt_file(file_path: str) -> list:
    """Reads the external TXT compliance file and breaks it down by sections."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ Error: {file_path} nahi mili! Pehle data folder check karein.")
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Sections ya heavy paragraphs ke basis par data ko split karna
    raw_chunks = content.split("SECTION")
    cleaned_chunks = []
    
    # Pehle header ko handle karte hain agar paragraph bada hai
    header = raw_chunks[0].strip()
    if header:
        cleaned_chunks.append({
            "id": "kb_header_000",
            "category": "general",
            "text": header
        })
        
    # Baaki bache sections ko loop karke loop items banana
    for idx, chunk in enumerate(raw_chunks[1:], start=1):
        text_content = f"SECTION {chunk.strip()}"
        
        # Simple string matching se category identify karna taaki partition key sahi baithe
        category = "general"
        if "electronics" in text_content.lower():
            category = "electronics"
        elif "groceries" in text_content.lower() or "food" in text_content.lower():
            category = "groceries"
        elif "furniture" in text_content.lower():
            category = "furniture"
        elif "refund" in text_content.lower():
            category = "refunds"
            
        cleaned_chunks.append({
            "id": f"kb_chunk_00{idx}",
            "category": category,
            "text": text_content
        })
        
    return cleaned_chunks

def seed_cosmos_vector_store():
    if not COSMOS_ENDPOINT or not COSMOS_KEY:
        print("❌ Error: Please configure AZURE_COSMOS_ENDPOINT and AZURE_COSMOS_KEY in your .env")
        return

    # 2. Dynamic Text Parsing Step
    txt_source_path = "data/warehouse_compliance.txt"
    print(f"📖 Reading dynamic compliance rules from: '{txt_source_path}'...")
    try:
        documents_corpus = load_and_chunk_txt_file(txt_source_path)
        print(f"✅ Successfully extracted {len(documents_corpus)} computational chunks from file.")
    except Exception as e:
        print(str(e))
        return

    # 3. Cosmos DB Service Link Activation
    print("🔌 Connecting to Azure Cosmos DB Client...")
    client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
    database = client.create_database_if_not_exists(id=DATABASE_NAME)
    container = database.create_container_if_not_exists(
        id=CONTAINER_NAME,
        partition_key=PartitionKey(path="/category"),
        offer_throughput=400
    )

    # 4. Math Vector Representation (TF-IDF Vectorizer Engine)
    raw_texts = [doc["text"] for doc in documents_corpus]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(raw_texts).toarray()

    # Model parameters archive matrix dump
    os.makedirs("models", exist_ok=True)
    joblib.dump(vectorizer, "models/cosmos_vectorizer.pkl")
    print("📦 Local query vectorizer model saved to 'models/cosmos_vectorizer.pkl'")

    # 5. Ingestion Payload Push to Cloud Container
    print("🚀 Seeding dynamic structures up to Azure Cosmos DB...")
    for idx, doc in enumerate(documents_corpus):
        doc["vector_values"] = tfidf_matrix[idx].tolist()
        container.upsert_item(body=doc)
        print(f" 🗂️ Ingested text array: {doc['id']} [{doc['category']}] -> Cloud Storage.")

    print("\n🎉 Dynamic Cosmos DB Vector Store setup completely finalized out of your text file!")

if __name__ == "__main__":
    seed_cosmos_vector_store()