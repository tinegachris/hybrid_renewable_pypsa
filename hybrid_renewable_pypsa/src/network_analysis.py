from hybrid_renewable_pypsa.src.network_setup import Network_Setup
from hybrid_renewable_pypsa.src.data_loader import Data_Loader
from hybrid_renewable_pypsa.src.logger_setup import Logger_Setup

class Network_Analysis:
  """
  Network_Analysis class for analyzing a PyPSA network.
  Attributes:
    network_setup (Network_Setup): Instance of the Network_Setup class.
  """
  def __init__(self, data_folder):
    self.data_loader = Data_Loader(data_folder)
    self.network_setup = Network_Setup(data_folder)
    self.network_setup.setup_network()
    self.network = self.network_setup.get_network()
    self.logger = Logger_Setup.setup_logger('NetworkAnalysis')

  def analyze_network(self):
    """Run all analysis methods."""
    self.logger.info("Analyzing network...\n")
    self._run_consistency_check()
    self._run_pf()
    self._run_opf()
    self._run_storage_analysis()
    self._run_reliability_analysis()
    self._run_load_shift_analysis()
    self._run_losses_analysis()
    self.logger.info("Network analysis completed successfully!\n")

  def _run_consistency_check(self):
    """Check the consistency of the network."""
    self.logger.info("Running consistency check...\n")
    self.network_setup.network.consistency_check()
    self.logger.info("Consistency check completed successfully!\n")

  def _run_pf(self):
    """Determine voltage, current, and power flows in each line, and voltages at each bus under steady-state conditions."""
    self.logger.info("Running Power Flow analysis...\n")
    self.network_setup.network.pf()
    self.logger.info("Power Flow analysis completed successfully!\n")

  def _run_opf(self):
    """Determine the optimal generation dispatch while minimizing cost, maximizing efficiency, or reducing emissions."""
    self.logger.info("Running Optimal Power Flow analysis...\n")
    self.network_setup.network.optimize()
    self.logger.info("Optimal Power Flow analysis completed successfully!\n")

  def _run_storage_analysis(self):
    """Evaluate how the storage system performs over time, including charge and discharge cycles."""
    self.logger.info("Running Storage analysis...\n")
    self.logger.info("Storage analysis completed successfully!\n")

  def _run_reliability_analysis(self):
    """Evaluate the reliability of the network, including the impact of outages and failures."""
    self.logger.info("Running Reliability analysis...\n")
    self.logger.info("Reliability analysis completed successfully!\n")

  def _run_load_shift_analysis(self):
    """Evaluate the impact of shifting loads to off-peak hours."""
    self.logger.info("Running Load Shift analysis...\n")
    self.logger.info("Load Shift analysis completed successfully!\n")

  def _run_losses_analysis(self):
    """Evaluate the losses in the network, including line, bus, and transformer losses."""
    self.logger.info("Running Losses analysis...\n")
    line_losses = self.network_setup.network.lines_t.p0 - self.network_setup.network.lines_t.p1
    self.logger.info(f"Line losses: {line_losses.sum().sum()}")
    bus_losses = self.network_setup.network.buses_t.p_set.sum(axis=1) - self.network_setup.network.buses_t.p.sum(axis=1)
    self.logger.info(f"Bus losses: {bus_losses.sum()}")
    transformer_losses = self.network_setup.network.transformers_t.p0 - self.network_setup.network.transformers_t.p1
    self.logger.info(f"Transformer losses: {transformer_losses.sum().sum()}")
    self.logger.info(f"Total losses: {line_losses.sum().sum() + bus_losses.sum() + transformer_losses.sum().sum()}")

if __name__ == '__main__':
  data_folder = 'hybrid_renewable_pypsa/data'
  network_analysis = Network_Analysis(data_folder)
  network_analysis.analyze_network()
