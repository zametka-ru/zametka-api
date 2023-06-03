import dataclasses

from datetime import datetime
from typing import Optional


@dataclasses.dataclass
class CreateScriptInputDTO:
    script_title: str
    script_text: str
    script_created_at: Optional[datetime]


@dataclasses.dataclass
class ReadScriptInputDTO:
    script_id: int
