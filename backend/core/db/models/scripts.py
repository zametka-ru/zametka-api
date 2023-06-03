from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime

from . import Base
from .users import User


class Script(Base):
    """The user scripts"""

    __tablename__ = "scripts"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    title: str = Column(String(50), nullable=False)
    text: str = Column(Text, nullable=False)
    created_at: datetime = Column(DateTime, nullable=False)

    user_id: int = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user: User = relationship("User", back_populates="scripts")
