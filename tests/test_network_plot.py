import pytest
from src.network_plot import Network_Plot

@pytest.fixture
def network_plot():
  data_folder = 'data'
  return Network_Plot(data_folder)

def test_network_setup(network_plot):
  assert network_plot.network_setup is not None
  assert network_plot.network is not None

def test_plot_network(network_plot):
  try:
    network_plot.plot_network()
  except Exception as e:
    pytest.fail(f"plot_network() raised an exception: {e}")
