from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_another_jwt_auth import AuthJWT
from fastapi_mail import FastMail

from jinja2 import Environment, PackageLoader, select_autoescape

from infrastructure.db.main import get_engine
from presentation import include_routers, include_exception_handlers

from main.ioc import IoC

from infrastructure.config_loader import (
    load_settings,
    load_mail_settings,
    load_authjwt_settings,
)

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


@AuthJWT.load_config
def load_authjwt_config():
    authjwt_config = load_authjwt_settings()

    return [
        ("authjwt_secret_key", authjwt_config.authjwt_secret_key),
        ("authjwt_token_location", authjwt_config.authjwt_token_location),
    ]


@app.on_event("startup")
async def on_startup():
    engine_factory = get_engine(settings.db)
    engine = await engine_factory.__anext__()

    session_factory = await get_async_sessionmaker(engine)

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
        token_link="http://localhost:8000/v1/auth/verify/{}",
    )

    app.dependency_overrides[InteractorFactory] = lambda: ioc

    include_routers(app)
