Installation
============

To install Hybrid Renewable PyPSA, follow these steps:

1. **Clone the repository**:
  ```
  git clone https://github.com/tinegachris/hybrid_renewable_pypsa.git
  ```

2. **Navigate to the project directory**:
  ```
  cd hybrid_renewable_pypsa
  ```

3. **Create a virtual environment**:
  ```
  python -m venv venv
  ```

4. **Activate the virtual environment**:
  - On Windows:
    ```
    venv\Scripts\activate
    ```
  - On macOS/Linux:
    ```
    source venv/bin/activate
    ```

5. **Install Poetry**:
  ```
  pip install poetry
  ```

6. **Install the required dependencies using Poetry**:
  ```
  poetry install
  ```

7. **Run the tests to ensure everything is set up correctly**:
  ```
  poetry run pytest
  ```

Generating Documentation
------------------------

To generate the HTML documentation using Sphinx, follow these steps:

1. **Navigate to the `docs` directory**:
   ```
   cd docs
   ```

2. **Run Sphinx to build the HTML documentation**:
   ```
   sphinx-build -b html . _build/html
   ```

3. **Open the generated documentation**:
   Open the `_build/html/index.html` file in your web browser to view the documentation.

You are now ready to use Hybrid Renewable PyPSA and view its documentation!
