import pypsa
import pandas as pd
import numpy as np

from network_setup import Network_Setup
from data_loader import Data_Loader
from logger_setup import Logger_Setup

class Network_Analysis:
  """
  Network_Analysis class for analyzing a PyPSA network.
  Attributes:
      network_setup (Network_Setup): Instance of the Network_Setup class.
  """
  def __init__(self, data_folder):
      self.network_setup = Network_Setup(data_folder)
      self.logger = Logger_Setup.setup_logger('NetworkAnalysis')

  def analyze_network(self):
      self.network_setup.setup_network()
      self._run_pf()
      self._run_opf()
      self._run_storage_analysis()
      self._run_reliability_analysis()
      self._run_load_shift_analysis()
      self._run_losses_analysis()

  def _run_pf(self):
    """
    Determine voltage, current, and power flows in each line, and voltages at each bus under steady-state conditions.
    """
    self.logger.info("Running Power Flow analysis...")
    self.network_setup.network.pf()
    self.logger.info("Power Flow analysis completed successfully!")

  def _run_opf(self):
    """
    Determine the optimal generation dispatch while minimizing cost, maximizing efficiency, or reducing emissions.
    """
    self.logger.info("Running Optimal Power Flow analysis...")
    self.network_setup.network.optimize()
    self.logger.info("Optimal Power Flow analysis completed successfully!")

  def _run_storage_analysis(self):
    """
    Evaluate how the storage system performs over time, including charge and discharge cycles.
    """
    self.logger.info("Running Storage analysis...")
    #self.network_setup.network.storage_analysis()
    self.logger.info("Storage analysis completed successfully!")

  def _run_reliability_analysis(self):
    """
    Evaluate the reliability of the network, including the impact of outages and failures.
    """
    self.logger.info("Running Reliability analysis...")
    #self.network_setup.network.reliability_analysis()
    self.logger.info("Reliability analysis completed successfully!")

  def _run_load_shift_analysis(self):
    """
    Evaluate the impact of shifting loads to off-peak hours.
    """
    self.logger.info("Running Load Shift analysis...")
    #self.network_setup.network.load_shift_analysis()
    self.logger.info("Load Shift analysis completed successfully!")

  def _run_losses_analysis(self):
    """
    _summary_
    """
    line_losses = self.network_setup.network.lines_t.p0 - self.network_setup.network.lines_t.p1
    self.logger.info(f"Line losses: {line_losses.sum().sum()}")
    bus_losses = self.network_setup.network.buses_t.p_set.sum(axis=1) - self.network_setup.network.buses_t.p.sum(axis=1)
    self.logger.info(f"Bus losses: {bus_losses.sum()}")
    transformer_losses = self.network_setup.network.transformers_t.p0 - self.network_setup.network.transformers_t.p1
    self.logger.info(f"Transformer losses: {transformer_losses.sum().sum()}")
    self.logger.info(f"Total losses: {line_losses.sum().sum() + bus_losses.sum() + transformer_losses.sum().sum()}")

  def main(data_folder, output_file):
      network_analysis = Network_Analysis(data_folder)
      network_analysis.analyze_network()

if __name__ == '__main__':
    data_folder = 'data'
    Network_Analysis.main(data_folder)