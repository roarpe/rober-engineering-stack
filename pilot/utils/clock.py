"""Clock utilities to keep time-dependent code testable."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Protocol


class Clock(Protocol):
    """Minimal clock protocol used by the pilot."""

    def monotonic(self) -> float:
        """Return a monotonic time reference in seconds."""

    def utc_ms(self) -> int:
        """Return the current UTC timestamp in milliseconds."""


class SystemClock:
    """Clock backed by the stdlib ``time`` module."""

    def monotonic(self) -> float:  # pragma: no cover - thin wrapper
        return time.monotonic()

    def utc_ms(self) -> int:  # pragma: no cover - thin wrapper
        return int(time.time() * 1000)


@dataclass
class FakeClock:
    """Deterministic clock for tests."""

    monotonic_seconds: float = 0.0
    utc_millis: int = 0

    def monotonic(self) -> float:
        return self.monotonic_seconds

    def utc_ms(self) -> int:
        return self.utc_millis

    def advance(self, seconds: float = 0.0, millis: int = 0) -> None:
        self.monotonic_seconds += seconds
        self.utc_millis += millis or int(seconds * 1000)
