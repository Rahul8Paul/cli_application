from abc import abstractmethod
from asyncio.log import logger
import pandas as pd

class AbstractIO:
    """Abstract class for IO
    """

    def __init__(self) -> None:
        """Constructor of the class
        """
        pass

    def _validate_query(self, query: str) -> None:
        """method to see any potential threat in the query

        Args:
            query (str): query string
        """
        if "insert" in query.lower() or "overwrite" in query.lower() or "delete" in query.lower():
            logger.critical("Seems like a harmful query. Please validate")
            exit(4)
        if query.count(";") > 1 or len(query.rstrip().split(";")) > 1:
            logger.critical("multiple query are not supported for security reasons. Please validate")
            exit(4)


    @abstractmethod
    def query_table(self, query: str, **kwargs) -> pd.DataFrame:
        """Abstract method to run query to a target DB

         Args:
            query (str): query string

        Returns:
            pd.DataFrame: Returns a pandas df
        """

    @abstractmethod
    def write_dataset(self, data: pd.DataFrame, mode: str = "replace", **kwargs) -> None:
        """abstract method to 

        Args:
            data (pd.DataFrame): dataframe to write data to a FS/DB
            mode (str, optional): mode of write. Defaults to "replace".
        """

