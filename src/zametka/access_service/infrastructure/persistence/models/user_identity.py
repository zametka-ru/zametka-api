from uuid import UUID

from sqlalchemy import Boolean, Uuid, String
from sqlalchemy.orm import Mapped, mapped_column

from zametka.access_service.infrastructure.persistence.models.base import Base


class UserIdentity(Base):
    """User identity persistence model"""

    __tablename__ = "users"

    identity_id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    email: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(300), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
