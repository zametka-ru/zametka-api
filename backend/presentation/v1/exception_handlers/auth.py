import jwt

from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse
from fastapi import Request, FastAPI

from application.v1.exceptions.auth import JWTCheckError


def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"details": exc.message})


def jwt_check_error(request: Request, exc: JWTCheckError):
    return JSONResponse(status_code=403, content={"details": str(exc)})


def jwt_decode_error(request: Request, exc: jwt.DecodeError):
    return JSONResponse(
        status_code=403, content={"details": "Error while decoding your token."}
    )


def include(app: FastAPI) -> None:
    """Include auth exception handlers"""

    app.exception_handler(AuthJWTException)(authjwt_exception_handler)
    app.exception_handler(JWTCheckError)(jwt_check_error)
    app.exception_handler(jwt.DecodeError)(jwt_decode_error)
