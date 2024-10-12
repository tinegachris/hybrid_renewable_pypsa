import unittest
import os
import pandas as pd
from src.network_setup import Network_Setup

class TestNetworkSetup(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    cls.data_folder = 'test_data'
    os.makedirs(cls.data_folder, exist_ok=True)
    cls.create_test_data_files()

  @classmethod
  def tearDownClass(cls):
    for file in os.listdir(cls.data_folder):
      os.remove(os.path.join(cls.data_folder, file))
    os.rmdir(cls.data_folder)

  @classmethod
  def create_test_data_files(cls):
    buses_data = pd.DataFrame({
      'name': ['bus1', 'bus2'],
      'v_nom': [110, 220],
      'x': [0, 1],
      'y': [0, 1],
      'carrier': ['AC', 'AC']
    })
    buses_data.to_csv(os.path.join(cls.data_folder, 'buses.csv'), index=False)

    generators_data = pd.DataFrame({
      'name': ['gen1', 'gen2'],
      'bus': ['bus1', 'bus2'],
      'p_nom': [100, 200],
      'efficiency': [0.9, 0.85],
      'capital_cost': [1000, 2000],
      'op_cost': [10, 20]
    })
    generators_data.to_csv(os.path.join(cls.data_folder, 'generators.csv'), index=False)

    storage_units_data = pd.DataFrame({
      'name': ['storage1'],
      'bus': ['bus1'],
      'p_nom': [50],
      'capital_cost': [500],
      'state_of_charge_initial': [0.5],
      'efficiency_store': [0.95],
      'efficiency_dispatch': [0.9]
    })
    storage_units_data.to_csv(os.path.join(cls.data_folder, 'storage_units.csv'), index=False)

    loads_data = pd.DataFrame({
      'name': ['load1'],
      'bus': ['bus1'],
      'carrier': ['electricity'],
      'p_set': [50],
      'q_set': [30]
    })
    loads_data.to_csv(os.path.join(cls.data_folder, 'loads.csv'), index=False)

    lines_data = pd.DataFrame({
      'name': ['line1'],
      'bus0': ['bus1'],
      'bus1': ['bus2'],
      'x': [0.1],
      'r': [0.01],
      'capital_cost': [100],
      'length': [10]
    })
    lines_data.to_csv(os.path.join(cls.data_folder, 'lines.csv'), index=False)

  def setUp(self):
    self.network_setup = Network_Setup(self.data_folder)
    self.network_setup.setup_network()

  def test_buses_added(self):
    buses = self.network_setup.get_buses()
    self.assertEqual(len(buses), 2)
    self.assertIn('bus1', buses.index)
    self.assertIn('bus2', buses.index)

  def test_generators_added(self):
    generators = self.network_setup.get_generators()
    self.assertEqual(len(generators), 2)
    self.assertIn('gen1', generators.index)
    self.assertIn('gen2', generators.index)

  def test_storage_units_added(self):
    storage_units = self.network_setup.get_storage_units()
    self.assertEqual(len(storage_units), 1)
    self.assertIn('storage1', storage_units.index)

  def test_loads_added(self):
    loads = self.network_setup.get_loads()
    self.assertEqual(len(loads), 1)
    self.assertIn('load1', loads.index)

  def test_lines_added(self):
    lines = self.network_setup.get_lines()
    self.assertEqual(len(lines), 1)
    self.assertIn('line1', lines.index)

  def test_network_not_empty(self):
    network = self.network_setup.get_network()
    self.assertFalse(network.buses.empty)
    self.assertFalse(network.generators.empty)
    self.assertFalse(network.storage_units.empty)
    self.assertFalse(network.loads.empty)
    self.assertFalse(network.lines.empty)

if __name__ == '__main__':
  unittest.main()