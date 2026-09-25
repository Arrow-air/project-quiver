# Obstacle Avoidance Testing Roadmap

Derived from the [Arrow DAO forum roadmap](https://dao.arrowair.com/t/project-quiver-obstacle-avoidance-testing-roadmap/142) and QGB-02 acceptance criteria.

## Overall Pass Criteria

- Zero obstacle contact
- Minimum separation ≥ `OA_MARGIN_MAX` − 1 m at all times
- ≥ 95% AUTO mission success rate (Phase 3+)

Record for every test flight:

- `.BIN` DataFlash log
- CSV export for `analyze_proximity_log.py`
- Completed [template.md](./template.md) report

---

## Phase 1 — Sensor & Alignment Checks

**Site:** Texas open field  
**Altitude:** 8–10 m AGL  
**Mode:** Loiter

| ID | Procedure | Pass criteria |
|----|-----------|---------------|
| 1.1 | 360° yaw at ≤15°/s | PRX plot continuous; no blank sectors > 0.5 s |
| 1.2 | Walk-around with reflective board at 6–10 m | Smooth angle response; ±5° forward alignment |
| 1.3 | Hover 60 s, obstacle-free | No false detections; no prop-wash ghosts |

**Gate:** Do not proceed to Phase 2 until [S2L dropout investigation](../../task-grant-bounty/Dev-Kit/OA-S2L-Dropout-Investigation.md) criteria are met.

---

## Phase 2 — Simple Avoidance, Manual Control

**Site:** Texas open field  
**Parameter set:** [`params-object-avoidance-texas-v1.param`](../../docs/Operations/firmware/parameters/params-object-avoidance-texas-v1.param) (candidate)

| ID | Procedure | Pass criteria |
|----|-----------|---------------|
| 2.1 | Single obstacle circling (barrel/pole, figure-8) | Maintains ≥ `OA_MARGIN_MAX` − 1 m; no contact |
| 2.2 | Stick disturbance (padded stick, all approach angles) | Smooth deflection; recovery to Loiter | 
| 2.3 | Narrow gate (10 m gap, repeated passes) | Consistent clearance both directions |
| 2.4 | Payload impact (Brush-Bullet, full and discharged) | No EMI-induced PRX loss; margins unchanged |

**Deliverable:** On successful 2.1–2.3, promote Texas v1 from *candidate* to *validated* in [`OA-Texas-Baseline-v1.md`](../../task-grant-bounty/Dev-Kit/OA-Texas-Baseline-v1.md).

---

## Phase 3 — AUTO Missions

**Site:** Texas open field  
**Mode:** AUTO with BendyRuler (`OA_TYPE = 1`)

| ID | Procedure | Pass criteria |
|----|-----------|---------------|
| 3.1 | Two waypoints, single obstacle midway | Mission completes; clearance maintained |
| 3.2 | Two-obstacle gate (10 m openings) | ≥ 95% success over 20 runs |
| 3.3 | Wind & gusts (optional, 5–8 m/s) | No contact; mission success ≥ 95% |

---

## Phase 4 — Dense Environment Validation

**Site:** Germany tree-dense site  
**Parameter set:** Apply validated Texas Baseline v1; compare against Germany baseline if needed

| ID | Procedure | Pass criteria |
|----|-----------|---------------|
| 4.1 | Tree-gap navigation with payload | Same margins/stability as Texas |
| 4.2 | Landing accuracy | Within ±1.5 m of target |
| 4.3 | Failsafe to SmartRTL | Executes correctly on induced fault |

If Texas margins prove too large for tree gaps, document a Germany-specific override in `params-object-avoidance.param` and cross-reference both baselines in the OA overview doc.

---

## Post-Flight Analysis

1. Run proximity dropout check:
   ```bash
   python task-grant-bounty/Tools/OA-Analysis/analyze_proximity_log.py flight.csv --json
   ```
2. Verify minimum distance ≥ `OA_MARGIN_MAX` − 1 m using Mission Planner proximity viewer or custom scripts.
3. Attach logs and summary to the flight report under `flight-test/OA/reports/` (create per flight).
