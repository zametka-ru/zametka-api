import os
from dataclasses import dataclass
from datetime import timedelta

from fastapi_mail import ConnectionConfig


@dataclass
class BaseDB:
    """Base database config"""

    host: str
    db_name: str
    user: str
    password: str

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

    secret_key: str
    algorithm: str


@dataclass
class CORSSettings:
    """CORS Allowed Domains Settings"""

    frontend_url: str


@dataclass
class Settings:
    """App settings"""

    db: DB
    auth: AuthSettings
    cors: CORSSettings


@dataclass
class AuthJWTSettings:
    """AuthJWT Settings"""

    authjwt_secret_key: str

    authjwt_token_location: set

    authjwt_access_token_expires: timedelta

    authjwt_cookie_secure: bool = False

    authjwt_cookie_csrf_protect: bool = True

    # authjwt_cookie_samesite: str = 'lax'


@dataclass
class MailSettings:
    """Mail Settings"""

    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    mail_from_name: str


def load_settings() -> Settings:
    """Get app settings"""

    db = DB(
        db_name=os.environ["DB_NAME"],
        host=os.environ["DB_HOST"],
        password=os.environ["DB_PASS"],
        user=os.environ["DB_USER"],
    )

    auth = AuthSettings(
        algorithm=os.environ["ALGORITHM"],
        secret_key=os.environ["SECRET_KEY"],
    )

    cors = CORSSettings(frontend_url=os.environ["FRONTEND"])

    return Settings(
        db=db,
        auth=auth,
        cors=cors,
    )


def load_alembic_settings() -> AlembicDB:
    """Get alembic settings"""

    return AlembicDB(
        db_name=os.environ["DB_NAME"],
        host=os.environ["DB_HOST"],
        password=os.environ["DB_PASS"],
        user=os.environ["DB_USER"],
    )


def load_authjwt_settings() -> AuthJWTSettings:
    return AuthJWTSettings(
        authjwt_secret_key=os.environ["AUTHJWT_SECRET_KEY"],
        authjwt_token_location={"cookies"},
        authjwt_access_token_expires=timedelta(
            minutes=int(os.environ["AUTHJWT_TOKEN_EXPIRES_MINUTES"])
        ),
    )


def load_mail_settings() -> ConnectionConfig:
    mail_settings = MailSettings(
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
