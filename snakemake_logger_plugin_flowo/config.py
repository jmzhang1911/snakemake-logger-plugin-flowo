from pydantic_settings import BaseSettings
import logging


def setup_logger() -> logging.Logger:
    YELLOW = "\033[33m"
    LIGHT_BLUE = "\033[38;5;117m"
    RESET = "\033[0m"

    logger = logging.getLogger("Flowo")

    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        class ColoredFormatter(logging.Formatter):
            def format(self, record):
                msg = super().format(record)
                if record.levelname == "INFO":
                    return LIGHT_BLUE + msg + RESET
                elif record.levelname == "WARNING":
                    return YELLOW + msg + RESET
                return msg

        console_handler.setFormatter(
            ColoredFormatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        logger.addHandler(console_handler)

    return logger


class Settings(BaseSettings):
    POSTGRES_USER: str = "flowo"
    POSTGRES_PASSWORD: str = "flowo_password"
    POSTGRES_DB: str = "flowo_logs"
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
    def SQLALCHEMY_DATABASE_URI(self) -> str | None:
        if not self.POSTGRES_HOST or not self.POSTGRES_PORT:
            return None
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
logger = setup_logger()
