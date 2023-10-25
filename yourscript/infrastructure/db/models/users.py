from passlib.context import CryptContext

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text

from sqlalchemy.orm import relationship, Mapped

from datetime import datetime

from . import Base


class User(Base):
    """App user"""

    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = Column(String(60), nullable=False, unique=True)
    password: Mapped[str] = Column(String(100), nullable=False)
    first_name: Mapped[str] = Column(String(40), nullable=False)
    last_name: Mapped[str] = Column(String(60), nullable=False)
    joined_at: Mapped[datetime] = Column(DateTime, nullable=False)
    is_superuser: Mapped[bool] = Column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = Column(Boolean, default=False, nullable=False)

    scripts = relationship("Script", back_populates="user")


class RefreshToken(Base):
    """JWT Refresh token"""

    __tablename__ = "refresh_tokens"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = Column(Text, nullable=False)

    user_id: Mapped[int] = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
