"""ArduPilot obstacle-avoidance parameter file utilities."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

ParamValue = float | int | str
ParamDict = dict[str, ParamValue]

OA_PARAM_GROUPS: dict[str, tuple[str, ...]] = {
    "avoid": (
        "AVOID_ENABLE",
        "AVOID_ACCEL_MAX",
        "AVOID_ALT_MIN",
        "AVOID_ANGLE_MAX",
        "AVOID_BACKUP_DZ",
        "AVOID_BACKUP_SPD",
        "AVOID_BACKZ_SPD",
        "AVOID_BEHAVE",
        "AVOID_DIST_MAX",
        "AVOID_MARGIN",
    ),
    "oa_core": ("OA_TYPE", "OA_OPTIONS", "OA_MARGIN_MAX"),
    "oa_database": (
        "OA_DB_SIZE",
        "OA_DB_QUEUE_SIZE",
        "OA_DB_EXPIRE",
        "OA_DB_OUTPUT",
        "OA_DB_BEAM_WIDTH",
        "OA_DB_RADIUS_MIN",
        "OA_DB_DIST_MAX",
        "OA_DB_ALT_MIN",
    ),
    "oa_bendyruler": (
        "OA_BR_TYPE",
        "OA_BR_LOOKAHEAD",
        "OA_BR_CONT_RATIO",
        "OA_BR_CONT_ANGLE",
    ),
}

# Conservative bounds used for pre-flight validation (not flight guarantees).
OA_PARAM_BOUNDS: dict[str, tuple[float, float]] = {
    "AVOID_ENABLE": (0, 7),
    "AVOID_MARGIN": (1, 15),
    "AVOID_DIST_MAX": (1, 30),
    "OA_MARGIN_MAX": (1, 15),
    "OA_BR_LOOKAHEAD": (3, 30),
    "OA_BR_CONT_ANGLE": (10, 180),
    "OA_BR_CONT_RATIO": (0.1, 5.0),
    "OA_DB_DIST_MAX": (1, 30),
    "OA_DB_EXPIRE": (0.5, 30),
}


def _coerce_value(raw: str) -> ParamValue:
    text = raw.strip()
    if not text:
        raise ValueError("empty parameter value")
    try:
        if "." in text:
            return float(text)
        return int(text)
    except ValueError:
        return text


def load_param_file(path: Path | str) -> ParamDict:
    """Load an ArduPilot ``.param`` file into a name → value mapping."""
    params: ParamDict = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "," not in stripped:
            continue
        name, _, value = stripped.partition(",")
        name = name.strip()
        if not name:
            continue
        params[name] = _coerce_value(value)
    return params


def compare_param_sets(
    baseline: Mapping[str, ParamValue],
    candidate: Mapping[str, ParamValue],
    *,
    names: tuple[str, ...] | None = None,
) -> dict[str, tuple[ParamValue, ParamValue]]:
    """Return parameters that differ between *baseline* and *candidate*."""
    keys = names or tuple(sorted(set(baseline) | set(candidate)))
    diffs: dict[str, tuple[ParamValue, ParamValue]] = {}
    for key in keys:
        base_val = baseline.get(key)
        candidate_val = candidate.get(key)
        if base_val != candidate_val:
            diffs[key] = (base_val, candidate_val)
    return diffs


def validate_oa_params(params: Mapping[str, ParamValue]) -> list[str]:
    """Return human-readable validation issues for OA-related parameters."""
    issues: list[str] = []

    if params.get("OA_TYPE") not in (None, 1):
        issues.append("OA_TYPE should be 1 (BendyRuler) for Quiver OA configuration")

    if params.get("OA_BR_TYPE") not in (None, 1):
        issues.append("OA_BR_TYPE should be 1 when BendyRuler is enabled")

    avoid_margin = params.get("AVOID_MARGIN")
    oa_margin = params.get("OA_MARGIN_MAX")
    if avoid_margin is not None and oa_margin is not None:
        if float(avoid_margin) > float(oa_margin):
            issues.append(
                "AVOID_MARGIN exceeds OA_MARGIN_MAX; hard-stop margin must not exceed "
                "BendyRuler clearance target"
            )

    dist_max = params.get("AVOID_DIST_MAX")
    if dist_max is not None and oa_margin is not None:
        if float(dist_max) < float(oa_margin):
            issues.append(
                "AVOID_DIST_MAX should be >= AVOID_MARGIN so the vehicle slows before "
                "the hard-stop envelope"
            )

    lookahead = params.get("OA_BR_LOOKAHEAD")
    db_dist = params.get("OA_DB_DIST_MAX")
    if lookahead is not None and db_dist is not None:
        if float(lookahead) > float(db_dist) + 5:
            issues.append(
                "OA_BR_LOOKAHEAD is much larger than OA_DB_DIST_MAX; distant obstacles "
                "may be ignored by the proximity database"
            )

    for name, (lo, hi) in OA_PARAM_BOUNDS.items():
        value = params.get(name)
        if value is None or isinstance(value, str):
            continue
        if not lo <= float(value) <= hi:
            issues.append(f"{name}={value} is outside recommended range [{lo}, {hi}]")

    return issues
