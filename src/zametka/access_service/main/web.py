import logging
import uvicorn

from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_another_jwt_auth import AuthJWT
from fastapi_mail import FastMail

from jinja2 import Environment, PackageLoader, select_autoescape

from zametka.access_service.application.common.id_provider import IdProvider
from zametka.access_service.infrastructure.config_loader import (
    load_authjwt_settings,
    load_mail_settings,
    load_settings,
)

from zametka.access_service.infrastructure.db.main import get_async_sessionmaker
from zametka.access_service.infrastructure.db.main import get_engine
from zametka.access_service.main.ioc import IoC
from zametka.access_service.presentation import (
    include_exception_handlers,
    include_routers,
)
from zametka.access_service.presentation.interactor_factory import InteractorFactory
from zametka.access_service.presentation.web_api.dependencies.id_provider import (
    get_token_id_provider,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
settings = load_settings()

logging.info("Config was loaded.")

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


@AuthJWT.load_config  # type:ignore
def load_authjwt_config() -> list[tuple[str, Any]]:
    authjwt_config = load_authjwt_settings()

    return [
        ("authjwt_secret_key", authjwt_config.authjwt_secret_key),
        ("authjwt_token_location", authjwt_config.authjwt_token_location),
        ("authjwt_access_token_expires", authjwt_config.authjwt_access_token_expires),
        ("authjwt_cookie_max_age", authjwt_config.authjwt_cookie_expires),
    ]


@app.on_event("startup")
async def on_startup() -> None:
    engine_factory = get_engine(settings.db)
    engine = await engine_factory.__anext__()

    session_factory = await get_async_sessionmaker(engine)

    auth_settings = settings.auth
    mail_settings = load_mail_settings()

    mail = FastMail(mail_settings)

    jinja_env: Environment = Environment(
        loader=PackageLoader("zametka.access_service.presentation.web_api"),
        autoescape=select_autoescape(),
    )

    ioc: InteractorFactory = IoC(
        session_factory=session_factory,
        auth_settings=auth_settings,
        jinja_env=jinja_env,
        mailer=mail,
        token_link=f"{settings.cors.frontend_url}/verify?token=" + "{}",
    )

    app.dependency_overrides[InteractorFactory] = lambda: ioc
    app.dependency_overrides[IdProvider] = get_token_id_provider

    include_routers(app)


if __name__ == "__main__":
    uvicorn.run("web:app", host="0.0.0.0", reload=False, port=80)
