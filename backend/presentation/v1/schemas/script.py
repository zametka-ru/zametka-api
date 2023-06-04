from datetime import datetime

from typing import Optional

from pydantic import BaseModel, Field, root_validator


class CreateScriptSchema(BaseModel):
    title: str = Field(max_length=50)
    text: str


class UpdateScriptSchema(BaseModel):
    title: str = Field(max_length=50)
    text: str
