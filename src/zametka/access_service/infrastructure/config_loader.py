import logging
import os

from dataclasses import dataclass
from datetime import timedelta

from fastapi_mail import ConnectionConfig


@dataclass
class BaseDBConfig:
    """Base database config"""

    host: str
    db_name: str
    user: str
    password: str

    def get_connection_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}/{self.db_name}"


@dataclass
class DBConfig(BaseDBConfig):
    """App database config"""


@dataclass
class AlembicDBConfig(BaseDBConfig):
    """Alembic database config"""


@dataclass
class AuthConfig:
    secret_key: str
    algorithm: str


@dataclass
class CORSConfig:
    frontend_url: str


@dataclass
class AMQPConfig:
    host: str = "localhost"
    port: int = 5672
    login: str = "guest"
    password: str = "guest"


@dataclass
class GeneralConfig:
    db: DBConfig
    auth: AuthConfig
    cors: CORSConfig
    amqp: AMQPConfig


@dataclass
class AuthJWTConfig:
    authjwt_secret_key: str

    authjwt_token_location: set[str]

    authjwt_access_token_expires: timedelta
    authjwt_cookie_expires: int

    authjwt_cookie_secure: bool = False

    authjwt_cookie_csrf_protect: bool = True

    # authjwt_cookie_samesite: str = 'lax'


@dataclass
class MailConfig:
    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    mail_from_name: str


def load_general_config() -> GeneralConfig:
    db = DBConfig(
        db_name=os.environ["ACCESS_POSTGRES_DB"],
        host=os.environ["DB_HOST"],
        password=os.environ["POSTGRES_PASSWORD"],
        user=os.environ["POSTGRES_USER"],
    )

    auth = AuthConfig(
        algorithm=os.environ["ALGORITHM"],
        secret_key=os.environ["SECRET_KEY"],
    )

    cors = CORSConfig(frontend_url=os.environ["FRONTEND"])

    amqp = AMQPConfig(
        host=os.environ.get("AMQP_HOST", "localhost"),
        port=int(os.environ.get("AMQP_PORT", 5672)),
        login=os.environ.get("AMQP_LOGIN", "guest"),
        password=os.environ.get("AMQP_PASSWORD", "guest"),
    )

    logging.info("Access config was loaded.")

    return GeneralConfig(
        db=db,
        auth=auth,
        cors=cors,
        amqp=amqp,
    )


def load_alembic_config() -> AlembicDBConfig:
    return AlembicDBConfig(
        db_name=os.environ["ACCESS_POSTGRES_DB"],
        host=os.environ["DB_HOST"],
        password=os.environ["POSTGRES_PASSWORD"],
        user=os.environ["POSTGRES_USER"],
    )


def load_authjwt_config() -> AuthJWTConfig:
    return AuthJWTConfig(
        authjwt_secret_key=os.environ["AUTHJWT_SECRET_KEY"],
        authjwt_token_location={"cookies"},
        authjwt_access_token_expires=timedelta(
            minutes=int(os.environ["AUTHJWT_TOKEN_EXPIRES_MINUTES"])
        ),
        authjwt_cookie_expires=int(os.environ["AUTHJWT_COOKIE_EXPIRES_SECONDS"]),
    )


def load_mail_config() -> ConnectionConfig:
    mail_settings = MailConfig(
        mail_from=os.environ["MAIL_FROM"],
        mail_from_name=os.environ["MAIL_FROM_NAME"],
        mail_password=os.environ["MAIL_PASSWORD"],
        mail_port=int(os.environ.get("MAIL_PORT", 443)),
        mail_server=os.environ["MAIL_SERVER"],
        mail_username=os.environ["MAIL_USERNAME"],
    )

    conf = ConnectionConfig(
        MAIL_USERNAME=mail_settings.mail_username,
        MAIL_PASSWORD=mail_settings.mail_password,
        MAIL_FROM=mail_settings.mail_from,
        MAIL_PORT=mail_settings.mail_port,
        MAIL_SERVER=mail_settings.mail_server,
        MAIL_FROM_NAME=mail_settings.mail_from_name,
        MAIL_STARTTLS=False,
        MAIL_SSL_TLS=True,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
    )

    return conf
