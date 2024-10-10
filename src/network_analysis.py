import pandas as pd
import numpy as np

from network_setup import Network_Setup

class NetworkAnalysis:
  """
  NetworkAnalysis class for analyzing a PyPSA network.
  Attributes:
    network (pypsa.Network): Instance of the PyPSA Network.
  """
  def __init__(self, network):
    self.network_setup = Network_Setup(data_folder)
    self.network_setup.setup_network()
    self.network = self.network_setup.get_network()

  def analyze_network(self):
    self._analyze_buses()
    self._analyze_generators()
    self._analyze_storage_units()
    self._analyze_lines()
    self._analyze_loads()

  def _analyze_buses(self):
    buses = self.network_setup.get_buses()
    print(buses, "\n")

  def _analyze_generators(self):
    generators = self.network_setup.get_generators()
    print(generators, "\n")

  def _analyze_storage_units(self):
    storage_units = self.network_setup.get_storage_units()
    print(storage_units, "\n")

  def _analyze_lines(self):
    lines = self.network_setup.get_lines()
    print(lines, "\n")

  def _analyze_loads(self):
    loads = self.network_setup.get_loads()
    print(loads, "\n")

  def _analyze_power_flows(self):
    """Perform Newton-Raphson power flow analysis on the network.
    """
    power_flows = self.network.pf()
    self.network.lines_t.p0
    self.network.buses_t.v_ang * 180 / np.pi
    self.network.buses_t.v_mag_pu

if __name__ == "__main__":
  data_folder = 'data'
  network_analysis = NetworkAnalysis(data_folder)
  network_analysis.analyze_network()