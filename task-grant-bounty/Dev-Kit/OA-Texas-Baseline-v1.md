# Status

`Author: QGB-02 contributor`

`Status: Draft — pending field validation`

`Revision History: v0.1 (2026-08-29)`

`Reference: [QGB-02](https://github.com/Arrow-air/project-quiver/issues/203)`

# Project Description

This note documents the **Texas Baseline v1** candidate obstacle-avoidance parameter set for Project Quiver open-field testing. The configuration is derived from the validated Germany tree-dense baseline and adjusted using the Quiver SITL environment (SF45 LiDAR proxy) for open-field operating assumptions.

> **This parameter set is not flight-validated.** It is a starting point for Phase 2 testing in Texas. Final acceptance requires completion of the [OA testing roadmap](../../flight-test/OA/testing-roadmap.md).

# Methodology

## Baseline Comparison

| Parameter | Germany baseline | Texas v1 candidate | Rationale |
|-----------|------------------|--------------------|-----------|
| `OA_MARGIN_MAX` | 4 m | **5 m** | Open field allows a larger clearance envelope without blocking feasible paths |
| `AVOID_MARGIN` | 4 m | **5 m** | Matches BendyRuler margin; slow-down begins at `AVOID_DIST_MAX` |
| `AVOID_DIST_MAX` | 5 m | **6 m** | Earlier deceleration before hard-stop at moderate cruise speeds |
| `OA_BR_LOOKAHEAD` | 12 m | **14 m** | Additional reaction distance in low-clutter environments |
| `OA_DB_DIST_MAX` | 10 m | **12 m** | Keeps lookahead obstacles inside the proximity database |

All other OA parameters match the Germany baseline documented in [`Obstacle-Avoidance.md`](./Obstacle-Avoidance.md).

## SITL Exploration Matrix

Use the Quiver SITL environment documented in [`SITL-Evaluation.md`](./SITL-Evaluation.md):

```bash
../Tools/autotest/sim_vehicle.py --map --console \
  -A "--serial5=sim:sf45b --serial6=sim:obstacle"
```

Recommended sweep before each flight campaign (Loiter at 8 m AGL, single virtual obstacle ahead):

| Sweep | Parameter | Values to test | Pass signal |
|-------|-----------|----------------|-------------|
| Margin | `OA_MARGIN_MAX` / `AVOID_MARGIN` | 4, 5, 6 m | No contact; path remains smooth |
| Lookahead | `OA_BR_LOOKAHEAD` | 12, 14, 16 m | No oscillation around obstacle |
| Slow-down | `AVOID_DIST_MAX` | 5, 6, 7 m | Decel before hard stop; no overshoot |
| Database | `OA_DB_DIST_MAX` | 10, 12, 14 m | Obstacle retained through avoidance arc |

Eliminate configurations that cause oscillation, path reversal loops, or failure to resume mission track. Record QGroundControl screen captures and `.BIN` logs for each candidate.

## Parameter File

Load order on the flight controller:

1. [`standard-params.param`](../../docs/Operations/firmware/parameters/standard-params.param)
2. [`params-object-avoidance-texas-v1.param`](../../docs/Operations/firmware/parameters/params-object-avoidance-texas-v1.param)

Validate locally before upload:

```bash
python task-grant-bounty/Tools/OA-Analysis/compare_oa_params.py \
  docs/Operations/firmware/parameters/params-object-avoidance-texas-v1.param
```

# Results and Deliverables

| Deliverable | Status |
|-------------|--------|
| Texas Baseline v1 parameter file | **Candidate** — in repo |
| SITL exploration matrix | **Documented** — this note |
| Phase 2 stick-disturbance validation | **Pending** — requires Texas airframe |
| Germany cross-validation (Phase 4) | **Pending** — apply validated Texas set in trees |

# Remarks

- Revert to [`params-object-avoidance.param`](../../docs/Operations/firmware/parameters/params-object-avoidance.param) for Germany tree-dense operations until Phase 4 confirms Texas settings transfer safely.
- If S2L flight dropouts persist, resolve per [`OA-S2L-Dropout-Investigation.md`](OA-S2L-Dropout-Investigation.md) before structured OA tuning.
