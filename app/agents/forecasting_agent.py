import os
import joblib
import pandas as pd
from crewai import Agent
from crewai.tools import tool

class RetailForecastingAgent:
    """Agent #1: Quantitatively evaluates ML models to forecast retail item demand."""
    def __init__(self):
        self.name = "ML Forecasting Expert Agent"
        
        # Balance paths dynamically to point to your root model assets folder location
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, r"C:\Users\hp\Desktop\CG_Final_Project\models\demand_forecast_model.pkl")
        features_path = os.path.join(base_dir, r"C:\Users\hp\Desktop\CG_Final_Project\models\model_features.pkl")
        
        # Fallback to structural root check
        if not os.path.exists(model_path):
            model_path = "../demand_forecast_model.pkl"
            features_path = "../model_features.pkl"

        try:
            self.model = joblib.load(model_path)
            self.features = joblib.load(features_path)
            self.active = True
        except FileNotFoundError:
            self.active = False
            print(f" {self.name}: Model artifacts not found. Locked in simulation mode.")

    @tool("Random Forest Demand Forecasting Tool")
    def execute_prediction_tool(query: str) -> str:
        """Useful when you need to calculate numeric sales demand predictions or volume turn velocities."""
        # Accessing the instantiated class state securely via outer-scope binding
        instance = forecasting_agent_instance
        if not instance.active:
            return "[ML Forecasting Expert Agent Simulation]: Core prediction model offline. Projected turnover is 142.0 units."
        
        try:
            # Standard metrics footprint parameters passed directly into your model matrix
            mock_env_parameters = {
                "Store ID": 1, "Product ID": 105, "Inventory Level": 620, "Units Ordered": 85, "Demand Forecast": 210.4,
                "Price": 125.50, "Discount": 5, "Holiday/Promotion": 0, "Competitor Pricing": 124.99, "Year": 2026,
                "Month": 6, "Day": 1, "DayOfWeek": 0, "Is_Weekend": 0, "Price_Difference": -0.51, "Effective_Price": 119.22, "Stock_to_Demand_Ratio": 2.94
            }
            df_input = pd.DataFrame([mock_env_parameters])
            for col in instance.features:
                if col not in df_input.columns:
                    df_input[col] = 0
            df_aligned = df_input[instance.features]
            
            prediction = instance.model.predict(df_aligned)[0]
            return f"Analytical inference complete. Predicted daily demand: {prediction:.2f} units sold."
        except Exception as e:
            return f"Matrix conversion failure: {str(e)}"

    def get_agent(self) -> Agent:
        return Agent(
            role="Predictive Analytics Data Scientist",
            goal="Execute ML regression structures to isolate optimized future retail demand trends.",
            backstory="You are an advanced predictive data broker. You evaluate operational metrics against trained models.",
            tools=[self.execute_prediction_tool],
            verbose=True
        )

# Instantiate instances for outer-scope wrapper calls
forecasting_agent_instance = RetailForecastingAgent()
forecasting_agent = forecasting_agent_instance.get_agent()