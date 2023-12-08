from typing import Optional

from pydantic import BaseModel


class NoteSchema(BaseModel):
    title: str
    text: Optional[str] = None
