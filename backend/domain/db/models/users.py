from passlib.context import CryptContext

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text

from sqlalchemy.orm import relationship

from datetime import datetime

from . import Base


class User(Base):
    """App user"""

    __tablename__ = "users"

    id: Column[int] = Column(Integer, primary_key=True, autoincrement=True)
    email: Column[str] = Column(String(60), nullable=False, unique=True)
    password: Column[str] = Column(String(100), nullable=False)
    first_name: Column[str] = Column(String(40), nullable=False)
    last_name: Column[str] = Column(String(60), nullable=False)
    joined_at: Column[datetime] = Column(DateTime, nullable=False)
    is_superuser: Column[bool] = Column(Boolean, default=False, nullable=False)
    is_active: Column[bool] = Column(Boolean, default=False, nullable=False)

    scripts = relationship("Script", back_populates="user")

    @classmethod
    def hash_password(cls, password: str, pwd_context: CryptContext) -> str:
        return pwd_context.hash(password)

    def compare_passwords(self, plain_password: str, pwd_context: CryptContext) -> bool:
        return pwd_context.verify(plain_password, self.password)


class RefreshToken(Base):
    """JWT Refresh token"""

    __tablename__ = "refresh_tokens"

    id: Column[int] = Column(Integer, primary_key=True, autoincrement=True)
    token: Column[str] = Column(Text, nullable=False)

    user_id: int = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
