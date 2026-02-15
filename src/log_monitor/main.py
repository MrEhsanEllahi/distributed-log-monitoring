from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated
from uuid import uuid4

from fastapi import FastAPI, Header, HTTPException, status

from log_monitor.contracts import LogEventAccepted, LogEventIn

app = FastAPI(title="Distributed Log Monitor")


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/v1/logs",
    response_model=LogEventAccepted,
    status_code=status.HTTP_202_ACCEPTED,
)
async def ingest_log(
    payload: LogEventIn,
    tenant_id: Annotated[str, Header(alias="X-Tenant-ID", min_length=1, max_length=64)],
) -> LogEventAccepted:
    normalized_tenant_id = tenant_id.strip()
    if not normalized_tenant_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="X-Tenant-ID must not be blank",
        )

    # Milestone 2 returns an acceptance contract. Queue transport is added next.
    _ = payload

    return LogEventAccepted(
        event_id=uuid4(),
        tenant_id=normalized_tenant_id,
        received_at=datetime.now(timezone.utc),
    )
