Command-Line Interface
======================

Hybrid Renewable PyPSA provides a command-line interface (CLI) for easy interaction with
the tool.

Usage
-----

To use the CLI, navigate to the project directory and run the following command:

```
python -m hybrid_renewable_pypsa.cli <command> [options]
```

Available Commands
------------------

- `setup-network`: Set up the network using the provided data files.
- `plot-network`: Plot the network components and their connections.
- `analyze-network`: Perform various analyses on the network.

Examples
--------

Set up the network:

```
python -m hybrid_renewable_pypsa.cli setup-network --data-folder hybrid_renewable_pypsa/data
```

Plot the network:

```
python -m hybrid_renewable_pypsa.cli plot-network --data-folder hybrid_renewable_pypsa/data
```

Analyze the network:

```
python -m hybrid_renewable_pypsa.cli analyze-network --data-folder hybrid_renewable_pypsa/data
```
