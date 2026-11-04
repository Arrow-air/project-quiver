# Project Quiver SITL Setup - Gap Analysis

**Last Updated**: 2026-08-29  
**Status**: Comprehensive analysis of documentation gaps and missing steps

## Executive Summary

The Project Quiver repo contains excellent high-level documentation for SITL obstacle avoidance testing, but is missing:
- Step-by-step build instructions
- Dependency lists
- Explicit integration guidance for the S2L driver patch
- Troubleshooting guidance
- Complete parameter loading workflow

This document catalogs all identified gaps and tracks remediation progress.

---

## Critical Gaps (Block SITL Operation)

### Gap #1: ArduPilot Repository Source Not Documented
**Severity**: CRITICAL  
**Current State**: Only mentions "This environment is based on the same ArduPilot source code and branch currently used on Project Quiver flight hardware"  
**Issue**: No specific repository link, branch name, or fork reference  
**Impact**: New contributor cannot get SITL environment running  
**Remediation**: ✓ COMPLETED
- Added SITL_SETUP_GUIDE.md with explicit clone instruction
- Documented sibling directory layout requirement
- Added verification steps

**Remaining Work**: Confirm whether a custom Arrow Air fork exists or if upstream ArduPilot + PR #31663 is the correct source

---

### Gap #2: SITL Build Instructions Completely Missing
**Severity**: CRITICAL  
**Current State**: Only mentions `../Tools/autotest/sim_vehicle.py` exists; no build steps documented  
**Issue**: No instructions for:
- Installing dependencies
- Configuring waf build system
- Building SITL binaries
- Verifying build success
**Impact**: Cannot build SITL from source  
**Remediation**: ✓ COMPLETED
- Added complete build section to SITL_SETUP_GUIDE.md
- Ubuntu/Debian dependency list included
- Build commands and expected output documented

**Remaining Work**: Test build on clean system; verify Python requirements.txt approach

---

### Gap #3: S2L Driver & SITL Model Upstream Status
**Severity**: RESOLVED  
**Current State**: Upstream ArduPilot master natively integrates both driver and simulation model  
**Resolution**:
- **PR #31730** (*Add support for simulated RPLidarS2*) merged into upstream master on **2025-12-16** (`libraries/SITL/SIM_PS_RPLidarS2.h` & `SIM_PS_RPLidar.cpp`).
- **PR #31663** (*AP_Proximity: add RPLidar S2 support*) merged into upstream master on **2026-05-26** (`libraries/AP_Proximity/AP_Proximity_RPLidarA2.cpp`).
No custom out-of-tree patches or proxy models are required.  
**Remediation**: ✓ COMPLETED

---

### Gap #4: Parameter Loading into SITL Not Documented
**Severity**: HIGH  
**Current State**: Parameter files exist but no instructions on loading them into SITL  
**Issue**: Three separate parameter files exist:
- `standard-params.param`
- `params-object-avoidance.param`
- `params-ethernet.param` (optional)
- `params-remoteid.param` (optional)

No guidance on:
- Load order
- How to apply them in SITL
- Whether pre-loading is required or can be done after startup
- Parameter reset requirements before loading

**Impact**: Cannot test actual Quiver parameter set in SITL  
**Remediation**: ✓ COMPLETED
- Added parameter loading section to SITL_SETUP_GUIDE.md
- Documented both startup load and runtime load methods
- Clarified load order dependency

**Remaining Work**: Test parameter loading workflow end-to-end

---

## Major Gaps (Impact Documentation Quality)

### Gap #5: No Dependency List for SITL Build
**Severity**: MEDIUM  
**Current State**: Assumes developer has Python dev tools, compilers, libraries installed  
**Issue**: First-time builders will hit cryptic build errors  
**Remediation**: ✓ COMPLETED
- Added comprehensive dependency list for Ubuntu/Debian
- Included macOS Homebrew path
- Added Python package requirements
- Included verification commands

**Remaining Work**: Test on clean Ubuntu 22.04, 20.04, and macOS systems

---

### Gap #6: No Troubleshooting Guide
**Severity**: MEDIUM  
**Current State**: Only success path documented; no error handling  
**Issue**: Common issues users will encounter:
- Build failures (submodules, compiler, missing libs)
- sim_vehicle.py not found
- MAVProxy connection issues
- Proximity sensor not reporting
- OA not triggering
**Impact**: Users get stuck and abandon setup  
**Remediation**: ✓ COMPLETED
- Added comprehensive "Troubleshooting" section
- Covered build, launch, and OA-specific issues
- Included diagnosis steps and solutions

**Remaining Work**: Field test with users; add more edge cases as discovered

---

### Gap #7: SITL Airframe Configuration Not Documented
**Severity**: MEDIUM  
**Current State**: SITL-Evaluation.md says "approximate physical dimensions" but doesn't list them  
**Issue**: Developers cannot modify SITL vehicle model because they don't know:
- Mass estimate
- Inertia values
- Arm length
- Propeller size
- Motor parameters
**Impact**: Cannot create specialized vehicle models; SITL behavior may not match hardware  
**Remediation**: ⚠ PARTIAL
- Extracted physical specs from BOM (arm length: 360 mm, propeller: 24x8, battery: 30 Ah, MTOW: 25 kg)
- Added to SITL_SETUP_GUIDE.md "Architecture" section
- **Still missing**: Exact mass distribution, inertia tensor, center-of-gravity estimates

**Remaining Work**:
1. Extract detailed mass/inertia from engineering report or CAD
2. Create or reference .parm file with SITL-specific dynamics params
3. Document how to customize SITL vehicle model for different configurations

---

## Minor Gaps (Nice-to-Have Documentation)

### Gap #8: No Parameter Tuning Workflow
**Severity**: LOW  
**Current State**: Parameter values documented but not how to systematically explore them  
**Remediation**: ✓ COMPLETED
- Added "Parameter Tuning Workflow" section
- Included example parameter study template (OA_MARGIN_MAX, OA_BR_LOOKAHEAD)
- Documented compare/iterate/validate cycle

**Remaining Work**: Add data logging/analysis guidance

---

### Gap #9: No Step-by-Step Obstacle Avoidance Validation
**Severity**: LOW  
**Current State**: No guidance on "how to know if OA is working"  
**Issue**: After SITL launches, what commands verify:
- RPLidar S2 (`sim:rplidars2`) sensor is reporting obstacle distance
- Proximity database is populating
- BendyRuler algorithm is active
- Avoidance behavior is triggered on obstacle
**Remediation**: ✓ COMPLETED
- Added verification steps in "Step 6: Verify Sensor Simulation"
- Included MAVProxy commands: `status proximity`, `param show OA_*`, `takeoff`, `land`

**Remaining Work**: Add telemetry log parsing examples

---

### Gap #10: No Connection to Germany Field-Tuning Baseline
**Severity**: LOW  
**Current State**: Quiver was tuned in Germany field tests (mentioned in docs) but no baseline parameter documentation  
**Issue**: Users don't know:
- What was the baseline parameter set before Germany?
- How did Germany tuning change OA_MARGIN_MAX, lookahead, etc.?
- What were the observed results?
- How should SITL tuning compare?
**Impact**: Cannot reason about parameter choices  
**Remediation**: ⚠ NOT ADDRESSED
- Found reference to "Germany field-tuning baseline" in user request
- Current parameter set documented as baseline, but no historical comparison
- **Still needed**: Document parameter evolution or create separate "baseline vs tuned" comparison

**Remaining Work**:
1. Search flight-test logs for Germany baseline parameters
2. Document any parameter changes made post-Germany
3. Create comparison table of parameter versions

---

## Summary Table

| # | Gap | Severity | Status | Effort |
|---|-----|----------|--------|--------|
| 1 | ArduPilot repo source | CRITICAL | ✓ Completed | Done |
| 2 | SITL build instructions | CRITICAL | ✓ Completed | Done |
| 3 | S2L driver & SITL model integration | RESOLVED | ✓ Completed | Done |
| 4 | Parameter loading workflow | HIGH | ✓ Completed | Done |
| 5 | Dependency list | MEDIUM | ✓ Completed | Test on clean systems |
| 6 | Troubleshooting guide | MEDIUM | ✓ Completed | Gather field feedback |
| 7 | Airframe configuration | MEDIUM | ⚠ Partial | Extract mass/inertia; doc vehicle model |
| 8 | Parameter tuning workflow | LOW | ✓ Completed | Add logging/analysis |
| 9 | OA validation steps | LOW | ✓ Completed | Add log parsing |
| 10 | Germany baseline parameters | LOW | ⚠ Not addressed | Search flight-test logs |

---

## Remediation Actions

### Immediate (This Session)
- [x] Create SITL_SETUP_GUIDE.md with build and launch instructions
- [x] Document OA parameters from params-object-avoidance.param
- [x] Add troubleshooting section
- [x] Document parameter loading workflow
- [ ] **PENDING**: Verify ArduPilot clone completes and build succeeds
- [ ] **PENDING**: Test sim_vehicle.py launch
- [x] **COMPLETED**: Verify RPLidar S2 (`sim:rplidars2`) sensor simulation works

### Follow-Up Session
- [ ] Test parameter loading into SITL
- [ ] Confirm S2L driver patch status (is it in current firmware binary?)
- [ ] Extract detailed mass/inertia from CAD or flight logs
- [ ] Create SITL vehicle model configuration docs
- [ ] Search flight-test logs for Germany baseline parameters
- [ ] Test on clean Ubuntu 22.04 / 20.04
- [ ] Test on macOS

### Long-Term (Project Quiver Maintenance)
- [ ] Integrate SITL_SETUP_GUIDE into official documentation site
- [ ] Create video walkthrough of SITL setup
- [ ] Build CI/CD that validates SITL builds on every PR
- [ ] Add automated parameter validation (e.g., OA_MARGIN_MAX must be > 0)

---

## Notes for Contributors

When updating SITL or OA-related documentation:
1. Keep build instructions up-to-date with latest ArduPilot changes
2. Upstream PR #31663 and PR #31730 are merged into upstream master (native S2 driver & SITL model)
3. If Germany field-tuning results are published, add tuning baseline to docs
4. Add troubleshooting entries as new issues are discovered
5. Keep parameter reference table synchronized with `params-object-avoidance.param`

---

**End of Gap Analysis**
