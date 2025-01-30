import pandas as pd
import os
from pathlib import Path
from typing import Dict
from .logger_setup import Logger_Setup

class Data_Loader:
    def __init__(self, data_folder: str):
        self.data_folder = Path(data_folder)
        self.logger = Logger_Setup.setup_logger('DataLoader')

    def _sanitize_file_name(self, file_name):
        allowed_files = {'buses.csv', 'generators.csv', 'storage_units.csv', 'loads.csv', 'lines.csv', 'transformers.csv', 'links.csv'}
        if file_name not in allowed_files:
            raise ValueError(f"Invalid file name: {file_name}")
        return file_name

    def read_csv(self, file_name):
        try:
            sanitized_file_name = self._sanitize_file_name(file_name)
            file_path = self.data_folder / sanitized_file_name
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

    def load_profile(self, profile_id):
        try:
            file_path = self.data_folder / f'load_profiles/{profile_id}.csv'
            return pd.read_csv(file_path, index_col='time', parse_dates=True)
        except FileNotFoundError:
            self.logger.error(f"Profile {profile_id} not found.")
        except pd.errors.EmptyDataError:
            self.logger.error(f"Profile {profile_id} is empty.")
        except Exception as e:
            self.logger.error(f"An error occurred while reading profile {profile_id}.")
            self.logger.error(e)
        return pd.DataFrame()

    def load_dynamic_constraints(self) -> pd.DataFrame:
        try:
            return pd.read_csv(self.data_folder / "dynamic_constraints.csv")
        except FileNotFoundError:
            self.logger.error("File dynamic_constraints.csv not found.")
        except pd.errors.EmptyDataError:
            self.logger.error("File dynamic_constraints.csv is empty.")
        except Exception as e:
            self.logger.error("An error occurred while reading dynamic_constraints.csv.")
            self.logger.error(e)
        return pd.DataFrame()

    def load_constraint_profiles(self) -> Dict[str, pd.Series]:
        try:
            df = pd.read_csv(self.data_folder / "constraint_profiles.csv", parse_dates=["time"])
            return {cid: grp.set_index("time")["value"] for cid, grp in df.groupby("constraint_id")}
        except FileNotFoundError:
            self.logger.error("File constraint_profiles.csv not found.")
        except pd.errors.EmptyDataError:
            self.logger.error("File constraint_profiles.csv is empty.")
        except Exception as e:
            self.logger.error("An error occurred while reading constraint_profiles.csv.")
            self.logger.error(e)
        return {}

    def load_component_constraints(self) -> pd.DataFrame:
        try:
            return pd.read_csv(self.data_folder / "component_constraints.csv")
        except FileNotFoundError:
            self.logger.error("File component_constraints.csv not found.")
        except pd.errors.EmptyDataError:
            self.logger.error("File component_constraints.csv is empty.")
        except Exception as e:
            self.logger.error("An error occurred while reading component_constraints.csv.")
            self.logger.error(e)
        return pd.DataFrame()

    def load_storage_tech_library(self) -> pd.DataFrame:
        """Load storage technology specifications"""
        try:
            return pd.read_csv(
                self.data_folder / "storage_tech_library.csv",
                index_col="type"
            )
        except FileNotFoundError:
            self.logger.error("File storage_tech_library.csv not found.")
        except pd.errors.EmptyDataError:
            self.logger.error("File storage_tech_library.csv is empty.")
        except Exception as e:
            self.logger.error("An error occurred while reading storage_tech_library.csv.")
            self.logger.error(e)
        return pd.DataFrame()

    def load_transformer_tech_library(self) -> pd.DataFrame:
        """Load transformer technology specifications"""
        try:
            return pd.read_csv(
                self.data_folder / "transformer_tech_library.csv",
                index_col="type"
            )
        except FileNotFoundError:
            self.logger.error("File transformer_tech_library.csv not found.")
        except pd.errors.EmptyDataError:
            self.logger.error("File transformer_tech_library.csv is empty.")
        except Exception as e:
            self.logger.error("An error occurred while reading transformer_tech_library.csv.")
            self.logger.error(e)
        return pd.DataFrame()

    def load_generator_tech_library(self) -> pd.DataFrame:
        """Load generator technology specifications"""
        try:
            return pd.read_csv(
                self.data_folder / "generator_tech_library.csv",
                index_col="type"
            )
        except FileNotFoundError:
            self.logger.error("File generator_tech_library.csv not found.")
        except pd.errors.EmptyDataError:
            self.logger.error("File generator_tech_library.csv is empty.")
        except Exception as e:
            self.logger.error("An error occurred while reading generator_tech_library.csv.")
            self.logger.error(e)
        return pd.DataFrame()
