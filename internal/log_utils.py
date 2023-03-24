import logging

import internal.ansi as ansi

"""Because people tend to ignore log messages when they don't have color,
but we can't use an external package."""


class CustomLogger(logging.Logger):
    SUCCESS = 25
    ATTENTION = 35

    def success(self, msg, *args, **kwargs) -> None:
        """Log 'msg % args' with severity 'SUCCESS'.

        To pass exception information, use the keyword argument exc_info with a true value, e.g.

        logger.success("Houston, we have %s", "good news", exc_info=1)
        """

    def attention(self, msg, *args, **kwargs) -> None:
        """Log a message while trying very hard to get the user's attention.

        From beta testing and user feedback, users tend to ignore all most
        messages, irrespective of the severity or the color of the message, as
        long as the program does not obviously exit with an error.

        This log message should be used sparingly and times when it won't get
        drowned out by other output.
        """

    @staticmethod
    def _attention_format() -> str:
        return (
            f"{ansi.YELLOW}"
            f"{ansi.BLINK}{'⚠️ ' * 4}{ansi.NO_BLINK}"
            f"{ansi.BOLD} VERY IMPORTANT "
            f"{ansi.BLINK}{'⚠️ ' * 4}{ansi.NO_BLINK}"
            f" DO NOT SKIP {ansi.NO_BOLD}"
            f"{ansi.BLINK}{'⚠️ ' * 4}{ansi.NO_BLINK}\n"
            "%(message)s\n"
            f"{ansi.RESET}"
        )


class ColorFormatter(logging.Formatter):
    BASE_FORMAT = "[%(levelname)s] %(message)s"
    COLOR_FORMATS = {
        logging.CRITICAL: f"{ansi.BOLD}{ansi.RED}{BASE_FORMAT}{ansi.RESET}",
        logging.ERROR: f"{ansi.RED}{BASE_FORMAT}{ansi.RESET}",
        CustomLogger.ATTENTION: CustomLogger._attention_format(),
        logging.WARNING: f"{ansi.YELLOW}{BASE_FORMAT}{ansi.RESET}",
        CustomLogger.SUCCESS: f"{ansi.GREEN}{BASE_FORMAT}{ansi.RESET}",
        logging.INFO: f"{ansi.CYAN}{BASE_FORMAT}{ansi.RESET}",
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
    add_log_level(CustomLogger.ATTENTION, "ATTENTION")

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(ColorFormatter())

    logger = logging.getLogger("ros-noetic-docker")
    logger.setLevel(handler.level)
    logger.addHandler(handler)

    return logger  # type: ignore
