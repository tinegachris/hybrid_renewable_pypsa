import pandas as pd
from pathlib import Path
from typing import Dict
from .logger_setup import LoggerSetup

class DataLoader:
    def __init__(self, data_folder: str):
        self.data_folder = Path(data_folder)
        self.logger = LoggerSetup.setup_logger('DataLoader')
        self._tech_libraries = {}

    def read_csv(self, relative_path: str) -> pd.DataFrame:
        """
        Read a CSV file given a relative path from the data folder.
        """
        file_path = self.data_folder / relative_path
        try:
            return pd.read_csv(file_path)
        except FileNotFoundError:
            self.logger.error(f"File {relative_path} not found in {self.data_folder}.")
        except pd.errors.EmptyDataError:
            self.logger.error(f"File {relative_path} is empty.")
        except Exception as e:
            self.logger.error(f"An error occurred while reading file {relative_path}: {e}")
        return pd.DataFrame()

    def load_component(self, file_name: str) -> pd.DataFrame:
        """
        Load a component file from the 'components' folder.
        """
        return self.read_csv(f"components/{file_name}")

    def load_tech_library(self, file_name: str) -> pd.DataFrame:
        """
        Load a technology library file from the 'tech_libraries' folder.
        """
        return self.read_csv(f"tech_libraries/{file_name}")

    def load_constraint(self, file_name: str) -> pd.DataFrame:
        """
        Load a constraint file from the 'constraints' folder.
        """
        return self.read_csv(f"constraints/{file_name}")

    def load_profile(self, profile_id: str, profile_type: str) -> pd.DataFrame:
        """
        Load a time-series profile from a subfolder of 'profiles'.
        For example, profile_type can be 'load_profiles', 'generator_profiles',  storage_profiles or 'grid_profiles'.
        The CSV file is expected to be named {profile_id}.csv.
        """
        file_path = self.data_folder / "profiles" / profile_type / f"{profile_id}.csv"
        try:
            df = pd.read_csv(file_path, index_col=0)
            if 'snapshot' in df.columns:
                df['snapshot'] = pd.to_datetime(df['snapshot'], format='%Y-%m-%d %H:%M:%S')
                df.set_index('snapshot', inplace=True)
            df.index.name = 'snapshot'
            return df
        except FileNotFoundError:
            self.logger.error(f"Profile {profile_id} not found in profiles/{profile_type}.")
        except pd.errors.EmptyDataError:
            self.logger.error(f"Profile {profile_id} in profiles/{profile_type} is empty.")
        except Exception as e:
            self.logger.error(f"An error occurred while reading profile {profile_id} from profiles/{profile_type}: {e}")
        return pd.DataFrame()

    def load_metadata(self, file_name: str) -> pd.DataFrame:
        """
        Load a metadata file from the 'metadata' folder.
        """
        return self.read_csv(f"metadata/{file_name}")

    def load_documentation(self, file_name: str) -> str:
        """
        Load a text-based documentation file from the 'documentation' folder.
        """
        file_path = self.data_folder / "documentation" / file_name
        try:
            return file_path.read_text()
        except FileNotFoundError:
            self.logger.error(f"Documentation file {file_name} not found in the documentation folder.")
        except Exception as e:
            self.logger.error(f"An error occurred while reading documentation file {file_name}: {e}")
        return ""

    def load_dynamic_constraints(self) -> pd.DataFrame:
        """
        Load dynamic constraints from the 'constraints' folder.
        """
        return self.read_csv("constraints/dynamic_constraints.csv")

    def load_constraint_profiles(self) -> Dict[str, pd.Series]:
        """
        Load constraint profiles from the 'constraints' folder.
        Expects a CSV file with a 'constraint_id' column and a 'time' column.
        """
        try:
            df = pd.read_csv(
                self.data_folder / "constraints/constraint_profiles.csv",
                parse_dates=["time"],
                index_col="time"
            )
            return {cid: grp["value"] for cid, grp in df.groupby("constraint_id")}
        except FileNotFoundError:
            self.logger.error("File constraint_profiles.csv not found in the constraints folder.")
        except pd.errors.EmptyDataError:
            self.logger.error("File constraint_profiles.csv in the constraints folder is empty.")
        except Exception as e:
            self.logger.error(f"An error occurred while reading constraint_profiles.csv: {e}")
        return {}

    def load_component_constraints(self) -> pd.DataFrame:
        """
        Load component constraints. If these are stored in the components folder,
        adjust the path accordingly.
        """
        return self.read_csv("components/component_constraints.csv")

    def load_storage_tech_library(self) -> pd.DataFrame:
        """
        Load storage technology specifications from the tech_libraries folder.
        """
        try:
            return pd.read_csv(
                self.data_folder / "tech_libraries/storage_tech_library.csv",
                index_col="type"
            )
        except FileNotFoundError:
            self.logger.error("File storage_tech_library.csv not found in tech_libraries.")
        except pd.errors.EmptyDataError:
            self.logger.error("File storage_tech_library.csv in tech_libraries is empty.")
        except Exception as e:
            self.logger.error(f"An error occurred while reading storage_tech_library.csv: {e}")
        return pd.DataFrame()

    def load_transformer_tech_library(self) -> pd.DataFrame:
        """
        Load transformer technology specifications from the tech_libraries folder.
        """
        try:
            return pd.read_csv(
                self.data_folder / "tech_libraries/transformer_tech_library.csv",
                index_col="type"
            )
        except FileNotFoundError:
            self.logger.error("File transformer_tech_library.csv not found in tech_libraries.")
        except pd.errors.EmptyDataError:
            self.logger.error("File transformer_tech_library.csv in tech_libraries is empty.")
        except Exception as e:
            self.logger.error(f"An error occurred while reading transformer_tech_library.csv: {e}")
        return pd.DataFrame()

    def load_generator_tech_library(self) -> pd.DataFrame:
        """
        Load generator technology specifications from the tech_libraries folder.
        """
        try:
            return pd.read_csv(
                self.data_folder / "tech_libraries/generator_tech_library.csv",
                index_col="type"
            )
        except FileNotFoundError:
            self.logger.error("File generator_tech_library.csv not found in tech_libraries.")
        except pd.errors.EmptyDataError:
            self.logger.error("File generator_tech_library.csv in tech_libraries is empty.")
        except Exception as e:
            self.logger.error(f"An error occurred while reading generator_tech_library.csv: {e}")
        return pd.DataFrame()
