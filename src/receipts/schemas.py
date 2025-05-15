from pydantic import BaseModel, ConfigDict


class ScanReceiptResponseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    extracted_text: str
