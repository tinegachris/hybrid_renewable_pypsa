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
        return pd.DataFrame() # Return an empty DataFrame if an error occurs

    def _add_buses(self):
        buses = self._read_csv('buses.csv')
        if buses.empty:
            logger.warning("No buses were added to the network.")
            return
        for _, row in buses.iterrows():
            self.network.add("Bus", row['name'],
            v_nom=row['v_nom'],
            x=row['x'],
            y=row['y'],
            carrier=row['carrier'],
            v_mag_pu_set=row.get('v_mag_pu_set', None),
            v_mag_pu_min=row.get('v_mag_pu_min', None),
            v_mag_pu_max=row.get('v_mag_pu_max', None),
            control=row.get('control', None),
            v_target=row.get('v_target', None),
            marginal_cost=row.get('marginal_cost', None),
            zone=row.get('zone', None),
            type=row.get('type', None),
            max_shunt_capacitor=row.get('max_shunt_capacitor', None),
            min_shunt_capacitor=row.get('min_shunt_capacitor', None),
            reactive_power_setpoint=row.get('reactive_power_setpoint', None),
            load_profile=row.get('load_profile', None)
            )
        logger.info("Buses added successfully!")

    def _add_generators(self):
        generators = self._read_csv('generators.csv')
        if generators.empty:
            logger.warning("No generators were added to the network.")
            return
        for _, row in generators.iterrows():
            self.network.add("Generator", row['name'],
            bus=row['bus'],
            control=row['control'],
            p_nom=row['p_nom'],
            efficiency=row['efficiency'],
            capital_cost=row['capital_cost'],
            marginal_cost=row['marginal_cost'],
            p_max_pu=row['p_max_pu'],
            p_min_pu=row['p_min_pu']
            )
        logger.info("Generators added successfully!")

    def _add_storage_units(self):
        storage_units = self._read_csv('storage_units.csv')
        if storage_units.empty:
            logger.warning("No storage units were added to the network.")
            return
        for _, row in storage_units.iterrows():
            self.network.add("StorageUnit", row['name'],
            bus=row['bus'],
            p_nom=row['p_nom'],
            capital_cost=row['capital_cost'],
            state_of_charge_initial=row['state_of_charge_initial'],
            efficiency_store=row['efficiency_store'],
            efficiency_dispatch=row['efficiency_dispatch'],
            max_hours=row['max_hours'],
            marginal_cost=row['marginal_cost'],
            p_min_pu=row['p_min_pu'],
            p_max_pu=row['p_max_pu'],
            cyclic_state_of_charge=row['cyclic_state_of_charge'],
            state_of_charge_min=row['state_of_charge_min'],
            state_of_charge_max=row['state_of_charge_max']
            )
        logger.info("Storage units added successfully!")

    def _add_loads(self):
        loads = self._read_csv('loads.csv')
        if loads.empty:
            logger.warning("No loads were added to the network.")
            return
        for _, load in loads.iterrows():
            self.network.add("Load", load['name'],
            bus=load['bus'],
            p_set=pd.Series([float(x) for x in load['p_set'].split(',')], index=self.network.snapshots),
            q_set=pd.Series([float(x) for x in load['q_set'].split(',')], index=self.network.snapshots),
            p_min=load['p_min'],
            p_max=load['p_max'],
            scaling_factor=load['scaling_factor'],
            status=load['status'],
            control_type=load['control_type'],
            response_time=load['response_time'],
            priority=load['priority']
            )
        logger.info("Loads added successfully!")

    def _add_lines(self):
        lines = self._read_csv('lines.csv')
        if lines.empty:
            logger.warning("No lines were added to the network.")
            return
        for _, line in lines.iterrows():
            self.network.add("Line", line['name'],
            bus0=line['bus0'],
            bus1=line['bus1'],
            length=line['length'],
            r=line['r_per_length'] * line['length'],
            x=line['x_per_length'] * line['length'],
            c=line['c_per_length'] * line['length'],
            s_nom=line['s_nom'],
            type=line['type'],
            capital_cost=line['capital_cost']
            )
        logger.info("Lines added successfully!")

    def _add_transformers(self):
        transformers = self._read_csv('transformers.csv')
        if transformers.empty:
            logger.warning("No transformers were added to the network.")
            return
        for _, transformer in transformers.iterrows():
            self.network.add("Transformer", transformer['name'],
            bus0=transformer['bus0'],
            bus1=transformer['bus1'],
            s_nom=transformer['s_nom'],
            x=transformer['x_pu'],
            r=transformer['r_pu'],
            tap_position=transformer['tap_position'],
            tap_min=transformer['tap_min'],
            tap_max=transformer['tap_max'],
            tap_step=transformer['tap_step'],
            efficiency=transformer['efficiency'],
            capital_cost=transformer['capital_cost']
            )
        logger.info("Transformers added successfully!")

    def _add_links(self):
        links = self._read_csv('links.csv')
        if links.empty:
            logger.warning("No links were added to the network.")
            return
        for _, link in links.iterrows():
            self.network.add("Link", link['name'],
            bus0=link['bus0'],
            bus1=link['bus1'],
            p_nom=link['p_nom'],
            efficiency=link['efficiency'],
            capital_cost=link['capital_cost'],
            transformer_type=link['transformer_type'],
            min_pu=link['min_pu'],
            max_pu=link['max_pu'],
            reactive_power_capacity=link['reactive_power_capacity'],
            r=link['r'],
            x=link['x'],
            startup_cost=link['startup_cost'],
            shutdown_cost=link['shutdown_cost'],
            ramp_up=link['ramp_up'],
            ramp_down=link['ramp_down'],
            maintenance_cost=link['maintenance_cost'],
            control_type=link['control_type']
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