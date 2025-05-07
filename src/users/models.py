import uuid
from datetime import datetime, timezone

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.config.session import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc).replace(tzinfo=None)
    )
