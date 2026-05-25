# =====================================================================
# FILE: app/azure_storage.py (Optimized with Local Cache Bypass)
# =====================================================================

import os
from azure.storage.blob import BlobServiceClient

class AzureBlobManager:
    def __init__(self):
        self.connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.container_name = os.getenv("AZURE_BLOB_CONTAINER_NAME", "retail-assets")
        
        if self.connection_string and "DefaultEndpointsProtocol" in self.connection_string:
            try:
                self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
                self.container_client = self.blob_service_client.get_container_client(self.container_name)
            except Exception as e:
                print(f"⚠️ Azure Blob Connection Failed: {str(e)}")
                self.connection_string = None

    def sync_asset_from_cloud(self, blob_name: str, local_target_path: str):
        """Checks for local file existence first to guarantee lightning-fast execution."""
        
        # 🚀 QUICK LOCAL BYPASS: Agar file pehle se folder me hai, toh cloud fetch skip karo!
        if os.path.exists(local_target_path) and os.path.getsize(local_target_path) > 0:
            print(f"⚡ [Local Cache Hit]: '{blob_name}' already exists locally. Skipping cloud download to save time.")
            return local_target_path

        if not self.connection_string:
            print(f"ℹ️ Storage connection not bound. Using local cached asset: {local_target_path}")
            return local_target_path

        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            os.makedirs(os.path.dirname(local_target_path), exist_ok=True)
            
            print(f"📥 Cloud Asset Sync: Syncing '{blob_name}' from Azure Blob Storage...")
            with open(local_target_path, "wb") as download_file:
                download_file.write(blob_client.download_blob().readall())
            print(f"✅ Cloud Sync Complete: Ready for execution -> '{local_target_path}'")
            return local_target_path
        except Exception as err:
            print(f"⚠️ Cloud download failed for {blob_name}: {str(err)}. Using local fallback.")
            return local_target_path