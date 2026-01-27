# azure_connect.py
import os
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient

# Load environment variables from .env
load_dotenv()

AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
AZURE_STORAGE_ACCOUNT_URL = os.getenv("AZURE_STORAGE_ACCOUNT_URL")

if not all([
    AZURE_TENANT_ID,
    AZURE_CLIENT_ID,
    AZURE_CLIENT_SECRET,
    AZURE_STORAGE_ACCOUNT_URL,
]):
    raise RuntimeError("Missing one or more Azure environment variables")

# Entra ID (Service Principal) credential
credential = ClientSecretCredential(
    tenant_id=AZURE_TENANT_ID,
    client_id=AZURE_CLIENT_ID,
    client_secret=AZURE_CLIENT_SECRET,
)

# Blob service client (NO shared key)
blob_service_client = BlobServiceClient(
    account_url=AZURE_STORAGE_ACCOUNT_URL,
    credential=credential,
)

def list_containers():
    return [container.name for container in blob_service_client.list_containers()]
