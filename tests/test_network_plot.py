import unittest
from src.network_plot import Network_Plot

class TestNetworkPlot(unittest.TestCase):

  def setUp(self):
    self.data_folder = 'data'
    self.network_plot = Network_Plot(self.data_folder)

  def test_network_setup(self):
    self.assertIsNotNone(self.network_plot.network_setup)
    self.assertIsNotNone(self.network_plot.network)

  def test_plot_network(self):
    try:
      self.network_plot.plot_network()
    except Exception as e:
      self.fail(f"plot_network() raised an exception: {e}")

if __name__ == "__main__":
  unittest.main()