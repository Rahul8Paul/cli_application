import importlib
from command_lib.parser.parse_config import Parser
from command_lib.utils.log import logger
from pkg_resources import resource_filename


class DatasetFactory:
    """Factory class to create dataset object dynamically based on config to support multiple data source.
    """

    def __init__(self, source_type: str = "mysql") -> None:
        """constructor method for dataset factory

        Args:
            source_type (str, optional): source db type e.g mysql/postres/mssql/hive. Defaults to "mysql".
        """
        self.config = Parser(resource_filename("command_lib", "/factory/dataset_mapping.yaml")).read_yaml()["dataset_mapping"]
        if source_type.lower() not in self.config:
            logger.error(f"Source db type : {source_type} is not supported")
            exit(8)
        class_module = importlib.import_module(self.config[source_type]["package"])
        self.data_class = getattr(class_module, self.config[source_type]["class"])