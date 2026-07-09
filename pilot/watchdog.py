"""Watchdog monitor owned by the ingestion service."""

from __future__ import annotations

import math
from typing import Optional

from .models import ValidationClassification, WatchdogSnapshot


class WatchdogMonitor:
    def __init__(self, cadence_seconds: float = 2.0, tolerance_seconds: float = 0.2) -> None:
        self.cadence_seconds = cadence_seconds
        self.tolerance_seconds = tolerance_seconds
        self._cadence_ms = int(cadence_seconds * 1000)
        self._tolerance_ms = int(tolerance_seconds * 1000)
        self._last_timestamp_ms: Optional[int] = None
        self._missed_heartbeats = 0
        self._communication_recovery_frames = 0
        self._measurement_recovery_frames = 0

    def observe(
        self,
        timestamp_ms: Optional[int],
        classification: ValidationClassification,
    ) -> WatchdogSnapshot:
        if timestamp_ms is not None and self._last_timestamp_ms is not None:
            gap = timestamp_ms - self._last_timestamp_ms
            if gap > self._cadence_ms + self._tolerance_ms:
                misses = max(1, math.floor((gap - self._tolerance_ms) / self._cadence_ms))
                self._missed_heartbeats += misses
                self._communication_recovery_frames = 0
            else:
                self._missed_heartbeats = 0
                self._communication_recovery_frames += 1
        elif timestamp_ms is not None:
            self._communication_recovery_frames = 1

        if timestamp_ms is not None:
            if self._last_timestamp_ms is None or timestamp_ms >= self._last_timestamp_ms:
                self._last_timestamp_ms = timestamp_ms

        if classification in {ValidationClassification.VALID, ValidationClassification.ANOMALOUS}:
            self._measurement_recovery_frames += 1
        elif classification == ValidationClassification.NO_DATA:
            self._measurement_recovery_frames = 0
            self._missed_heartbeats = 0
            self._communication_recovery_frames += 1
        else:
            self._measurement_recovery_frames = 0

        return WatchdogSnapshot(
            missed_heartbeats=self._missed_heartbeats,
            communication_recovery_frames=self._communication_recovery_frames,
            measurement_recovery_frames=self._measurement_recovery_frames,
        )
