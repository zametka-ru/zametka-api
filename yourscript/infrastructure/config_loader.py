import os
from typing import Optional

from fastapi_mail import ConnectionConfig

from dataclasses import dataclass


@dataclass
class BaseDB:
    """Base database config"""

    host: Optional[str]
    db_name: Optional[str]
    user: Optional[str]
    password: Optional[str]

    def get_connection_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}/{self.db_name}"


@dataclass
class DB(BaseDB):
    """App database config"""


@dataclass
class AlembicDB(BaseDB):
    """Alembic database config"""


@dataclass
class AuthSettings:
    """Auth Settings"""

    secret_key: Optional[str]
    algorithm: Optional[str]


@dataclass
class CORSSettings:
    """CORS Allowed Domains Settings"""

    frontend_url: Optional[str]


@dataclass
class Settings:
    """App settings"""

    db: DB
    auth: AuthSettings
    cors: CORSSettings


@dataclass
class AuthJWTSettings:
    """AuthJWT Settings"""

    authjwt_secret_key: Optional[str]

    authjwt_token_location: set

    authjwt_cookie_secure: bool = False

    authjwt_cookie_csrf_protect: bool = True

    # authjwt_cookie_samesite: Optional[str] = 'lax' production mode


@dataclass
class MailSettings:
    """Mail Settings"""

    mail_username: Optional[str]
    mail_password: Optional[str]
    mail_from: Optional[str]
    mail_port: int
    mail_server: Optional[str]
    mail_from_name: Optional[str]


def load_settings() -> Settings:
    """Get app settings"""

    db = DB(
        db_name=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
        password=os.getenv("DB_PASS"),
        user=os.getenv("DB_USER"),
    )

    auth = AuthSettings(
        algorithm=os.getenv("ALGORITHM"),
        secret_key=os.getenv("SECRET_KEY"),
    )

    cors = CORSSettings(frontend_url=os.getenv("FRONTEND"))

    return Settings(
        db=db,
        auth=auth,
        cors=cors,
    )


def load_alembic_settings() -> AlembicDB:
    """Get alembic settings"""

    return AlembicDB(
        db_name=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
        password=os.getenv("DB_PASS"),
        user=os.getenv("DB_USER"),
    )


def load_authjwt_settings() -> AuthJWTSettings:
    return AuthJWTSettings(
        authjwt_secret_key=os.getenv("AUTHJWT_SECRET_KEY"),
        authjwt_token_location={"cookies"},
    )


def load_mail_settings() -> ConnectionConfig:
    mail_settings = MailSettings(
        mail_from=os.getenv("MAIL_FROM"),
        mail_from_name=os.getenv("MAIL_FROM_NAME"),
        mail_password=os.getenv("MAIL_PASSWORD"),
        mail_port=int(os.getenv("MAIL_PORT", 443)),
        mail_server=os.getenv("MAIL_SERVER"),
        mail_username=os.getenv("MAIL_USERNAME"),
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
