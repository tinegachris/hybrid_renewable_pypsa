import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from network_setup import Network_Setup

class Network_Plot:
  """
  A class to handle the plotting of the network.
  """

  def __init__(self, data_folder):
    self.network_setup = Network_Setup(data_folder)
    self.network_setup.setup_network()
    self.network = self.network_setup.get_network()

  # # Plot the network using pypsa.Network.plot() method
  # def plot_network(self):
  #   lines_current_type = self.network.lines.bus0.map(self.network.buses.carrier)
  #   lines_current_type
  #   self.network.plot(
  #     line_colors=lines_current_type.map(lambda ct: "r" if ct == "DC" else "b"),
  #     title="Network Plot",
  #     color_geomap=True,
  #     jitter=0.3,
  #   )
  #   plt.tight_layout()

  # Plot the network using matplotlib
  def plot_network(self):
    """
    Plot the network using the setup network object.
    """

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)

    ax.set_extent([self.network.buses.x.min() - 1, self.network.buses.x.max() + 1, self.network.buses.y.min() - 1, self.network.buses.y.max() + 1])

    ax.scatter(self.network.buses.x, self.network.buses.y, transform=ccrs.PlateCarree(), s=200, color='red', zorder=5)
    for bus_name, bus in self.network.buses.iterrows():
      ax.text(bus.x, bus.y, bus_name, transform=ccrs.PlateCarree(), fontsize=12, zorder=5)

    for _, line in self.network.lines.iterrows():
      bus0 = self.network.buses.loc[line.bus0]
      bus1 = self.network.buses.loc[line.bus1]
      ax.plot([bus0.x, bus1.x], [bus0.y, bus1.y], transform=ccrs.PlateCarree(), color='black', zorder=1)

    print("Network is now plotting...\n")
    plt.show()

if __name__ == "__main__":
  data_folder = 'data'
  network_plot = Network_Plot(data_folder)
  network_plot.plot_network()