import logging
from contextlib import contextmanager
from pathlib import Path
from sqlalchemy.orm import Session
from typing import Generator, Any
from logging import Handler, LogRecord
from datetime import datetime
import sys
import uuid

from snakemake_interface_logger_plugins.common import LogEvent
from snakemake_interface_logger_plugins.settings import OutputSettingsLoggerInterface
from .models.workflow import Workflow
from .models.enums import Status
from .event_handlers import (
    EventHandler,
    WorkflowStartedHandler,
    JobInfoHandler,
    JobStartedHandler,
    JobFinishedHandler,
    JobErrorHandler,
    RuleGraphHandler,
    GroupInfoHandler,
    GroupErrorHandler,
    ErrorHandler,
    RunInfoHandler,
)
from .session import get_db


class PostgresqlLogHandler(Handler):
    """Log handler that stores Snakemake events in a PostgreSQL database.

    This handler processes log records from Snakemake and uses
    event parsers and handlers to store them in a PostgreSQL database.
    """

    def __init__(
        self,
        common_settings: OutputSettingsLoggerInterface,
    ):
        """Initialize the PostgreSQL log handler.

        Args:
            common_settings: Common settings for the logger interface.
        """
        super().__init__()

        self.common_settings = common_settings

        self.event_handlers: dict[str, EventHandler] = {  # type: ignore
            LogEvent.WORKFLOW_STARTED.value: WorkflowStartedHandler(),
            LogEvent.JOB_INFO.value: JobInfoHandler(),
            LogEvent.JOB_STARTED.value: JobStartedHandler(),
            LogEvent.JOB_FINISHED.value: JobFinishedHandler(),
            LogEvent.JOB_ERROR.value: JobErrorHandler(),
            LogEvent.RULEGRAPH.value: RuleGraphHandler(),
            LogEvent.GROUP_INFO.value: GroupInfoHandler(),
            LogEvent.GROUP_ERROR.value: GroupErrorHandler(),
            LogEvent.ERROR.value: ErrorHandler(),
            LogEvent.RUN_INFO.value: RunInfoHandler(),
        }

        self._workflow_config = self._get_workflow_config()

        self.context = {
            "current_workflow_id": None,
            "dryrun": self.common_settings.dryrun,
            "jobs": {},
            "logfile": str(Path(f"flowo_logs/log_{uuid.uuid4()}.log").resolve()),
            **self._workflow_config,
        }

    def _get_workflow_config(self):
        data = {}
        for _, module in sys.modules.items():
            if hasattr(module, "__dict__"):
                for attr_name, attr_value in module.__dict__.items():
                    if attr_name == "workflow" and hasattr(attr_value, "globals"):
                        data["config"] = attr_value.globals["config"]
                        configfiles = attr_value.__dict__[
                            "config_settings"
                        ].__dict__.get("configfiles")
                        workdir = attr_value.__dict__.get("overwrite_workdir")
                        if configfiles:
                            data["configfiles"] = [str(_) for _ in configfiles]
                        if workdir:
                            data["workdir"] = str(workdir)
                        return data

    @contextmanager
    def session_scope(self) -> Generator[Session, Any, Any]:
        """Provide a transactional scope around a series of operations."""
        self.session = next(get_db())
        try:
            yield self.session
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            self.handleError(
                logging.LogRecord(
                    name="snkmtLogHandler",
                    level=logging.ERROR,
                    pathname="",
                    lineno=0,
                    msg=f"Database error: {str(e)}",
                    args=(),
                    exc_info=None,
                )
            )
        finally:
            self.session.close()

    def emit(self, record: LogRecord) -> None:
        """Process a log record and store it in the database.

        Args:
            record: The log record to process.
        """
        self.file_handler.emit(record)
        try:
            event = getattr(record, "event", None)
            if not event:
                return
            event_value = event.value if hasattr(event, "value") else str(event).lower()
            handler = self.event_handlers.get(event_value)
            if not handler or self.context.get("dryrun"):
                return
            with self.session_scope() as session:
                handler.handle(record, session, self.context)
        except Exception:
            self.handleError(record)

    def close(self) -> None:
        """Close the handler and update the workflow status."""
        self.file_handler.close()
        if self.context.get("current_workflow_id"):
            try:
                with self.session_scope() as session:
                    workflow = session.query(Workflow).get(
                        self.context["current_workflow_id"]
                    )
                    if workflow and workflow.status != Status.ERROR:
                        workflow.status = Status.SUCCESS
                        workflow.end_time = datetime.now()
            except Exception as e:
                self.handleError(
                    logging.LogRecord(
                        name="snkmtLogHandler",
                        level=logging.ERROR,
                        pathname="",
                        lineno=0,
                        msg=f"Error closing workflow: {str(e)}",
                        args=(),
                        exc_info=None,
                    )
                )

        super().close()
