import logging
from collections import deque
from utils import create_debug_file, remove_debug_file
from .argparser import ParserWrapper
import os, threading

class CustomLoggingHandler(logging.Handler):
    """
    A custom logging handler that processes log records.
    ---
    Attributes:
        `logging.Handler`: logging handler object to passthrough
    """

    def __init__(self, level=logging.NOTSET):
        self.verbose = False
        self.buffer = deque()
        super().__init__(level)  # Initialize the parent logging.Handler class

    def set_verbose(self, flag: bool):
        """
        Simple function to set the verbose flag in the class.
        ---
        Attributes:
            flag `bool`: boolean value of the verbosity of the logger
        """
        self.verbose = flag

    def emit(self, record: logging.LogRecord):
        """
        Process the log record and send it to the desired output.
        ---
        Attributes:
            record logging.LogRecord: A LogRecord instance containing the log event.
        """
        log_entry = self.format(record)

        if logging.getLevelName(record.levelno) in ["DEBUG", "INFO"]:
            created_file = create_debug_file()
            with open(created_file, "a", encoding="UTF-8") as file:
                write_string = log_entry 
                file.write(write_string + "\n")
                if self.verbose:
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
    if level == "debug":
        logger.setLevel(logging.DEBUG)
    elif level == "info":
        logger.setLevel(logging.INFO)
    elif level in ["warn", "warning"]:
        logger.setLevel(logging.WARNING)
    elif level == "error":
        logger.setLevel(logging.ERROR)
    elif level == "critical":
        logger.setLevel(logging.CRITICAL)
    else:
        # Default to DEBUG if unknown level
        logger.setLevel(logging.DEBUG)

class LoggerSingleton:
    """
    Singleton class to initalize and get logger.
    """
    _logger = None
    _custom_handler = None

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

            LoggerSingleton._custom_handler = CustomLoggingHandler()
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            LoggerSingleton._custom_handler.setFormatter(formatter)

            LoggerSingleton._logger.addHandler(LoggerSingleton._custom_handler)

        return LoggerSingleton._logger

    @staticmethod
    def set_verbose(flag: bool):
        """
        Toggle verbose mode dynamically.
        ---
        Attributes:
            flag `bool`: flag of verbosity, true or false
        """
        if LoggerSingleton._custom_handler:
            LoggerSingleton._custom_handler.set_verbose(flag)

def get_logger() -> logging.Logger:
    """
    Utility function to easily get logger. It returns the Singleton Class logger.
    """
    parser = ParserWrapper()
    args = parser.parse_args()

    if args.verbose:
        LoggerSingleton.set_verbose(args.verbose)

    if args.clear:
        def clear_logs():
            try:
                remove_debug_file()
            except FileNotFoundError:
                pass

        # Start file removal in a separate thread (non-blocking)
        threading.Thread(target=clear_logs, daemon=True).start()

    return LoggerSingleton.init_logger(os.getenv("LOGGING_LEVEL", "DEBUG"))
