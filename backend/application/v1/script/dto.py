import dataclasses

from datetime import datetime


@dataclasses.dataclass
class CreateScriptInputDTO:
    script_title: str
    script_text: str


@dataclasses.dataclass
class ReadScriptInputDTO:
    script_id: int


@dataclasses.dataclass
class UpdateScriptInputDTO:
    script_id: int
    script_title: str
    script_text: str


@dataclasses.dataclass
class DeleteScriptInputDTO:
    script_id: int
