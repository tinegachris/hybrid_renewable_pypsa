import pypsa
import pandas as pd
import os

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

  def setup_network(self):
    self._add_buses()
    self._add_generators()
    self._add_storage_units()
    self._add_loads()
    self._add_lines()
    print("Network was setup successfully!\n")

  def _add_buses(self):
    buses_file = os.path.join(self.data_folder, 'buses.csv')
    buses = pd.read_csv(buses_file)
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
      load_profile=row.get('load_profile', None),
      description=row.get('description', None)
      )
    print("\nBuses added successfully!\n")

  def _add_generators(self):
    generators_file = os.path.join(self.data_folder, 'generators.csv')
    generators = pd.read_csv(generators_file)
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
    print("Generators added successfully!\n")

  def _add_storage_units(self):
    storage_units_file = os.path.join(self.data_folder, 'storage_units.csv')
    storage_units = pd.read_csv(storage_units_file)
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
      state_of_charge_max=row['state_of_charge_max'],
      description=row['description']
      )
    print("Storage units added successfully!\n")

  def _add_loads(self):
    loads_file = os.path.join(self.data_folder, 'loads.csv')
    loads = pd.read_csv(loads_file)
    for _, load in loads.iterrows():
      self.network.add("Load", load['name'],
      bus=load['bus'],
      p_set=load['p_set'],
      p_min=load['p_min'],
      p_max=load['p_max'],
      scaling_factor=load['scaling_factor'],
      status=load['status'],
      control_type=load['control_type'],
      response_time=load['response_time'],
      priority=load['priority']
      )
    print("Loads added successfully!\n")

  def _add_lines(self):
    lines_file = os.path.join(self.data_folder, 'lines.csv')
    lines = pd.read_csv(lines_file)
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
      capital_cost=line['capital_cost'],
      description=line['description']
      )
    print("Lines added successfully!\n")

  def _add_transformers(self):
    transformers_file = os.path.join(self.data_folder, 'transformers.csv')
    transformers = pd.read_csv(transformers_file)
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
      capital_cost=transformer['capital_cost'],
      description=transformer['description']
      )

  def get_network(self):
    if self.network.buses.empty and self.network.generators.empty and self.network.storage_units.empty and self.network.loads.empty and self.network.lines.empty:
      print("Warning: The network is empty.\n")
    return self.network

  def get_generators(self):
    if self.network.generators.empty:
      print("Warning: The generators DataFrame is empty.\n")
    return self.network.generators

  def get_loads(self):
    if self.network.loads.empty:
      print("Warning: The loads DataFrame is empty.\n")
    return self.network.loads

  def get_lines(self):
    if self.network.lines.empty:
      print("Warning: The lines DataFrame is empty.\n")
    return self.network.lines

  def get_buses(self):
    if self.network.buses.empty:
      print("Warning: The buses DataFrame is empty.\n")
    return self.network.buses

  def get_time_series(self):
    if self.network.loads_t.p_set.empty:
      print("Warning: The time series DataFrame is empty.\n")
    return self.network.loads_t.p_set

  def get_time_series_for_bus(self, bus_name):
    if bus_name not in self.network.loads_t.p_set.columns:
      print(f"Warning: No time series data for bus '{bus_name}'.\n")
    return self.network.loads_t.p_set[bus_name]

  def get_time_series_for_generator(self, generator_name):
    if generator_name not in self.network.generators_t.p.columns:
      print(f"Warning: No time series data for generator '{generator_name}'.\n")
    return self.network.generators_t.p[generator_name]

  def get_time_series_for_line(self, line_name):
    if line_name not in self.network.lines_t.p0.columns:
      print(f"Warning: No time series data for line '{line_name}'.\n")
    return self.network.lines_t.p0[line_name]

  def get_time_series_for_load(self, load_name):
    if load_name not in self.network.loads_t.p.columns:
      print(f"Warning: No time series data for load '{load_name}'.\n")
    return self.network.loads_t.p[load_name]

if __name__ == "__main__":
  data_folder = 'data'
  network_setup = Network_Setup(data_folder)
  network_setup.setup_network()
  network = network_setup.get_network()
  print(network.buses, "\n")
  print(network.generators, "\n")
  print(network.storage_units, "\n")
  print(network.loads, "\n")
  print(network.lines, "\n")
