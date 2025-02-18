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

```
Hybrid Renewable PyPSA Network Analysis/
├── .github/                # CI/CD workflows
├── data/                   # Input data (e.g., wind, solar, load profiles)
├── docs/                   # Project documentation
├── hybrid_renewable_pypsa/
│   ├── src/                # Source code for network setup, analysis, and visualization
│   └── utils/              # Utility functions and logging
├── results/                # Output results (e.g., plots, optimization results)
├── tests/                  # Unit tests
├── .gitignore              # Files to ignore in version control
├── Dockerfile              # Containerization setup
├── poetry.lock             # Dependency lock file
├── pyproject.toml          # Project dependencies and metadata
└── README.md               # Project overview
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