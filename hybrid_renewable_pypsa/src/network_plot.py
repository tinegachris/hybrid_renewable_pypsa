import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from hybrid_renewable_pypsa.src.data_loader import Data_Loader
from hybrid_renewable_pypsa.src.network_setup import Network_Setup
from hybrid_renewable_pypsa.src.logger_setup import Logger_Setup
from matplotlib.axes import Axes

class Network_Plot:
  def __init__(self, data_folder: str) -> None:
    self.data_loader = Data_Loader(data_folder)
    self.network_setup = Network_Setup(data_folder)
    self.network_setup.setup_network()
    self.network = self.network_setup.get_network()
    self.logger = Logger_Setup.setup_logger('NetworkPlot')

  def plot_buses(self, ax: Axes) -> None:
    ax.scatter(
      self.network.buses.x, self.network.buses.y, transform=ccrs.PlateCarree(),
      s=200, color='red', zorder=5, label='Buses'
    )
    for bus_name, bus in self.network.buses.iterrows():
      ax.text(
        bus.x, bus.y, bus_name, transform=ccrs.PlateCarree(),
        fontsize=8, zorder=5, ha='right'
      )

  def plot_lines(self, ax: Axes) -> None:
    for _, line in self.network.lines.iterrows():
      bus0 = self.network.buses.loc[line.bus0]
      bus1 = self.network.buses.loc[line.bus1]
      line_color = 'black' if line.s_nom > 100 else 'gray'
      line_style = '--' if line.type == 'MV_line' else '-'
      ax.plot(
        [bus0.x, bus1.x], [bus0.y, bus1.y], transform=ccrs.PlateCarree(),
        color=line_color, linestyle=line_style, linewidth=1.5, zorder=1
      )
      ax.text(
        0.5 * (bus0.x + bus1.x), 0.5 * (bus0.y + bus1.y), line.name,
        transform=ccrs.PlateCarree(), fontsize=8, zorder=5, ha='center'
      )

  def plot_generators(self, ax: Axes) -> None:
    for _, gen in self.network.generators.iterrows():
      bus = self.network.buses.loc[gen.bus]
      ax.plot(
        bus.x, bus.y, marker='o', markersize=10, color='yellow',
        transform=ccrs.PlateCarree(), zorder=5, label='Generators'
      )
      ax.text(
        bus.x, bus.y, gen.name, transform=ccrs.PlateCarree(),
        fontsize=8, zorder=5, ha='left'
      )

  def plot_loads(self, ax: Axes) -> None:
    for _, load in self.network.loads.iterrows():
      bus = self.network.buses.loc[load.bus]
      ax.plot(
        bus.x, bus.y, marker='o', markersize=10, color='black',
        transform=ccrs.PlateCarree(), zorder=5, label='Loads'
      )
      ax.text(
        bus.x, bus.y, load.name, transform=ccrs.PlateCarree(),
        fontsize=8, zorder=5, ha='left'
      )

  def plot_transformers(self, ax: Axes) -> None:
    for _, transformer in self.network.transformers.iterrows():
      bus0 = self.network.buses.loc[transformer.bus0]
      bus1 = self.network.buses.loc[transformer.bus1]
      ax.plot(
        [bus0.x, bus1.x], [bus0.y, bus1.y], transform=ccrs.PlateCarree(),
        color='purple', linestyle='-', linewidth=1.5, zorder=1
      )
      ax.text(
        0.5 * (bus0.x + bus1.x), 0.5 * (bus0.y + bus1.y), transformer.name,
        transform=ccrs.PlateCarree(), fontsize=8, zorder=5, ha='center'
      )

  def plot_storage_units(self, ax: Axes) -> None:
    for _, storage_unit in self.network.storage_units.iterrows():
      bus = self.network.buses.loc[storage_unit.bus]
      ax.plot(
        bus.x, bus.y, marker='o', markersize=10, color='green',
        transform=ccrs.PlateCarree(), zorder=5, label='Storage Units'
      )
      ax.text(
        bus.x, bus.y, storage_unit.name, transform=ccrs.PlateCarree(),
        fontsize=8, zorder=5, ha='right'
      )

  def plot_links(self, ax: Axes) -> None:
    for _, link in self.network.links.iterrows():
      bus0 = self.network.buses.loc[link.bus0]
      bus1 = self.network.buses.loc[link.bus1]
      ax.plot(
        [bus0.x, bus1.x], [bus0.y, bus1.y], transform=ccrs.PlateCarree(),
        color='brown', linestyle='-', linewidth=1.5, zorder=1
      )
      ax.text(
        0.5 * (bus0.x + bus1.x), 0.5 * (bus0.y + bus1.y), link.name,
        transform=ccrs.PlateCarree(), fontsize=8, zorder=5, ha='center'
      )

  def add_map_features(self, ax: Axes) -> None:
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)

  def set_plot_extent(self, ax: Axes) -> None:
    ax.set_extent([
      self.network.buses.x.min() - 6, self.network.buses.x.max() + 6,
      self.network.buses.y.min() - 6, self.network.buses.y.max() + 6
    ])

  def create_legend(self, ax: Axes) -> None:
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys())

  def plot_network(self) -> None:
    """
    Plot the network
    """
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    #self.add_map_features(ax)

    self.set_plot_extent(ax)
    self.plot_buses(ax)
    self.plot_lines(ax)
    self.plot_generators(ax)
    self.plot_storage_units(ax)
    self.plot_links(ax)
    self.plot_transformers(ax)
    self.plot_loads(ax)
    self.create_legend(ax)
    plt.show()

  def main(self) -> None:
    self.logger.info(f'Plotting {len(self.network.buses)} buses and {len(self.network.lines)} lines...')
    self.plot_network()

if __name__ == '__main__':
    data_folder = 'hybrid_renewable_pypsa/data'
    network_plotter = Network_Plot(data_folder)
    network_plotter.main()