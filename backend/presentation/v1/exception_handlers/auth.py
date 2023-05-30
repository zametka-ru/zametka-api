from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse
from fastapi import Request, FastAPI


def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


def include(app: FastAPI) -> None:
    """Include auth exception handlers"""

    app.exception_handler(AuthJWTException)(authjwt_exception_handler)
