from typing import Dict
import pandas as pd
import psycopg2
import logging

from plugins.utils.configparser import ConfigParser

logging.basicConfig(format="%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]", datefmt="%d/%m/%Y %I:%M:%S %p", level=logging.INFO)


class DataLoader():

    """
    Base class for loading data.

    Args:
        sql_path (str): The path to the SQL file.

    Methods:
        read_sql_file(self, sql_path: str) -> str:
            Reads and returns the contents of an SQL file as a string.
    """

    def __init__(self) -> None:
        pass

    def read_sql_file(self, sql_path: str) -> str:
        """Reads and returns the contents of an SQL file as a string."""
        with open(sql_path, 'r') as file:
            return file.read()
    

class PostgresLoader(DataLoader):

    """
    Loads data into a PostgreSQL database.

    Args:
        pgconn_params (Dict[str, str]): Dictionary containing PostgreSQL connection parameters.
        config_parser (ConfigParser): An instance of ConfigParser used for schema retrieval.

    Attributes:
        pg_conn (Dict[str, str]): PostgreSQL connection parameters.
        config_parser (ConfigParser): ConfigParser instance for schema management.

    Methods:
        create_table(self, create_table_sql_path: str) -> None:
            Creates a table in the PostgreSQL database using the SQL file specified.
        
        insert_data(self, dataframe: pd.DataFrame, file_name: str, insert_data_sql_path: str) -> None:
            Inserts data into the PostgreSQL table using a DataFrame and an SQL file.
    """

    def __init__(self, pgconn_params: Dict[str, str], config_parser: ConfigParser) -> None:
        super().__init__()
        self.pg_conn = pgconn_params
        self.config_parser = config_parser

    def create_table(self, create_table_sql_path: str) -> None:
        """Creates a table in the PostgreSQL database using the SQL file specified."""
        create_table_query = self.read_sql_file(sql_path=create_table_sql_path)

        try:
            conn = psycopg2.connect(**self.pg_conn)
            with conn.cursor() as cur:
                cur.execute(create_table_query)
                conn.commit()
                logging.info("Table created successfully.")

        except Exception as e:
            logging.error(f"An error occurred while creating the table: {e}")
            raise

        finally:
            conn.close()

    def insert_data(self, dataframe: pd.DataFrame, file_name: str, insert_data_sql_path: str) -> None:
        """Inserts data into the PostgreSQL table using a DataFrame and an SQL file."""
        schema = self.config_parser.get_schema(file_name)
        column_names = [col["column_name"] for col in schema]

        try:
            conn = psycopg2.connect(**self.pg_conn)
            
            with conn.cursor() as cur:
                data_to_insert = [
                    tuple(row[col] for col in column_names)
                    for _, row in dataframe.iterrows()
                ]
                insert_query = self.read_sql_file(sql_path=insert_data_sql_path)

                # Insert data using executemany
                cur.executemany(insert_query, data_to_insert)
                conn.commit()

                logging.info("Data inserted successfully.")

        except Exception as e:
            logging.error(f"An error occurred while inserting data: {e}")
            raise

        finally:
            conn.close()

