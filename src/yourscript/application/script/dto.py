from dataclasses import dataclass
from typing import Optional

from yourscript.domain.entities.script import Script
from yourscript.domain.value_objects.script_id import ScriptId


@dataclass(frozen=True)
class CreateScriptInputDTO:
    title: str
    text: str


@dataclass(frozen=True)
class CreateScriptOutputDTO:
    script: Script


@dataclass(frozen=True)
class UpdateScriptInputDTO:
    script_id: ScriptId
    title: str
    text: str


@dataclass(frozen=True)
class UpdateScriptOutputDTO:
    script: Script


@dataclass(frozen=True)
class ReadScriptInputDTO:
    script_id: ScriptId


@dataclass(frozen=True)
class ReadScriptOutputDTO:
    script: Script


@dataclass(frozen=True)
class ListScriptsInputDTO:
    page: int
    search: Optional[str] = None


@dataclass(frozen=True)
class ListScriptsOutputDTO:
    scripts: list[Script]


@dataclass(frozen=True)
class DeleteScriptInputDTO:
    script_id: ScriptId


@dataclass(frozen=True)
class DeleteScriptOutputDTO:
    pass
