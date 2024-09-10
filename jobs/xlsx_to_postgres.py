from dotenv import load_dotenv
from pathlib import Path
import os
import logging

from plugins.extract.data_extractor import DataExtractor
from plugins.load.data_loader import PostgresLoader
from plugins.utils.configparser import ConfigParser

logging.basicConfig(format="%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]", datefmt="%d/%m/%Y %I:%M:%S %p", level=logging.INFO)


def main():
    
    """
    Orchestrates the process of extracting data from an Excel file and loading it into a PostgreSQL database.

    1. Initializes the data extractor and PostgreSQL loader with configuration and file paths.
    2. Loads environment variables for PostgreSQL connection parameters.
    3. Extracts data from a specified sheet in the Excel file, skipping specific rows.
    4. Creates the necessary database table and inserts the extracted data into the PostgreSQL database.
    """
    
    try:

        logging.info("Execution started.")

        # Initialize local module
        config_path = "config.yaml"
        conf = ConfigParser(config_path)

        source_path = conf.get_info(file_name="challenge_data", info="path")
        source_format = conf.get_info(file_name="challenge_data", info="format")
        extractor = DataExtractor(file_path=source_path, format=source_format)

        dotenv_path = Path(".env")
        load_dotenv(dotenv_path=dotenv_path)
        PG_CONN = {
            "dbname": os.getenv("PGFS_DBNAME"),
            "user": os.getenv("PGFS_USER"),
            "password": os.getenv("PGFS_PASSWORD"),
            "port": os.getenv("PGFS_PORT")
        }
        pgloader = PostgresLoader(pgconn_params=PG_CONN, config_parser=conf)

        # Extract data
        try:
            sheet_name = conf.get_info(file_name="challenge_data", info="sheet")
            rows_to_skip = conf.get_info(file_name="challenge_data", info="skiprows")
            data = extractor.read_data(sheet_name=sheet_name, skiprows=rows_to_skip)

        except Exception as e:
            logging.error(f"Failed to extract data: {e}")
            raise

        # Load data
        try:
            create_table_sql_path = conf.get_info(file_name="create_foodsales_table_script", info="path")
            insert_data_sql_path = conf.get_info(file_name="insert_into_foodsales_script", info="path")
            pgloader.create_table(create_table_sql_path=create_table_sql_path)
            pgloader.insert_data(dataframe=data, file_name="challenge_data", insert_data_sql_path=insert_data_sql_path)

        except Exception as e:
            logging.error(f"Failed to load data into PostgreSQL: {e}")
            raise

        logging.info("Execution complete.")

    except Exception as e:
        logging.error("Execution stopped.")


if __name__ == "__main__":
    main()