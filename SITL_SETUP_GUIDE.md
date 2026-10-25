# Project Quiver SITL Setup & Obstacle Avoidance Guide

**Document Status**: Verified against live SITL execution  
**Date**: 2026-08-30  
**Target Platform**: ArduCopter SITL (Master branch `af2a1ba`)  

> **Path convention used in this document**  
> Commands below reference an `$ARDUPILOT` shell variable that points to your local ArduPilot checkout:
> ```bash
> export ARDUPILOT=/path/to/your/ardupilot/checkout
> ```
> Paths beginning with `docs/` or `bom/` are relative to the root of this repository.

---

## 1. Overview & Verification Summary

This guide documents the verified setup and execution flow for ArduPilot Software-In-The-Loop (SITL) simulation configured with Project Quiver's obstacle avoidance parameters and the native Slamtec RPLidar S2 sensor model (`sim:rplidars2`).

### Verified Baseline

The live SITL baseline configuration has been confirmed with the following parameter set:
- **`PRX1_TYPE = 5`**: RPLidar S2 proximity driver backend enabled.
- **`OA_TYPE = 1`**: BendyRuler path planning algorithm enabled.
- **`SERIAL5_BAUD = 1000`**: Configured for 1 Mbaud telemetry communication (mapped via `AP_SerialManager::map_baudrate()`).

Live execution confirms that 8-sector `DISTANCE_SENSOR` telemetry streams valid range data across all 8 cardinal/intercardinal orientations (0° to 315°), confirming the proximity database populates correctly with Quiver's object avoidance parameter set (`params-object-avoidance.param`).

### Verification Matrix

| Step / Feature | Status | Evidence / Verification Method |
| :--- | :--- | :--- |
| Upstream RPLidar S2 Driver & SITL Code | **VERIFIED** | Code present in master (`libraries/AP_Proximity/AP_Proximity_RPLidarA2.cpp`, `libraries/SITL/SIM_PS_RPLidarS2.h`) |
| ArduCopter SITL Compilation | **VERIFIED** | Binary compiled at `build/sitl/bin/arducopter` |
| SITL Launch & Driver Handshake | **VERIFIED** | Live log output: `AP: RPLidar S2 hw=6 fw=17.42` |
| Parameter File Loading | **VERIFIED** | Parameters verified live via MAVLink (`PRX1_TYPE=5`, `OA_TYPE=1`, `SERIAL5_BAUD=1000`) |
| Baud Rate Parameter Mapping | **VERIFIED** | `SERIAL5_BAUD,1000` verified to map to **1 Mbaud** via `AP_SerialManager::map_baudrate()` |
| EKF Origin Initialization | **VERIFIED** | Telemetry log output: `[STATUSTEXT] EKF3 IMU0 origin set` |
| Proximity Database Live Range Telemetry | **VERIFIED** | Live `DISTANCE_SENSOR` messages streaming numeric range data across all 8 sectors (0° to 315°) |
| In-Flight Autonomous OA Navigation | **UNVERIFIED** | Has not been tested in live flight simulation |
| Physical Airframe Integration | **UNVERIFIED** | Physical Pixhawk 6C TELEM3 connection with physical S2L hardware pending flight line testing |

---

## 2. Driver & Upstream Status Resolution

### Upstream PR Confirmation
Upstream ArduPilot natively supports both the RPLidar S2 proximity driver and the native SITL simulator model:

- **PR #31730** (*Add support for simulated RPLidarS2*) merged into upstream master on **2025-12-16** (`libraries/SITL/SIM_PS_RPLidarS2.h` & `SIM_PS_RPLidar.cpp`).
- **PR #31663** (*AP_Proximity: add RPLidar S2 support*) merged into upstream master on **2026-05-26** (`libraries/AP_Proximity/AP_Proximity_RPLidarA2.cpp`).

**Resolution**: Upstream ArduPilot master natively supports the RPLidar S2 proximity driver and SITL simulator model (`sim:rplidars2`). Separate custom driver patching or proxy models are no longer required.

### Hardware Identification Note (Open Item for Erick)
- **Repo Specification**: Quiver BOM ([bom/3000-equipment.yaml](bom/3000-equipment.yaml#L55)) specifies `RPLidar S2L` (DFRobot SKU DFR0987 / Product 2617).
- **Driver Match**: Slamtec's taxonomy designates **S2L** as the 5V TTL UART serial model of the S2 family (Model ID `0x71`). ArduPilot's `PRX1_TYPE = 5` driver detects Model `0x71` and uses the 1 Mbaud Dense Express scan protocol.
- **Open Action Item for Erick**: Confirm physical airframe hardware inventory matches DFRobot SKU DFR0987 (TTL UART version) and verify pinout for the Pixhawk 6C TELEM3 connector.

---

## 3. Baud Rate Parameter Mapping Source Analysis

In Quiver's [standard-params.param](docs/Operations/firmware/parameters/standard-params.param#L235):
```ini
SERIAL5_BAUD,1000
```

### Source Code Mapping Citation
In ArduPilot's [AP_SerialManager.cpp](libraries/AP_SerialManager/AP_SerialManager.cpp#L737-L770) (path relative to `$ARDUPILOT`):
```cpp
uint32_t AP_SerialManager::map_baudrate(int32_t rate)
{
    if (rate <= 0) {
        rate = 57;
    }
    switch (rate) {
    case 1:    return 1200;
    case 2:    return 2400;
    ...
    case 921:  return 921600;
    case 1500: return 1500000;
    case 2000: return 2000000;
    }

    if (rate > 2000) {
        return (uint32_t)rate;
    }

    // otherwise allow any other kbaud rate
    return rate*1000;
}
```
*Because `1000` is below 2000 and does not match explicit enum cases, it falls through to line 769 (`return rate * 1000;`), evaluating to **1,000,000 baud (1 Mbaud)**.*

---

## 4. Execution & Launch Instructions

### Prerequisites
- Environment: Linux / WSL2
- ArduPilot location: `$ARDUPILOT` (see path convention note at the top of this document)
- Python environment: a virtualenv with `pymavlink` installed (activate before running any `python3` commands below)

### Step 1: Build ArduCopter SITL
```bash
cd "$ARDUPILOT"
./waf configure --board sitl
./waf build --target bin/arducopter
```
*Verified output*: Binary compiled at `$ARDUPILOT/build/sitl/bin/arducopter`.

### Step 2: Launch SITL with Native RPLidar S2 Sensor Model & Quiver Parameters

Primary launch command:
```bash
../Tools/autotest/sim_vehicle.py --map --console -A "--serial5=sim:rplidars2"
```

Full launch command with Quiver parameter files and custom location:

> **Activate your Python virtualenv first**, then run:

```bash
cd "$ARDUPILOT/ArduCopter"
python3 ../Tools/autotest/sim_vehicle.py -N -v ArduCopter \
  --map --console \
  -A "-O 51.8752066,14.6487830,0,0" \
  -A "--serial5=sim:rplidars2" \
  --add-param-file=<quiver-repo>/docs/Operations/firmware/parameters/standard-params.param \
  --add-param-file=<quiver-repo>/docs/Operations/firmware/parameters/params-object-avoidance.param
```

> Replace `<quiver-repo>` with the absolute path to your local clone of this repository.

#### Verified Console Output Evidence
```text
SIM_VEHICLE: Start
SIM_VEHICLE: Adding parameters from (<quiver-repo>/docs/Operations/firmware/parameters/standard-params.param)
SIM_VEHICLE: Adding parameters from (<quiver-repo>/docs/Operations/firmware/parameters/params-object-avoidance.param)
SIM_VEHICLE: Run ArduCopter
RiTW: Starting ArduCopter : $ARDUPILOT/build/sitl/bin/arducopter --model + --speedup 1 --slave 0 -O 51.8752066,14.6487830,0,0 --serial5=sim:rplidars2 --defaults <quiver-repo>/docs/Operations/firmware/parameters/standard-params.param,<quiver-repo>/docs/Operations/firmware/parameters/params-object-avoidance.param --sim-address=127.0.0.1 -I0
Connect tcp:127.0.0.1:5760 source_system=255
STABILIZE> Mode STABILIZE
AP: Initialising ArduPilot
AP: RPLidar S2 hw=6 fw=17.42
AP: ArduPilot Ready
```

---

## 5. Proximity Database & Range Telemetry Verification

### Known Gotcha: EKF Origin Required for Proximity Data

In ArduPilot's [AP_Proximity_Backend.cpp](libraries/AP_Proximity/AP_Proximity_Backend.cpp#L97) (path relative to `$ARDUPILOT`):
```cpp
bool AP_Proximity_Backend::database_prepare_for_push(Vector3f &current_pos, Matrix3f &body_to_ned)
{
    if (!AP::ahrs().get_relative_position_NED_origin_float(current_pos)) {
        return false;
    }
    return true;
}
```

**Gotcha Details**: `AP_Proximity_Backend::database_prepare_for_push()` gates all proximity data pushes on a valid AHRS/EKF position origin. The proximity database will appear completely empty until the EKF origin is set (indicated by `[STATUSTEXT] EKF3 IMU0 origin set` in the console). This behavior is not obvious from stock ArduPilot documentation. Until the EKF origin is initialized, proximity pushes are silently discarded by the backend. In addition, setting `PRX_ALT_MIN = 0` allows ground-level testing.

### Live Telemetry Evidence Output
Once EKF origin is initialized (`EKF3 IMU0 origin set`), `DISTANCE_SENSOR` messages stream live from all 8 45° sectors of the proximity database:

```text
[STATUSTEXT] EKF3 IMU0 origin set
[STATUSTEXT] EKF3 IMU1 origin set
[DISTANCE_SENSOR] id: 10, current_distance: 630 cm, min: 5 cm, max: 5000 cm, orient: 0
[DISTANCE_SENSOR] id: 11, current_distance: 1431 cm, min: 5 cm, max: 5000 cm, orient: 1
[DISTANCE_SENSOR] id: 12, current_distance: 1167 cm, min: 5 cm, max: 5000 cm, orient: 2
[DISTANCE_SENSOR] id: 13, current_distance: 1195 cm, min: 5 cm, max: 5000 cm, orient: 3
[DISTANCE_SENSOR] id: 14, current_distance: 1260 cm, min: 5 cm, max: 5000 cm, orient: 4
[DISTANCE_SENSOR] id: 15, current_distance: 320 cm, min: 5 cm, max: 5000 cm, orient: 5
[DISTANCE_SENSOR] id: 16, current_distance: 1802 cm, min: 5 cm, max: 5000 cm, orient: 6
[DISTANCE_SENSOR] id: 17, current_distance: 689 cm, min: 5 cm, max: 5000 cm, orient: 7
```

### Proximity Sector Readings Summary

| Sector ID | Orientation Angle | Cardinal Direction | Verified Distance |
| :--- | :--- | :--- | :--- |
| **`id: 10`** | `0` | Forward (0°) | **`6.30 m`** (`630 cm`) |
| **`id: 11`** | `1` | Forward-Right (45°) | **`14.31 m`** (`1431 cm`) |
| **`id: 12`** | `2` | Right (90°) | **`11.67 m`** (`1167 cm`) |
| **`id: 13`** | `3` | Back-Right (135°) | **`11.95 m`** (`1195 cm`) |
| **`id: 14`** | `4` | Back (180°) | **`12.60 m`** (`1260 cm`) |
| **`id: 15`** | `5` | Back-Left (225°) | **`3.20 m`** (`320 cm`) |
| **`id: 16`** | `6` | Left (270°) | **`18.02 m`** (`1802 cm`) |
| **`id: 17`** | `7` | Forward-Left (315°) | **`6.89 m`** (`689 cm`) |

---

## 6. Unverified Items & Next Steps

1. **In-Flight BendyRuler Avoidance Maneuvers**: **UNVERIFIED**  
   - Testing vehicle path re-routing around obstacles during AUTO waypoint navigation in SITL remains to be executed.
2. **Physical Hardware Wiring & Flight Line Flight Testing**: **UNVERIFIED**  
   - Connecting physical RPLidar S2L sensor to Pixhawk 6C TELEM3 port on hardware flight vehicle remains pending.
