import formatter
import logging
class Logger:
    """Class for logging
    """

    def __init__(self) -> None:
        """constructor for the logger
        """
        logger = logging.getLogger(__name__)
        ch = logging.StreamHandler()
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        self.logger = logger

    def error(self, msg: str):
        """method to log error

        Args:
            msg (str): log string
        """
        self.logger.error(str(msg))

    def info(self, msg: str):
        """method to log info

        Args:
            msg (str): log string
        """
        self.logger.info(str(msg))

    def debug(self, msg: str):
        """method to log debug msg

        Args:
            msg (str): log string
        """
        self.logger.debug(str(msg))

    def critical(self, msg: str):
        """method to log error

        Args:
            msg (str): log string
        """
        self.logger.critical(str(msg))

logger = Logger()
