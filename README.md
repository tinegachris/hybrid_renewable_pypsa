# Hybrid Renewable PyPSA Network Analysis

[![Github license](https://img.shields.io/github/license/tinegachris/hybrid_renewable_pypsa.svg)](https://github.com/tinegachris/hybrid_renewable_pypsa/blob/main/LICENSE)
[![GitHub contributors](https://img.shields.io/github/contributors/tinegachris/hybrid_renewable_pypsa.svg)](https://github.com/tinegachris/hybrid_renewable_pypsa/graphs/contributors)
[![GitHub issues](https://img.shields.io/github/issues/tinegachris/hybrid_renewable_pypsa.svg)](https://github.com/tinegachris/hybrid_renewable_pypsa/issues)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/tinegachris/hybrid_renewable_pypsa.svg)](https://github.com/tinegachris/hybrid_renewable_pypsa/pulls)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![GitHub watchers](https://img.shields.io/github/watchers/tinegachris/hybrid_renewable_pypsa.svg?style=social&label=Watch)](https://github.com/tinegachris/hybrid_renewable_pypsa/watchers)
[![GitHub forks](https://img.shields.io/github/forks/tinegachris/hybrid_renewable_pypsa.svg?style=social&label=Fork)](https://github.com/tinegachris/hybrid_renewable_pypsa/network/members)
[![GitHub stars](https://img.shields.io/github/stars/tinegachris/hybrid_renewable_pypsa.svg?style=social&label=Star)](https://github.com/tinegachris/hybrid_renewable_pypsa/stargazers)

![pypsa_cover](https://github.com/user-attachments/assets/931c8053-ea86-47ee-acb4-826bf21262ae)

This project involves the analysis of a hybrid renewable energy network using PyPSA (Python for Power System Analysis).

## Overview

This project uses PyPSA, a Python library for simulating and optimizing power systems, to analyze a hybrid renewable energy network incorporating various static network components. The goal is to optimize network design for cost and reliability. This analysis will model energy flows, identify bottlenecks, and compare different scenarios to enhance the overall efficiency and performance of the network.

## Features

- Models wind, solar, and battery storage
- Performs optimal power flow analysis
- Supports different network topologies
- Provides detailed network visualization
- Identifies network bottlenecks and inefficiencies
- Compares different energy scenarios for optimization

## Project Structure

The project is organized as follows:

- `src/`: Contains the main source code for network setup, plotting, and analysis.
- `data/`: Contains input data for the network analysis.
- `docs/`: Documentation files for the project.
- `results/`: Output results from the analysis.
- `.github/workflows/`: CI/CD workflow configuration.

## Getting Started

To get started with this project, follow these steps:

### Prerequisites

- Python 3.10.4 or higher
- Poetry 2.0.1 or higher

### Installation

**Clone the repository:**

```sh
git clone https://github.com/tinegachris/hybrid_renewable_pypsa.git
cd hybrid_renewable_pypsa
```

**Install Poetry:**

If you don't have Poetry installed, you can install it using the following command:

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

**Install the required dependencies:**

```sh
poetry install
```

### Usage

**Run the network setup:**

```sh
poetry run python -m src.network_setup
```

**Run the network analysis:**

```sh
poetry run python -m src.network_analysis
```

**Plot the network:**

```sh
poetry run python -m src.network_plot
```

## Data

Input data for the network analysis is located in the `data/` directory. This includes CSV files containing hourly wind and solar generation data.

## Results

Output results from the analysis are stored in the `results/` directory. This includes network diagrams, optimized power flow solutions, and key performance indicators.

## Contributing

Contributions are welcome! Please open an issue to discuss proposed changes or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [PyPSA Documentation](https://pypsa.readthedocs.io/en/latest/)
