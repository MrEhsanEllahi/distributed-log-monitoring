from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogEventIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    timestamp: datetime
    level: LogLevel
    message: str = Field(min_length=1, max_length=8192)
    service: str = Field(min_length=1, max_length=128)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("message", "service")
    @classmethod
    def validate_non_blank(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("must not be blank")
        return trimmed


class LogEventAccepted(BaseModel):
    status: Literal["accepted"] = "accepted"
    event_id: UUID
    tenant_id: str
    received_at: datetime
