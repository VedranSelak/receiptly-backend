from typing import Annotated

from fastapi import Depends, UploadFile
from google.cloud import documentai_v1 as documentai
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import gcp
from src.config.session import get_db_session
from src.config.settings import settings
from src.receipts.schemas import ScanReceiptResponseDto


class ReceiptService:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_db_session)]):
        self.session = session

    async def scan_receipt(self, file: UploadFile) -> ScanReceiptResponseDto:
        file_content = await file.read()

        raw_document = documentai.RawDocument(content=file_content, mime_type="image/jpeg")
        request = documentai.ProcessRequest(name=settings.GCP_PROCESSOR_PATH, raw_document=raw_document)

        result = gcp.document_ai_client.process_document(request=request)
        return ScanReceiptResponseDto(extracted_text=result.document.text)
