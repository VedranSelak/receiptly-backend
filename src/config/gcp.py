from google.cloud import documentai_v1 as documentai
from google.oauth2 import service_account

from src.config.settings import settings

credentials = service_account.Credentials.from_service_account_file(settings.GCP_SERVICE_ACCOUNT_JSON)

document_ai_client = documentai.DocumentProcessorServiceClient(
    credentials=credentials, client_options={"api_endpoint": settings.GCP_API_ENDPOINT}
)
