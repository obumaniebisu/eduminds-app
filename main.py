# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from azure.storage.blob import BlobServiceClient
import os

app = FastAPI(title="Azure Blob Storage API")

# Get Azure Storage info from environment variables
AZURE_STORAGE_URL = os.getenv("AZURE_STORAGE_URL")
AZURE_SAS_TOKEN = os.getenv("AZURE_SAS_TOKEN")

if not AZURE_STORAGE_URL or not AZURE_SAS_TOKEN:
    print("⚠️ Azure Storage environment variables not set")

# Build the full BlobServiceClient URL with SAS token
sas_token = AZURE_SAS_TOKEN.lstrip("?") if AZURE_SAS_TOKEN else None

blob_service_client = (
    BlobServiceClient(account_url=AZURE_STORAGE_URL, credential=sas_token)
    if AZURE_STORAGE_URL and sas_token
    else None
)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Azure Blob Storage API is running"}

# List all containers
@app.get("/containers")
def list_containers():
    if not blob_service_client:
        raise HTTPException(status_code=500, detail="Azure Storage not configured")
    try:
        containers = [c.name for c in blob_service_client.list_containers()]
        return {"containers": containers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# List blobs in a container
@app.get("/containers/{container_name}/blobs")
def list_blobs(container_name: str):
    if not blob_service_client:
        raise HTTPException(status_code=500, detail="Azure Storage not configured")
    try:
        container_client = blob_service_client.get_container_client(container_name)
        blobs = [b.name for b in container_client.list_blobs()]
        return {"blobs": blobs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Upload a file to a container
@app.post("/containers/{container_name}/upload")
async def upload_file(container_name: str, file: UploadFile = File(...)):
    if not blob_service_client:
        raise HTTPException(status_code=500, detail="Azure Storage not configured")
    try:
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(file.filename)
        content = await file.read()
        blob_client.upload_blob(content, overwrite=True)
        return {"filename": file.filename, "container": container_name, "status": "uploaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
