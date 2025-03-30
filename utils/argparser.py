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
            epilog="Good luck understanding that haha"
        )

        # Define arguments once during initialization
        self._define_arguments()

    def _define_arguments(self):
        # Verbose flag for logging/debugging
        self.parser.add_argument(
            '-v', '--verbose', action='store_true', 
            help="Enable verbose output for debugging or logging"
        )

        # Optional log file path
        self.parser.add_argument(
            '-l', '--logfile', type=str, 
            help="Path to the log file where bot logs will be saved"
        )

    def parse_args(self):
        """Parse and return the command line arguments."""
        return self.parser.parse_args()
