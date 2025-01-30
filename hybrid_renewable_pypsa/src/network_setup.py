import pypsa
import pandas as pd
from typing import Any, List, Dict
from pathlib import Path
from hybrid_renewable_pypsa.src.data_loader import Data_Loader
from hybrid_renewable_pypsa.src.logger_setup import Logger_Setup

class NetworkSetupError(Exception):
    """Custom exception for network setup errors."""
    pass

class NetworkSetup:
    """
    NetworkSetup class for setting up and managing a PyPSA network.
    Handles complex component relationships and constraint management.
    """

    def __init__(self, data_folder: str) -> None:
        self.data_folder = Path(data_folder)
        self.network = pypsa.Network()
        self._configure_network()
        self.data_loader = Data_Loader(self.data_folder)
        self.logger = Logger_Setup.setup_logger('NetworkSetup')
        self._tech_libraries = {}

    def _configure_network(self) -> None:
        """Initialize network with temporal structure"""
        self.network.set_snapshots(pd.date_range("2024-10-01", periods=24, freq="h"))
        self.network.name = "Hybrid_Renewable_System"

    def _load_tech_libraries(self) -> None:
        """Load all required technology libraries"""
        self._tech_libraries = {
            'storage': self.data_loader.load_storage_tech_library(),
            'transformer': self.data_loader.load_transformer_tech_library(),
            'generator': self.data_loader.load_generator_tech_library()
        }

    def setup_network(self) -> None:
        """Orchestrate full network setup with validation"""
        try:
            self._load_tech_libraries()
            self._add_carriers()
            self._add_components()
            self._add_dynamic_constraints()
            self._validate_network()
            self.logger.info("Network setup completed successfully")
        except Exception as e:
            self.logger.error(f"Network setup failed: {str(e)}")
            raise NetworkSetupError(f"Network initialization error: {str(e)}")

    def _add_carriers(self) -> None:
        """Configure energy carriers with emission factors"""
        carriers = {
            'AC': {'co2_emissions': 0},
            'DC': {'co2_emissions': 0},
            'electricity': {'co2_emissions': 0.5}
        }
        for name, params in carriers.items():
            self.network.add("Carrier", name, **params)

    def _add_components(self) -> None:
        """Add all network components with dependency order"""
        component_adders = [
            self._add_buses,
            self._add_lines,
            self._add_transformers,
            # self._add_generators,
            self._add_storage_units,
            self._add_links,
            self._add_loads
        ]

        for adder in component_adders:
            adder()

    def _add_buses(self) -> None:
        """Add buses with voltage level validation"""
        buses = self.data_loader.read_csv('buses.csv')
        for _, bus in buses.iterrows():
            self.network.add("Bus",
                name=bus['name'],
                v_nom=bus['v_nom'],
                x=bus.get('x', 0),
                y=bus.get('y', 0),
                carrier=bus.get('carrier', 'AC')
            )
        self.logger.info(f"Added {len(buses)} buses")

    def _add_lines(self) -> None:
        """Add transmission lines with impedance calculation"""
        lines = self.data_loader.read_csv('lines.csv')
        for _, line in lines.iterrows():
            self.network.add("Line",
                name=line['name'],
                bus0=line['bus0'],
                bus1=line['bus1'],
                r=line['r_per_length'] * line['length'],
                x=line['x_per_length'] * line['length'],
                s_nom=line['s_nom'],
                capital_cost=line['capital_cost'],
                terrain_factor=line.get('terrain_factor', 1.0),
                max_i_ka=line.get('max_i_ka', 1.0)
            )
        self.logger.info(f"Added {len(lines)} transmission lines")

    def _add_transformers(self) -> None:
        """Add transformers with technical specifications"""
        transformers = self.data_loader.read_csv('transformers.csv')
        tech_lib = self._tech_libraries['transformer']

        for _, xfmr in transformers.iterrows():
            tech_specs = tech_lib.loc[xfmr['type']]
            self.network.add("Transformer",
                name=xfmr['name'],
                bus0=xfmr['bus0'],
                bus1=xfmr['bus1'],
                s_nom=xfmr['s_nom'],
                x=xfmr['per_unit_impedance']/100 * (xfmr['voltage0']**2 / xfmr['s_nom']),
                r=xfmr['per_unit_impedance']/100 / xfmr['x_r_ratio'] * (xfmr['voltage0']**2 / xfmr['s_nom']),
                tap_ratio=xfmr['tap_position'],
                efficiency=xfmr['efficiency'],
                capital_cost=xfmr['capital_cost'],
                **tech_specs.to_dict()
            )
        self.logger.info(f"Added {len(transformers)} transformers")

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
                ramp_limit_up=gen.get('ramp_limit_up', 1.0),
                ramp_limit_down=gen.get('ramp_limit_down', 1.0),
                **tech_specs.to_dict()
            )
        self.logger.info(f"Added {len(generators)} generators")

    def _add_storage_units(self) -> None:
        """Add storage units with detailed technical parameters"""
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
                **tech_specs.to_dict(),
                **unit[['capital_cost_power', 'capital_cost_energy']].to_dict()
            )
        self.logger.info(f"Added {len(storage_units)} storage units")

    def _add_links(self) -> None:
        """Add energy conversion links with detailed parameters"""
        links = self.data_loader.read_csv('links.csv')
        for _, link in links.iterrows():
            self.network.add("Link",
                name=link['name'],
                bus0=link['bus0'],
                bus1=link['bus1'],
                p_nom=link['p_nom'],
                efficiency=link['efficiency'],
                capital_cost=link['capital_cost'],
                carrier=link['carrier'],
                voltage_level_0=link.get('voltage_level_0', 0),
                voltage_level_1=link.get('voltage_level_1', 0)
            )
        self.logger.info(f"Added {len(links)} links")

    def _add_loads(self) -> None:
        """Add time-varying loads with profile data"""
        loads = self.data_loader.read_csv('loads.csv')
        for _, load in loads.iterrows():
            profile = self.data_loader.load_profile(load['profile_id'])
            self.network.add("Load",
                name=load['name'],
                bus=load['bus'],
                p_set=profile['p_set'],
                q_set=profile['q_set'],
                p_min=load['p_min'],
                p_max=load['p_max'],
                carrier=load.get('carrier', 'electricity')
            )
        self.logger.info(f"Added {len(loads)} loads with profiles")

    def _add_dynamic_constraints(self) -> None:
        """Apply operational constraints and limitations"""
        constraints = self.data_loader.load_dynamic_constraints()
        profiles = self.data_loader.load_constraint_profiles()
        component_limits = self.data_loader.load_component_constraints()

        self._apply_static_constraints(constraints)
        self._apply_time_varying_constraints(constraints, profiles)
        self._apply_component_limits(component_limits)

    def _apply_static_constraints(self, constraints: pd.DataFrame) -> None:
        """Apply non-temporal constraints"""
        static = constraints[constraints['start_time'].isna()]
        for _, row in static.iterrows():
            component = getattr(self.network, f"{row['component_type']}s").loc[row['component_id']]
            component[row['constraint_type']] = row['value']
        self.logger.info(f"Applied {len(static)} static constraints")

    def _apply_time_varying_constraints(self, constraints: pd.DataFrame, profiles: Dict) -> None:
        """Apply temporal constraints with profile data"""
        temporal = constraints[~constraints['start_time'].isna()]
        for _, row in temporal.iterrows():
            component = getattr(self.network, f"{row['component_type']}s").loc[row['component_id']]
            time_slice = slice(row['start_time'], row['end_time'])
            component[row['constraint_type']].loc[time_slice] = profiles[row['constraint_id']]
        self.logger.info(f"Applied {len(temporal)} temporal constraints")

    def _apply_component_limits(self, limits: pd.DataFrame) -> None:
        """Enforce operational boundaries"""
        for _, row in limits.iterrows():
            component = self.network.get_components(row['component_id'])
            for limit_type in ['min', 'max']:
                setattr(component, f"p_{limit_type}_pu", row[f"{limit_type}_value"])
        self.logger.info(f"Applied {len(limits)} component limits")

    def _validate_network(self) -> None:
        """Perform comprehensive network validation"""
        self._check_voltage_levels()
        self._check_component_links()
        self.network.consistency_check()
        self.logger.info("Network validation passed")

    def _check_voltage_levels(self) -> None:
        """Verify voltage consistency between connected components"""
        for trafo in self.network.transformers.itertuples():
            bus0_volt = self.network.buses.at[trafo.bus0, 'v_nom']
            bus1_volt = self.network.buses.at[trafo.bus1, 'v_nom']

            if abs(bus0_volt - trafo.voltage0) > 1e-3 or abs(bus1_volt - trafo.voltage1) > 1e-3:
                raise ValueError(f"Transformer {trafo.name} voltage mismatch with connected buses")

    def _check_component_links(self) -> None:
        """Verify all components are connected to existing buses"""
        components = ['Generator', 'Load', 'StorageUnit', 'Link']
        for comp_type in components:
            for name, comp in getattr(self.network, f"{comp_type}s").iterrows():
                if comp.bus not in self.network.buses.index:
                    raise ValueError(f"{comp_type} {name} connected to non-existent bus {comp.bus}")

    def get_network(self) -> pypsa.Network:
        """Retrieve the configured network with validation"""
        if self.network.buses.empty:
            raise NetworkSetupError("Network configuration failed - no buses defined")
        return self.network

def main() -> None:
    """Main execution routine with error handling"""
    try:
        data_folder = 'hybrid_renewable_pypsa/data'
        network_setup = NetworkSetup(data_folder)
        network_setup.setup_network()
        network = network_setup.get_network()

        logger = Logger_Setup.setup_logger('Main')
        logger.info("\nNetwork Summary:\n" + str(network))

    except NetworkSetupError as e:
        print(f"Critical network setup error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()