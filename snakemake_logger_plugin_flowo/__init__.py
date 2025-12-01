"""
Snakemake PostgreSQL Logger Plugin

A logger plugin for Snakemake that stores workflow execution data in PostgreSQL.
"""

from snakemake_interface_logger_plugins.base import LogHandlerBase
from snakemake_interface_logger_plugins.settings import LogHandlerSettingsBase
from dataclasses import dataclass, field
from .log_handler import PostgresqlLogHandler
from typing import Optional

__version__ = "0.1.0"

from .config import logger


@dataclass
class LogHandlerSettings(LogHandlerSettingsBase):
    name: Optional[str] = field(
        default=None,
        metadata={
            "help": "Set name of this workflow",
            "env_var": False,
            "required": False,
        },
    )
    tags: Optional[str] = field(
        default=None,
        metadata={
            "help": "Set tags of this workflow, separated by ',' ",
            "env_var": False,
            "required": False,
        },
    )


class LogHandler(LogHandlerBase, PostgresqlLogHandler):
    """Main LogHandler class for the PostgreSQL plugin."""

    def __post_init__(self) -> None:
        PostgresqlLogHandler.__init__(self, 
                                      self.common_settings, 
                                      flowo_project_name = self.settings.name,
                                      flowo_tags = self.settings.tags)

        if not self.db_connected():
            self.emit = lambda _: None
            self.close = lambda: None
        else:
            logger.info(
                "Plugin is successfully initialized and running. Monitoring ..."
            )
        self.flowo_path_valid()

    @property
    def writes_to_stream(self) -> bool:
        """Whether this plugin writes to stderr/stdout"""
        return False

    @property
    def writes_to_file(self) -> bool:
        """Whether this plugin writes to a file"""
        return False

    @property
    def has_filter(self) -> bool:
        """Whether this plugin attaches its own filter"""
        return True

    @property
    def has_formatter(self) -> bool:
        """Whether this plugin attaches its own formatter"""
        return True

    @property
    def needs_rulegraph(self) -> bool:
        """Whether this plugin requires the DAG rulegraph."""
        return True

    def emit(self, record):
        return PostgresqlLogHandler.emit(self, record)


__all__ = ["LogHandler"]
