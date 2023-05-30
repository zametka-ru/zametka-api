from pydantic import BaseSettings, BaseModel

from fastapi_mail import ConnectionConfig


class BaseDB(BaseModel):
    """Base database config"""

    host: str
    db_name: str
    user: str
    password: str

    def get_connection_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}/{self.db_name}"


class DB(BaseDB, BaseSettings):
    """App database config"""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

        fields = {
            "host": {
                "env": "DB_HOST",
            },
            "db_name": {
                "env": "DB_NAME",
            },
            "user": {
                "env": "DB_USER",
            },
            "password": {
                "env": "DB_PASS",
            },
        }


class AlembicDB(BaseDB, BaseSettings):
    """Alembic database config"""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

        fields = {
            "host": {
                "env": "DB_HOST",
            },
            "db_name": {
                "env": "DB_NAME",
            },
            "user": {
                "env": "DB_USER",  # dev code, another user of alembic in the production NOT FOR PRODUCTION
            },
            "password": {
                "env": "DB_PASS",  # dev code, another user of alembic in the production NOT FOR PRODUCTION
            },
        }


class AuthSettings(BaseSettings):
    """Auth Settings"""

    secret_key: str
    algorithm: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

        fields = {
            "secret_key": {
                "env": "SECRET_KEY",
            },
            "algorithm": {
                "env": "ALGORITHM",
            },
        }


class Settings(BaseModel):
    """App settings"""

    db = DB()  # type:ignore
    auth = AuthSettings()  # type:ignore


class AuthJWTSettings(BaseSettings):
    """AuthJWT Settings"""

    authjwt_secret_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

        fields = {
            "authjwt_secret_key": {
                "env": "AUTHJWT_SECRET_KEY",
            },
        }


class MailSettings(BaseSettings):
    """Mail Settings"""

    mail_username: str
    mail_password: str
    mail_from: str
    mail_port: int
    mail_server: str
    mail_from_name: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

        fields = {
            "mail_username": {
                "env": "MAIL_USERNAME",
            },
            "mail_password": {
                "env": "MAIL_PASSWORD",
            },
            "mail_from": {
                "env": "MAIL_FROM",
            },
            "mail_port": {
                "env": "MAIL_PORT",
            },
            "mail_server": {
                "env": "MAIL_SERVER",
            },
            "mail_from_name": {
                "env": "MAIL_FROM_NAME",
            },
        }


def load_settings() -> Settings:
    """Get app settings"""

    return Settings()


def load_alembic_settings() -> AlembicDB:
    """Get alembic settings"""

    return AlembicDB()  # type:ignore


def load_authjwt_settings() -> AuthJWTSettings:
    return AuthJWTSettings()  # type:ignore


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
