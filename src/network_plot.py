import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from data_loader import Data_Loader
from network_setup import Network_Setup
from logger_setup import LoggerSetup

class Network_Plot:
  def __init__(self, data_folder):
      self.data_loader = Data_Loader(data_folder)
      self.network_setup = Network_Setup(data_folder)
      self.network_setup.setup_network()
      self.network = self.network_setup.get_network()
      self.logger = LoggerSetup.setup_logger('NetworkPlot')

  def plot_buses(self, ax):
    ax.scatter(
      self.network.buses.x, self.network.buses.y, transform=ccrs.PlateCarree(),
      s=200, color='red', zorder=5, label='Buses'
    )
    for bus_name, bus in self.network.buses.iterrows():
      ax.text(
        bus.x, bus.y, bus_name, transform=ccrs.PlateCarree(),
        fontsize=8, zorder=5, ha='right'
      )

  def plot_lines(self, ax):
      for _, line in self.network.lines.iterrows():
          bus0 = self.network.buses.loc[line.bus0]
          bus1 = self.network.buses.loc[line.bus1]
          line_color = 'black' if line.s_nom > 100 else 'gray'
          line_style = '--' if line.type == 'MV_line' else '-'
          ax.plot(
              [bus0.x, bus1.x], [bus0.y, bus1.y], transform=ccrs.PlateCarree(),
              color=line_color, linestyle=line_style, linewidth=1.5, zorder=1
          )
          # ax.text(
          #     0.5 * (bus0.x + bus1.x), 0.5 * (bus0.y + bus1.y), line.name,
          #     transform=ccrs.PlateCarree(), fontsize=8, zorder=5, ha='center'
          # )

  def add_map_features(self, ax):
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)

  def plot_network(self):
    """
    Plot the network
    """
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    self.add_map_features(ax)

    ax.set_extent([
      self.network.buses.x.min() - 6, self.network.buses.x.max() + 6,
      self.network.buses.y.min() - 6, self.network.buses.y.max() + 6
    ])

    self.plot_buses(ax)
    self.plot_lines(ax)

    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys())
    plt.show()



  def main(self):
    self.logger.info(f'Plotting {len(self.network.buses)} buses and {len(self.network.lines)} lines...')
    self.plot_network()

if __name__ == '__main__':
    data_folder = 'data'
    network_plotter = Network_Plot(data_folder)
    network_plotter.main()