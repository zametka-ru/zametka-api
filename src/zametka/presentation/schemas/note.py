from pydantic import BaseModel, Field


class CreateNoteSchema(BaseModel):
    title: str = Field(max_length=50)
    text: str


class UpdateNoteSchema(BaseModel):
    title: str = Field(max_length=50)
    text: str
