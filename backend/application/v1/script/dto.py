import dataclasses

from fastapi_jwt_auth import AuthJWT

from presentation.v1.schemas.script import CreateScriptSchema

from adapters import repository


@dataclasses.dataclass
class CreateScriptInputDTO:
    script_data: CreateScriptSchema
    uow: repository.UnitOfWork
    Authorize: AuthJWT
