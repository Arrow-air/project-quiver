# S2L Flight Dropout Investigation

# Status

`Author: QGB-02 contributor`

`Status: Open — root cause not confirmed`

`Revision History: v0.1 (2026-08-29)`

`Reference: [Forum post #6](https://dao.arrowair.com/t/project-quiver-obstacle-avoidance-testing-roadmap/142/6), [QGB-02](https://github.com/Arrow-air/project-quiver/issues/203)`

# Project Description

The RPLidar S2L exhibits intermittent proximity data dropouts during flight that are not observed on the ground. Structured obstacle-avoidance testing (Phases 1–4) must not proceed until dropout behavior is characterized and mitigated or accepted with documented operating limits.

This note consolidates known symptoms, investigation hypotheses, diagnostic procedures, and log-analysis tooling contributed under QGB-02.

# Methodology

## Observed Symptoms

| Symptom | Notes |
|---------|-------|
| Empty proximity screen at ~5 m AGL with obstacle directly ahead | Reported in flight; ground bench test shows normal returns |
| Data returns improve during 360° yaw turns | Suggests attitude-dependent or vibration-state dependency |
| No dropout on ground with identical parameter set | Points away from pure configuration error |

## Investigation Hypotheses (priority order)

1. **Vibration resonance** — LiDAR internal RPM may couple with airframe vibration modes after autotune or under prop wash.
2. **Connector / harness differences** — Texas vs Germany build connector or strain-relief variance on the TELEM3 UART path.
3. **Electrical load** — Voltage sag or UART noise under combined ESC + payload load in flight.
4. **Radome / body immersion** — LiDAR partially immersed in enclosure airflow; printing a raised lid may improve optical path.

## Recommended Diagnostic Sequence

Per Zeynep's forum guidance:

1. **Fresh build + autotune** — Re-run autotune and compare `VIBE` spectra before/after; improved vibration profile may resolve dropout.
2. **Connector audit** — Photograph and continuity-check TELEM3 harness (Main PCB U5 → S2L) on affected vs unaffected builds.
3. **Raised lid trial** — If steps 1–2 fail, print a lid variant that raises the S2L above the body airflow zone and re-test Phase 1 loiter + yaw.
4. **Log correlation** — For every suspect flight, export CSV and run proximity dropout analysis (below).

## Phase 1 Sensor Check (minimum bar before OA tuning)

At 8–10 m AGL in Loiter:

- [ ] 360° yaw at ≤15°/s — PRX plot continuous, no blank sectors > 0.5 s
- [ ] Walk-around with reflective board at 6–10 m — smooth angle response, ±5° forward alignment
- [ ] No false detections from prop wash or ground reflection at test altitude

**Pass:** Smooth angles, ±5° forward alignment, no false detections or blind sectors.

# Results and Deliverables

## Log Analysis Tooling

Export a CSV log from Mission Planner (`Review a Log` → `Save` as `.log` / CSV text), then run:

```bash
python task-grant-bounty/Tools/OA-Analysis/analyze_proximity_log.py path/to/flight.csv
```

Example JSON output for automated triage:

```bash
python task-grant-bounty/Tools/OA-Analysis/analyze_proximity_log.py \
  path/to/flight.csv --json
```

Interpretation guide:

| Metric | Healthy target | Investigate if |
|--------|----------------|----------------|
| `update_rate_hz` | ≥ 8 Hz (S2L ~10 Hz scan) | Sustained < 5 Hz in Loiter |
| `dropout_count` | 0 during Phase 1 hover | Any gap > 0.5 s with obstacle in FOV |
| `max_dropout_s` | < 0.5 s | ≥ 1.0 s during forward flight |

Cross-check dropout timestamps against `VIBE` and `ATT` in the same log. Correlation with high `VIBE.Z` supports the resonance hypothesis.

## Resolution Status

| Action | Status |
|--------|--------|
| Document symptoms and diagnostic path | **Complete** (this note) |
| Provide log analysis tooling | **Complete** ([`OA-Analysis`](../Tools/OA-Analysis/)) |
| Confirm root cause | **Open** — requires airframe access |
| Validate fix in flight | **Open** — blocked on root-cause work |

# Remarks

- Do not treat SITL results as evidence that S2L dropouts are resolved; SITL uses an SF45 model without dropout simulation.
- Attach anonymized CSV excerpts and `analyze_proximity_log.py` JSON output to forum post #6 when sharing findings with the core team.
