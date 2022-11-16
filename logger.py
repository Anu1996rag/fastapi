import logging
import os
import posixpath
import sys
from logging.handlers import TimedRotatingFileHandler
from gunicorn.glogging import Logger
from loguru import logger

LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL", "DEBUG"))
JSON_LOGS = True if os.environ.get("JSON_LOGS", "0") == "1" else False
WORKERS = int(os.environ.get("GUNICORN_WORKERS", "5"))


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class StubbedGunicornLogger(Logger):
    def setup(self, cfg):
        handler = logging.NullHandler()
        self.error_logger = logging.getLogger("gunicorn.error")
        self.error_logger.addHandler(handler)
        self.access_logger = logging.getLogger("gunicorn.access")
        self.access_logger.addHandler(handler)
        self.error_logger.setLevel(LOG_LEVEL)
        self.access_logger.setLevel(LOG_LEVEL)


loggers = (
    logging.getLogger(name)
    for name in logging.root.manager.loggerDict
    if name.startswith(("uvicorn", "gunicorn"))
)


for uvicorn_logger in loggers:
    uvicorn_logger.handlers = []

# change handler for default uvicorn logger
intercept_handler = InterceptHandler()
logging.getLogger("uvicorn").handlers = [intercept_handler]
logging.getLogger("gunicorn").handlers = [intercept_handler]

# configure loguru
loguru_format = "<level>{level: <8}</level> <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>"
logger.configure(
    handlers=[{"sink": sys.stdout, "format": loguru_format, "serialize": JSON_LOGS}]
)

# file level logging
file_rotation_handler = TimedRotatingFileHandler(
    filename=posixpath.join("logs", "api.log"),
    when="midnight",
    interval=1,
    backupCount=31
)
logger.add(file_rotation_handler, format=loguru_format)
