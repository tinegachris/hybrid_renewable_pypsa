from hybrid_renewable_pypsa.src.network_setup import NetworkSetup
from hybrid_renewable_pypsa.src.data_loader import DataLoader
from hybrid_renewable_pypsa.src.logger_setup import LoggerSetup
from typing import Dict, Any
import pandas as pd
import traceback

class NetworkAnalysisError(Exception):
    """Custom exception for network analysis errors."""
    pass

class NetworkAnalysis:
    """
    NetworkAnalysis class for analyzing a PyPSA network.
    
    This class performs various analyses:
        - Consistency check
        - Power flow (PF) analysis
        - Optimal power flow (OPF) analysis
        - Storage system performance analysis
        - Reliability analysis (e.g. unmet demand)
        - Load shift analysis
        - Losses analysis
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
        try:
            self.network.consistency_check()  # Raises error if inconsistencies are found
        except Exception as e:
            self.logger.error(f"Consistency check error: {e}")
            raise
        self.logger.info("Consistency check completed successfully.")
        return True

    def _run_pf(self) -> Dict[str, pd.DataFrame]:
        """Run power flow analysis and return results."""
        self.logger.info("Running Power Flow analysis...")
        try:
            self.network.pf()
            if hasattr(self.network, "converged") and not self.network.converged:
                raise Exception("Load flow did not converge.")
        except Exception as e:
            self.logger.error("Power Flow analysis failed:")
            self.logger.error(traceback.format_exc())
            raise Exception(f"Power Flow analysis failed: {str(e)}")
        
        self.logger.info("Power Flow analysis completed successfully.")
        try:
            bus_voltages = self.network.buses_t.get('v_mag_pu', pd.DataFrame()).copy()
            line_flows = self.network.lines_t.get('p0', pd.DataFrame()).copy()
            generator_dispatch = self.network.generators_t.get('p', pd.DataFrame()).copy()
        except Exception as e:
            self.logger.error("Error extracting power flow results:")
            self.logger.error(traceback.format_exc())
            raise Exception(f"Error extracting PF results: {str(e)}")
        
        return {
            "bus_voltages": bus_voltages,
            "line_flows": line_flows,
            "generator_dispatch": generator_dispatch,
        }

    def _run_opf(self) -> Dict[str, pd.DataFrame]:
        """Run optimal power flow analysis and return results."""
        self.logger.info("Running Optimal Power Flow analysis...")
        try:
            self.network.optimize()
        except Exception as e:
            self.logger.error(f"OPF optimization failed: {e}")
            raise
        self.logger.info("Optimal Power Flow analysis completed successfully.")
        try:
            generator_dispatch = self.network.generators_t.p.copy()
            storage_dispatch = self.network.storage_units_t.get('p', pd.DataFrame()).copy()
            marginal_costs = self.network.buses_t.get('marginal_price', pd.DataFrame()).copy()
        except Exception as e:
            self.logger.error(f"Error extracting OPF results: {e}")
            raise
        return {
            "generator_dispatch": generator_dispatch,
            "storage_dispatch": storage_dispatch,
            "marginal_costs": marginal_costs,
        }

    def _run_storage_analysis(self) -> Dict[str, pd.DataFrame]:
        """Analyze storage system performance over time."""
        self.logger.info("Running Storage analysis...")
        try:
            storage_dispatch = self.network.storage_units_t.get('p', pd.DataFrame()).copy()
            state_of_charge = self.network.storage_units_t.get('state_of_charge', pd.DataFrame()).copy()
        except Exception as e:
            self.logger.error(f"Error during storage analysis: {e}")
            raise
        self.logger.info("Storage analysis completed successfully.")
        return {
            "storage_dispatch": storage_dispatch,
            "state_of_charge": state_of_charge,
        }

    def _run_reliability_analysis(self) -> Dict[str, float]:
        """Evaluate the reliability of the network."""
        self.logger.info("Running Reliability analysis...")
        try:
            unmet_demand = (self.network.loads_t.p_set - self.network.loads_t.p).sum().sum()
        except Exception as e:
            self.logger.error(f"Error during reliability analysis: {e}")
            raise
        self.logger.info(f"Unmet demand: {unmet_demand}")
        self.logger.info("Reliability analysis completed successfully.")
        return {"unmet_demand": unmet_demand}

    def _run_load_shift_analysis(self) -> Dict[str, float]:
        """Evaluate the impact of shifting loads to off-peak hours."""
        self.logger.info("Running Load Shift analysis...")
        try:
            peak_load = self.network.loads_t.p_set.max().sum()
            off_peak_load = self.network.loads_t.p_set.min().sum()
            load_shift_potential = peak_load - off_peak_load
        except Exception as e:
            self.logger.error(f"Error during load shift analysis: {e}")
            raise
        self.logger.info(f"Load shift potential: {load_shift_potential}")
        self.logger.info("Load Shift analysis completed successfully.")
        return {"load_shift_potential": load_shift_potential}

    def _run_losses_analysis(self) -> Dict[str, float]:
        """Evaluate losses in the network."""
        self.logger.info("Running Losses analysis...")
        try:
            line_losses = (self.network.lines_t.p0 - self.network.lines_t.p1).sum().sum()
            bus_losses = (self.network.buses_t.p_set.sum(axis=1) - self.network.buses_t.p.sum(axis=1)).sum()
            transformer_losses = (self.network.transformers_t.p0 - self.network.transformers_t.p1).sum().sum()
            total_losses = line_losses + bus_losses + transformer_losses
        except Exception as e:
            self.logger.error(f"Error during losses analysis: {e}")
            raise
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
    try:
        network_analysis = NetworkAnalysis(data_folder)
        results = network_analysis.analyze_network()
        print(results)
    except NetworkAnalysisError as nae:
        print(f"Network Analysis Error: {nae}")
