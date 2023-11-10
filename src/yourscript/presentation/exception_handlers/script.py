from fastapi import Request
from fastapi.responses import JSONResponse

from yourscript.domain.exceptions.script import (
    ScriptAccessDeniedError,
    ScriptNotExistsError,
)


async def script_access_denied_exception_handler(
    _request: Request, _exc: ScriptAccessDeniedError
):
    return JSONResponse(
        status_code=403,
        content={"message": "Доступ закрыт."},
    )


async def script_not_exists_exception_handler(
    _request: Request, _exc: ScriptNotExistsError
):
    return JSONResponse(
        status_code=404,
        content={"message": "Такой записи не существует."},
    )
