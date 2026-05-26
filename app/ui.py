# =====================================================================
# FILE: app/ui.py
# Purpose: Dynamic Multi-Tab Enterprise Frontend Control Center
# Execution: streamlit run ui.py
# =====================================================================

import streamlit as st
import requests
import os
import datetime
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

st.set_page_config(
    page_title="AuraStream AI - Retail Control Center",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Core API endpoints node mappings
# DYNAMIC BACKEND ROUTING ENGINE (AUTOMATIC NODE RE-MAPPING)
BACKEND_BASE = "https://aurastream-retail-api-hnfwgrdpccdtbwec.koreacentral-01.azurewebsites.net"

CHAT_URL = f"{BACKEND_BASE}/api/agent/chat"
INGEST_URL = f"{BACKEND_BASE}/api/ingest"
PREDICT_URL = f"{BACKEND_BASE}/api/predict-demand"
SEARCH_URL = f"{BACKEND_BASE}/api/search-knowledge"

# CSS Framework Injector
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    .badge-swarm { background-color: #DFF6DD; color: #107C41; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 13px; }
    .badge-cloud { background-color: #CCE4F7; color: #0078D4; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 13px; }
    .badge-guard { background-color: #FDE7E9; color: #A80000; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 13px; }
    div.stTabs [data-baseweb="tab-list"] { gap: 12px; }
    div.stTabs [data-baseweb="tab"] { background-color: #F3F2F1; padding: 10px 20px; border-radius: 4px; font-weight: bold; }
    div.stTabs [data-baseweb="tab"]:focus { color: #0078D4; }
    </style>
""", unsafe_allow_html=True)


# SIDEBAR CONTROL PANEL
with st.sidebar:
    st.image("https://img.icons8.com/fluent/96/000000/artificial-intelligence.png", width=70)
    st.title("AuraStream AI")
    st.markdown("### **System Telemetry Network**")
    st.write("---")
    st.markdown("**FastAPI Core**: `Active`")
    st.markdown("**MongoDB Atlas**: `Linked`")
    st.markdown("**CrewAI Matrix**: `3 Agents Active`")
    st.markdown("**Cognitive Guardrail**: `Armed`")
    st.write("---")
    st.caption("**Host**: Local Virtual Machine (`myvenv`)")

st.title("Smart Retail Assistant Platform")
st.markdown("Production-grade workspace mapped across all core capstone REST API nodes.")

# Setup global container Tabs
tabs = st.tabs([
    "Multi-Agent Chat Swarm", 
    "Live Stream Ingestion", 
    "ML Predictive Inference", 
    "Document Knowledge Base"
])


# TAB 1: AI MULTI-AGENT CHAT SWARM
with tabs[0]:
    st.header("Autonomous Multi-Agent Matrix")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            if chat["role"] == "assistant":
                if "Swarm Matrix" in chat["handler"]:
                    st.markdown(f"<span class='badge-swarm'> Handler: {chat['handler']}</span>", unsafe_allow_html=True)
                elif "Knowledge Core" in chat["handler"]:
                    st.markdown(f"<span class='badge-cloud'> Handler: {chat['handler']}</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<span class='badge-guard'> Handler: {chat['handler']}</span>", unsafe_allow_html=True)
                st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
            st.markdown(chat["text"])

    if user_input := st.chat_input("Ask a question regarding warehouse safety caps, demand velocity, or general strategies..."):
        st.session_state.chat_history.append({"role": "user", "text": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            
        with st.chat_message("assistant"):
            with st.spinner(" Routing query loops across cognitive bounds..."):
                try:
                    payload = {"user_query": user_input, "session_id": "streamlit_session"}
                    response = requests.post(CHAT_URL, json=payload, timeout=300)
                    if response.status_code == 200:
                        data = response.json()
                        handler_tag = data.get("active_handler", "Unknown Node")
                        agent_reply = data.get("agent_response", "Empty stream.")
                        
                        if "Swarm Matrix" in handler_tag:
                            st.markdown(f"<span class='badge-swarm'> Handler: {handler_tag}</span>", unsafe_allow_html=True)
                        elif "Knowledge Core" in handler_tag:
                            st.markdown(f"<span class='badge-cloud'> Handler: {handler_tag}</span>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<span class='badge-guard'> Handler: {handler_tag}</span>", unsafe_allow_html=True)
                        
                        st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
                        st.markdown(agent_reply)
                        st.session_state.chat_history.append({"role": "assistant", "text": agent_reply, "handler": handler_tag})
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")
                except Exception as e:
                    st.error(f"Communication Failure: {str(e)}")

# TAB 2: LIVE STREAM INGESTION (SLIDERS & FORMS)
with tabs[1]:
    st.header(" Real-Time Transaction Ingestion Engine")
    st.markdown("Simulates data generation feeding directly into the MongoDB Atlas Cluster.")
    
    with st.form("ingest_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            store_id = st.number_input("Store ID Identifier", min_value=1, max_value=500, value=10)
            product_id = st.number_input("Product ID Stock SKU", min_value=1, max_value=1000, value=25)
            inventory_level = st.slider("Current Warehouse Inventory Level", 0, 500, 120)
        with col2:
            units_ordered = st.slider("Units Ordered Metric", 0, 300, 45)
            price = st.slider("Unit Listing Price ($)", 1.0, 500.0, 49.99)
            discount = st.slider("Active Discount Promotional Margin", 0.0, 1.0, 0.10)
        with col3:
            competitor_pricing = st.slider("Competitor Market Price ($)", 1.0, 500.0, 45.50)
            holiday_promotion = st.selectbox("Holiday/Promotion Active Node", [0, 1], index=0)
            region = st.selectbox("Operational Regional Zone", ["Region_North", "Region_South", "Region_East", "Region_West"])
            
    # Autogenerate time headers behind the screen
        now = datetime.datetime.now()
        
        submit_ingest = st.form_submit_button("Commit Streaming Record to Cloud Cluster")
        if submit_ingest:
            # Structuring standard mock dictionary matching ingestion payload specifications
            mock_record = {
                "Date": now.strftime("%Y-%m-%d"),
                "Store ID": int(store_id), "Product ID": int(product_id), "Inventory Level": int(inventory_level),
                "Units Ordered": int(units_ordered), "Demand Forecast": int(units_ordered + 10), "Price": float(price),
                "Discount": float(discount), "Holiday/Promotion": int(holiday_promotion), "Competitor Pricing": float(competitor_pricing),
                "Year": now.year, "Month": now.month, "Day": now.day, "DayOfWeek": now.weekday(), "Is_Weekend": 1 if now.weekday() >= 5 else 0,
                "Price_Difference": float(price - competitor_pricing), "Effective_Price": float(price * (1 - discount)),
                "Stock_to_Demand_Ratio": float(inventory_level / (units_ordered if units_ordered > 0 else 1)),
                "category_flags": {"Category_Groceries": 1, "Category_Electronics": 0, "Category_Clothing": 0, "Category_Home": 0},
                "region_flags": {f"Region_{region.split('_')[1]}": 1},
                "weather_flags": {"Weather_Sunny": 1, "Weather_Rainy": 0, "Weather_Snowy": 0},
                "seasonality_flags": {"Season_Spring": 1, "Season_Summer": 0, "Season_Fall": 0, "Season_Winter": 0}
            }
            
            with st.spinner("Shipping records down to MongoDB cloud array clusters..."):
                try:
                    payload = {"records": [mock_record]}
                    res = requests.post(INGEST_URL, json=payload)
                    if res.status_code == 200:
                        st.success(f"Cloud Persistence Resolved: {res.json().get('message')}")
                        # Temporarily cache to session state so Tab 3 can automatically grab choices
                        st.session_state["last_ingested_record"] = mock_record
                    else:
                        st.error(f"Ingestion Fault: {res.text}")
                except Exception as ex:
                    st.error(f"Failed connecting to server: {str(ex)}")

# TAB 3: LIVE ML FORECASTING (ZERO REDUNDANCY DROPDOWN SELECT)
with tabs[2]:
    st.header("Production Machine Learning Analytics Core")
    st.markdown("Fetches active document payloads to execute predictive Random Forest metrics.")
    
    # Check if a transaction is currently in session memory to bypass manual entries entirely!
    if "last_ingested_record" in st.session_state:
        rec = st.session_state["last_ingested_record"]
        st.info(f"Detected Active Cloud Session Item: **Store {rec['Store ID']} | SKU {rec['Product ID']}**")
        
        # Display summary mapping to user
        st.json({
            "Store ID": rec["Store ID"], "Product ID": rec["Product ID"], 
            "Inventory Level": rec["Inventory Level"], "Units Ordered": rec["Units Ordered"],
            "Effective Price": rec["Effective_Price"]
        })
        
        if st.button("Trigger Machine Learning Model Inference"):
            with st.spinner(" Activating cached Random Forest compilation nodes..."):
                try:
                    res = requests.post(PREDICT_URL, json=rec)
                    if res.status_code == 200:
                        pred_units = res.json().get("predicted_units_sold")
                        st.metric(label=" Aligned Model Projection Output", value=f"{pred_units} Units Sold")
                        st.success("Mathematical execution sequence complete.")
                    else:
                        st.error(res.text)
                except Exception as ex:
                    st.error(str(ex))
    else:
        st.warning(" No active transaction record loaded. Go to 'Live Stream Ingestion' and push a record to MongoDB first to test this seamlessly!")


# TAB 4: DOCUMENT KNOWLEDGE BASE (SEPARATE RAG MATRIX TESTER)
with tabs[3]:
    st.header("🔍 Isolated Document Semantic Search Node")
    st.markdown("Tests structural vector chunks matching within the database schemas.")
    
    rag_query = st.text_input("Enter search phrase to probe index embeddings (e.g., 'electronics lockers caps'):")
    search_k = st.slider("Vector Top_K Matches", 1, 5, 2)
    
    if st.button("Execute Similarity Retrieval"):
        if rag_query:
            with st.spinner("🔍 Executing high-dimensional cosine boundary analysis..."):
                try:
                    payload = {"query": rag_query, "top_k": search_k}
                    res = requests.post(SEARCH_URL, json=payload)
                    if res.status_code == 200:
                        chunks = res.json().get("matched_chunks", [])
                        if chunks:
                            st.write(f"Found {len(chunks)} contextual vector boundaries matches:")
                            for idx, c in enumerate(chunks):
                                st.info(f"**Match #{idx+1}**: {c}")
                        else:
                            st.warning("No matches found within database arrays.")
                    else:
                        st.error(res.text)
                except Exception as ex:
                    st.error(str(ex))