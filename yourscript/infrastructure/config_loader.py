from fastapi_mail import ConnectionConfig

from dataclasses import dataclass


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

    authjwt_cookie_secure: bool = False

    authjwt_cookie_csrf_protect: bool = True

    # authjwt_cookie_samesite: str = 'lax' production mode


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


def load_alembic_settings() -> AlembicDB:
    """Get alembic settings"""


def load_authjwt_settings() -> AuthJWTSettings:
    pass


def load_mail_settings() -> ConnectionConfig:
    mail_settings = MailSettings()  # type:ignore

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
