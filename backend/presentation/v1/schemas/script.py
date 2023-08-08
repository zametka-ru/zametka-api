from pydantic import BaseModel, Field


class CreateScriptSchema(BaseModel):
    title: str = Field(max_length=50)
    text: str


class UpdateScriptSchema(BaseModel):
    title: str = Field(max_length=50)
    text: str
