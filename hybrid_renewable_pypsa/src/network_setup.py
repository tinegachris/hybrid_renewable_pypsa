import pypsa
import pandas as pd
from typing import Optional
from pathlib import Path
from hybrid_renewable_pypsa.src.data_loader import DataLoader
from hybrid_renewable_pypsa.src.logger_setup import LoggerSetup

class NetworkSetupError(Exception):
    """Custom exception for network setup errors with component context"""
    def __init__(self, message: str, component: Optional[str] = None):
        super().__init__(f"{(component + ': ') if component else ''}{message}")
        self.component = component

class NetworkSetup:
    """
    Network setup class for PyPSA network configuration.
    This class loads technology libraries, components, constraints, and configures
    energy carriers and temporal parameters.
    """

    CARRIER_CONFIG = {
        'AC': {'color': '#1f77b4', 'co2_emissions': 0},
        'DC': {'color': '#ff7f0e', 'co2_emissions': 0},
        'electricity': {'color': '#2ca02c', 'co2_emissions': 0.5},
        'Hydro': {'color': '#17becf', 'co2_emissions': 0},
        'Solar': {'color': '#bcbd22', 'co2_emissions': 0},
        'Grid': {'color': '#d62728', 'co2_emissions': 0.5},
    }

    def __init__(self, data_folder: str) -> None:
        self.data_folder = Path(data_folder)
        self.data_loader = DataLoader(self.data_folder)
        self.network = pypsa.Network()
        self._network_components = {}
        self._tech_libraries = {}
        self._profiles = {}
        self._constraints = {}

        self.logger = LoggerSetup.setup_logger('NetworkSetup')
        self.logger.info("Network setup initialized")

        self._configure_temporal()
        self._configure_network_properties()
        self._load_tech_libraries()
        self._load_components()
        self._load_profiles()
        self._load_constraints()

    def _configure_temporal(self) -> None:
        """Configure time parameters with validation."""
        try:
            snapshots = pd.date_range("2024-01-01", periods=24*7, freq="h")
            self.network.set_snapshots(snapshots)
            self.network.snapshot_weightings[:] = 1.0
            self.logger.info("Temporal configuration successful")
        except Exception as e:
            raise NetworkSetupError(f"Temporal configuration failed: {str(e)}")

    def _configure_network_properties(self) -> None:
        """Set global network properties."""
        self.network.name = "Hybrid_Renewable_System"
        self.network._meta = {
            "version": "1.3",
            "data_sources": ["synthetic"],
            "author": "Chrispine Tinega"
        }
        self.logger.info("Network properties configured")

    def _add_carriers(self) -> None:
        """
        Add energy carriers to the network based on the CARRIER_CONFIG.
        Each carrier is added with its specific properties.
        """
        try:
            for carrier, properties in self.CARRIER_CONFIG.items():
                self.network.add("Carrier", carrier, **properties)
            self.logger.info("Carriers added to the network")
        except Exception as e:
            raise NetworkSetupError(f"Error adding carriers: {str(e)}", component="Carriers")

    def _load_tech_libraries(self) -> None:
        """Load component technology specifications with version checking."""
        tech_files = {
            'storage': "storage_tech_library.csv",
            'transformer': "transformer_tech_library.csv",
            'generator': "generator_tech_library.csv",
            'line_types': "line_types.csv"
        }
        try:
            for tech, file in tech_files.items():
                self._tech_libraries[tech] = self.data_loader.load_tech_library(file).set_index('type')
                self.logger.info(f"Loaded {len(self._tech_libraries[tech])} {tech} tech specs")
            self.logger.info("Technology libraries loaded from CSV files")
        except Exception as e:
            raise NetworkSetupError(f"Error loading tech libraries: {str(e)}", component="Tech Libraries")

    def _load_components(self) -> None:
        """Load network components from the 'components' folder."""
        components = ["buses", "transformers", "lines", "generators", "storage_units", "links", "loads"]
        try:
            for component in components:
                self._network_components[component] = self.data_loader.load_component(f"{component}.csv")
            self.logger.info("Components loaded from CSV files")
        except Exception as e:
            raise NetworkSetupError(f"Error loading components: {str(e)}", component="Components")

    def _load_constraints(self) -> None:
        """Load network constraints from the 'constraints' folder."""
        constraint_files = ["global_constraints.csv", "node_constraints.csv", "branch_constraints.csv"]
        try:
            for file in constraint_files:
                key = file.split('.')[0]
                self._constraints[key] = self.data_loader.load_constraint(file)
            self.logger.info(f"Loaded constraints: {list(self._constraints.keys())}")
        except Exception as e:
            raise NetworkSetupError(f"Error loading constraints: {str(e)}", component="Constraints")

    def _load_profiles(self) -> None:
        """Load time-series profiles for loads, generators, grid, and storage units."""
        profile_types = ["load_profiles", "generator_profiles", "storage_profiles", "grid_profiles"]
        try:
            for profile_type in profile_types:
                profile_folder = self.data_folder / "profiles" / profile_type
                self._profiles[profile_type] = {}
                for profile_file in profile_folder.glob("*.csv"):
                    profile_id = profile_file.stem
                    self._profiles[profile_type][profile_id] = self.data_loader.load_profile(profile_id, profile_type)
            self.logger.info("Profiles loaded from CSV files")
        except Exception as e:
            raise NetworkSetupError(f"Error loading profiles: {str(e)}", component="Profiles")

    def _add_buses(self) -> None:
        """Add buses to the network with voltage levels and optional coordinates."""
        try:
            for _, bus in self._network_components['buses'].iterrows():
                self.network.add("Bus", **bus.to_dict())
            self.logger.info(f"Added {len(self._network_components['buses'])} buses")
        except Exception as e:
            raise NetworkSetupError(f"Error adding buses: {str(e)}", component="Buses")

    def _add_transformers(self) -> None:
        """Add transformers to the network with impedance and tap ratio specifications."""
        try:
            tx_tech_lib = self._tech_libraries['transformer']
            self.network.transformer_types = tx_tech_lib.copy()
            for _, xfmr in self._network_components['transformers'].iterrows():
                if xfmr['type'] not in tx_tech_lib.index:
                    raise NetworkSetupError(f"Transformer type {xfmr['type']} not found in tech library", component="Transformer")
                tech_specs = tx_tech_lib.loc[xfmr['type']]
                transformer_data = {**xfmr.to_dict(), **tech_specs.to_dict()}
                self.network.add("Transformer", **transformer_data)
            self.logger.info(f"Added {len(self._network_components['transformers'])} transformers")
        except Exception as e:
            raise NetworkSetupError(f"Error adding transformers: {str(e)}", component="Transformers")

    def _add_lines(self) -> None:
        """Add transmission lines with type-based parameters."""
        try:
            line_types = self._tech_libraries['line_types']
            self.network.line_types = line_types.copy()

            for _, line in self._network_components['lines'].iterrows():
                if line['type'] not in line_types.index:
                    raise NetworkSetupError(
                        f"Line {line['name']} uses undefined type: {line['type']}",
                        component="Line"
                    )
                line_specs = line_types.loc[line['type']]
                line_data = {**line.to_dict(), **line_specs.to_dict()}
                self.network.add("Line", **line_data)
            self.logger.info(f"Added {len(self._network_components['lines'])} lines")
        except Exception as e:
            raise NetworkSetupError(f"Error adding lines: {str(e)}", component="Lines")


    def _add_generators(self) -> None:
        """Add generators with capacity, efficiency, and cost specifications."""
        try:
            gen_tech_lib = self._tech_libraries['generator']
            self.network.generator_types = gen_tech_lib.copy()
            for _, gen in self._network_components['generators'].iterrows():
                if gen['type'] not in gen_tech_lib.index:
                    raise NetworkSetupError(f"Generator type {gen['type']} not found in tech library", component="Generator")
                tech_specs = gen_tech_lib.loc[gen['type']]
                generator_data = {**gen.to_dict(), **tech_specs.to_dict()}
                self.network.add("Generator", **generator_data)
            self.logger.info(f"Added {len(self._network_components['generators'])} generators")
        except Exception as e:
            raise NetworkSetupError(f"Error adding generators: {str(e)}", component="Generators")

    def _add_storage_units(self) -> None:
        """Add storage units with capacity, efficiency, and degradation specifications."""
        try:
            storage_tech_lib = self._tech_libraries['storage']
            self.network.storage_units_types = storage_tech_lib.copy()
            for _, storage in self._network_components['storage_units'].iterrows():
                if storage['type'] not in storage_tech_lib.index:
                    raise NetworkSetupError(f"Storage type {storage['type']} not found in tech library", component="StorageUnit")
                tech_specs = storage_tech_lib.loc[storage['type']]
                storage_data = {**storage.to_dict(), **tech_specs.to_dict()}
                self.network.add("StorageUnit", **storage_data)
            self.logger.info(f"Added {len(self._network_components['storage_units'])} storage units")
        except Exception as e:
            raise NetworkSetupError(f"Error adding storage units: {str(e)}", component="Storage Units")

    def _add_links(self) -> None:
        """Add power conversion links with efficiency and cost specifications."""
        try:
            for _, link in self._network_components['links'].iterrows():
                self.network.add("Link", **link.to_dict())
            self.logger.info(f"Added {len(self._network_components['links'])} links")
        except Exception as e:
            raise NetworkSetupError(f"Error adding links: {str(e)}", component="Links")

    def _add_loads(self) -> None:
        """Add loads to the network with power profiles and constraints."""
        try:
            for _, load in self._network_components['loads'].iterrows():
                load_profile = self.data_loader.load_profile(load['profile_id'], profile_type="load_profiles")
                self.network.add("Load", **load.to_dict())
            self.logger.info(f"Added {len(self._network_components['loads'])} loads")
        except Exception as e:
            raise NetworkSetupError(f"Error adding loads: {str(e)}", component="Loads")

    def _add_all_components(self) -> None:
        """Add all network components in the proper order."""
        component_adders = [
            self._add_buses,
            self._add_transformers,
            self._add_lines,
            self._add_generators,
            self._add_storage_units,
            self._add_links,
            self._add_loads
        ]
        try:
            for add_component in component_adders:
                add_component()
            self.logger.info("All components added to the network successfully")
        except Exception as e:
            raise NetworkSetupError(f"Error adding components: {str(e)}", component="Components")


    def _add_global_constraints(self) -> None:
        """Add global constraints to the network."""
        try:
            for _, constraint in self._constraints['global_constraints'].iterrows():
                self.network.add("GlobalConstraint", **constraint.to_dict())
            self.logger.info(f"Added {len(self._constraints['global_constraints'])} global constraints")
        except Exception as e:
            raise NetworkSetupError(f"Error adding global constraints: {str(e)}", component="Global Constraints")

    def _add_node_constraints(self) -> None:
        """Add node constraints to the network."""
        try:
            for _, constraint in self._constraints['node_constraints'].iterrows():
                self.network.add("NodeConstraint", **constraint.to_dict())
            self.logger.info(f"Added {len(self._constraints['node_constraints'])} node constraints")
        except Exception as e:
            raise NetworkSetupError(f"Error adding node constraints: {str(e)}", component="Node Constraints")

    def _add_branch_constraints(self) -> None:
        """Add branch constraints to the network."""
        try:
            for _, constraint in self._constraints['branch_constraints'].iterrows():
                self.network.add("BranchConstraint", **constraint.to_dict())
            self.logger.info(f"Added {len(self._constraints['branch_constraints'])} branch constraints")
        except Exception as e:
            raise NetworkSetupError(f"Error adding branch constraints: {str(e)}", component="Branch Constraints")

    def _add_all_constraints(self) -> None:
        """Apply loaded constraints to the network."""
        try:
            constraint_adders = [
                self._add_global_constraints,
                # self._add_node_constraints,
                # self._add_branch_constraints
            ]
            for add_constraint in constraint_adders:
                add_constraint()
            self.logger.info("Applied all network constraints")
        except Exception as e:
            raise NetworkSetupError(f"Error applying constraints: {str(e)}", component="Constraints")

    def _validate_network_topology(self) -> None:
        """
        Validate network topology to ensure all components are connected and the system is consistent.
        """
        try:
            self.network.consistency_check()
            self.logger.info("Network topology validated successfully")
        except Exception as e:
            raise NetworkSetupError(f"Network topology validation failed: {str(e)}", component="Topology")

    def _cleanup_resources(self) -> None:
        """Cleanup resources if an error occurs during network setup."""
        self.logger.info("Cleaning up temporary resources...")
        self.network = None
        self._tech_libraries.clear()
        self._network_components.clear()
        self._profiles.clear()
        self._constraints.clear()
        self.logger.info("Temporary resources cleaned up")

    def setup_network(self) -> pypsa.Network:
        """Orchestrate the network build process with rollback support."""
        try:
            self._add_carriers()
            self._add_all_components()
            self._add_all_constraints()
            self._validate_network_topology()
            self.logger.info("\n\nNetwork setup complete\n")
            return self.network
        except Exception as e:
            self.logger.error(f"Network build failed: {str(e)}")
            self._cleanup_resources()
            raise

    def get_network(self) -> pypsa.Network:
        """Retrieve the network object for external use."""
        return self.network

def main() -> None:
    """Main execution with performance monitoring."""
    try:
        data_folder = 'hybrid_renewable_pypsa/data'
        network_setup = NetworkSetup(data_folder)
        network = network_setup.setup_network()

        print("Buses:\n", network.buses)
        print("Lines:\n", network.lines)
        print("Generators:\n", network.generators)
        print("Storage Units:\n", network.storage_units)
        print("Links:\n", network.links)
        print("Loads:\n", network.loads)
        print("Global Constraints:\n", network.global_constraints)

    except NetworkSetupError as e:
        print(f"Network Configuration Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
