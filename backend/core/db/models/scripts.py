from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime

from . import Base
from .users import User


class Script(Base):
    """The user scripts"""

    __tablename__ = "scripts"

    id: Column[int] = Column(Integer, primary_key=True, autoincrement=True)
    title: Column[str] = Column(String(50), nullable=False)
    text: Column[str] = Column(Text, nullable=False)
    created_at: Column[datetime] = Column(DateTime, nullable=False)

    user_id: Column[int] = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user: User = relationship("User", back_populates="scripts")
