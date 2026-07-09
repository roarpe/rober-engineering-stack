"""Custom exceptions for the telemetry ingestion pilot."""

from __future__ import annotations


class UsageError(Exception):
    """Raised when CLI arguments are invalid."""


class ValidationError(Exception):
    """Non-fatal validation error raised during frame processing."""


class PersistenceRetryableError(Exception):
    """Raised when a retryable SQLite error occurs."""


class PersistenceFatalError(Exception):
    """Raised when a non-recoverable SQLite error occurs."""


class PipelineInternalError(Exception):
    """Raised for unexpected internal errors."""
