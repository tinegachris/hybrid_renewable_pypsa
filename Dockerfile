FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY hybrid_renewable_pypsa/ ./hybrid_renewable_pypsa
RUN pip install poetry && poetry install

# CMD ["poetry", "run", "python", "-m", "hybrid_renewable_pypsa.network_setup"]
