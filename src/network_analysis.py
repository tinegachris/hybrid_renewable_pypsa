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

    def _run_pf(self):
        self.logger.info("Running Power Flow analysis...")
        self.network_setup.network.pf()
        self.logger.info("Power Flow analysis completed successfully!")

    def _run_opf(self):
        self.logger.info("Running Optimal Power Flow analysis...")
        self.network_setup.network.optimize()
        self.logger.info("Optimal Power Flow analysis completed successfully!")

    def get_results(self):
        return self.network_setup.network.buses_t.p_set

    def save_results(self, output_file):
        results = self.get_results()
        results.to_csv(output_file)
        self.logger.info(f"Results saved to {output_file}")

    def main(data_folder, output_file):
        network_analysis = Network_Analysis(data_folder)
        network_analysis.analyze_network()
        network_analysis.save_results(output_file)

if __name__ == '__main__':
    data_folder = 'data'
    output_file = 'results.csv'
    Network_Analysis.main(data_folder, output_file)