from pydantic import BaseSettings, BaseModel


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


class Settings(BaseModel):
    """App settings"""

    db = DB()  # type:ignore


def load_settings() -> Settings:
    """Get app settings"""

    return Settings()


def load_alembic_settings() -> AlembicDB:
    """Get alembic settings"""

    return AlembicDB()  # type:ignore
