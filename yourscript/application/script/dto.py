from dataclasses import dataclass

from domain.entities.script import Script
from domain.value_objects.script_id import ScriptId


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
class DeleteScriptInputDTO:
    script_id: ScriptId


@dataclass
class DeleteScriptOutputDTO:
    pass
