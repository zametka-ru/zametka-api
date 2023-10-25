import uvicorn

from fastapi import FastAPI
from fastapi_mail import FastMail
from fastapi.middleware.cors import CORSMiddleware
from jinja2 import Environment, PackageLoader, select_autoescape

from infrastructure.db.provider import (
    DbProvider,
    get_uow,
    get_auth_repository,
    get_script_repository,
)
from presentation.v1 import include_routers, include_exception_handlers

from infrastructure.config_loader import load_settings, load_mail_settings

from infrastructure.db import get_async_sessionmaker

from infrastructure.stubs import (
    SessionStub,
    JinjaStub,
)

from application.common.adapters import JWTOperations, PasswordHasher, MailTokenSender
from application.common.repository import AuthRepository, ScriptRepository
from application.common.uow import UoW

from infrastructure.adapters.v1.auth.jwtops import JWTOperationsImpl
from infrastructure.adapters.v1.auth.password_hasher import PasswordHasherImpl

settings = load_settings()

app = FastAPI()

origins = [
    settings.cors.frontend_url,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

include_exception_handlers(app)


@app.on_event("startup")
async def on_startup():
    auth_settings = settings.auth
    mail_settings = load_mail_settings()

    async_sessionmaker = await get_async_sessionmaker(settings.db)
    db_provider = DbProvider(pool=async_sessionmaker)

    mail = FastMail(mail_settings)
    jinja_env: Environment = Environment(
        loader=PackageLoader("infrastructure.adapters.v1.auth"),
        autoescape=select_autoescape(),
    )

    password_hasher = PasswordHasherImpl()
    jwt_operations = JWTOperationsImpl()

    app.dependency_overrides[SessionStub] = db_provider.get_session
    app.dependency_overrides[PasswordHasher] = lambda: password_hasher
    app.dependency_overrides[MailTokenSender] = lambda: mail
    app.dependency_overrides[AuthRepository] = get_auth_repository
    app.dependency_overrides[UoW] = get_uow
    app.dependency_overrides[ScriptRepository] = get_script_repository
    app.dependency_overrides[JinjaStub] = lambda: jinja_env
    app.dependency_overrides[JWTOperations] = lambda: jwt_operations

    include_routers(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=80)
