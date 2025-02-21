# Hybrid Renewable PyPSA Network Analysis

[![GitHub License](https://img.shields.io/github/license/tinegachris/hybrid_renewable_pypsa.svg)](https://github.com/tinegachris/hybrid_renewable_pypsa/blob/main/LICENSE)
[![GitHub Contributors](https://img.shields.io/github/contributors/tinegachris/hybrid_renewable_pypsa.svg)](https://github.com/tinegachris/hybrid_renewable_pypsa/graphs/contributors)
[![GitHub Issues](https://img.shields.io/github/issues/tinegachris/hybrid_renewable_pypsa.svg)](https://github.com/tinegachris/hybrid_renewable_pypsa/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/tinegachris/hybrid_renewable_pypsa.svg)](https://github.com/tinegachris/hybrid_renewable_pypsa/pulls)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![GitHub Stars](https://img.shields.io/github/stars/tinegachris/hybrid_renewable_pypsa.svg?style=social&label=Star)](https://github.com/tinegachris/hybrid_renewable_pypsa/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/tinegachris/hybrid_renewable_pypsa.svg?style=social&label=Fork)](https://github.com/tinegachris/hybrid_renewable_pypsa/network/members)
[![GitHub Watchers](https://img.shields.io/github/watchers/tinegachris/hybrid_renewable_pypsa.svg?style=social&label=Watch)](https://github.com/tinegachris/hybrid_renewable_pypsa/watchers)

![PyPSA Cover](https://github.com/user-attachments/assets/931c8053-ea86-47ee-acb4-826bf21262ae)

This project leverages **PyPSA** (Python for Power System Analysis) to model and analyze hybrid renewable energy networks. It focuses on optimizing network design for cost, reliability, and efficiency by simulating energy flows, identifying bottlenecks, and comparing various scenarios.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
- [Data](#data)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Overview

The project aims to:

- Model hybrid renewable energy systems incorporating wind, solar, and battery storage.
- Perform optimal power flow analysis to identify inefficiencies.
- Visualize network topology and energy flows.
- Compare different scenarios to enhance system performance.

---

## Features

- **Hybrid Energy Modeling**: Supports wind, solar, and battery storage integration.
- **Optimal Power Flow**: Performs cost and reliability optimization.
- **Network Visualization**: Provides detailed visualizations of network components and energy flows.
- **Scenario Comparison**: Evaluates different configurations for improved efficiency.
- **Bottleneck Identification**: Highlights inefficiencies and critical paths in the network.

---

## Project Structure

```sh
Hybrid Renewable PyPSA Network Analysis/
├── config/                      # Configuration files (anticipated)
│   └── (your config files here)
├── cwd/                         # Standalone scripts for generating profiles
│   ├── generate_generator_profiles.py
│   ├── generate_grid_import_profiles.py
│   └── generate_load_profiles.py
├── data/
│   ├── components/              # Component definitions (buses, generators, etc.)
│   │   ├── buses.csv
│   │   ├── generators.csv
│   │   ├── loads.csv
│   │   ├── storage_units.csv
│   │   ├── lines.csv
│   │   ├── transformers.csv
│   │   └── links.csv
│   ├── tech_libraries/          # Technology libraries
│   │   ├── generator_tech_library.csv
│   │   ├── storage_tech_library.csv
│   │   ├── transformer_tech_library.csv
│   │   └── line_types.csv
│   ├── constraints/             # Constraint definitions
│   │   ├── global_constraints.csv
│   │   ├── node_constraints.csv
│   │   └── branch_constraints.csv
│   ├── profiles/                # Time-series profiles
│   │   ├── load_profiles/
│   │   │   ├── residential_1.csv
│   │   │   ├── residential_2.csv
│   │   │   ├── residential_3.csv
│   │   │   ├── residential_4.csv
│   │   │   ├── commercial_1.csv
│   │   │   ├── commercial_2.csv
│   │   │   ├── commercial_3.csv
│   │   │   ├── industrial_1.csv
│   │   │   ├── industrial_2.csv
│   │   │   └── industrial_3.csv
│   │   ├── generator_profiles/
│   │   │   ├── solar-p_max_pu.csv
│   │   │   └── hydro-p_max_pu.csv
│   │   ├── grid_profiles/
│   │   │   └── grid_import_p_max_pu.csv
│   │   └── storage_profiles/    # (Optional storage profiles)
│   ├── metadata/                # Metadata for profiles and other data
│   │   ├── load_profiles_metadata.csv
│   │   ├── generator_profiles_metadata.csv
│   │   └── grid_profiles_metadata.csv
│   └── documentation/           # Project documentation and supplementary info
│       ├── README.md            # Additional docs if needed
│       └── LICENSE
├── results/                     # Output files (plots, analysis results, etc.)
│   ├── network_plot.png
│   └── network_interactive.html
├── src/                         # Python source code for the project
│   ├── data_loader.py
│   ├── logger_setup.py
│   ├── network_setup.py
│   ├── network_plot.py
│   └── network_analysis.py
├── pyproject.toml               # Poetry configuration and dependencies
├── README.md                    # Project overview
└── LICENSE                      # Project license

tests/                          # Tests for the code in the src folder
│   └── (your test scripts here)
docs/                           # Sphinx-generated documentation
│   └── (documentation build output)
.github/                        # GitHub workflows and CI/CD configurations
│   └── workflows/
│       └── ci.yml
```

---

## Getting Started

### Prerequisites

- **Python 3.10.4 or higher**
- **Poetry 2.0.1 or higher** (for dependency management)

### Installation

1. **Clone the Repository**:

  ```sh
  git clone https://github.com/tinegachris/hybrid_renewable_pypsa.git
  cd hybrid_renewable_pypsa
  ```

2. **Install Poetry (if not already installed)**:

  ```sh
  curl -sSL https://install.python-poetry.org | python3 -
  ```

3. **Install Dependencies**:

  ```sh
  poetry install
  ```

### Usage

1. **Run Network Setup**:

  ```sh
  poetry run python -m hybrid_renewable_pypsa.src.network_setup
  ```

2. **Run Network Analysis**:

  ```sh
  poetry run python -m hybrid_renewable_pypsa.src.network_analysis
  ```

3. **Plot Network**:

  ```sh
  poetry run python -m hybrid_renewable_pypsa.src.network_plot
  ```

---

## Data

Input data for the network analysis is stored in the `data/` directory. This includes:

- **CSV files**: Hourly wind, solar, and load profiles.
- **Configuration files**: Network parameters and settings.

---

## Results

Outputs are saved in the `results/` directory, including:

- **Network diagrams**: Visual representations of the network.
- **Optimized power flow solutions**: Results from the optimization process.
- **Key performance indicators**: Metrics for evaluating network performance.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Open an issue to discuss proposed changes.
2. Fork the repository and create a new branch.
3. Submit a pull request with your changes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/tinegachris/hybrid_renewable_pypsa/blob/main/LICENSE) file for details.

---

## Acknowledgements

- **PyPSA Documentation**
- The open-source community for their invaluable tools and resources.
