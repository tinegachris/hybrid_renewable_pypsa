import pypsa
import pandas as pd
from hybrid_renewable_pypsa.src.data_loader import Data_Loader
from hybrid_renewable_pypsa.src.logger_setup import Logger_Setup
from typing import Any

class Network_Setup:
    """
    Network_Setup class for setting up and managing a PyPSA network.
    Attributes:
        data_folder (str): Path to the folder containing network data files.
        network (pypsa.Network): Instance of the PyPSA Network.
    """
    def __init__(self, data_folder: str) -> None:
        self.data_folder: str = data_folder
        self.network: pypsa.Network = pypsa.Network()
        self.network.set_snapshots(pd.date_range("2024-10-01", periods=24, freq="h"))
        self.data_loader: Data_Loader = Data_Loader(data_folder)
        self.logger: Any = Logger_Setup.setup_logger('NetworkSetup')

        # Define necessary carriers for buses, lines, and links
        self._add_carriers()

    def _add_carriers(self) -> None:
        carriers = ["AC", "DC", "electricity"]
        for carrier in carriers:
            self.network.add("Carrier", carrier)

    def setup_network(self) -> None:
        self._add_buses()
        self._add_generators()
        self._add_storage_units()
        self._add_lines()
        self._add_transformers()
        self._add_links()
        self._add_loads()
        self.logger.info("Network was setup successfully!\n")

    def _add_component(self, component_type: str, data_file: str, **kwargs: Any) -> None:
        data: pd.DataFrame = self.data_loader.read_csv(data_file)
        if not data.empty:
            for _, row in data.iterrows():
                self.network.add(component_type, row['name'], **{key: row.get(key, kwargs[key]) for key in kwargs})
            self.logger.info(f"{component_type} added successfully!\n")
        else:
            self.logger.warning(f"No {component_type} were added to the network.")

    def _add_buses(self) -> None:
        self._add_component("Bus", 'buses.csv',
            v_nom=0.0,
            x=0.0,
            y=0.0,
            carrier='',
            v_mag_pu_set=0.0,
            v_mag_pu_min=0.0,
            v_mag_pu_max=0.0,
            control='',
            v_target=0.0,
            marginal_cost=0.0,
            zone='',
            max_shunt_capacitor=0.0,
            min_shunt_capacitor=0.0,
            reactive_power_setpoint=0.0
        )

    def _add_generators(self) -> None:
        self._add_component("Generator", 'generators.csv',
            bus='',
            control='',
            p_nom=0.0,
            efficiency=0.0,
            capital_cost=0.0,
            op_cost=0.0,
            p_max_pu=0.0,
            p_min_pu=0.0,
            marginal_cost=0.0
        )

    def _add_storage_units(self) -> None:
        self._add_component("StorageUnit", 'storage_units.csv',
            bus='',
            p_nom=0.0,
            max_hours=0.0,
            efficiency_store=0.0,
            efficiency_dispatch=0.0,
            capital_cost=0.0,
            marginal_cost=0.0,
            p_min_pu=0.0,
            p_max_pu=0.0,
            cyclic_state_of_charge=False,
            state_of_charge_initial=0.0,
            state_of_charge_min=0.0,
            state_of_charge_max=0.0
        )

    def _add_lines(self) -> None:
        data: pd.DataFrame = self.data_loader.read_csv('lines.csv')
        if not data.empty:
            for _, row in data.iterrows():
                self._add_line(row)
            self.logger.info("Lines added successfully!\n")
        else:
            self.logger.warning("No lines were added to the network.")

    def _add_line(self, row: pd.Series) -> None:
        self.network.add("Line", row['name'],
            bus0=row.get('bus0', ''),
            bus1=row.get('bus1', ''),
            length=row.get('length', 0.0),
            r_per_length=row.get('r_per_length', 0.0),
            x_per_length=row.get('x_per_length', 0.0),
            c_per_length=row.get('c_per_length', 0.0),
            s_nom=row.get('s_nom', 0.0),
            r=row['r_per_length'] * row['length'],
            x=row['x_per_length'] * row['length'],
            capital_cost=row.get('capital_cost', 0.0),
            carrier=row.get('carrier', 'electricity')
        )

    def _add_transformers(self) -> None:
        self._add_component("Transformer", 'transformers.csv',
            bus0='',
            bus1='',
            s_nom=0.0,
            x=0.0,
            r=0.0,
            tap_position=0,
            tap_min=0,
            tap_max=0,
            tap_step=0.0,
            efficiency=0.0,
            capital_cost=0.0
        )

    def _add_links(self) -> None:
        self._add_component("Link", 'links.csv',
            bus0='',
            bus1='',
            p_nom=0.0,
            efficiency=0.0,
            capital_cost=0.0,
            transformer_type='',
            p_min_pu=0.0,
            p_max_pu=0.0,
            reactive_power_capacity=0.0,
            r=0.0,
            x=0.0,
            startup_cost=0.0,
            shutdown_cost=0.0,
            ramp_up=0.0,
            ramp_down=0.0,
            maintenance_cost=0.0,
            status=True,
            control_type='',
            carrier='electricity'
        )

    def _add_loads(self) -> None:
        loads: pd.DataFrame = self.data_loader.read_csv('loads.csv')
        if loads.empty:
            self.logger.warning("No loads were added to the network.")
            return
        for _, load in loads.iterrows():
            self._add_load(load)
        self.logger.info("Loads added successfully!\n")

    def _add_load(self, load: pd.Series) -> None:
        p_set_values = [float(x) for x in load.get('p_set', '').split(',')]
        if len(p_set_values) != len(self.network.snapshots):
            raise ValueError(f"Length of p_set values ({len(p_set_values)}) does not match length of snapshots ({len(self.network.snapshots)})")
        p_set = pd.Series(p_set_values, index=self.network.snapshots)
        self.network.add("Load", load['name'],
            bus=load.get('bus', ''),
            p_set=p_set,
            q_set=pd.Series([float(x) for x in load.get('q_set', '').split(',')], index=self.network.snapshots),
            p_min=load.get('p_min', 0.0),
            p_max=load.get('p_max', 0.0),
            scaling_factor=load.get('scaling_factor', 1.0),
            status=load.get('active', True),
            carrier=load.get('carrier', '')
        )

    def get_network(self) -> pypsa.Network:
        if self.network.buses.empty and self.network.generators.empty and self.network.storage_units.empty and self.network.loads.empty and self.network.lines.empty:
            self.logger.warning("The network is empty.\n")
        return self.network

def main():
    data_folder = 'hybrid_renewable_pypsa/data'
    network_setup = Network_Setup(data_folder)
    network_setup.setup_network()
    network: pypsa.Network = network_setup.get_network()
    logger: Any = Logger_Setup.setup_logger('Main')
    logger.info(network.buses)
    logger.info(network.generators)
    logger.info(network.storage_units)
    logger.info(network.loads)
    logger.info(network.lines)
    logger.info(network.transformers)
    logger.info(network.links)

if __name__ == "__main__":
    main()