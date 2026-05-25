# =====================================================================
# FILE: schemas.py
# Purpose: Pydantic Data Validation Schemas for Capstone (Aligned Layout)
# =====================================================================

from pydantic import BaseModel, Field
from typing import List, Dict

# --- API 1: Data Ingestion Schemas ---
class IngestionRecord(BaseModel):
    """Represents a single raw row transaction from a retail store log."""
    Date: str = Field(..., example="2026-06-01")
    Store_ID: int = Field(..., alias="Store ID", example=0)
    Product_ID: int = Field(..., alias="Product ID", example=12)
    Inventory_Level: int = Field(..., alias="Inventory Level", example=450)
    Units_Ordered: int = Field(..., alias="Units Ordered", example=100)
    Demand_Forecast: float = Field(..., alias="Demand Forecast", example=340.5)
    Price: float = Field(..., example=89.99)
    Discount: float = Field(..., example=0.10)
    Holiday_Promotion: int = Field(..., alias="Holiday/Promotion", example=1)
    Competitor_Pricing: float = Field(..., alias="Competitor Pricing", example=92.5)

    class Config:
        populate_by_name = True


class IngestionPayload(BaseModel):
    """Batch wrapper for multi-row data ingestion pipeline."""
    records: List[IngestionRecord]


# --- API 2: ML Demand Prediction Schemas ---
class PredictionPayload(BaseModel):
    """The complete numeric array parameters required by the Random Forest model."""
    store_id: int = Field(..., alias="Store ID")
    product_id: int = Field(..., alias="Product ID")
    inventory_level: int = Field(..., alias="Inventory Level")
    units_ordered: int = Field(..., alias="Units Ordered")
    demand_forecast: float = Field(..., alias="Demand Forecast")
    price: float = Field(..., alias="Price")
    discount: float = Field(..., alias="Discount")
    holiday_promotion: int = Field(..., alias="Holiday/Promotion")
    competitor_pricing: float = Field(..., alias="Competitor Pricing")
    year: int = Field(..., alias="Year")
    month: int = Field(..., alias="Month")
    day: int = Field(..., alias="Day")
    day_of_week: int = Field(..., alias="DayOfWeek")
    is_weekend: int = Field(..., alias="Is_Weekend")
    price_difference: float = Field(..., alias="Price_Difference")
    effective_price: float = Field(..., alias="Effective_Price")
    stock_to_demand_ratio: float = Field(..., alias="Stock_to_Demand_Ratio")
    
    category_flags: Dict[str, int]
    region_flags: Dict[str, int]
    weather_flags: Dict[str, int]
    seasonality_flags: Dict[str, int]

    class Config:
        populate_by_name = True


# --- API 3: RAG Document Knowledge Search Schemas ---
class SearchPayload(BaseModel):
    query: str = Field(..., example="How do I store fragile electronics inventory?")
    top_k: int = Field(default=2, ge=1, le=5)


# --- API 4: Multi-Agent Interaction Schemas ---
class AgentPayload(BaseModel):
    user_query: str = Field(..., example="Can you forecast sales volume for product 12 tomorrow?")
    session_id: str = Field(..., example="session_retail_alpha_99")