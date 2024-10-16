import pypsa
import pandas as pd
import os
import logging

logger = logging.getLogger('NetworkSetup')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False

class Network_Setup:
    """
    NetworkSetup class for setting up and managing a PyPSA network.
    Attributes:
        data_folder (str): Path to the folder containing network data files.
        network (pypsa.Network): Instance of the PyPSA Network.
    """
    def __init__(self, data_folder):
        self.data_folder = data_folder
        self.network = pypsa.Network()
        self.network.set_snapshots(pd.date_range("2021-01-01", periods=24, freq="h"))

    def setup_network(self):
        self._add_buses()
        self._add_generators()
        self._add_storage_units()
        self._add_loads()
        self._add_lines()
        self._add_transformers()
        self._add_links()
        logger.info("Network was setup successfully!")

    def _sanitize_file_name(self, file_name):
        allowed_files = {'buses.csv', 'generators.csv', 'storage_units.csv', 'loads.csv', 'lines.csv', 'transformers.csv', 'links.csv'}
        if file_name not in allowed_files:
            raise ValueError(f"Invalid file name: {file_name}")
        return file_name

    def _read_csv(self, file_name):
        try:
            sanitized_file_name = self._sanitize_file_name(file_name)
            file_path = os.path.join(self.data_folder, sanitized_file_name)
            return pd.read_csv(file_path)
        except ValueError as ve:
            logger.error(ve)
        except FileNotFoundError:
            logger.error(f"File {file_name} not found in the data folder.")
        except pd.errors.EmptyDataError:
            logger.error(f"File {file_name} is empty.")
        except Exception as e:
            logger.error(f"An error occurred while reading file {file_name}.")
            logger.error(e)
        return pd.DataFrame()

    def _add_component(self, component_type, data_file, **kwargs):
        data = self._read_csv(data_file)
        if not data.empty:
            for _, row in data.iterrows():
                self.network.add(component_type, row['name'], **{key: row.get(key) for key in kwargs})
            logger.info(f"{component_type} added successfully!")
        else:
            logger.warning(f"No {component_type} were added to the network.")


    def _add_buses(self):
        buses = self._read_csv('buses.csv')
        if buses.empty:
            logger.warning("No buses were added to the network.")
            return
        for _, row in buses.iterrows():
            self.network.add("Bus", row['name'],
            v_nom=row.get('v_nom', 0.0),
            x=row.get('x', 0.0),
            y=row.get('y', 0.0),
            carrier=row.get('carrier', ''),
            v_mag_pu_set=row.get('v_mag_pu_set', None),
            v_mag_pu_min=row.get('v_mag_pu_min', None),
            v_mag_pu_max=row.get('v_mag_pu_max', None),
            control=row.get('control', None),
            v_target=row.get('v_target', None),
            marginal_cost=row.get('marginal_cost', 0.0),
            zone=row.get('zone', ''),
            type=row.get('type', ''),
            max_shunt_capacitor=row.get('max_shunt_capacitor', 0.0),
            min_shunt_capacitor=row.get('min_shunt_capacitor', 0.0),
            reactive_power_setpoint=row.get('reactive_power_setpoint', 0.0),
            load_profile=row.get('load_profile', '')
            )
        logger.info("Buses added successfully!")

    def _add_generators(self):
        generators = self._read_csv('generators.csv')
        if generators.empty:
            logger.warning("No generators were added to the network.")
            return
        for _, row in generators.iterrows():
            self.network.add("Generator", row['name'],
            bus=row.get('bus', ''),
            control=row.get('control', ''),
            p_nom=row.get('p_nom', 0.0),
            efficiency=row.get('efficiency', 0.0),
            capital_cost=row.get('capital_cost', 0.0),
            marginal_cost=row.get('marginal_cost', 0.0),
            p_max_pu=row.get('p_max_pu', 0.0),
            p_min_pu=row.get('p_min_pu', 0.0)
            )
        logger.info("Generators added successfully!")

    def _add_storage_units(self):
        storage_units = self._read_csv('storage_units.csv')
        if storage_units.empty:
            logger.warning("No storage units were added to the network.")
            return
        for _, row in storage_units.iterrows():
            self.network.add("StorageUnit", row['name'],
            bus=row.get('bus', ''),
            p_nom=row.get('p_nom', 0.0),
            capital_cost=row.get('capital_cost', 0.0),
            state_of_charge_initial=row.get('state_of_charge_initial', 0.0),
            efficiency_store=row.get('efficiency_store', 0.0),
            efficiency_dispatch=row.get('efficiency_dispatch', 0.0),
            max_hours=row.get('max_hours', 0.0),
            marginal_cost=row.get('marginal_cost', 0.0),
            p_min_pu=row.get('p_min_pu', 0.0),
            p_max_pu=row.get('p_max_pu', 0.0),
            cyclic_state_of_charge=row.get('cyclic_state_of_charge', False),
            state_of_charge_min=row.get('state_of_charge_min', 0.0),
            state_of_charge_max=row.get('state_of_charge_max', 0.0)
            )
        logger.info("Storage units added successfully!")

    def _add_loads(self):
        loads = self._read_csv('loads.csv')
        if loads.empty:
            logger.warning("No loads were added to the network.")
            return
        for _, load in loads.iterrows():
            self.network.add("Load", load['name'],
            bus=load.get('bus', ''),
            p_set=pd.Series([float(x) for x in load.get('p_set', '').split(',')], index=self.network.snapshots),
            q_set=pd.Series([float(x) for x in load.get('q_set', '').split(',')], index=self.network.snapshots),
            p_min=load.get('p_min', 0.0),
            p_max=load.get('p_max', 0.0),
            scaling_factor=load.get('scaling_factor', 1.0),
            status=load.get('status', True),
            control_type=load.get('control_type', ''),
            response_time=load.get('response_time', 0.0),
            priority=load.get('priority', 0)
            )
        logger.info("Loads added successfully!")

    def _add_lines(self):
        lines = self._read_csv('lines.csv')
        if lines.empty:
            logger.warning("No lines were added to the network.")
            return
        for _, line in lines.iterrows():
            self.network.add("Line", line['name'],
            bus0=line.get('bus0', ''),
            bus1=line.get('bus1', ''),
            length=line.get('length', 0.0),
            r=line.get('r_per_length', 0.0) * line.get('length', 0.0),
            x=line.get('x_per_length', 0.0) * line.get('length', 0.0),
            c=line.get('c_per_length', 0.0) * line.get('length', 0.0),
            s_nom=line.get('s_nom', 0.0),
            type=line.get('type', ''),
            capital_cost=line.get('capital_cost', 0.0)
            )
        logger.info("Lines added successfully!")

    def _add_transformers(self):
        transformers = self._read_csv('transformers.csv')
        if transformers.empty:
            logger.warning("No transformers were added to the network.")
            return
        for _, transformer in transformers.iterrows():
            self.network.add("Transformer", transformer['name'],
            bus0=transformer.get('bus0', ''),
            bus1=transformer.get('bus1', ''),
            s_nom=transformer.get('s_nom', 0.0),
            x=transformer.get('x_pu', 0.0),
            r=transformer.get('r_pu', 0.0),
            tap_position=transformer.get('tap_position', 0),
            tap_min=transformer.get('tap_min', 0),
            tap_max=transformer.get('tap_max', 0),
            tap_step=transformer.get('tap_step', 0.0),
            efficiency=transformer.get('efficiency', 0.0),
            capital_cost=transformer.get('capital_cost', 0.0)
            )
        logger.info("Transformers added successfully!")

    def _add_links(self):
        links = self._read_csv('links.csv')
        if links.empty:
            logger.warning("No links were added to the network.")
            return
        for _, link in links.iterrows():
            self.network.add("Link", link['name'],
            bus0=link.get('bus0', ''),
            bus1=link.get('bus1', ''),
            p_nom=link.get('p_nom', 0.0),
            efficiency=link.get('efficiency', 0.0),
            capital_cost=link.get('capital_cost', 0.0),
            transformer_type=link.get('transformer_type', ''),
            min_pu=link.get('min_pu', 0.0),
            max_pu=link.get('max_pu', 0.0),
            reactive_power_capacity=link.get('reactive_power_capacity', 0.0),
            r=link.get('r', 0.0),
            x=link.get('x', 0.0),
            startup_cost=link.get('startup_cost', 0.0),
            shutdown_cost=link.get('shutdown_cost', 0.0),
            ramp_up=link.get('ramp_up', 0.0),
            ramp_down=link.get('ramp_down', 0.0),
            maintenance_cost=link.get('maintenance_cost', 0.0),
            control_type=link.get('control_type', '')
            )
        logger.info("Links added successfully!")

    def get_network(self):
        if self.network.buses.empty and self.network.generators.empty and self.network.storage_units.empty and self.network.loads.empty and self.network.lines.empty:
            logger.warning("The network is empty.")
        return self.network

    def get_generators(self):
        if self.network.generators.empty:
            logger.warning("The generators DataFrame is empty.")
        return self.network.generators

    def get_loads(self):
        if self.network.loads.empty:
            logger.warning("The loads DataFrame is empty.")
        return self.network.loads

    def get_lines(self):
        if self.network.lines.empty:
            logger.warning("The lines DataFrame is empty.")
        return self.network.lines

    def get_buses(self):
        if self.network.buses.empty:
            logger.warning("The buses DataFrame is empty.")
        return self.network.buses

    def get_storage_units(self):
        if self.network.storage_units.empty:
            logger.warning("The storage units DataFrame is empty.")
        return self.network.storage_units

    def get_transformers(self):
        if self.network.transformers.empty:
            logger.warning("The transformers DataFrame is empty.")
        return self.network.transformers

    def get_links(self):
        if self.network.links.empty:
            logger.warning("The links DataFrame is empty.")
        return self.network.links

def main():
    data_folder = 'data'
    network_setup = Network_Setup(data_folder)
    network_setup.setup_network()
    network = network_setup.get_network()
    logger.info(network.buses)
    logger.info(network.generators)
    logger.info(network.storage_units)
    logger.info(network.loads)
    logger.info(network.lines)
    logger.info(network.transformers)
    logger.info(network.links)

if __name__ == "__main__":
    main()