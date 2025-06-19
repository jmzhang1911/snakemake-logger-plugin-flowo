from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str = "snakemake"
    POSTGRES_PASSWORD: str = "snakemake_password"
    POSTGRES_DB: str = "snakemake_logs"
    POSTGRES_HOST: str | None = None
    POSTGRES_PORT: str | None = None
    SQL_ECHO: bool = False

    FLOWO_USER: str | None = None
    FLOWO_WORKING_PATH: str | None = None

    class Config:
        env_file = "~/.config/flowo/.env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if not self.POSTGRES_HOST or not self.POSTGRES_PORT:
            return None
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
