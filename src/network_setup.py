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

  def _add_buses(self):
    buses_file = os.path.join(self.data_folder, 'buses.csv')
    buses = pd.read_csv(buses_file)
    for _, row in buses.iterrows():
      self.network.add("Bus", row['name'],
      v_nom=row['v_nom'],
      x=row['x'],
      y=row['y'],
      carrier=row['carrier']
      )

  def _add_generators(self):
    generators_file = os.path.join(self.data_folder, 'generators.csv')
    generators = pd.read_csv(generators_file)
    for _, row in generators.iterrows():
      self.network.add("Generator", row['name'],
      bus=row['bus'],
      p_nom=row['p_nom'],
      efficiency=row['efficiency'],
      capital_cost=row['capital_cost'],
      marginal_cost=row['op_cost']
      )

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
      efficiency_dispatch=row['efficiency_dispatch']
      )

  def _add_loads(self):
    loads_file = os.path.join(self.data_folder, 'loads.csv')
    loads = pd.read_csv(loads_file)
    for _, load in loads.iterrows():
      self.network.add("Load", load['name'],
      bus=load['bus'],
      carrier=load['carrier'],
      p_set=load['p_set'],
      q_set=load['q_set']
      )

  def _add_lines(self):
    lines_file = os.path.join(self.data_folder, 'lines.csv')
    lines = pd.read_csv(lines_file)
    for _, line in lines.iterrows():
      self.network.add("Line", line['name'],
      bus0=line['bus0'],
      bus1=line['bus1'],
      x=line['x'],
      r=line['r'],
      capital_cost=line['capital_cost'],
      length=line['length']
      )

  def get_network(self):
    return self.network

  def get_generators(self):
    return self.network.generators

  def get_loads(self):
    return self.network.loads

  def get_lines(self):
    return self.network.lines

  def get_buses(self):
    return self.network.buses

  def get_snapshots(self):
    return self.network.snapshots

  def get_time_series(self):
    return self.network.loads_t.p_set

  def get_time_series_for_bus(self, bus_name):
    return self.network.loads_t.p_set[bus_name]

  def get_time_series_for_generator(self, generator_name):
    return self.network.generators_t.p[generator_name]

  def get_time_series_for_line(self, line_name):
    return self.network.lines_t.p0[line_name]

  def get_time_series_for_load(self, load_name):
    return self.network.loads_t.p[load_name]

if __name__ == "__main__":
  data_folder = 'data'
  network_setup = Network_Setup(data_folder)
  network_setup.setup_network()
  network = network_setup.get_network()
  print(network.buses)
  print(network.generators)
  print(network.storage_units)
  print(network.loads)
  print(network.lines)
