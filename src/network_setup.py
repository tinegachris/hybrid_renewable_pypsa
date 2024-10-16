import pypsa
import pandas as pd
from data_loader import Data_Loader
from logger_setup import Logger_Setup

class Network_Setup:
    """
    Network_Setup class for setting up and managing a PyPSA network.
    Attributes:
        data_folder (str): Path to the folder containing network data files.
        network (pypsa.Network): Instance of the PyPSA Network.
    """
    def __init__(self, data_folder):
        self.data_folder = data_folder
        self.network = pypsa.Network()
        self.network.set_snapshots(pd.date_range("2024-01-01", periods=24, freq="h"))
        self.data_loader = Data_Loader(data_folder)
        self.logger = Logger_Setup.setup_logger('NetworkSetup')

    def setup_network(self):
        self._add_buses()
        self._add_generators()
        self._add_storage_units()
        self._add_lines()
        self._add_transformers()
        self._add_links()
        self._add_loads()
        self.logger.info("Network was setup successfully!\n")

    def _add_component(self, component_type, data_file, **kwargs):
        data = self.data_loader.read_csv(data_file)
        if not data.empty:
            for _, row in data.iterrows():
                self.network.add(component_type, row['name'], **{key: row.get(key, kwargs[key]) for key in kwargs})
            self.logger.info(f"{component_type} added successfully!\n")
        else:
            self.logger.warning(f"No {component_type} were added to the network.")

    def _add_buses(self):
        self._add_component("Bus", 'buses.csv',
            v_nom=0.0,
            x=0.0,
            y=0.0,
            carrier='',
            v_mag_pu_set=None,
            v_mag_pu_min=None,
            v_mag_pu_max=None,
            control=None,
            v_target=None,
            marginal_cost=0.0,
            zone='',
            type='',
            max_shunt_capacitor=0.0,
            min_shunt_capacitor=0.0,
            reactive_power_setpoint=0.0
        )

    def _add_generators(self):
        self._add_component("Generator", 'generators.csv',
            bus='',
            control='',
            p_nom=0.0,
            efficiency=0.0,
            capital_cost=0.0,
            marginal_cost=0.0,
            p_max_pu=0.0,
            p_min_pu=0.0
        )

    def _add_storage_units(self):
        self._add_component("StorageUnit", 'storage_units.csv',
            bus='',
            p_nom=0.0,
            capital_cost=0.0,
            state_of_charge_initial=0.0,
            efficiency_store=0.0,
            efficiency_dispatch=0.0,
            max_hours=0.0,
            marginal_cost=0.0,
            p_min_pu=0.0,
            p_max_pu=0.0,
            cyclic_state_of_charge=False,
            state_of_charge_min=0.0,
            state_of_charge_max=0.0
        )

    def _add_lines(self):
        self._add_component("Line", 'lines.csv',
            bus0='',
            bus1='',
            length=0.0,
            r_per_length=0.0,
            x_per_length=0.0,
            c_per_length=0.0,
            s_nom=0.0,
            capital_cost=0.0,
            carrier=''
        )

    def _add_transformers(self):
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

    def _add_links(self):
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
            control_type=''
        )

    def _add_loads(self):
        loads = self.data_loader.read_csv('loads.csv')
        if loads.empty:
            self.logger.warning("No loads were added to the network.")
            return
        for _, load in loads.iterrows():
            self.network.add("Load", load['name'],
            bus=load.get('bus', ''),
            p_set=pd.Series([float(x) for x in load.get('p_set', '').split(',')], index=self.network.snapshots),
            q_set=pd.Series([float(x) for x in load.get('q_set', '').split(',')], index=self.network.snapshots),
            p_min=load.get('p_min', 0.0),
            p_max=load.get('p_max', 0.0),
            scaling_factor=load.get('scaling_factor', 1.0),
            status=load.get('active', True),
            carrier=load.get('carrier', ''),
            )
        self.logger.info("Loads added successfully!\n")

    def get_network(self):
        if self.network.buses.empty and self.network.generators.empty and self.network.storage_units.empty and self.network.loads.empty and self.network.lines.empty:
            self.logger.warning("The network is empty.\n")
        return self.network

def main():
    data_folder = 'data'
    network_setup = Network_Setup(data_folder)
    network_setup.setup_network()
    network = network_setup.get_network()
    logger = Logger_Setup.setup_logger('Main')
    logger.info(network.buses)
    logger.info(network.generators)
    logger.info(network.storage_units)
    logger.info(network.loads)
    logger.info(network.lines)
    logger.info(network.transformers)
    logger.info(network.links)

if __name__ == "__main__":
    main()