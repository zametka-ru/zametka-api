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
    MailStub,
    AuthSettingsStub,
    AuthRepositoryStub,
    ScriptRepositoryStub,
    UnitOfWorkStub,
    SessionStub,
    CryptContextStub,
    JinjaStub,
)

from application.v1.auth.interfaces import JWTOpsInterface
from adapters.v1.auth.jwtops import JWTOps

from passlib.context import CryptContext

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

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    mail = FastMail(mail_settings)

    jinja_env: Environment = Environment(
        loader=PackageLoader("adapters.v1.auth"), autoescape=select_autoescape()
    )

    app.dependency_overrides[SessionStub] = db_provider.get_session

    app.dependency_overrides[CryptContextStub] = lambda: pwd_context

    app.dependency_overrides[MailStub] = lambda: mail

    app.dependency_overrides[AuthSettingsStub] = lambda: auth_settings

    app.dependency_overrides[AuthRepositoryStub] = get_auth_repository

    app.dependency_overrides[UnitOfWorkStub] = get_uow

    app.dependency_overrides[ScriptRepositoryStub] = get_script_repository

    app.dependency_overrides[JinjaStub] = lambda: jinja_env

    app.dependency_overrides[JWTOpsInterface] = lambda: JWTOps()

    include_routers(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=80)
