# Obstacle Avoidance Flight Testing

Structured flight-test documentation for Quiver obstacle avoidance (QGB-02). Physical execution requires access to the Texas open-field site (Phases 1–3) and Germany tree-dense site (Phase 4).

## Contents

| Document | Purpose |
|----------|---------|
| [testing-roadmap.md](./testing-roadmap.md) | Phase 1–4 procedures, pass criteria, log requirements |
| [template.md](./template.md) | Per-flight report template (extends PT3-TX format) |

## Related Documentation

- [OA System Overview](../../task-grant-bounty/Dev-Kit/Obstacle-Avoidance.md)
- [SITL Evaluation](../../task-grant-bounty/Dev-Kit/SITL-Evaluation.md)
- [Texas Baseline v1 (candidate)](../../task-grant-bounty/Dev-Kit/OA-Texas-Baseline-v1.md)
- [S2L Dropout Investigation](../../task-grant-bounty/Dev-Kit/OA-S2L-Dropout-Investigation.md)
- [OA Log Analysis Tooling](../../task-grant-bounty/Tools/OA-Analysis/information-note.md)

## Parameter Files

| File | Environment |
|------|-------------|
| [`params-object-avoidance.param`](../../docs/Operations/firmware/parameters/params-object-avoidance.param) | Germany tree-dense baseline (validated low-speed) |
| [`params-object-avoidance-texas-v1.param`](../../docs/Operations/firmware/parameters/params-object-avoidance-texas-v1.param) | Texas open-field candidate (pending validation) |

## Pre-Flight Checklist (all phases)

- [ ] Custom ArduPilot firmware with S2L driver ([PR #31663](https://github.com/ArduPilot/ardupilot/pull/31663)) flashed
- [ ] Correct OA parameter file loaded and validated (`compare_oa_params.py`)
- [ ] Phase 1 sensor checks passed — **no S2L dropouts** per [dropout investigation](../../task-grant-bounty/Dev-Kit/OA-S2L-Dropout-Investigation.md)
- [ ] Failsafes configured (SmartRTL recommended for payload tests)
- [ ] `.BIN` log + CSV export planned for post-flight analysis

## Status (2026-08-29)

| Phase | Status |
|-------|--------|
| 1 — Sensor & alignment | **Not started** (blocked on S2L dropout) |
| 2 — Manual avoidance | **Not started** |
| 3 — AUTO missions | **Not started** |
| 4 — Dense environment | **Not started** |

SITL parameter exploration and analysis tooling are available; field validation remains open.
