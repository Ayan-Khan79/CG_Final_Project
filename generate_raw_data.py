# =====================================================================
# FILE: generate_raw_data.py
# Purpose: High-Volume Mock Retail Transaction Log Generator (Raw Ingestion Source)
# =====================================================================

import pandas as pd
import numpy as np
import datetime

def build_raw_retail_dataset(output_path="raw_retail_transactions.csv", num_rows=100000):
    print(f"Generating {num_rows} raw retail transactional records...")
    np.random.seed(42)
    
    start_date = datetime.date(2025, 1, 1)
    date_list = [start_date + datetime.timedelta(days=int(i)) for i in np.random.randint(0, 500, num_rows)]
    
    store_ids = np.random.randint(101, 111, num_rows)     # 10 Stores
    product_ids = np.random.randint(50, 75, num_rows)     # 25 SKUs/Products
    
    inventory_levels = np.random.randint(5, 500, num_rows)
    units_ordered = np.random.randint(1, 150, num_rows)
    
    # Intentionally inserting some missing values (Nulls) to simulate real messy raw data
    inventory_levels = [np.nan if x % 97 == 0 else x for x in inventory_levels]
    units_ordered = [np.nan if x % 101 == 0 else x for x in units_ordered]
    
    base_prices = np.random.uniform(5.0, 150.0, num_rows)
    discounts = np.random.choice([0.0, 0.05, 0.10, 0.15, 0.20], num_rows, p=[0.5, 0.2, 0.15, 0.1, 0.05])
    holiday_promo = np.random.choice([0, 1], num_rows, p=[0.85, 0.15])
    
    # Create variance for competitor prices
    competitor_pricing = base_prices * np.random.uniform(0.9, 1.1, num_rows)
    
    df = pd.DataFrame({
        "Trans_Date": [d.strftime("%Y-%m-%d") for d in date_list],
        "Store_ID": store_ids,
        "Product_ID": product_ids,
        "Inventory_Level": inventory_levels,
        "Units_Ordered": units_ordered,
        "Price": np.round(base_prices, 2),
        "Discount": discounts,
        "Holiday_Promotion": holiday_promo,
        "Competitor_Pricing": np.round(competitor_pricing, 2)
    })
    
    df.to_csv(output_path, index=False)
    print(f"Success! Raw dataset dropped at: '{output_path}'")

if __name__ == "__main__":
    build_raw_retail_dataset()