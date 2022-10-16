from asyncio.log import logger
from pkg_resources import resource_filename
from command_lib.parser.parse_config import Parser
from datetime import date
from command_lib.factory.dataset_factory import DatasetFactory
import pandas as pd

class Command:
    """Main class to build the command functionality
    """

    def __init__(self, package_name: str = "command_lib", path_config: str = "query_mapping.yaml") -> None:
        """Constructor for command class

        Args:
            package_name (str, optional): package name where the config file is present. Defaults to "command_lib".
            path_config (str, optional): config file path inside the package. Defaults to "query_mapping.yaml".
        """
        self.config_file = resource_filename(package_name, path_config)
        self.query_config = Parser(self.config_file).read_yaml()["query"]

    
    def _is_query_exists(self, query_name: str) -> bool:
        """method to check if the query exists in the system

        Args:
            query (str): name of the query to run

        Returns:
            bool: return true or false based on presence
        """
        if query_name.lower() in self.query_config:
            return True
        else:
            return False


    def _validate_granularity(self, granularity: str) -> None:
        """method to validate if the granularity is supported

        Args:
            granularity (str): string describing granularity
        """
        #TODO: set a granularity mapping config file to enable diff granularity. For this case we consider only daily
        granularity_list = {"daily":True}
        if granularity not in granularity_list:
            logger.error(f"Given granularity {granularity} currently not supported")
            exit(7)


    def _get_date_list(self, start: date, end: date) -> list:
        """get the list of dates between tow dates

        Args:
            start (date): start date
            end (date): end date

        Returns:
            list: list of dates between start and end date
        """
        list_dates = pd.date_range(start=start, end=end, freq='D')
        logger.info(f"list of dates : {list_dates}")
        return list_dates

    
    def _execute_daily_query(self, io_obj, query_name: str, category: str, date: date, conn_url: str) -> pd.DataFrame:
        """method to run query for each day

        Args:
            io_obj (_type_): generic io obj for table query
            query_name (str): name of the query
            category (str): category to run the query
            date (date): date to run the query
            conn_url (str): conn_url sqlalchemy like to connect to db

        Returns:
            pd.DataFrame: _description_
        """
        query_str = self.query_config[query_name]
        additiona_filter_str= f" where date(InvoiceDate) = '{date.strftime('%Y-%m-%d')}' and Description like '%{category}%' "
        idx = query_str.index("group by")
        query_str = query_str[:idx] + additiona_filter_str + query_str[idx:]
        df = io_obj.query_table(query_str, conn_url=conn_url)
        return df


    def execute(self, query_name: str, granularity: str, start: date, end: date, category: str, conn_url: str, **kwargs):
        """entry method to run the cli functionality of the command class.

        Args:
            query_name (str): name of the query
            granularity (str): granularity to run the query
            start (date): start date of the window
            end (date): end date of the window
            category (str): category to run the query
            conn_url (str): conn_url sqlalchemy like to connect to db
        """
        if not self._is_query_exists(query_name=query_name):
            logger.error("Query is not present in the list of known query")
            exit(6)
        self._validate_granularity(granularity=granularity)
        list_dates = self._get_date_list(start, end)
        io_obj = DatasetFactory("mysql").data_class()
        df = pd.DataFrame()
        for dt in list_dates:
            df_daily = self._execute_daily_query(io_obj, query_name=query_name, category=category, date=dt, conn_url=conn_url)
            df_daily["date"] = dt.strftime("%Y-%m-%d")
            df = pd.concat([df, df_daily])
        print(df.head())
        


        
        

