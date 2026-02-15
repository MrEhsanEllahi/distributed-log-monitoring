# Distributed Log Monitoring System

Production-oriented, multi-tenant log monitoring platform built with Python for real-world B2B observability use cases.

## Vision

This project targets the core capabilities required to run a SaaS log monitoring product:
- High-throughput log ingestion
- Reliable event processing
- Fast search and analytics
- Real-time alerting
- Tenant isolation and role-based access control

## Current Capabilities

- FastAPI service bootstrap
- Health endpoint (`GET /health`)
- Ingestion endpoint (`POST /v1/logs`)
- Required tenant boundary (`X-Tenant-ID`)
- Strict log event contract validation
- Test baseline with `pytest`

## Planned Architecture

1. Ingestion API (FastAPI)
2. Stream transport and buffering (Kafka/Redpanda)
3. Processing workers (parsing, enrichment, redaction, validation)
4. Storage layer (search + analytics + archive)
5. Alerting engine and notification integrations
6. Multi-tenant auth, RBAC, and operational controls

## Local Development

### Prerequisites

- Python 3.11+

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Run API

```bash
uvicorn log_monitor.main:app --reload --app-dir src
```

API health check:
- http://127.0.0.1:8000/health

## Repository Goals

- Clean architecture with explicit boundaries
- Automated tests for each feature
- Production-ready operational patterns (observability, reliability, security)
- Incremental, verifiable delivery of system components
