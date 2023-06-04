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


class ScriptSchema(BaseModel):
    id: int
    title: str = Field(max_length=50)
    text: str
    created_at: datetime
    author_id: int


class UpdateScriptSchema(BaseModel):
    title: str = Field(max_length=50)
    text: str


class ScriptResponse(BaseModel):
    status: str


class ScriptFailedResponse(ScriptResponse):
    status: str = "failed"
    details: str
    code: int


class ScriptReaderSuccessResponse(ScriptResponse):
    status: str = "ok"
    script: ScriptSchema


class CreateScriptFailedResponse(ScriptFailedResponse):
    pass


class CreateScriptSuccessResponse(ScriptReaderSuccessResponse):
    pass


class ReadScriptSuccessResponse(ScriptReaderSuccessResponse):
    pass


class ReadScriptFailedResponse(ScriptFailedResponse):
    pass


class UpdateScriptSuccessResponse(ScriptReaderSuccessResponse):
    pass


class UpdateScriptFailedResponse(ScriptFailedResponse):
    pass


class DeleteScriptSuccessResponse(ScriptResponse):
    status: str = "ok"


class DeleteScriptFailedResponse(ScriptFailedResponse):
    pass
