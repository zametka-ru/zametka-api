import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mail import FastMail
from jinja2 import Environment, PackageLoader, select_autoescape

from main.ioc import IoC
from presentation import include_routers, include_exception_handlers

from infrastructure.config_loader import load_settings, load_mail_settings

from infrastructure.db import get_async_sessionmaker
from presentation.interactor_factory import InteractorFactory

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
    session_factory = await get_async_sessionmaker()

    auth_settings = settings.auth
    mail_settings = load_mail_settings()

    mail = FastMail(mail_settings)

    jinja_env: Environment = Environment(
        loader=PackageLoader("infrastructure.adapters.auth"),
        autoescape=select_autoescape(),
    )

    ioc: InteractorFactory = IoC(
        session_factory=session_factory,
        auth_settings=auth_settings,
        jinja_env=jinja_env,
        mailer=mail,
        token_link="/v1/auth/verify/{}",
    )

    app.dependency_overrides[InteractorFactory] = ioc

    include_routers(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=80)
