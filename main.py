import os
from typing import List

from fastapi import FastAPI, HTTPException
from azure.storage.blob import BlobServiceClient, ContainerClient

# --------------------------------------------------
# App initialization
# --------------------------------------------------
app = FastAPI(title="Eduminds Backend")

# --------------------------------------------------
# Root endpoint (IMPORTANT for Azure App Service)
# --------------------------------------------------
@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "Eduminds Backend",
        "message": "API is running"
    }

# --------------------------------------------------
# Health check (CRITICAL for Azure)
# --------------------------------------------------
@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "message": "Eduminds backend running"
    }

# --------------------------------------------------
# Lazy Azure Blob Service Client
# --------------------------------------------------
def get_blob_service() -> BlobServiceClient:
    conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not conn_str:
        raise RuntimeError("AZURE_STORAGE_CONNECTION_STRING not set")
    return BlobServiceClient.from_connection_string(conn_str)

# --------------------------------------------------
# List blobs in a container
# --------------------------------------------------
@app.get("/containers/{container_name}/blobs", response_model=List[str])
def list_blobs(container_name: str):
    try:
        service: BlobServiceClient = get_blob_service()
        container_client: ContainerClient = service.get_container_client(container_name)

        blobs = [blob.name for blob in container_client.list_blobs()]
        return blobs

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
