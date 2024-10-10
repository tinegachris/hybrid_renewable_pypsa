#import warnings
from network_setup import Network_Setup

# Suppress specific warning from cartopy
#warnings.filterwarnings("ignore", message='facecolor will have no effect as it has been defined as "never"')

class NetworkPlot:
  """
  A class to handle the plotting of the network.
  """

  def __init__(self, data_folder):
    self.network_setup = Network_Setup(data_folder)
    self.network_setup.setup_network()
    self.network = self.network_setup.get_network()

  def plot_network(self):
    """
    Plot the network using the setup network object.
    """
    self.network.plot()

if __name__ == "__main__":
  data_folder = 'data'
  network_plot = NetworkPlot(data_folder)
  network_plot.plot_network()