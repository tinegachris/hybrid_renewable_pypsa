FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY hybrid_renewable_pypsa/ ./hybrid_renewable_pypsa
RUN apt-get update && apt-get install -y build-essential gcc && \
    pip install poetry==2.0.1 && poetry install

CMD ["poetry", "run", "python", "-m", "hybrid_renewable_pypsa.src.network_setup"]
