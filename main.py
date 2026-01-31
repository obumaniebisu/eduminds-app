import os
from typing import List
from fastapi import FastAPI, HTTPException
from azure.storage.blob import BlobServiceClient, ContainerClient

app = FastAPI(title="Eduminds Backend")

# --- Basic health check (CRITICAL for Azure) ---
@app.get("/health")
def health() -> dict:
    """
    Health check endpoint for Azure App Service
    """
    return {"status": "ok", "message": "Eduminds backend running"}


# --- Lazy Blob client (DO NOT initialize at import time) ---
def get_blob_service() -> BlobServiceClient:
    """
    Lazily initializes Azure BlobServiceClient using env variable.
    Raises RuntimeError if the connection string is missing.
    """
    conn_str: str | None = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not conn_str:
        raise RuntimeError("AZURE_STORAGE_CONNECTION_STRING not set")
    return BlobServiceClient.from_connection_string(conn_str)


# --- Endpoint to list blobs in a container ---
@app.get("/containers/{container_name}/blobs")
def list_blobs(container_name: str) -> List[str]:
    """
    Returns a list of blob names in the specified container.
    """
    try:
        service: BlobServiceClient = get_blob_service()
        container_client: ContainerClient = service.get_container_client(container_name)
        blobs: List[str] = [blob.name for blob in container_client.list_blobs()]
        return blobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
