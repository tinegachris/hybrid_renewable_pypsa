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


  def plot_network(self):
    """
    Plot the network using the setup network object.
    """
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    # Add geographical features
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)

    # Set the extent of the plot
    ax.set_extent([
      self.network.buses.x.min() - 1, self.network.buses.x.max() + 1,
      self.network.buses.y.min() - 1, self.network.buses.y.max() + 1
    ])

    # Plot buses
    ax.scatter(
      self.network.buses.x, self.network.buses.y, transform=ccrs.PlateCarree(),
      s=200, color='red', zorder=5, label='Buses'
    )
    for bus_name, bus in self.network.buses.iterrows():
      ax.text(
        bus.x, bus.y, bus_name, transform=ccrs.PlateCarree(),
        fontsize=12, zorder=5, ha='right'
      )

    # Plot lines
    for _, line in self.network.lines.iterrows():
      bus0 = self.network.buses.loc[line.bus0]
      bus1 = self.network.buses.loc[line.bus1]
      ax.plot(
        [bus0.x, bus1.x], [bus0.y, bus1.y], transform=ccrs.PlateCarree(),
        color='black', zorder=1, label='Lines' if _ == 0 else ""
      )

    # Plot links
    for _, link in self.network.links.iterrows():
      bus0 = self.network.buses.loc[link.bus0]
      bus1 = self.network.buses.loc[link.bus1]
      ax.plot(
        [bus0.x, bus1.x], [bus0.y, bus1.y], transform=ccrs.PlateCarree(),
        color='blue', linestyle='--', zorder=2, label='Links' if _ == 0 else ""
      )

    # Plot transformers
    for _, transformer in self.network.transformers.iterrows():
      bus0 = self.network.buses.loc[transformer.bus0]
      bus1 = self.network.buses.loc[transformer.bus1]
      ax.plot(
        [bus0.x, bus1.x], [bus0.y, bus1.y], transform=ccrs.PlateCarree(),
        color='green', linestyle=':', zorder=3, label='Transformers' if _ == 0 else ""
      )

    # Plot Generators
    for _, generator in self.network.generators.iterrows():
      bus = self.network.buses.loc[generator.bus]
      ax.scatter(
        bus.x, bus.y, transform=ccrs.PlateCarree(),
        s=200, color='yellow', zorder=4, label='Generators' if _ == 0 else ""
      )
      ax.text(
        bus.x, bus.y, generator.name, transform=ccrs.PlateCarree(),
        fontsize=12, zorder=5, ha='right' if bus.x < 0 else 'left'
      )

    # Add legend
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys())

    print("Network is now plotting...\n")
    plt.show()

if __name__ == "__main__":
  data_folder = 'data'
  network_plot = Network_Plot(data_folder)
  network_plot.plot_network()