import uvicorn

from fastapi import FastAPI
from fastapi_mail import FastMail

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
)

from sqlalchemy.orm import Session

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

    app.dependency_overrides[Session] = db_provider.get_session

    app.dependency_overrides[CryptContext] = lambda: pwd_context

    app.dependency_overrides[MailDependency] = lambda: mail

    app.dependency_overrides[AuthSettingsDependency] = lambda: auth_settings

    app.dependency_overrides[AuthRepositoryDependency] = get_auth_repository

    app.dependency_overrides[UnitOfWorkDependency] = get_uow

    app.dependency_overrides[ScriptRepositoryDependency] = get_script_repository

    include_routers(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=80)
