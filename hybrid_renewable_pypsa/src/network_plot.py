import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from typing import Optional, Dict, Any
from matplotlib.axes import Axes
from hybrid_renewable_pypsa.src.data_loader import DataLoader
from hybrid_renewable_pypsa.src.network_setup import NetworkSetup
from hybrid_renewable_pypsa.src.logger_setup import LoggerSetup

class NetworkPlotError(Exception):
    """Custom exception for network plotting errors."""
    pass

class NetworkPlot:
    def __init__(self, data_folder: str) -> None:
        self.data_loader = DataLoader(data_folder)
        self.network_setup = NetworkSetup(data_folder)
        self.network_setup.setup_network()
        self.network = self.network_setup.get_network()
        self.logger = LoggerSetup.setup_logger('NetworkPlot')
        self.plot_config = self._load_plot_config()

    def _load_plot_config(self) -> Dict[str, Any]:
        """Load plot configuration (e.g., colors, markers) from a file or use defaults."""
        return {
            "buses": {"color": "red", "marker": "o", "size": 200, "label": "Buses"},
            "lines": {"color": "black", "linestyle": "-", "linewidth": 1.5, "label": "Lines"},
            "generators": {"color": "yellow", "marker": "o", "size": 10, "label": "Generators"},
            "loads": {"color": "black", "marker": "o", "size": 10, "label": "Loads"},
            "transformers": {"color": "purple", "linestyle": "-", "linewidth": 1.5, "label": "Transformers"},
            "storage_units": {"color": "green", "marker": "o", "size": 10, "label": "Storage Units"},
            "links": {"color": "brown", "linestyle": "-", "linewidth": 1.5, "label": "Links"},
        }

    def _plot_connections(self, ax: Axes, component_type: str, **kwargs) -> None:
        """Helper method to plot connections (e.g., lines, links, transformers)."""
        if component_type not in self.network:
            self.logger.warning(f"Component type '{component_type}' not found in the network.")
            return
        for _, connection in self.network[component_type].iterrows():
            if connection.bus0 not in self.network.buses.index or connection.bus1 not in self.network.buses.index:
                self.logger.warning(f"Bus '{connection.bus0}' or '{connection.bus1}' not found in the network.")
                continue
            bus0 = self.network.buses.loc[connection.bus0]
            bus1 = self.network.buses.loc[connection.bus1]
            ax.plot(
                [bus0.x, bus1.x], [bus0.y, bus1.y], transform=ccrs.PlateCarree(),
                **kwargs
            )
            ax.text(
                0.5 * (bus0.x + bus1.x), 0.5 * (bus0.y + bus1.y), connection.name,
                transform=ccrs.PlateCarree(), fontsize=8, zorder=5, ha='center'
            )

    def plot_buses(self, ax: Axes) -> None:
        """Plot buses on the map."""
        config = self.plot_config["buses"]
        ax.scatter(
            self.network.buses.x, self.network.buses.y, transform=ccrs.PlateCarree(),
            s=config["size"], color=config["color"], zorder=5, label=config["label"]
        )
        for bus_name, bus in self.network.buses.iterrows():
            ax.text(
                bus.x, bus.y, bus_name, transform=ccrs.PlateCarree(),
                fontsize=8, zorder=5, ha='right'
            )

    def plot_lines(self, ax: Axes) -> None:
        """Plot transmission lines on the map."""
        self._plot_connections(ax, "lines", **self.plot_config["lines"])

    def plot_generators(self, ax: Axes) -> None:
        """Plot generators on the map."""
        config = self.plot_config["generators"]
        for _, gen in self.network.generators.iterrows():
            bus = self.network.buses.loc[gen.bus]
            ax.plot(
                bus.x, bus.y, marker=config["marker"], markersize=config["size"], color=config["color"],
                transform=ccrs.PlateCarree(), zorder=5, label=config["label"]
            )
            ax.text(
                bus.x, bus.y, gen.name, transform=ccrs.PlateCarree(),
                fontsize=8, zorder=5, ha='left'
            )

    def plot_loads(self, ax: Axes) -> None:
        """Plot loads on the map."""
        config = self.plot_config["loads"]
        for _, load in self.network.loads.iterrows():
            bus = self.network.buses.loc[load.bus]
            ax.plot(
                bus.x, bus.y, marker=config["marker"], markersize=config["size"], color=config["color"],
                transform=ccrs.PlateCarree(), zorder=5, label=config["label"]
            )
            ax.text(
                bus.x, bus.y, load.name, transform=ccrs.PlateCarree(),
                fontsize=8, zorder=5, ha='left'
            )

    def plot_transformers(self, ax: Axes) -> None:
        """Plot transformers on the map."""
        self._plot_connections(ax, "transformers", **self.plot_config["transformers"])

    def plot_storage_units(self, ax: Axes) -> None:
        """Plot storage units on the map."""
        config = self.plot_config["storage_units"]
        for _, storage_unit in self.network.storage_units.iterrows():
            bus = self.network.buses.loc[storage_unit.bus]
            ax.plot(
                bus.x, bus.y, marker=config["marker"], markersize=config["size"], color=config["color"],
                transform=ccrs.PlateCarree(), zorder=5, label=config["label"]
            )
            ax.text(
                bus.x, bus.y, storage_unit.name, transform=ccrs.PlateCarree(),
                fontsize=8, zorder=5, ha='right'
            )

    def plot_links(self, ax: Axes) -> None:
        """Plot links on the map."""
        self._plot_connections(ax, "links", **self.plot_config["links"])

    def add_map_features(self, ax: Axes) -> None:
        """Add geographical features to the map."""
        ax.add_feature(cfeature.LAND)
        ax.add_feature(cfeature.OCEAN)
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS, linestyle=':')
        ax.add_feature(cfeature.LAKES, alpha=0.5)
        ax.add_feature(cfeature.RIVERS)

    def set_plot_extent(self, ax: Axes, padding: float = 6.0) -> None:
        """Set the plot extent based on bus coordinates."""
        min_x, max_x = self.network.buses.x.min(), self.network.buses.x.max()
        min_y, max_y = self.network.buses.y.min(), self.network.buses.y.max()
        ax.set_extent([min_x - padding, max_x + padding, min_y - padding, max_y + padding])

    def create_legend(self, ax: Axes) -> None:
        """Create a legend for the plot."""
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), title="Network Components", loc="upper right")

    def plot_network(self, save_path: Optional[str] = None, show_map: bool = True) -> None:
        """Plot the network and optionally save the figure."""
        fig = plt.figure(figsize=(12, 12))
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

        if show_map:
            self.add_map_features(ax)

        self.set_plot_extent(ax)
        self.plot_buses(ax)
        self.plot_lines(ax)
        self.plot_generators(ax)
        self.plot_storage_units(ax)
        self.plot_links(ax)
        self.plot_transformers(ax)
        self.plot_loads(ax)
        self.create_legend(ax)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            self.logger.info(f"Plot saved to {save_path}.")
        plt.show()

    def main(self) -> None:
        """Main method to plot the network."""
        self.logger.info(f'Plotting {len(self.network.buses)} buses and {len(self.network.lines)} lines...')
        self.plot_network(save_path="hybrid_renewable_pypsa/results/network_plot.png", show_map=True)

if __name__ == '__main__':
    data_folder = 'hybrid_renewable_pypsa/data'
    network_plotter = NetworkPlot(data_folder)
    network_plotter.main()