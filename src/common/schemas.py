from pydantic import BaseModel, ConfigDict


class TokenData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    expires: int
