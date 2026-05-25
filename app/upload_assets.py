# =====================================================================
# FILE: app/upload_assets.py
# Purpose: One-click script to push binary models and scripts to Blob Storage
# =====================================================================

import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("AZURE_BLOB_CONTAINER_NAME", "retail-assets")

def push_assets_to_azure_blob():
    if not connection_string or "DefaultEndpointsProtocol" not in connection_string:
        print("❌ Error: Please configure a valid AZURE_STORAGE_CONNECTION_STRING in your .env file!")
        return

    print("🚀 Linking with Azure Blob Storage Services...")
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        
        # Array map of local components that need cloud persistence
        assets_to_upload = {
            "forecasting_model.pkl": r"C:\Users\hp\Desktop\CG_Final_Project\models\demand_forecast_model.pkl",
            "warehouse_compliance.txt": r"C:\Users\hp\Desktop\CG_Final_Project\app\data\warehouse_compliance.txt"
        }

        print(f"📦 Target Cloud Container Bucket: '{container_name}'")
        
        for blob_name, local_path in assets_to_upload.items():
            if os.path.exists(local_path):
                print(f"⬆️ Uploading '{local_path}' to cloud layer as '{blob_name}'...")
                blob_client = container_client.get_blob_client(blob_name)
                
                with open(local_path, "rb") as data:
                    blob_client.upload_blob(data, overwrite=True)
                print(f"✅ Successfully synced: {blob_name}")
            else:
                print(f"⚠️ Warning: Missing local asset component at '{local_path}'. Skiped.")
                
        print("\n🎉 All production assets are now safely locked on Azure Blob Storage cloud layer!")

    except Exception as e:
        print(f"❌ Critical connection failure: {str(e)}")

if __name__ == "__main__":
    push_assets_to_azure_blob()