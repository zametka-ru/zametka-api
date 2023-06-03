import dataclasses

from fastapi_jwt_auth import AuthJWT

from presentation.v1.schemas.script import CreateScriptSchema

from adapters.repository import UnitOfWork


@dataclasses.dataclass
class CreateScriptInputDTO:
    script_data: CreateScriptSchema
    uow: UnitOfWork
    Authorize: AuthJWT
