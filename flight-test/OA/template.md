## 1. Flight Information

Flight ID: OA-___

Date / Time:

Location: Texas open field / Germany tree-dense

Pilot in Command:

Aircraft Designation:

OA parameter file loaded: `params-object-avoidance` / `params-object-avoidance-texas-v1`

## 2. Test Conditions

Weather:

Wind speed / direction:

Temperature:

Test phase & ID (from [testing-roadmap.md](./testing-roadmap.md)): e.g. Phase 2.2

## 3. Test Aim / Procedure

### 3.1. Test Aim

### 3.2. Test Plan

## 4. Preflight Checklist

- [ ] S2L PRX returns on ground (Proximity viewer)
- [ ] OA parameter file validated (`compare_oa_params.py`)
- [ ] Phase 1 dropout check passed (if applicable)
- [ ] Failsafes verified (SmartRTL / RTL / Land)

## 5. Flight Test

### 5.1. Observations

Minimum clearance observed (estimate):

OA behaviour (smooth / oscillation / stop-slide / failed):

### 5.2. Pass / Fail

| Criterion | Result |
|-----------|--------|
| No obstacle contact | |
| Separation ≥ `OA_MARGIN_MAX` − 1 m | |
| PRX dropout_count = 0 (hover/check) | |

## 6. Logs & Analysis

`.BIN` log path:

CSV export path:

```bash
python task-grant-bounty/Tools/OA-Analysis/analyze_proximity_log.py <csv> --json
```

Paste JSON summary:

## 7. Recommendations
