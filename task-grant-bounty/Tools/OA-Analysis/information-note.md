# Status

`Valid`

# Project Description

Command-line utilities for validating Quiver obstacle-avoidance parameter files and analyzing RPLidar S2L proximity dropouts in ArduPilot CSV log exports. Contributed under [QGB-02](https://github.com/Arrow-air/project-quiver/issues/203).

# Methodology

## compare_oa_params.py

Loads an ArduPilot `.param` file, checks OA parameter consistency (margin ordering, BendyRuler enablement, recommended ranges), and diffs against the Germany baseline.

```bash
python task-grant-bounty/Tools/OA-Analysis/compare_oa_params.py \
  docs/Operations/firmware/parameters/params-object-avoidance-texas-v1.param
```

## analyze_proximity_log.py

Parses `PRX` rows from a Mission Planner CSV export, computes update rate, and flags gaps longer than a configurable threshold (default 0.5 s) to support [S2L dropout investigation](../../Dev-Kit/OA-S2L-Dropout-Investigation.md).

```bash
python task-grant-bounty/Tools/OA-Analysis/analyze_proximity_log.py flight.csv --json
```

Core logic lives in `src/quiver/oa/` and is covered by `src/tests/test_oa.py`.

# Results and Deliverables

- Parameter validation and baseline diff tooling
- PRX dropout detection for flight log triage
- Unit tests runnable via `python -m pytest src/tests/test_oa.py`

# Remarks

- Requires CSV log export; native `.BIN` parsing is out of scope (use Mission Planner export or pymavlink separately).
- Dropout detection identifies timestamp gaps only — correlate with `VIBE` manually for root-cause analysis.
