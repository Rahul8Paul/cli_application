from command_lib.dataset_io.abstract_io import AbstractIO
from sqlalchemy import create_engine, engine
from command_lib.utils.log import logger
from urllib.parse import quote
import pandas as pd

class MySqlIO(AbstractIO):

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.driver_name = "mysql"
    

    def _validate_conn_url(self, conn_url: str):
        """method to validate conn url

        Args:
            conn_url (str): conn url to connect with db
        """
        if conn_url is None:
            logger.error("connection url must be present to connect with DB")
            exit(1)
        if conn_url.count("@") != 1 or self.driver_name not in conn_url:
            logger.error("Connection url format is not correct")
            exit(1)

    
    def _get_connection_engine(self, conn_url: str, password: str = None) -> None:
        """method to create connection engine for mysql

        Args:
            conn_url (str): connection url
            password (str, optional): mention password separately incase it have special character. Defaults to None.
        """
        self._validate_conn_url(conn_url=conn_url)
        if password is not None and "?" not in conn_url:
            logger.error("Connection url should contain ? which will be replaced with the password mainly used for password with special char")
            exit(2)
        if password is not None:
            conn_url = conn_url.replace("?", quote(password))
        self.conn_engine = create_engine(engine.make_url(conn_url), pool_pre_ping=True)


    def query_table(self, query: str, **kwargs) -> pd.DataFrame:
        """run query on mysql table

         Args:
            query (str): query string

        Returns:
            pd.DataFrame: read mysql data in a dataframe
        """
        if "conn_url" not in kwargs:
            logger.error("conn_url is mandetory for reading data from mysql")
            exit(3)
        if "password" in kwargs:
            self._get_connection_engine(kwargs["conn_url"], kwargs["password"])
        else:
            self._get_connection_engine(kwargs["conn_url"])
        self._validate_query(query=query)
        logger.info(f"Trying to run query on mysql db")
        logger.info(f"query : {query}")
        df = pd.read_sql(query, con=self.conn_engine)
        return df


    def write_dataset(self, data: pd.DataFrame, mode: str = "replace", **kwargs) -> None:
        """method to write back a datafrme to mysql

        Args:
            data (pd.DataFrame): pd datafrmae to write
            mode (str, optional): mode of writing replace/append. Defaults to "replace".
        """
        if "table_name" not in kwargs:
            logger.error("table_name is mandetory for reading data from mysql")
            exit(3)
        if "conn_url" not in kwargs:
            logger.error("conn_url is mandetory for reading data from mysql")
            exit(3)
        if "password" in kwargs:
            self._get_connection_engine(kwargs["conn_url"], kwargs["password"])
        else:
            self._get_connection_engine(kwargs["conn_url"])
        logger.info(f"Writing data to the mysql db {kwargs['table_name']}")
        data.to_sql(kwargs["table_name"], con=self.conn_engine, if_exists=mode)
        logger.info("Write completed successfully...")
        


