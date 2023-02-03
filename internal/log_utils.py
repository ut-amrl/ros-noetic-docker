import logging

"""Because people tend to ignore log messages when they don't have color,
but we can't use an external package."""


class CustomLogger(logging.Logger):
    SUCCESS = 25

    def success(
        self, msg, *args, **kwargs
    ) -> None:
        """Log 'msg % args' with severity 'SUCCESS'.

        To pass exception information, use the keyword argument exc_info with a true value, e.g.

        logger.success("Houston, we have %s", "good news", exc_info=1)
        """


class ColorFormatter(logging.Formatter):
    ANSI_PREFIX = "\x1b["

    ANSI_RED = ANSI_PREFIX + "31m"
    ANSI_GREEN = ANSI_PREFIX + "32m"
    ANSI_YELLOW = ANSI_PREFIX + "33m"
    ANSI_CYAN = ANSI_PREFIX + "36m"
    ANSI_RESET = ANSI_PREFIX + "0m"

    BASE_FORMAT = "[%(levelname)s] %(message)s"
    COLOR_FORMATS = {
        logging.ERROR: f"{ANSI_RED}{BASE_FORMAT}{ANSI_RESET}",
        logging.WARNING: f"{ANSI_YELLOW}{BASE_FORMAT}{ANSI_RESET}",
        CustomLogger.SUCCESS: f"{ANSI_GREEN}{BASE_FORMAT}{ANSI_RESET}",
        logging.INFO: f"{ANSI_CYAN}{BASE_FORMAT}{ANSI_RESET}",
    }

    def format(self, record: logging.LogRecord) -> str:
        fmt = self.BASE_FORMAT
        if record.levelno in self.COLOR_FORMATS:
            fmt = self.COLOR_FORMATS[record.levelno]
        return logging.Formatter(fmt).format(record)


def add_log_level(level: int, level_name: str) -> None:
    # https://stackoverflow.com/a/35804945
    method_name = level_name.lower()

    if hasattr(logging, level_name):
        return
    if hasattr(logging, method_name):
        return
    if hasattr(logging.getLoggerClass(), method_name):
        return

    def log_for_level(self, message: str, *args, **kwargs) -> None:
        if self.isEnabledFor(level):
            self._log(level, message, args, **kwargs)

    def log_to_root(message, *args, **kwargs) -> None:
        logging.log(level, message, *args, **kwargs)

    logging.addLevelName(level, level_name)
    setattr(logging, level_name, level)
    setattr(logging.getLoggerClass(), method_name, log_for_level)
    setattr(logging, method_name, log_to_root)


def get_logger() -> CustomLogger:
    add_log_level(CustomLogger.SUCCESS, "SUCCESS")

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(ColorFormatter())

    logger = logging.getLogger("ros-noetic-docker")
    logger.setLevel(handler.level)
    logger.addHandler(handler)

    return logger  # type: ignore
