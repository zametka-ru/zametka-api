from fastapi.responses import JSONResponse
from fastapi import Request, FastAPI

from application.v1.exceptions.script import RestrictScriptAccess


def restrict_script_access(request: Request, exc: RestrictScriptAccess):
    return JSONResponse(status_code=403, content={"details": str(exc)})


def include(app: FastAPI) -> None:
    """Include script exception handlers"""

    app.exception_handler(RestrictScriptAccess)(restrict_script_access)
