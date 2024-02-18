import logging

import aiohttp
import uvicorn

from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_another_jwt_auth import AuthJWT
from fastapi_mail import FastMail

from jinja2 import Environment, PackageLoader, select_autoescape

from zametka.access_service.application.common.id_provider import (
    IdProvider as AccessIdProvider,
)
from zametka.access_service.infrastructure.config_loader import (
    load_authjwt_config,
    load_mail_config,
    load_general_config as load_access_settings,
)

from zametka.access_service.infrastructure.persistence import (
    main as access_infrastructure,
)

from zametka.access_service.main.ioc import IoC as AccessIoC
from zametka.access_service import presentation as access_presentation
from zametka.access_service.presentation.interactor_factory import (
    InteractorFactory as AccessInteractorFactory,
)
from zametka.access_service.presentation.web_api import (
    dependencies as access_dependencies,
)

from zametka.notes.application.common.id_provider import IdProvider as NotesIdProvider
from zametka.notes.infrastructure.config_loader import (
    load_settings as load_notes_settings,
)
from zametka.notes.infrastructure.db import main as notes_infrastructure
from zametka.notes.main.ioc import IoC as NotesIoC
from zametka.notes import presentation as notes_presentation
from zametka.notes.presentation.interactor_factory import (
    InteractorFactory as NotesInteractorFactory,
)
from zametka.notes.presentation.web_api import dependencies as notes_dependencies

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)
logger.propagate = False

access_settings = load_access_settings()
notes_settings = load_notes_settings()

app = FastAPI()

logging.info("App was created.")

origins = list({access_settings.cors.frontend_url, notes_settings.cors.frontend_url})

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.info("Initialized app middlewares.")

access_presentation.include_exception_handlers(app)
notes_presentation.include_exception_handlers(app)


@AuthJWT.load_config  # type:ignore
def load_authjwt_module_config() -> list[tuple[str, Any]]:
    authjwt_config = load_authjwt_config()

    return [
        ("authjwt_secret_key", authjwt_config.authjwt_secret_key),
        ("authjwt_token_location", authjwt_config.authjwt_token_location),
        ("authjwt_access_token_expires", authjwt_config.authjwt_access_token_expires),
        ("authjwt_cookie_max_age", authjwt_config.authjwt_cookie_expires),
    ]


@app.on_event("startup")
async def on_startup() -> None:
    access_engine_factory = access_infrastructure.get_engine(access_settings.db)
    access_engine = await anext(access_engine_factory)

    notes_engine_factory = notes_infrastructure.get_engine(notes_settings.db)
    notes_engine = await anext(notes_engine_factory)

    access_session_factory = await access_infrastructure.get_async_sessionmaker(
        access_engine
    )
    notes_session_factory = await notes_infrastructure.get_async_sessionmaker(
        notes_engine
    )

    auth_settings = access_settings.auth
    mail_settings = load_mail_config()

    mail = FastMail(mail_settings)

    jinja_env: Environment = Environment(
        loader=PackageLoader("zametka.access_service.presentation.web_api"),
        autoescape=select_autoescape(),
    )

    aiohttp_session = aiohttp.ClientSession()

    access_ioc: AccessInteractorFactory = AccessIoC(
        session_factory=access_session_factory,
        auth_settings=auth_settings,
        jinja_env=jinja_env,
        mailer=mail,
        token_link=f"{access_settings.cors.frontend_url}/verify?token=" + "{}",
    )

    notes_ioc: NotesInteractorFactory = NotesIoC(
        session_factory=notes_session_factory,
    )

    app.dependency_overrides[AccessInteractorFactory] = lambda: access_ioc
    app.dependency_overrides[
        AccessIdProvider
    ] = access_dependencies.get_token_id_provider

    app.dependency_overrides[NotesInteractorFactory] = lambda: notes_ioc
    app.dependency_overrides[NotesIdProvider] = notes_dependencies.get_token_id_provider

    app.dependency_overrides[aiohttp.ClientSession] = lambda: aiohttp_session

    access_presentation.include_routers(app)
    notes_presentation.include_routers(app)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", reload=False, port=80)
