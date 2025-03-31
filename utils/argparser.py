import argparse
from utils import getName

class ParserWrapper():
    """
    Wrapper around argparse for easier use in the bot.
    ---
    Attributes:
        _define_arguments `func`: function to define arguments.
        parse_args `func`: function to return the command line arguments.
    """
    def __init__(self) -> None:
        self.name: str = getName()
        self.parser = argparse.ArgumentParser(
            prog=self.name,
            description="This is the discord bot CLI interface.",
            epilog="Do `help` or `help all` anytime for help"
        )

        # Define arguments once during initialization
        self._define_arguments()

    def _define_arguments(self):
        self.parser.add_argument(
            '-v', '--verbose', action='store_true', 
            help="Enable verbose output for debugging or logging"
        )

        self.parser.add_argument(
            '-l', '--logfile', type=str, 
            help="Path to the log file where bot logs will be saved"
        )

        self.parser.add_argument(
            '-c', '--clear', action='store_true', 
            help="Enable clearing all logs and data at start of program to remove old data"
        )

    def parse_args(self):
        """parse and return the command line arguments."""
        return self.parser.parse_args()
