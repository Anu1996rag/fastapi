import logging
import posixpath
import sys
from logging.handlers import TimedRotatingFileHandler
from loguru import logger


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


loggers = (
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
        if name.startswith("uvicorn.")
    )
for uvicorn_logger in loggers:
    uvicorn_logger.handlers = []

# change handler for default uvicorn logger
intercept_handler = InterceptHandler()
logging.getLogger("uvicorn").handlers = [intercept_handler]


# configure loguru
loguru_format = "<level>{level: <8}</level> <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>"
logger.configure(
        handlers=[{"sink": sys.stdout, "format": loguru_format}]
    )


# file level logging
file_rotation_handler = TimedRotatingFileHandler(
    filename=posixpath.join("logs", "api.log"),
    when="midnight",
    interval=1,
    backupCount=31
)
logger.add(file_rotation_handler, format=loguru_format)
