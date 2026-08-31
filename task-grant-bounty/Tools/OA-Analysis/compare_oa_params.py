#!/usr/bin/env python3
"""Compare Quiver obstacle-avoidance parameter baselines."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "src"))

from quiver.oa.params import compare_param_sets, load_param_file, validate_oa_params  # noqa: E402

DEFAULT_BASELINE = (
    REPO_ROOT / "docs/Operations/firmware/parameters/params-object-avoidance.param"
)
DEFAULT_TEXAS = (
    REPO_ROOT
    / "docs/Operations/firmware/parameters/params-object-avoidance-texas-v1.param"
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate and compare Quiver OA parameter files.",
    )
    parser.add_argument(
        "param",
        nargs="?",
        type=Path,
        default=DEFAULT_TEXAS,
        help="Parameter file to validate (default: Texas Baseline v1 candidate)",
    )
    parser.add_argument(
        "--baseline",
        type=Path,
        default=DEFAULT_BASELINE,
        help="Baseline parameter file for diff output",
    )
    args = parser.parse_args()

    if not args.param.is_file():
        print(f"error: file not found: {args.param}", file=sys.stderr)
        return 1

    params = load_param_file(args.param)
    issues = validate_oa_params(params)
    if issues:
        print("validation issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("validation: ok")

    if args.baseline.is_file():
        baseline = load_param_file(args.baseline)
        diffs = compare_param_sets(baseline, params)
        if diffs:
            print("\ndifferences vs baseline:")
            for name, (base_val, candidate_val) in sorted(diffs.items()):
                print(f"  {name}: {base_val!r} → {candidate_val!r}")
        else:
            print("\nno differences vs baseline")

    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
