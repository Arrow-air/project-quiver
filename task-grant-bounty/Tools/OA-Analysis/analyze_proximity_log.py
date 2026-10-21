#!/usr/bin/env python3
"""Analyze ArduPilot CSV logs for RPLidar S2L proximity dropouts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "src"))

from quiver.oa.proximity import analyze_proximity_log  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Detect PRX gaps in an ArduPilot CSV log export.",
    )
    parser.add_argument("log", type=Path, help="Path to CSV log export")
    parser.add_argument(
        "--gap-threshold",
        type=float,
        default=0.5,
        help="Gap length in seconds that counts as a dropout (default: 0.5)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON summary",
    )
    args = parser.parse_args()

    if not args.log.is_file():
        print(f"error: file not found: {args.log}", file=sys.stderr)
        return 1

    summary = analyze_proximity_log(args.log, gap_threshold_s=args.gap_threshold)
    if args.json:
        payload = dict(summary)
        payload["dropouts"] = [
            {
                "start_us": event.start_us,
                "end_us": event.end_us,
                "duration_s": event.duration_s,
            }
            for event in summary["dropouts"]
        ]
        print(json.dumps(payload, indent=2))
        return 0

    print(f"samples:        {summary['sample_count']}")
    print(f"duration_s:     {summary['duration_s']}")
    print(f"update_rate_hz: {summary['update_rate_hz']}")
    print(f"dropout_count:  {summary['dropout_count']}")
    print(f"max_dropout_s:  {summary['max_dropout_s']}")
    print(f"min_distance_m: {summary['min_distance_m']}")
    for index, event in enumerate(summary["dropouts"], start=1):
        print(
            f"dropout {index}: {event.duration_s:.3f}s "
            f"({event.start_us} → {event.end_us} µs)"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
