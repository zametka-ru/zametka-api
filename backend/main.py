import uvicorn

from fastapi import FastAPI
from fastapi_mail import FastMail
from jinja2 import Environment, PackageLoader, select_autoescape

from domain.db.provider import (
    DbProvider,
    get_uow,
    get_auth_repository,
    get_script_repository,
)
from presentation.v1 import include_routers, include_exception_handlers

from core.settings import load_settings, load_mail_settings

from domain.db import get_async_sessionmaker

from core.dependencies import (
    MailDependency,
    AuthSettingsDependency,
    AuthRepositoryDependency,
    ScriptRepositoryDependency,
    UnitOfWorkDependency,
    SessionDependency,
    CryptContextDependency,
    JinjaDependency,
)

from application.v1.auth.interfaces import JWTOpsInterface
from adapters.v1.auth.jwtops import JWTOps

from passlib.context import CryptContext

app = FastAPI()
include_exception_handlers(app)


@app.on_event("startup")
async def on_startup():
    settings = load_settings()
    auth_settings = settings.auth

    mail_settings = load_mail_settings()

    async_sessionmaker = await get_async_sessionmaker(settings.db)

    db_provider = DbProvider(pool=async_sessionmaker)

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    mail = FastMail(mail_settings)

    jinja_env: Environment = Environment(
        loader=PackageLoader("adapters.v1.auth"), autoescape=select_autoescape()
    )

    app.dependency_overrides[SessionDependency] = db_provider.get_session

    app.dependency_overrides[CryptContextDependency] = lambda: pwd_context

    app.dependency_overrides[MailDependency] = lambda: mail

    app.dependency_overrides[AuthSettingsDependency] = lambda: auth_settings

    app.dependency_overrides[AuthRepositoryDependency] = get_auth_repository

    app.dependency_overrides[UnitOfWorkDependency] = get_uow

    app.dependency_overrides[ScriptRepositoryDependency] = get_script_repository

    app.dependency_overrides[JinjaDependency] = lambda: jinja_env

    app.dependency_overrides[JWTOpsInterface] = lambda: JWTOps()

    include_routers(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=80)
