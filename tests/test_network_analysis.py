import pytest
from unittest.mock import MagicMock
from hybrid_renewable_pypsa.src.network_analysis import Network_Analysis
from hybrid_renewable_pypsa.src.network_setup import Network_Setup
from hybrid_renewable_pypsa.src.data_loader import Data_Loader

@pytest.fixture
def mock_data_loader():
  """Fixture for mocking Data_Loader."""
  data_loader = Data_Loader('data')
  data_loader.read_csv = MagicMock(autospec=True)
  return data_loader

def create_mock_network():
  """Helper function to create a mocked network."""
  network = MagicMock(autospec=True)
  network.buses = MagicMock(autospec=True)
  network.generators = MagicMock(autospec=True)
  network.storage_units = MagicMock(autospec=True)
  network.loads = MagicMock(autospec=True)
  network.lines = MagicMock(autospec=True)
  network.transformers = MagicMock(autospec=True)
  network.links = MagicMock(autospec=True)
  network.consistency_check = MagicMock(autospec=True)
  network.pf = MagicMock(autospec=True)
  network.optimize = MagicMock(autospec=True)
  network.lines_t = MagicMock(autospec=True)
  network.buses_t = MagicMock(autospec=True)
  network.transformers_t = MagicMock(autospec=True)
  return network

@pytest.fixture
def mock_network_setup(mock_data_loader):
  """Fixture for mocking Network_Setup."""
  network_setup = Network_Setup('hybrid_renewable_pypsa/data')
  network_setup.data_loader = mock_data_loader
  network_setup.network = create_mock_network()
  return network_setup

@pytest.fixture
def network_analysis(mock_network_setup):
  """Fixture for creating Network_Analysis with mocked Network_Setup."""
  network_analysis = Network_Analysis('data')
  network_analysis.network_setup = mock_network_setup
  return network_analysis

def test_run_consistency_check(network_analysis):
  """Test the _run_consistency_check method."""
  network_analysis._run_consistency_check()
  network_analysis.network_setup.network.consistency_check.assert_called_once()

def test_run_pf(network_analysis):
  """Test the _run_pf method."""
  network_analysis._run_pf()
  network_analysis.network_setup.network.pf.assert_called_once()

def test_run_opf(network_analysis):
  """Test the _run_opf method."""
  network_analysis._run_opf()
  network_analysis.network_setup.network.optimize.assert_called_once()
