from hybrid_renewable_pypsa.src.network_setup import NetworkSetup
from hybrid_renewable_pypsa.src.data_loader import DataLoader
from hybrid_renewable_pypsa.src.logger_setup import LoggerSetup
from typing import Dict, Any
import pandas as pd

class NetworkAnalysisError(Exception):
    """Custom exception for network analysis errors."""
    pass

class NetworkAnalysis:
    """
    Network_Analysis class for analyzing a PyPSA network.
    Attributes:
        network_setup (NetworkSetup): Instance of the NetworkSetup class.
        network (pypsa.Network): The PyPSA network to analyze.
        logger (Logger): Logger instance for logging analysis progress.
    """
    def __init__(self, data_folder: str) -> None:
        self.data_loader = DataLoader(data_folder)
        self.network_setup = NetworkSetup(data_folder)
        self.network_setup.setup_network()
        self.network = self.network_setup.get_network()
        self.logger = LoggerSetup.setup_logger('NetworkAnalysis')

    def analyze_network(self) -> Dict[str, Any]:
        """Run all analysis methods and return a summary of results."""
        self.logger.info("Starting network analysis...")
        results = {}

        try:
            results["consistency_check"] = self._run_consistency_check()
            results["power_flow"] = self._run_pf()
            results["optimal_power_flow"] = self._run_opf()
            results["storage_analysis"] = self._run_storage_analysis()
            results["reliability_analysis"] = self._run_reliability_analysis()
            results["load_shift_analysis"] = self._run_load_shift_analysis()
            results["losses_analysis"] = self._run_losses_analysis()
            self.logger.info("Network analysis completed successfully!")
        except Exception as e:
            self.logger.error(f"Network analysis failed: {e}")
            raise NetworkAnalysisError(f"Analysis failed: {e}")

        return results

    def _run_consistency_check(self) -> bool:
        """Check the consistency of the network."""
        self.logger.info("Running consistency check...")
        self.network.consistency_check()
        self.logger.info("Consistency check completed successfully.")
        return True

    def _run_pf(self) -> Dict[str, pd.DataFrame]:
        """Run power flow analysis and return results."""
        self.logger.info("Running Power Flow analysis...")
        self.network.pf()
        self.logger.info("Power Flow analysis completed successfully.")

        # Extract and return power flow results
        return {
            "bus_voltages": self.network.buses_t.v_mag_pu,
            "line_flows": self.network.lines_t.p0,
            "generator_dispatch": self.network.generators_t.p,
        }

    def _run_opf(self) -> Dict[str, pd.DataFrame]:
        """Run optimal power flow analysis and return results."""
        self.logger.info("Running Optimal Power Flow analysis...")
        self.network.optimize()
        self.logger.info("Optimal Power Flow analysis completed successfully.")

        # Extract and return OPF results
        return {
            "generator_dispatch": self.network.generators_t.p,
            "storage_dispatch": self.network.storage_units_t.p,
            "marginal_costs": self.network.buses_t.marginal_price,
        }

    def _run_storage_analysis(self) -> Dict[str, pd.DataFrame]:
        """Analyze storage system performance over time."""
        self.logger.info("Running Storage analysis...")
        storage_units = self.network.storage_units_t.p
        state_of_charge = self.network.storage_units_t.state_of_charge
        self.logger.info("Storage analysis completed successfully.")

        return {
            "storage_dispatch": storage_units,
            "state_of_charge": state_of_charge,
        }

    def _run_reliability_analysis(self) -> Dict[str, float]:
        """Evaluate the reliability of the network."""
        self.logger.info("Running Reliability analysis...")
        # Example: Calculate load shedding or unmet demand
        unmet_demand = (self.network.loads_t.p_set - self.network.loads_t.p).sum().sum()
        self.logger.info(f"Unmet demand: {unmet_demand}")
        self.logger.info("Reliability analysis completed successfully.")

        return {"unmet_demand": unmet_demand}

    def _run_load_shift_analysis(self) -> Dict[str, float]:
        """Evaluate the impact of shifting loads to off-peak hours."""
        self.logger.info("Running Load Shift analysis...")
        # Example: Calculate peak and off-peak load differences
        peak_load = self.network.loads_t.p_set.max().sum()
        off_peak_load = self.network.loads_t.p_set.min().sum()
        load_shift_potential = peak_load - off_peak_load
        self.logger.info(f"Load shift potential: {load_shift_potential}")
        self.logger.info("Load Shift analysis completed successfully.")

        return {"load_shift_potential": load_shift_potential}

    def _run_losses_analysis(self) -> Dict[str, float]:
        """Evaluate losses in the network."""
        self.logger.info("Running Losses analysis...")
        line_losses = (self.network.lines_t.p0 - self.network.lines_t.p1).sum().sum()
        bus_losses = (self.network.buses_t.p_set.sum(axis=1) - self.network.buses_t.p.sum(axis=1)).sum()
        transformer_losses = (self.network.transformers_t.p0 - self.network.transformers_t.p1).sum().sum()
        total_losses = line_losses + bus_losses + transformer_losses

        self.logger.info(f"Line losses: {line_losses}")
        self.logger.info(f"Bus losses: {bus_losses}")
        self.logger.info(f"Transformer losses: {transformer_losses}")
        self.logger.info(f"Total losses: {total_losses}")
        self.logger.info("Losses analysis completed successfully.")

        return {
            "line_losses": line_losses,
            "bus_losses": bus_losses,
            "transformer_losses": transformer_losses,
            "total_losses": total_losses,
        }

if __name__ == '__main__':
    data_folder = 'hybrid_renewable_pypsa/data'
    network_analysis = NetworkAnalysis(data_folder)
    results = network_analysis.analyze_network()
    print(results)