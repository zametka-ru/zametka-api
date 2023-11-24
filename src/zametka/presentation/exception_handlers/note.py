from fastapi import Request
from fastapi.responses import JSONResponse

from zametka.domain.exceptions.note import (
    NoteAccessDeniedError,
    NoteNotExistsError,
)


async def note_access_denied_exception_handler(
    _request: Request, _exc: NoteAccessDeniedError
):
    return JSONResponse(
        status_code=403,
        content={"message": "Доступ закрыт."},
    )


async def note_not_exists_exception_handler(
    _request: Request, _exc: NoteNotExistsError
):
    return JSONResponse(
        status_code=404,
        content={"message": "Такой записи не существует."},
    )
