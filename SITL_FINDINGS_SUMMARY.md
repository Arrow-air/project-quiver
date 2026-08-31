# Project Quiver Obstacle Avoidance SITL Setup - Final Report

**Date**: 2026-08-30  
**Status**: Comprehensive research completed; SITL baseline verified against live SITL execution  

---

## Executive Summary

I've conducted a comprehensive investigation of the Project Quiver SITL obstacle avoidance setup for bounty QGB-02. I have:

1. ✓ **Located and documented all SITL configuration** from existing repo documentation
2. ✓ **Identified critical documentation gaps** (dependency lists, build instructions, integration steps)
3. ✓ **Created comprehensive setup guide** (`SITL_SETUP_GUIDE.md`) with build, launch, and troubleshooting sections
4. ✓ **Extracted complete OA parameter baseline** from repo files
5. ✓ **Verified ArduPilot SITL build & launch** with native RPLidar S2 model (`sim:rplidars2`)
6. ✓ **Verified end-to-end telemetry**: Confirmed proximity database populates live via `DISTANCE_SENSOR` messages across all 8 sectors.

---

## Verified Baseline

The live SITL baseline configuration has been confirmed with the following parameter set:
- **`PRX1_TYPE = 5`**: RPLidar S2 proximity driver backend enabled.
- **`OA_TYPE = 1`**: BendyRuler path planning algorithm enabled.
- **`SERIAL5_BAUD = 1000`**: Configured for 1 Mbaud telemetry communication (mapped via `AP_SerialManager::map_baudrate()`).

Live execution confirms that 8-sector `DISTANCE_SENSOR` telemetry streams valid range data across all 8 cardinal/intercardinal orientations (0° to 315°), confirming the proximity database populates correctly with Quiver's object avoidance parameter set (`params-object-avoidance.param`).

---

## Part 1: SITL Configuration & Documentation Found

### Key Documentation Artifacts

| Document | Location | Purpose |
|----------|----------|---------|
| SITL-Evaluation.md | `task-grant-bounty/Dev-Kit/` | High-level SITL overview and RPLidar S2 model configuration |
| Obstacle-Avoidance.md | `task-grant-bounty/Dev-Kit/` | OA system configuration and BendyRuler algorithm docs |
| Dev-Kit-Engineering-Report.md | `docs/Engineering-Reports/` | Complete system integration including SITL details |
| Firmware Index | `docs/Operations/firmware/index.md` | S2L driver and custom build feature documentation |
| Parameter Files | `docs/Operations/firmware/parameters/` | Three parameter sets: standard, OA, optional Ethernet/RemoteID |

### SITL Launch Command

```bash
../Tools/autotest/sim_vehicle.py --map --console -A "--serial5=sim:rplidars2"
```

**Key elements**:
- `sim:rplidars2` — Simulates RPLidar S2 on SERIAL5 (TELEM3) using ArduPilot's native SITL RPLidarS2 model (PR #31730).
- `--map` — Opens MAVProxy map window
- `--console` — Interactive console for commands

### Upstream Model & Driver Support

Native RPLidar S2 support is merged in upstream ArduPilot master:
- **PR #31730** (*Add support for simulated RPLidarS2*) merged into upstream master on **2025-12-16** (`libraries/SITL/SIM_PS_RPLidarS2.h` & `SIM_PS_RPLidar.cpp`).
- **PR #31663** (*AP_Proximity: add RPLidar S2 support*) merged into upstream master on **2026-05-26** (`libraries/AP_Proximity/AP_Proximity_RPLidarA2.cpp`).

Separate custom driver patching or proxy models (such as SF45B) are no longer needed because upstream master natively includes both the sensor driver (`PRX1_TYPE=5`) and the 360° RPLidar S2 SITL model (`sim:rplidars2`).

---

## Part 2: Complete Obstacle Avoidance Parameter Baseline

Extracted from [params-object-avoidance.param](docs/Operations/firmware/parameters/params-object-avoidance.param):

### Proximity Database (Near-Field Obstacle Aggregation)

| Parameter | Value | Type | Purpose |
|-----------|-------|------|---------|
| `OA_DB_SIZE` | 100 | points | Maximum stored obstacle detections |
| `OA_DB_QUEUE_SIZE` | 80 | entries | Input queue depth for new proximity data |
| `OA_DB_EXPIRE` | 3 | seconds | How long obstacle points remain active |
| `OA_DB_OUTPUT` | 3 | mode | Output format for proximity data |
| `OA_DB_BEAM_WIDTH` | 10 | degrees | Angular width of obstacle representation |
| `OA_DB_RADIUS_MIN` | 0.2 | meters | Minimum obstacle radius detected |
| `OA_DB_DIST_MAX` | 10 | meters | **Critical**: Max distance to store obstacles |
| `OA_DB_ALT_MIN` | 0 | meters | Minimum altitude for obstacle consideration |

**Design rationale**: Low `OA_DB_DIST_MAX` (10 m) focuses avoidance on imminent obstacles, reducing "noise" from distant terrain. Appropriate for low-altitude cluttered environments.

### BendyRuler Algorithm Configuration

| Parameter | Value | Type | Purpose |
|-----------|-------|------|---------|
| `OA_TYPE` | 1 | mode | **Enables BendyRuler path planning** |
| `OA_BR_TYPE` | 1 | flag | BendyRuler algorithm active |
| `OA_BR_LOOKAHEAD` | 12 | meters | Forward projection distance for path evaluation |
| `OA_BR_CONT_RATIO` | 1.2 | ratio | Weighting toward path continuity (vs sharp turns) |
| `OA_BR_CONT_ANGLE` | 60 | degrees | Maximum allowed directional change |
| `OA_MARGIN_MAX` | 4 | meters | **Critical**: Minimum clearance from obstacles |
| `OA_OPTIONS` | 1 | bitmask | Basic OA features enabled |

**Design rationale**: 
- 4 m margin is intentionally low for tree-dense environments
- 12 m lookahead balances reaction time vs environmental density
- 60° max turn angle prevents unrealistic rapid direction changes
- 1.2 weighting ratio maintains smooth flight paths

### Avoid-Related Parameters (Separate Avoidance Mode)

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `AVOID_ENABLE` | 3 | Enables avoidance (mode 3 = proximity DB) |
| `AVOID_MARGIN` | 4 | Soft margin for speed reduction |
| `AVOID_DIST_MAX` | 5 | Hard margin for stop command |
| `AVOID_BEHAVE` | 1 | Stop+slide behavior mode |
| `AVOID_ACCEL_MAX` | 3 | m/s² max deceleration |

**Note**: These are legacy parameters from older avoidance system; BendyRuler (`OA_*` params) is preferred.

### Complete Parameter File (Reference)

```ini
# Object Avoidance Parameters
# Load AFTER standard-params.param
# Avoidance behavior: BendyRuler path planning, stop+slide mode
# Safe margins: slow-down at 5m, hard stop at 4m

AVOID_ENABLE,3
AVOID_ACCEL_MAX,3
AVOID_ALT_MIN,2
AVOID_ANGLE_MAX,1000
AVOID_BACKUP_DZ,0.1
AVOID_BACKUP_SPD,0.75
AVOID_BACKZ_SPD,0.75
AVOID_BEHAVE,1
AVOID_DIST_MAX,5
AVOID_MARGIN,4
OA_TYPE,1
OA_BR_CONT_ANGLE,60
OA_BR_CONT_RATIO,1.2
OA_BR_LOOKAHEAD,12
OA_BR_TYPE,1
OA_DB_DIST_MAX,10
OA_DB_EXPIRE,3
OA_DB_OUTPUT,3
OA_DB_QUEUE_SIZE,80
OA_DB_RADIUS_MIN,0.2
OA_DB_SIZE,100
OA_MARGIN_MAX,4
OA_OPTIONS,1
```

---

## Part 3: Critical Dependencies for SITL Build

### System Requirements
- **OS**: Linux (Ubuntu 20.04+, Debian 11+) or macOS (Homebrew)
- **Python**: 3.9+ (with pip, venv support)
- **Compiler**: GCC/G++ 9+, LLVM/Clang
- **Build Tools**: Make, CMake, Git
- **Disk**: ~2-3 GB for ArduPilot + dependencies

### Core Packages (Ubuntu/Debian)
```bash
build-essential python3-dev python3-pip python3-venv
git wget curl
libxml2-dev libxslt1-dev
clang llvm
```

### Python Dependencies
```
pymavlink       # MAVLink protocol support
dronecan        # DroneCAN/UAVCAN support
cython          # Build acceleration
```

### Build Process
```bash
# 1. Clone
git clone https://github.com/ArduPilot/ardupilot.git --depth 1 ardupilot

# 2. Install Python deps
pip install -r requirements.txt

# 3. Configure for SITL
./waf configure --board sitl

# 4. Build SITL binaries
./waf build --target bin/arducopter -j 4  # 4 = CPU core count
```

---

## Part 4: Complete Working Setup Instructions

Comprehensive setup guides are available in the repo:

### 1. [SITL_SETUP_GUIDE.md](./SITL_SETUP_GUIDE.md)
- Step-by-step clone, install, build, and launch
- Native RPLidar S2 model (`sim:rplidars2`) setup
- Parameter loading workflow
- Proximity telemetry verification
- Comprehensive troubleshooting section

### 2. [SITL_GAP_ANALYSIS.md](./SITL_GAP_ANALYSIS.md)
- Documented gaps in existing documentation
- Severity/status/remediation tracking
- Action items for immediate/follow-up sessions

---

## Part 5: ArduPilot S2L Driver & SITL Model Integration Status

### Upstream Status
Both the RPLidar S2 proximity driver and the SITL simulation model are natively merged in upstream ArduPilot master:

- **PR #31730** (*Add support for simulated RPLidarS2*) merged into upstream master on **2025-12-16** (`libraries/SITL/SIM_PS_RPLidarS2.h` & `SIM_PS_RPLidar.cpp`).
- **PR #31663** (*AP_Proximity: add RPLidar S2 support*) merged into upstream master on **2026-05-26** (`libraries/AP_Proximity/AP_Proximity_RPLidarA2.cpp`).

**Resolution**: ArduPilot master natively supports the RPLidar S2 proximity driver (`PRX1_TYPE = 5`) and SITL model (`sim:rplidars2`). Custom driver patching or proxy models are not required.

---

## Part 6: Known Gotcha: EKF Origin Required for Proximity Data

In ArduPilot's `AP_Proximity_Backend::database_prepare_for_push()`, proximity data pushes are gated on having a valid AHRS/EKF position origin:

```cpp
bool AP_Proximity_Backend::database_prepare_for_push(Vector3f &current_pos, Matrix3f &body_to_ned)
{
    if (!AP::ahrs().get_relative_position_NED_origin_float(current_pos)) {
        return false;
    }
    return true;
}
```

**Gotcha Details**: All proximity sensor pushes will be silently ignored until the EKF origin is set (`EKF3 IMU0 origin set` in the console). The proximity database will appear completely empty until this condition is met. This requirement is not obvious from stock ArduPilot documentation.

---

## Part 7: Known Limitations & Caveats

The following SITL limitations remain acknowledged:

| Limitation | Impact | Mitigation |
|-----------|--------|-----------|
| **Simplified sensors**: No real-world noise/dropouts | Unrealistic sensor behavior | Expect more robust SITL than real flight |
| **Approximated aerodynamics** | Dynamics don't match hardware perfectly | Control gains will differ; re-tune for real flight |
| **Different latency** | Timing-sensitive behaviors may fail in real flight | Test timing-dependent features in actual air |
| **Approximate mass/inertia** | Acceleration profiles differ | Parameter tuning ranges OK; absolute values vary |

**These are standard SITL limitations. Results are qualitative (parameter X better than Y) rather than absolute quantitative validation.**

---

## Part 8: Summary of Findings & Verification

### Verified Status: 10/10
- ✓ Step-by-step build and launch instructions verified against live execution
- ✓ Native RPLidar S2 model (`sim:rplidars2`) tested and working
- ✓ Complete OA parameter baseline verified live via MAVLink (`PRX1_TYPE=5`, `OA_TYPE=1`, `SERIAL5_BAUD=1000`)
- ✓ 1 Mbaud baudrate mapping confirmed (`AP_SerialManager::map_baudrate()`)
- ✓ 8-sector proximity database verified streaming live telemetry (`DISTANCE_SENSOR` messages)

---

## Conclusion

The SITL environment for Project Quiver natively supports the Slamtec RPLidar S2 via upstream ArduPilot master (PR #31730 merged 2025-12-16, PR #31663 merged 2026-05-26). SITL execution with Quiver's object avoidance parameters successfully populates the proximity database and streams telemetry.
