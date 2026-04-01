#!/usr/bin/env python3
"""CLI helper to report the remaining time until the next BreakTimer break."""
from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from pathlib import Path

DEFAULT_LOG_PATH = Path.home() / "Library" / "Logs" / "BreakTimer" / "main.log"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Show the countdown until the next scheduled BreakTimer break "
            "by reading BreakTimer's log file."
        )
    )
    parser.add_argument(
        "--log-path",
        type=Path,
        default=DEFAULT_LOG_PATH,
        help=f"Path to BreakTimer's log file (default: {DEFAULT_LOG_PATH})",
    )
    return parser.parse_args()


def parse_timestamp(raw: str) -> datetime:
    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unrecognised timestamp format: {raw}")


def extract_schedule(line: str) -> tuple[datetime, datetime]:
    if "Scheduling next break" not in line or "[scheduledFor=" not in line:
        raise ValueError("Line does not contain schedule data")

    closing_bracket = line.find("]")
    if closing_bracket == -1:
        raise ValueError("Malformed log line; missing timestamp segment")
    timestamp = line[1:closing_bracket]
    logged_dt = parse_timestamp(timestamp)

    scheduled_marker = "[scheduledFor="
    scheduled_start = line.rfind(scheduled_marker)
    if scheduled_start == -1:
        raise ValueError("Malformed log line; missing scheduled time")
    scheduled_start += len(scheduled_marker)
    scheduled_end = line.find("]", scheduled_start)
    if scheduled_end == -1:
        raise ValueError("Malformed log line; missing scheduled time terminator")
    scheduled_raw = line[scheduled_start:scheduled_end]

    scheduled_time = datetime.strptime(scheduled_raw, "%H:%M:%S").time()
    scheduled_dt = logged_dt.replace(
        hour=scheduled_time.hour,
        minute=scheduled_time.minute,
        second=scheduled_time.second,
        microsecond=0,
    )
    if scheduled_dt < logged_dt:
        scheduled_dt += timedelta(days=1)

    return logged_dt, scheduled_dt


def find_next_break(log_path: Path) -> tuple[datetime, datetime]:
    lines = log_path.read_text(encoding="utf-8").splitlines()
    for line in reversed(lines):
        try:
            logged_dt, scheduled_dt = extract_schedule(line)
        except ValueError:
            continue
        return logged_dt, scheduled_dt
    raise RuntimeError("Could not find a scheduled break entry in the log")


def format_remaining(scheduled_dt: datetime, reference: datetime | None = None) -> str:
    now = reference or datetime.now()
    delta_seconds = int((scheduled_dt - now).total_seconds())
    minutes, seconds = divmod(abs(delta_seconds), 60)
    target = scheduled_dt.strftime("%Y-%m-%d %H:%M:%S")
    if delta_seconds >= 0:
        return f"Next break in {minutes} minutes {seconds} seconds (scheduled for {target})."
    return f"Break overdue by {minutes} minutes {seconds} seconds (scheduled for {target})."


def main() -> None:
    args = parse_args()
    log_path = args.log_path.expanduser().resolve()
    if not log_path.exists():
        raise SystemExit(f"Log file not found: {log_path}")

    _, scheduled_dt = find_next_break(log_path)
    print(format_remaining(scheduled_dt))


if __name__ == "__main__":
    main()
