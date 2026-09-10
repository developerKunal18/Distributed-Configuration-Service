# Distributed Configuration Service

Flask configuration registry for microservices.

## Features
- Central configuration registry
- Environment-based configuration
- Versioned configuration
- Configuration retrieval and updates
- Version history
- Thread-safe storage
- Tests

## Run
```bash
python -m venv .venv
pip install -r requirements.txt
python app.py
```

Endpoints:
- GET `/api/config/<service>`
- PUT `/api/config/<service>`
- GET `/api/config/<service>/history`
- GET `/health`

Run tests:
```bash
pytest
```

> Educational in-memory implementation. Production systems should use durable storage and authentication.
