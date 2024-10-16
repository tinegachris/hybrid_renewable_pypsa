import pandas as pd
import os
from logger_setup import LoggerSetup

class DataLoader:
    def __init__(self, data_folder):
        self.data_folder = data_folder
        self.logger = LoggerSetup.setup_logger('DataLoader')

    def _sanitize_file_name(self, file_name):
        allowed_files = {'buses.csv', 'generators.csv', 'storage_units.csv', 'loads.csv', 'lines.csv', 'transformers.csv', 'links.csv'}
        if file_name not in allowed_files:
            raise ValueError(f"Invalid file name: {file_name}")
        return file_name

    def read_csv(self, file_name):
        try:
            sanitized_file_name = self._sanitize_file_name(file_name)
            file_path = os.path.join(self.data_folder, sanitized_file_name)
            return pd.read_csv(file_path)
        except ValueError as ve:
            self.logger.error(ve)
        except FileNotFoundError:
            self.logger.error(f"File {file_name} not found in the data folder.")
        except pd.errors.EmptyDataError:
            self.logger.error(f"File {file_name} is empty.")
        except Exception as e:
            self.logger.error(f"An error occurred while reading file {file_name}.")
            self.logger.error(e)
        return pd.DataFrame()