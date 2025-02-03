import pypsa
import pandas as pd
import numpy as np
from typing import Dict, Optional
from pathlib import Path
from hybrid_renewable_pypsa.src.data_loader import Data_Loader
from hybrid_renewable_pypsa.src.logger_setup import Logger_Setup

class NetworkSetupError(Exception):
    """Custom exception for network setup errors with component context"""
    def __init__(self, message: str, component: Optional[str] = None):
        super().__init__(f"{component + ': ' if component else ''}{message}")
        self.component = component

class Network_Setup:
    """
    Advanced network configuration manager with:
    - Technology library integration
    - Dynamic constraint handling
    - Hierarchical component validation
    - Multi-carrier support
    """

    CARRIER_CONFIG = {
        'AC': {'color': '#1f77b4', 'co2_emissions': 0},
        'DC': {'color': '#ff7f0e', 'co2_emissions': 0},
        'electricity': {'color': '#2ca02c', 'co2_emissions': 0.5},
        'hydro': {'color': '#17becf', 'co2_emissions': 0},
        'solar': {'color': '#bcbd22', 'co2_emissions': 0}
    }

    def __init__(self, data_folder: str) -> None:
        self.data_folder = Path(data_folder)
        self.network = pypsa.Network()
        self._tech_libraries = {}
        self.data_loader = Data_Loader(self.data_folder)
        self.logger = Logger_Setup.setup_logger('NetworkSetup')

        # Initialize with full temporal structure
        self._configure_temporal()
        self._configure_network_properties()

    def _configure_temporal(self) -> None:
        """Configure time parameters with validation"""
        try:
            self.network.set_snapshots(
                pd.date_range("2024-01-01", periods=24*7, freq="h")
            )
            self.network.snapshot_weightings[:] = 1.0
            self.logger.info("Temporal configuration successful")
        except Exception as e:
            raise NetworkSetupError(f"Temporal configuration failed: {str(e)}")

    def _configure_network_properties(self) -> None:
        """Set global network properties"""
        self.network.name = "Hybrid_Renewable_System"
        self.network._meta = {
            "version": "1.3",
            "data_sources": ["synthetic", "NREL"],
            "author": "Chrispine Tinega"
        }
        self.logger.info("Network properties configured")

    def setup_network(self) -> pypsa.Network:
        """Orchestrate network build process with rollback support"""
        try:
            self._load_tech_libraries()
            self.logger.info("Technology libraries loaded successfully")
            self._add_carriers()
            self.logger.info("Energy carriers configured")
            self._add_components()
            self.logger.info("Network components added")
            self._add_constraints()
            self.logger.info("Network constraints applied")
            self._validate_network_topology()
            self.logger.info("Network topology validated")
            self._finalize_network()
            self.logger.info("Network setup complete")
            return self.network
        except Exception as e:
            self.logger.error(f"Network build failed: {str(e)}")
            self._cleanup_resources()
            raise

    def get_network(self) -> pypsa.Network:
        """Retrieve the network object for external use"""
        return self.network

    def _load_tech_libraries(self) -> None:
        """Load technology specifications with version checking"""
        self._tech_libraries = {
            'storage': self._validate_tech_library(
                self.data_loader.load_storage_tech_library(),
                required_columns=['roundtrip_efficiency', 'cycle_life']
            ),
            'transformer': self._validate_tech_library(
                self.data_loader.load_transformer_tech_library(),
                required_columns=['typical_impedance_pct', 'cooling_types']
            ),
            'generator': self._validate_tech_library(
                self.data_loader.load_generator_tech_library(),
                required_columns=['ramp_limit_up_pct_per_min', 'ramp_limit_down_pct_per_min']
            )
        }
        self.logger.info("Technology libraries loaded")

    def _validate_tech_library(self, df: pd.DataFrame, required_columns: list) -> pd.DataFrame:
        """Ensure technology libraries contain required data"""
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            raise NetworkSetupError(
                f"Technology library missing columns: {missing}",
                component="Tech Libraries"
            )
        return df

    def _add_carriers(self) -> None:
        """Configure energy carriers with emissions tracking"""
        for name, params in self.CARRIER_CONFIG.items():
            self.network.add("Carrier", name, **params)
        self.logger.info(f"Configured {len(self.CARRIER_CONFIG)} energy carriers")

    def _add_components(self) -> None:
        """Component addition pipeline with dependency management"""
        component_order = [
            self._add_buses,
            self._add_transformers,
            self._add_lines,
            self._add_generators,
            self._add_storage_units,
            self._add_links,
            self._add_loads
        ]

        for component_adder in component_order:
            try:
                component_adder()
            except Exception as e:
                raise NetworkSetupError(
                    f"Component addition failed: {str(e)}",
                    component=component_adder.__name__[5:]
                )

    def _add_buses(self) -> None:
        """Add buses with voltage level validation"""
        buses = self.data_loader.read_csv('buses.csv')
        for _, bus in buses.iterrows():
            self.network.add("Bus",
                name=bus['name'],
                v_nom=bus['v_nom'],
                x=bus.get('x', 0),
                y=bus.get('y', 0),
                carrier=bus['carrier'],
                v_mag_pu_set=bus.get('v_mag_pu_set', 1.0),
                max_shunt_capacitor=bus.get('max_shunt_capacitor', 0)
            )
        self.logger.info(f"Added {len(buses)} buses with voltage validation")

    def _add_transformers(self) -> None:
        """Add transformers with impedance calculations"""
        transformers = self.data_loader.read_csv('transformers.csv')
        tech_lib = self._tech_libraries['transformer']

        for _, xfmr in transformers.iterrows():
            tech_specs = tech_lib.loc[xfmr['type']]
            base_impedance = (xfmr['voltage0'] ** 2) / (xfmr['s_nom'] * 1e6)  # MVA base

            self.network.add("Transformer",
                name=xfmr['name'],
                bus0=xfmr['bus0'],
                bus1=xfmr['bus1'],
                s_nom=xfmr['s_nom'],
                x=xfmr['per_unit_impedance'] * base_impedance,
                r=(xfmr['per_unit_impedance'] / xfmr['x_r_ratio']) * base_impedance,
                tap_ratio=xfmr.get('tap_position', 1.0),
                phases=xfmr.get('phases', 3),
                model=xfmr.get('cooling', 'ONAN'),
                **tech_specs.to_dict()
            )
        self.logger.info(f"Added {len(transformers)} transformers with technical specs")

    def _add_lines(self) -> None:
        """Add transmission lines with thermal limits"""
        lines = self.data_loader.read_csv('lines.csv')
        for _, line in lines.iterrows():
            self.network.add("Line",
                name=line['name'],
                bus0=line['bus0'],
                bus1=line['bus1'],
                r=line['r_per_length'] * line['length'],
                x=line['x_per_length'] * line['length'],
                b=line.get('c_per_length', 0) * line['length'] * 1e-6,  # μS/km to S
                s_nom=line['s_nom'],
                capital_cost=line.get('capital_cost', 0),
                terrain_factor=line.get('terrain_factor', 1.0),
                max_i_ka=line.get('max_i_ka', 1.0),
                type=line.get('type', 'overhead')
            )
        self.logger.info(f"Added {len(lines)} lines with thermal constraints")

    def _add_generators(self) -> None:
        """Add generators with technology-specific parameters"""
        generators = self.data_loader.read_csv('generators.csv')
        tech_lib = self._tech_libraries['generator']

        for _, gen in generators.iterrows():
            tech_specs = tech_lib.loc[gen['type']]
            self.network.add("Generator",
                name=gen['name'],
                bus=gen['bus'],
                p_nom=gen['p_nom'],
                efficiency=gen['efficiency'],
                marginal_cost=gen['marginal_cost'],
                ramp_limit_up=tech_specs['ramp_limit_up_pct_per_min'],
                ramp_limit_down=tech_specs['ramp_limit_down_pct_per_min'],
                min_up_time=tech_specs['min_up_time_hr'],
                min_down_time=tech_specs['min_down_time_hr'],
                carrier=gen['carrier'],
                p_max_pu=gen['p_max_pu'],
                control=gen.get('control', 'PQ')
            )
        self.logger.info(f"Added {len(generators)} generators with tech specs")

    def _add_storage_units(self) -> None:
        """Add storage systems with degradation modeling"""
        storage_units = self.data_loader.read_csv('storage_units.csv')
        tech_lib = self._tech_libraries['storage']

        for _, unit in storage_units.iterrows():
            tech_specs = tech_lib.loc[unit['type']]
            self.network.add("StorageUnit",
                name=unit['name'],
                bus=unit['bus'],
                p_nom=unit['p_nom'],
                max_hours=unit['max_hours'],
                efficiency_store=unit['efficiency_store'],
                efficiency_dispatch=unit['efficiency_dispatch'],
                cyclic_state_of_charge=unit['cyclic'],
                standing_loss=unit.get('standing_loss', 0),
                **tech_specs.to_dict()
            )
        self.logger.info(f"Added {len(storage_units)} storage units with degradation")

    def _add_links(self) -> None:
        """Add power conversion links with voltage validation"""
        links = self.data_loader.read_csv('links.csv')
        for _, link in links.iterrows():
            self._validate_link_voltages(link)
            self.network.add("Link",
                name=link['name'],
                bus0=link['bus0'],
                bus1=link['bus1'],
                p_nom=link['p_nom'],
                efficiency=link['efficiency'],
                capital_cost=link['capital_cost'],
                carrier=link['carrier'],
                marginal_cost=link.get('marginal_cost', 0),
                p_min_pu=link.get('p_min_pu', 0),
                p_max_pu=link.get('p_max_pu', 1)
            )
        self.logger.info(f"Added {len(links)} links with voltage validation")

    def _validate_link_voltages(self, link: pd.Series) -> None:
        """Verify link voltage compatibility with connected buses"""
        bus0_volt = self.network.buses.at[link['bus0'], 'v_nom']
        bus1_volt = self.network.buses.at[link['bus1'], 'v_nom']

        # Validate DC-AC voltage transformation for inverters
        if link['type'] == 'inverter':
            if bus0_volt <= 1500 and bus1_volt not in [415, 800]:
                raise NetworkSetupError(
                    f"Inverter {link['name']} has invalid voltage pairing: " +
                    f"DC {bus0_volt}V to AC {bus1_volt}V",
                    component="Link"
                )

    def _add_loads(self) -> None:
        """Add time-varying loads with profile validation"""
        loads = self.data_loader.read_csv('loads.csv')
        for _, load in loads.iterrows():
            profile = self.data_loader.load_profile(load['profile_id'])
            self._validate_load_profile(profile, load['name'])

            self.network.add("Load",
                name=load['name'],
                bus=load['bus'],
                p_set=profile['p_set'],
                q_set=profile['q_set'],
                p_min=load['p_min'],
                p_max=load['p_max'],
                carrier=load['carrier'],
                load_type=load['load_type']
            )
        self.logger.info(f"Added {len(loads)} loads with profile validation")

    def _validate_load_profile(self, profile: pd.DataFrame, load_name: str):
        """Strict index validation with name check"""
        if profile.index.name != 'snapshot':
            raise NetworkSetupError(
                f"Profile index must be named 'snapshot', got '{profile.index.name}'",
                component="Load"
            )

        if not profile.index.equals(self.network.snapshots):
            raise NetworkSetupError(
                f"Time index mismatch for load {load_name}",
                component="Load"
            )

    def _add_constraints(self) -> None:
        """Constraint management pipeline"""
        constraints = {
            'static': self.data_loader.load_component_constraints(),
            'dynamic': self.data_loader.load_dynamic_constraints(),
            'profiles': self.data_loader.load_constraint_profiles()
        }

        self._apply_static_constraints(constraints['static'])
        # self._apply_dynamic_constraints(constraints['dynamic'], constraints['profiles'])
        self.logger.info("Applied all network constraints")

    def _apply_static_constraints(self, constraints: pd.DataFrame) -> None:
        COMPONENT_MAP = {
            'Generator': 'generators',
            'StorageUnit': 'storage_units',
            'Line': 'lines',
            'Load': 'loads',
            'Transformer': 'transformers'
        }

        for _, constraint in constraints.iterrows():
            try:
                component_type = constraint['component_id'].split('_', 1)[0]
                pypsa_component = COMPONENT_MAP[component_type]
                component_df = getattr(self.network, pypsa_component)

                # Update directly in the DataFrame using loc
                for limit_type in ['min', 'max']:
                    if value := constraint.get(f"{limit_type}_value"):
                        component_df.loc[constraint['component_id'], f"p_{limit_type}_pu"] = float(value)

            except KeyError:
                raise NetworkSetupError(f"Invalid component {constraint['component_id']}", component="Constraint")

    def _apply_dynamic_constraints(self, constraints: pd.DataFrame, profiles: Dict) -> None:
        """Apply constraints with proper PyPSA time-series handling"""
        COMPONENT_TIME_MAP = {
            'Generator': ('generators', 'generators_t'),
            'StorageUnit': ('storage_units', 'storage_units_t'),
            'Load': ('loads', 'loads_t'),
            'Line': ('lines', 'lines_t')
        }

        for _, constraint in constraints.iterrows():
            component_type = constraint['component_type']
            component_id = constraint['component_id']
            constraint_type = constraint['constraint_type']
            value = profiles.get(constraint['constraint_id'], constraint['value'])
            time_slice = self._parse_time_window(constraint)

            # Get component handlers
            static_attr, time_attr = COMPONENT_TIME_MAP[component_type]
            static_df = getattr(self.network, static_attr)

            try:
                # Handle time-varying constraints
                if hasattr(getattr(self.network, time_attr), constraint_type):
                    time_series = getattr(getattr(self.network, time_attr), constraint_type)
                    time_series.loc[time_slice, component_id] = value
                # Handle static constraints
                elif constraint_type in static_df.columns:
                    static_df.loc[component_id, constraint_type] = value
                else:
                    raise NetworkSetupError(
                        f"Invalid constraint {constraint_type} for {component_id}",
                        component=component_type
                    )

            except KeyError:
                raise NetworkSetupError(f"Component {component_id} not found", component=component_type)

    def _parse_time_window(self, constraint: pd.Series) -> slice:
        """Convert to proper datetime slice"""
        start = pd.to_datetime(constraint['start_time']) if pd.notna(constraint['start_time']) else None
        end = pd.to_datetime(constraint['end_time']) if pd.notna(constraint['end_time']) else None

        return self.network.snapshots.slice_indexer(
            start=start,
            end=end
        )

    def _validate_network_topology(self) -> None:
        """Perform comprehensive network validation"""
        self._check_component_connections()
        self._check_voltage_levels()
        self.network.consistency_check()
        self.logger.info("Network topology validation passed")

    def _check_component_connections(self) -> None:
        """Verify all components are connected to existing buses"""
        components = {
            'Generator': self.network.generators,
            'Load': self.network.loads,
            'StorageUnit': self.network.storage_units,
            'Link': self.network.links
        }

        for comp_type, df in components.items():
            for name, comp in df.iterrows():
                buses = [comp['bus']] if comp_type != 'Link' else [comp['bus0'], comp['bus1']]
                for bus in buses:
                    if bus not in self.network.buses.index:
                        raise NetworkSetupError(
                            f"{comp_type} {name} connected to invalid bus {bus}",
                            component=comp_type
                        )
        self.logger.info("Component connections validated")

    def _check_voltage_levels(self) -> None:
        """Validate voltage compatibility across connections"""
        for _, line in self.network.lines.iterrows():
            if pd.isna(line['bus0']) or pd.isna(line['bus1']):
                raise NetworkSetupError(
                    f"Line {line.name} has NaN bus values: bus0={line.bus0}, bus1={line.bus1}",
                    component="Line"
                )
            bus0_v = self.network.buses.at[line.bus0, 'v_nom']
            bus1_v = self.network.buses.at[line.bus1, 'v_nom']

            if abs(bus0_v - bus1_v) > 1e-3:
                raise NetworkSetupError(
                    f"Line {line.name} connects different voltage levels: " +
                    f"{bus0_v}V - {bus1_v}V",
                    component="Line"
                )

    def _finalize_network(self) -> None:
        """Final network preparation steps"""
        self.network.lopf(
            pyomo=False,
            formulation="kirchhoff",
            keep_files=False
        )
        self.logger.info("Network initialized for optimization")

    def _cleanup_resources(self) -> None:
        """Release resources after failed build"""
        self.network = None
        self._tech_libraries.clear()

def main() -> None:
    """Main execution with performance monitoring"""
    try:
        data_folder = 'hybrid_renewable_pypsa/data'
        network_setup = Network_Setup(data_folder)
        network = network_setup.setup_network()

        logger = Logger_Setup.setup_logger('Main')
        logger.info("\n\nNetwork Statistics:")
        logger.info(f"- Buses: {len(network.buses)}")
        logger.info(f"- Lines: {len(network.lines)}")
        logger.info(f"- Generators: {len(network.generators)}")
        logger.info(f"- Storage Units: {len(network.storage_units)}")
        logger.info(f"- Active Constraints: {len(network.global_constraints)}")

    except NetworkSetupError as e:
        print(f"Network Configuration Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()