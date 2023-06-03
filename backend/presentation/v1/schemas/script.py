from datetime import datetime

from typing import Optional

from pydantic import BaseModel, Field, root_validator


class CreateScriptSchema(BaseModel):
    title: str = Field(max_length=50)
    text: str
    created_at: Optional[datetime]

    class Config:
        validate_assignment = True

    # noinspection PyMethodParameters
    @root_validator
    def set_created_at(cls, values):
        values["created_at"] = datetime.now()

        return values


class CreateScriptResponse(BaseModel):
    status: str


class CreateScriptFailedResponse(CreateScriptResponse):
    status: str = "failed"
    details: str
    code: int


class CreateScriptSuccessResponse(CreateScriptResponse):
    status: str = "ok"
    script: CreateScriptSchema
