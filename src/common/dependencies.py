from datetime import datetime, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from src.common.schemas import TokenData
from src.config.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])

        if "id" not in payload or "sub" not in payload or "expires" not in payload:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        if datetime.fromtimestamp(payload["expires"], tz=timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Token has expired")

        return TokenData(id=payload["id"], email=payload["sub"], expires=payload["expires"])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate user!")
