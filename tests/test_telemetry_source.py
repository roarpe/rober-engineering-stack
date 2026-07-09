"""Test 1: Validates that the telemetry source produces ICD-conformant frames."""

from __future__ import annotations

import unittest

from pilot.models import QualityCode, Status
from pilot.telemetry_source import TelemetrySource
from pilot.utils.clock import FakeClock


class TestTelemetrySource(unittest.TestCase):
    """Verifies generator respects ICD contract: types, ranges, required fields."""

    def setUp(self) -> None:
        self.clock = FakeClock(monotonic_seconds=0.0, utc_millis=1_000_000)
        self.source = TelemetrySource(clock=self.clock, cadence_seconds=2.0)

    def test_frames_have_all_required_fields(self) -> None:
        frame = self.source.next_frame()
        for field in ("frame_id", "timestamp_utc", "temperature_c",
                      "vibration_mm_s", "cycle_count", "status", "quality_code"):
            self.assertIn(field, frame, f"Missing required field: {field}")

    def test_frame_id_is_string(self) -> None:
        frame = self.source.next_frame()
        self.assertIsInstance(frame["frame_id"], str)

    def test_timestamp_is_integer(self) -> None:
        frame = self.source.next_frame()
        self.assertIsInstance(frame["timestamp_utc"], int)

    def test_temperature_is_float_in_range(self) -> None:
        for _ in range(10):
            frame = self.source.next_frame()
            self.assertIsInstance(frame["temperature_c"], float)
            self.assertGreaterEqual(frame["temperature_c"], 0.0)
            self.assertLessEqual(frame["temperature_c"], 120.0)

    def test_vibration_is_float_in_range(self) -> None:
        for _ in range(10):
            frame = self.source.next_frame()
            self.assertIsInstance(frame["vibration_mm_s"], float)
            self.assertGreaterEqual(frame["vibration_mm_s"], 0.0)
            self.assertLessEqual(frame["vibration_mm_s"], 50.0)

    def test_cycle_count_increments(self) -> None:
        counts = [self.source.next_frame()["cycle_count"] for _ in range(5)]
        self.assertEqual(counts, [1, 2, 3, 4, 5])

    def test_status_is_running(self) -> None:
        frame = self.source.next_frame()
        self.assertEqual(frame["status"], Status.RUNNING.value)

    def test_quality_code_is_good(self) -> None:
        frame = self.source.next_frame()
        self.assertEqual(frame["quality_code"], QualityCode.GOOD.value)

    def test_timestamps_increment_by_cadence(self) -> None:
        ts = [self.source.next_frame()["timestamp_utc"] for _ in range(5)]
        for i in range(1, len(ts)):
            self.assertEqual(ts[i] - ts[i - 1], 2000)

    def test_no_data_frame_has_null_measurements(self) -> None:
        frame = TelemetrySource.build_no_data_frame(timestamp_utc=1_000_000)
        self.assertIsNone(frame["temperature_c"])
        self.assertIsNone(frame["vibration_mm_s"])
        self.assertIsNone(frame["cycle_count"])
        self.assertEqual(frame["quality_code"], QualityCode.NO_DATA.value)


if __name__ == "__main__":
    unittest.main()
