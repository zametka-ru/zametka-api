from dataclasses import dataclass
from datetime import datetime


@dataclass
class ScriptSchema:
    id: int
    title: str
    text: str
    created_at: datetime
    author_id: int


@dataclass
class ScriptFailedResponse:
    details: str
    code: int

@dataclass
class ScriptReaderSuccessResponse:
    script: ScriptSchema

@dataclass
class CreateScriptFailedResponse(ScriptFailedResponse):
    pass

@dataclass
class CreateScriptSuccessResponse(ScriptReaderSuccessResponse):
    pass

@dataclass
class ReadScriptSuccessResponse(ScriptReaderSuccessResponse):
    pass

@dataclass
class ReadScriptFailedResponse(ScriptFailedResponse):
    pass

@dataclass
class UpdateScriptSuccessResponse(ScriptReaderSuccessResponse):
    pass

@dataclass
class UpdateScriptFailedResponse(ScriptFailedResponse):
    pass

@dataclass
class DeleteScriptSuccessResponse:
    status: str = "ok"

@dataclass
class DeleteScriptFailedResponse(ScriptFailedResponse):
    pass
