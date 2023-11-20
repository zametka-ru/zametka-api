from typing import Optional

from yourscript.application.common.adapters import JWT
from yourscript.application.common.repository import AuthRepository, ScriptRepository
from yourscript.application.common.uow import UoW
from yourscript.domain.entities.script import Script
from yourscript.domain.entities.user import DBUser
from yourscript.domain.exceptions.script import (
    ScriptAccessDeniedError,
    ScriptNotExistsError,
)
from yourscript.domain.services.script_service import ScriptService
from yourscript.domain.value_objects.script_id import ScriptId
from yourscript.domain.value_objects.user_id import UserId

from .dto import (
    CreateScriptInputDTO,
    CreateScriptOutputDTO,
    DeleteScriptInputDTO,
    DeleteScriptOutputDTO,
    ReadScriptInputDTO,
    ReadScriptOutputDTO,
    ListScriptsInputDTO,
    ListScriptsOutputDTO,
    UpdateScriptInputDTO,
    UpdateScriptOutputDTO,
)

PAGE_SIZE = 3


class ScriptInteractor:
    def __init__(
            self,
            script_repository: ScriptRepository,
            auth_repository: AuthRepository,
            uow: UoW,
            service: ScriptService,
            jwt: JWT,
    ):
        self.uow = uow
        self.service = service
        self.script_repository = script_repository
        self.auth_repository = auth_repository
        self.jwt = jwt

    async def _get_current_user(self) -> DBUser:
        """Get current user from JWT"""

        user_id = UserId(int(self.jwt.get_jwt_subject()))

        user: DBUser = await self.auth_repository.get(user_id)

        return user

    async def _check_script_exists(self, script_id: ScriptId) -> Script:
        """Raises ScriptNotExists if script with given id is not exists"""

        script: Optional[Script] = await self.script_repository.get(script_id)

        if not script:
            raise ScriptNotExistsError()

        return script

    async def _get_script(self, script_id: ScriptId) -> Script:
        """
        Check can user do actions with this script. These are two checks.

        1. Is script exists
        2. Is user are author of this script

        DRY
        """

        script: Script = await self._check_script_exists(script_id)

        user: DBUser = await self._get_current_user()

        if not self.service.has_access(script, user.user_id):
            raise ScriptAccessDeniedError()

        return script

    async def create(self, data: CreateScriptInputDTO) -> CreateScriptOutputDTO:
        user = await self._get_current_user()

        script: Script = self.service.create(data.title, data.text, user.user_id)

        await self.script_repository.create(script)

        await self.uow.commit()

        return CreateScriptOutputDTO(script=script)

    async def read(self, data: ReadScriptInputDTO) -> ReadScriptOutputDTO:
        """Read script by id use case"""

        script: Script = await self._get_script(data.script_id)

        return ReadScriptOutputDTO(script=script)

    async def update(self, data: UpdateScriptInputDTO) -> UpdateScriptOutputDTO:
        script: Script = await self._get_script(data.script_id)

        new_script: Script = self.service.create(
            data.title, data.text, script.author_id
        )

        await self.script_repository.update(data.script_id, new_script)

        await self.uow.commit()

        return UpdateScriptOutputDTO(script=new_script)

    async def list(self, data: ListScriptsInputDTO) -> ListScriptsOutputDTO:
        user: DBUser = await self._get_current_user()

        offset: int = data.page * PAGE_SIZE
        limit: int = PAGE_SIZE

        if not data.search:
            scripts: list[Script] = await self.script_repository.list(
                author_id=user.user_id,
                limit=limit,
                offset=offset,
            )
        else:
            scripts: list[Script] = await self.script_repository.search(
                query=data.search,
                limit=limit,
                offset=offset,
            )  # type:ignore

        return ListScriptsOutputDTO(scripts=scripts)

    async def delete(self, data: DeleteScriptInputDTO) -> DeleteScriptOutputDTO:
        await self._get_script(data.script_id)

        await self.script_repository.delete(data.script_id)
        await self.uow.commit()

        return DeleteScriptOutputDTO()
