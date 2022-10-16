import yaml
from command_lib.utils.log import logger

class Parser:
    """class to parse the query mapping file
    """
    def __init__(self, path:str) -> None:
        """constructor for the parser class
        """
        self.config_path = path

    
    def read_yaml(self) -> dict:
        """read the yaml file and load in dict

        Returns:
            dict: dict with mapping
        """
        with open(self.config_path, "r") as stream:
            try:
                conf = yaml.safe_load(stream)
            except yaml.YAMLError as err:
                logger.error("Yaml file could not be parsed")
                logger.error(err)
                exit(5)
    
        return conf