# Extract and Upload FoodSales Data to Postgres Database

This project was developed as a practice exercise in refactoring code and adhering to best practice standards.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Used](#technology-used)
3. [Setup and Installation](#setup-and-installation)
4. [Steps](#steps)
5. [Usage](#usage)
6. [Project Structure](#project-structure)
7. [Features](#features)
8. [License](#license)

## Project Overview

This project involves extracting data from an Excel file and loading it into a PostgreSQL database. It includes a set of scripts and configuration files organized into directories for better management and readability.

## Technology Used

- **Python**: For scripting and processing.
- **pandas**: For data manipulation and reading Excel files.
- **openpyxl**: For handling Excel files.
- **psycopg2**: PostgreSQL database adapter for Python.
- **PyYAML**: For parsing YAML configuration files.
- **dotenv**: For managing environment variables.
- **PostgreSQL**: Database system for storing and managing the data.

## Setup and Installation

1. **Clone the Repository**: Clone this repository to your local machine.

    ```bash
    git clone https://github.com/MekWiset/ExcelToPostgres_CodeQuality_MiniProject.git
    cd path/to/ExcelToPostgres_CodeQuality_MiniProject/
    ```

2. **Create and Activate a Virtual Environment**: Create a virtual environment and activate it.

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies**: Install the required Python packages.

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Environment Variables**: Create a `.env` file in the root directory and add your PostgreSQL connection details. Example:

    ```plaintext
    PGFS_DBNAME=your_db_name
    PGFS_USER=your_db_user
    PGFS_PASSWORD=your_db_password
    PGFS_PORT=your_db_port
    ```

5. **Set PYTHONPATH**: Export the `PYTHONPATH` to include the project directory.

    ```bash
    export PYTHONPATH=path/to/ExcelToPostgres_CodeQuality_MiniProject/
    ```

6. **Update Configuration**: Edit `config.yaml` to match your file paths and other configuration settings.


## Steps
1. **Data Extraction**: The `DataExtractor` class handles the extraction of data from Excel or CSV files based on the configuration provided.
2. **Data Loading**: The `PostgresLoader` class takes the extracted data and loads it into the PostgreSQL database using SQL queries specified in configuration files.
3. **Configuration Management**: The `ConfigParser` class reads and manages configuration details from the YAML file to guide the ETL process.

## Usage
1. **Prepare Your Configuration**:
    Make sure you have followed the setup instructions thoroughly before running the script.

2. **Run the Script**:
    Execute the main script to start the process:
    ```bash
    python3 jobs/xlsx_to_postgres.py
    ```

## Project Structure
- **`README.md`**: Provides an overview and instructions for the project.
- **`config.yaml`**: Configuration file that specifies paths, formats, and schema definitions.
- **`datasets/`**: Contains data files for processing, such as Excel files.
- **`helpers/`**: SQL scripts for creating and inserting data into PostgreSQL tables.
  - **`create_table_foodsales.sql`**: SQL script to create the `foodsales` table in the PostgreSQL database.
  - **`insert_into_foodsales.sql`**: SQL script to insert data into the `foodsales` table.
- **`jobs/`**: Contains scripts for data processing tasks.
  - **`xlsx_to_postgres.py`**: Main script for extracting data from an Excel file and loading it into PostgreSQL.
- **`plugins/`**: Contains modular components of the ETL pipeline.
  - **`extract/`**: Contains classes for extracting data from files.
    - **`data_extractor.py`**: Contains the `DataExtractor` class.
  - **`load/`**: Contains classes for loading data into the database.
    - **`data_loader.py`**: Contains the `PostgresLoader` class.
  - **`transform/`**: Contains transformation logic (currently empty).
  - **`utils/`**: Utility modules for configuration and other helper functions.
    - **`configparser.py`**: Contains the `ConfigParser` class for handling YAML configurations.
- **`requirements.txt`**: Lists the Python packages required for the project.

## Features
- **Support for Multiple Data Formats**: Handles both CSV and Excel file formats.
- **Configurable Schema Management**: Schema details are managed via YAML configuration files.
- **Robust Logging**: Uses Python's logging module to track the ETL process and errors.
- **Flexible Class-Based Architecture**: Easily add or drop features by modifying classes.
- **Environment Variable Management**: Includes a `.env` file for securely storing crucial information, such as database passwords.



## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.