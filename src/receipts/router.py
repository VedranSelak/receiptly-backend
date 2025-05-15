from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile

from src.common.dependencies import get_current_user
from src.receipts.schemas import ScanReceiptResponseDto
from src.receipts.service import ReceiptService

router = APIRouter(
    prefix="/receipts",
    tags=["receipts"],
    responses={404: {"description": "Not found"}},
)


@router.post("/scan", status_code=201, dependencies=[Depends(get_current_user)], response_model=ScanReceiptResponseDto)
async def scan_receipt(file: UploadFile, service: Annotated[ReceiptService, Depends()]):
    return await service.scan_receipt(file)
