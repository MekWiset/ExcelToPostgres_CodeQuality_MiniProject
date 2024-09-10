import yaml
import logging

logging.basicConfig(format="%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]", datefmt="%d/%m/%Y %I:%M:%S %p", level=logging.INFO)


class ConfigParser:

    """
    Parses and manages configuration data from a YAML file.

    Args:
        config_path (str): The path to the YAML configuration file.

    Attributes:
        config (str): The path to the YAML configuration file.
        config_data (dict): The loaded configuration data.

    Methods:
        load_config(self) -> None:
            Loads configuration data from the YAML file.
        
        get_info(self, file_name: str, info: str) -> str:
            Retrieves the file path or information for a given file name from the configuration.

        get_schema(self, file_name: str) -> list:
            Retrieves the schema definition for a given file name.
    """

    def __init__(self, config_path: str) -> None:
        self.config = config_path
        self.load_config()

    def load_config(self) -> None:
        """Loads configuration data from the YAML file."""
        with open(self.config, "r") as file:
            self.config_data = yaml.safe_load(file)

    def get_info(self, file_name: str, info: str) -> str:
        """Retrieves the file path or information for a given file name from the configuration."""
        return self.config_data["files"][file_name][info]
    
    def get_schema(self, file_name: str) -> list:
        """Retrieves the schema definition for a given file name."""
        try:
            schema = self.config_data["files"][file_name]["schema"]
            schema_list = []
            for schema_data in schema:
                column_name = schema_data.get("column_name")
                data_type = schema_data.get("data_type")
                schema_list.append({"column_name": column_name, "data_type": data_type})
            return schema_list
        except KeyError as e:
            logging.error(f"Missing key in configuration: {e}")
            raise
    
        except Exception as e:
            logging.error(f"An unexpected error occurred while retrieving schema: {e}")
            raise


class PostgresConfigParser(ConfigParser):

    """
    Parses and manages PostgreSQL-specific configuration data from a YAML file.

    Args:
        config_path (str): The path to the YAML configuration file.

    Attributes:
        config (str): The path to the YAML configuration file.
        config_data (dict): The loaded configuration data.

    Methods:
        get_info(self, table_name: str, info: str) -> str:
            Retrieves information from the "postgres" section for a given table name.

        get_schema(self, table_name: str) -> list:
            Retrieves the schema definition for a given PostgreSQL table.
    """

    def __init__(self, config_path: str) -> None:
        super().__init__(config_path)

    def get_info(self, table_name: str, info: str) -> str:
        """Retrieves information from the "postgres" section for a given table name."""
        return self.config_data["Postgres"][table_name][info]

    def get_schema(self, table_name: str) -> list:
        """Retrieves the schema definition for a given PostgreSQL table."""
        try:
            schema = self.config_data["Postgres"][table_name]["schema"]
            schema_list = []
            for schema_data in schema:
                column_name = schema_data.get("column_name")
                data_type = schema_data.get("data_type")
                nullable = schema_data.get("nullable")
                schema_list.append({"column_name": column_name, "data_type": data_type, "nullable": nullable})
            return schema_list
        
        except KeyError as e:
            logging.error(f"Missing key in configuration: {e}")
            raise
    
        except Exception as e:
            logging.error(f"An unexpected error occurred while retrieving schema: {e}")
            raise
