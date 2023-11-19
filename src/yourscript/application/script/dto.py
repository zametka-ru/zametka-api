from dataclasses import dataclass
from typing import Optional

from yourscript.domain.entities.script import Script
from yourscript.domain.value_objects.script_id import ScriptId


@dataclass
class CreateScriptInputDTO:
    title: str
    text: str


@dataclass
class CreateScriptOutputDTO:
    script: Script


@dataclass
class UpdateScriptInputDTO:
    script_id: ScriptId
    title: str
    text: str


@dataclass
class UpdateScriptOutputDTO:
    script: Script


@dataclass
class ReadScriptInputDTO:
    script_id: ScriptId


@dataclass
class ReadScriptOutputDTO:
    script: Script


@dataclass
class ListScriptsInputDTO:
    page: int
    search: Optional[str] = None


@dataclass
class ListScriptsOutputDTO:
    scripts: list[Script]


@dataclass
class DeleteScriptInputDTO:
    script_id: ScriptId


@dataclass
class DeleteScriptOutputDTO:
    pass
