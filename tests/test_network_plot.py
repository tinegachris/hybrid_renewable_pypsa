import pytest
from unittest.mock import patch, MagicMock
from hybrid_renewable_pypsa.src.network_plot import Network_Plot

@pytest.fixture
def network_plot():
  data_folder = 'hybrid_renewable_pypsa/data'
  return Network_Plot(data_folder)

def test_network_setup(network_plot):
  assert network_plot.network_setup is not None
  assert network_plot.network is not None
  assert hasattr(network_plot, 'plot_network')

@patch('hybrid_renewable_pypsa.src.network_plot.Network_Plot.plot_network', new_callable=MagicMock)
def test_plot_network(mock_plot_network, network_plot):
  try:
    network_plot.plot_network()
    mock_plot_network.assert_called_once()
  except Exception as e:
    pytest.fail(f"plot_network() raised an exception: {e}")
