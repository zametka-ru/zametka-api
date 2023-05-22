from sqlalchemy import Column, Integer, String, Text, DateTime

from datetime import datetime

from . import Base


class Script(Base):
    __tablename__ = "scripts"

    id: Column[int] = Column(Integer, primary_key=True, autoincrement=True)
    title: Column[int] = Column(String(50), nullable=False)  # type:ignore
    text: Column[int] = Column(Text, nullable=False)  # type:ignore
    created_at: Column[datetime] = Column(DateTime, nullable=False)
