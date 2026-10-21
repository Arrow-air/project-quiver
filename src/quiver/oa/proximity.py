"""Proximity log analysis for S2L dropout characterization."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProximitySample:
    """One PRX log row with the minimum sector distance in centimeters."""

    time_us: int
    min_distance_cm: int


@dataclass(frozen=True)
class DropoutEvent:
    """Gap in PRX updates that may indicate a sensor dropout."""

    start_us: int
    end_us: int
    duration_s: float


def _sector_distances_cm(fields: list[str]) -> list[int]:
    """Extract horizontal sector distances (D0–D315) from a PRX CSV row."""
    distances: list[int] = []
    # ArduPilot PRX: Layer at index 2, then 8 horizontal sectors, DUp, CMin, CMax.
    for field in fields[3:11]:
        field = field.strip()
        if not field:
            continue
        try:
            value = int(float(field))
        except ValueError:
            break
        if value >= 0:
            distances.append(value)
    return distances


def parse_prx_lines(lines: list[str]) -> list[ProximitySample]:
    """Parse PRX rows from an ArduPilot CSV log export."""
    samples: list[ProximitySample] = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("PRX,"):
            continue
        fields = stripped.split(",")
        if len(fields) < 4:
            continue
        try:
            time_us = int(fields[1])
        except ValueError:
            continue
        distances = _sector_distances_cm(fields)
        if not distances:
            continue
        samples.append(ProximitySample(time_us=time_us, min_distance_cm=min(distances)))
    return samples


def detect_dropouts(
    samples: list[ProximitySample],
    *,
    gap_threshold_s: float = 0.5,
) -> list[DropoutEvent]:
    """Detect PRX update gaps longer than *gap_threshold_s*."""
    if len(samples) < 2:
        return []

    threshold_us = int(gap_threshold_s * 1_000_000)
    events: list[DropoutEvent] = []
    for prev, curr in zip(samples, samples[1:]):
        gap = curr.time_us - prev.time_us
        if gap > threshold_us:
            events.append(
                DropoutEvent(
                    start_us=prev.time_us,
                    end_us=curr.time_us,
                    duration_s=gap / 1_000_000,
                )
            )
    return events


def analyze_proximity_log(
    path: Path | str,
    *,
    gap_threshold_s: float = 0.5,
) -> dict[str, object]:
    """Summarize PRX availability and dropout events in a CSV log export."""
    lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    samples = parse_prx_lines(lines)
    dropouts = detect_dropouts(samples, gap_threshold_s=gap_threshold_s)

    if not samples:
        return {
            "sample_count": 0,
            "duration_s": 0.0,
            "update_rate_hz": 0.0,
            "dropout_count": 0,
            "dropouts": [],
            "max_dropout_s": 0.0,
            "min_distance_m": None,
        }

    duration_s = (samples[-1].time_us - samples[0].time_us) / 1_000_000
    update_rate_hz = (
        (len(samples) - 1) / duration_s if duration_s > 0 else float(len(samples))
    )

    return {
        "sample_count": len(samples),
        "duration_s": round(duration_s, 3),
        "update_rate_hz": round(update_rate_hz, 2),
        "dropout_count": len(dropouts),
        "dropouts": dropouts,
        "max_dropout_s": round(max((d.duration_s for d in dropouts), default=0.0), 3),
        "min_distance_m": round(min(s.min_distance_cm for s in samples) / 100.0, 2),
    }
