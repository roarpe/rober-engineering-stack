"""Minimal CLI entry point for the telemetry ingestion pilot."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Iterable, Optional

from .exceptions import (
    PipelineInternalError,
    PersistenceFatalError,
    PersistenceRetryableError,
    UsageError,
)
from .ingestion import build_ingestion_service
from .models import ValidationClassification
from .telemetry_source import TelemetrySource
from .utils.clock import SystemClock

LOGGER = logging.getLogger(__name__)

DEFAULT_FRAMES = 100
DEFAULT_DB_PATH = "./var/pilot.sqlite"


def configure_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s level=%(levelname)s logger=%(name)s event=%(message)s",
    )


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Industrial Machine Telemetry Ingestion & Diagnostics Pipeline (pilot)",
    )
    parser.add_argument("--frames", type=int, default=DEFAULT_FRAMES, help="Number of frames to simulate per run (>=1)")
    parser.add_argument(
        "--db-path",
        type=Path,
        default=None,
        help="SQLite file location (default: ./var/pilot.sqlite or PILOT_DB_PATH env var)",
    )
    parser.add_argument("--reset-db", action="store_true", help="Drop and recreate schema before processing")
    parser.add_argument("--log-level", default="INFO", help="Logging verbosity (DEBUG, INFO, WARNING, ERROR)")
    args = parser.parse_args(list(argv))

    if args.frames < 1:
        raise UsageError("--frames must be >= 1")

    if args.db_path is None:
        env_path = os.environ.get("PILOT_DB_PATH")
        args.db_path = Path(env_path) if env_path else Path(DEFAULT_DB_PATH)

    return args


def main(argv: Optional[Iterable[str]] = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]

    try:
        args = parse_args(argv)
    except UsageError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    configure_logging(args.log_level)
    LOGGER.info("event=cli_start frames=%d db_path=%s reset_db=%s", args.frames, args.db_path, args.reset_db)

    db_path = args.db_path
    db_path.parent.mkdir(parents=True, exist_ok=True)

    if args.reset_db and db_path.exists():
        db_path.unlink()

    clock = SystemClock()
    exit_code = 0
    ingestion = None

    try:
        ingestion = build_ingestion_service(str(db_path), clock)
        if args.reset_db:
            ingestion.persistence.reset_schema()
        ingestion.start()

        source = TelemetrySource(clock=clock)
        for _ in range(args.frames):
            payload = source.next_frame()
            ingestion.process_frame(payload)

        if ingestion.counters.frames_processed > 0 and ingestion.counters.frames_persisted == 0:
            LOGGER.error(
                "event=run_level_validation_failure frames_processed=%d frames_persisted=0",
                ingestion.counters.frames_processed,
            )
            exit_code = 3

        summary = ingestion.build_summary(exit_code)
        ingestion.finalize(exit_code)

        LOGGER.info("event=cli_end exit_code=%d", exit_code)
        print(json.dumps(asdict(summary), indent=2, sort_keys=True, default=str))
        return exit_code

    except PersistenceFatalError as exc:
        LOGGER.error("event=persistence_fatal error=%s", exc)
        LOGGER.error("event=cli_run_not_recorded reason=fatal_persistence_error")
        return 4
    except PersistenceRetryableError as exc:
        LOGGER.error("event=persistence_retryable_exhausted error=%s", exc)
        LOGGER.error("event=cli_run_not_recorded reason=persistence_retry_exhausted")
        return 4
    except PipelineInternalError as exc:
        LOGGER.exception("event=unexpected_error error=%s", exc)
        return 5
    except Exception as exc:
        LOGGER.exception("event=unexpected_error error=%s", exc)
        return 5
    finally:
        if ingestion is not None:
            try:
                ingestion.close()
            except Exception:
                pass


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
