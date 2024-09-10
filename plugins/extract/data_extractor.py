from typing import Optional, List
import pandas as pd
import logging

logging.basicConfig(format="%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]", datefmt="%d/%m/%Y %I:%M:%S %p", level=logging.INFO)


class DataExtractor():

    """
    Extracts data from source files.

    Args:
        file_path (str): The path to the data file.
        format (str): The format of the data file ("csv" or "xlsx").

    Methods:
        is_excel(self) -> bool:
            Checks if the file format is Excel (.xlsx).
        
        is_csv(self) -> bool:
            Checks if the file format is CSV (.csv).
        
        read_data(self, sheet_name: Optional[str] = None, header: int = 1, skiprows: Optional[List[int]] = None) -> pd.DataFrame:
            Reads data from the specified file and returns it as a pandas DataFrame.
    """
    
    def __init__(self, file_path: str, format: str) -> None:
        self.file_path = file_path
        self.format = format

    @property
    def is_excel(self) -> bool:
        return self.format.lower() == "xlsx"

    @property
    def is_csv(self) -> bool:
        return self.format.lower() == "csv"
    
    def read_data(self, sheet_name: Optional[str] = None, header: int = 1, skiprows: Optional[List[int]] = None) -> pd.DataFrame:
        """Reads data from the specified file and returns it as a pandas DataFrame."""
        try:
            if self.is_excel:
                dataframe = pd.read_excel(self.file_path, sheet_name=sheet_name, header=header, skiprows=skiprows)
            elif self.is_csv:
                dataframe = pd.read_csv(self.file_path, header=header, skiprows=skiprows)
            else:
                logging.error("Unsupported file format. Only 'csv' and 'xlsx' are acceptable.")
                return None
            logging.info(f"Data read successfully from {self.format} file.")
            return dataframe
        
        except FileNotFoundError:
            logging.error(f"The file '{self.file_path}' was not found.")
            raise
        
        except Exception as e:
            logging.error(f"An error occurred while reading the data: {e}")
            raise

