
Welcome to Hybrid Renewable PyPSA's documentation!
==================================================

This documentation provides comprehensive information on the Hybrid Renewable PyPSA
project, including installation instructions, usage guidelines, API references, and
more.  It's designed to help you understand, use, and contribute to the project.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   introduction
   installation
   usage
   api
   cli
   contributing
   changelog
   faq

Project Structure
=================

The project's directory structure is designed for clarity and maintainability:

- ``src/``: Contains the core source code for network setup, plotting, and analysis.
- ``data/``: Stores input data used for network analysis.  This is kept separate to
  improve reproducibility and allow for easy modification of inputs.
- ``docs/``:  Houses the documentation files (including this one!).
- ``results/``:  A directory to store the output results from the analysis.
- ``.github/workflows/``: Configuration files for Continuous Integration/Continuous
  Deployment (CI/CD).
- ``tests/``: Contains unit and integration tests to ensure code quality and
  stability.

Contributing
============

We welcome contributions to Hybrid Renewable PyPSA! To contribute, follow these steps:

1. **Fork the repository** on GitHub.

2. **Clone your fork** to your local machine:
   ```
   git clone https://github.com/tinegachris/hybrid_renewable_pypsa.git
   ```

3. **Create a new branch** for your feature or bugfix:
   ```
   git checkout -b my-feature-branch
   ```

4. **Make your changes** and commit them with a clear message:
   ```
   git commit -m "Add new feature"
   ```

5. **Push your changes** to your fork:
   ```
   git push origin my-feature-branch
   ```

6. **Create a pull request** on GitHub.

Please ensure your code follows the project's coding standards and includes appropriate
tests.

Coding Standards
----------------

- Follow PEP 8 for Python code.
- Write clear and concise commit messages.
- Include docstrings for all functions and classes.
- Write unit tests for new features and bug fixes.

Thank you for contributing!

Indices and tables
==================

* :ref:`genindex`: General Index
* :ref:`modindex`: Module Index
* :ref:`search`: Search Page