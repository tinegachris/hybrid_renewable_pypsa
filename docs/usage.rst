Usage
=====

This section provides examples and guidelines on how to use Hybrid Renewable PyPSA.

Setting Up a Network
--------------------

To set up a network, create an instance of the `Network_Setup` class and call the
`setup_network` method:

```python
from hybrid_renewable_pypsa.src.network_setup import Network_Setup

data_folder = 'hybrid_renewable_pypsa/data'
network_setup = Network_Setup(data_folder)
network_setup.setup_network()
network = network_setup.get_network()
```

Plotting the Network
--------------------

To plot the network, create an instance of the `Network_Plot` class and call the
`plot_network` method:

```python
from hybrid_renewable_pypsa.src.network_plot import Network_Plot

data_folder = 'hybrid_renewable_pypsa/data'
network_plotter = Network_Plot(data_folder)
network_plotter.plot_network()
```

Analyzing the Network
---------------------

To analyze the network, create an instance of the `Network_Analysis` class and call the
`analyze_network` method:

```python
from hybrid_renewable_pypsa.src.network_analysis import Network_Analysis

data_folder = 'hybrid_renewable_pypsa/data'
network_analysis = Network_Analysis(data_folder)
network_analysis.analyze_network()
