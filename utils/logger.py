import logging
from utils import create_debug_file
import os

verbose = False

class CustomLoggingHandler(logging.Handler):
    """
    A custom logging handler that processes log records.
    ---
    Attributes:
        `logging.Handler`: logging handler object to passthrough
    """

    def __init__(self, level=logging.NOTSET):
        super().__init__(level)  # Initialize the parent logging.Handler class

    def emit(self, record: logging.LogRecord):
        """
        Process the log record and send it to the desired output.
        ---
        Attributes:
            record `logging.LogRecord`: A LogRecord instance containing the log event.
        """
        log_entry = self.format(record)

        if logging.getLevelName(record.levelno) in ["DEBUG", "INFO"]:
            created_file = create_debug_file()
            with open(created_file, "a", encoding="UTF-8") as file:
                write_string = log_entry + "\n"
                file.write(write_string)
                if verbose:
                    print(write_string)

def set_log_level(logger: logging.Logger, level: str):
    """
    Set default log level. Only works with `logging.DEBUG` and `logging.INFO` for now.
    ---
    Attributes:
        logger `logging.Logger`: the logger class passed to the function
        level `str`: the logger level (case insensitive)
    """
    level = level.lower()
    if level in ["debug", "warn"]:
        logger.setLevel(logging.DEBUG)
    elif level == "info":
        logger.setLevel(logging.INFO)

class LoggerSingleton:
    """
    Singleton class to initalize and get logger.
    """
    _logger = None

    @staticmethod
    def init_logger(level: str):
        """
        Gets the logger (initializes if needed) with a custom handler and formatter.
        ---
        Attributes:
            level `str`: the logger level (case insensitive)

        Returns:
            logger `logging.Logger`: the custom logger with the added handler
        """

        if LoggerSingleton._logger is None:
            LoggerSingleton._logger = logging.getLogger("custom_logger")
            set_log_level(LoggerSingleton._logger, level)

            custom_handler = CustomLoggingHandler()
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            custom_handler.setFormatter(formatter)

            LoggerSingleton._logger.addHandler(custom_handler)

        return LoggerSingleton._logger

def get_logger() -> logging.Logger:
    """
    Utility function to easily get logger. It returns the Singleton Class logger.
    """
    return LoggerSingleton.init_logger(os.getenv("LOGGING_LEVEL", "INFO")) #info is the default level
