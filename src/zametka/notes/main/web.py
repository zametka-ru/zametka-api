import logging
import uvicorn
import aiohttp

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from zametka.notes.application.common.id_provider import IdProvider
from zametka.notes.infrastructure.config_loader import (
    load_settings,
)
from zametka.notes.infrastructure.db.main import get_async_sessionmaker
from zametka.notes.infrastructure.db.main import get_engine
from zametka.notes.main.ioc import IoC
from zametka.notes.presentation import include_exception_handlers, include_routers
from zametka.notes.presentation.interactor_factory import InteractorFactory
from zametka.notes.presentation.web_api.dependencies.id_provider import (
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


@app.on_event("startup")
async def on_startup() -> None:
    engine_factory = get_engine(settings.db)
    engine = await anext(engine_factory)

    session_factory = await get_async_sessionmaker(engine)

    aiohttp_session = aiohttp.ClientSession()

    ioc: InteractorFactory = IoC(
        session_factory=session_factory,
    )

    app.dependency_overrides[InteractorFactory] = lambda: ioc
    app.dependency_overrides[IdProvider] = get_token_id_provider
    app.dependency_overrides[aiohttp.ClientSession] = lambda: aiohttp_session

    include_routers(app)


if __name__ == "__main__":
    uvicorn.run("web:app", host="0.0.0.0", reload=False, port=80)
