# Project Quiver Prototypes 20-Hour Flight Test Plan  


###  Mission Objective
The multipurpose drone will carry a brush bullet dispenser and autonomously follow a predefined waypoint mission to deliver the payload (bullet) at specific coordinates. The test plan ensures system safety, flight performance, stability, and successful payload delivery.

---

## Test Plan Overview

| Phase                              | Flight Time |
|------------------------------------|-------------|
| Payload Integration & Basic Handling | 3.0 hrs     |
| PID Tuning & Stabilization           | 4.0 hrs     |
| Automated Mission & Dispensing      | 4.0 hrs     |
| Performance Envelope & Final Validation | 3.5 hrs |
| Emergency Handling & Failsafe       | 2.0 hrs     |
| **Total**                           | **20.0 hrs**|


## General Guidelines

- **Flight Controller**: Pixhawk with ArduPilot
- **Modes Used**: Stabilize, AltHold, PosHold, Loiter, Auto, RTL, Guided
- **Payload**: Brush Bullet Dispenser 
- **Logging**: Full logs including Ardupilot parameters as well as ESC and battery related ones

---

##  Phase 1: Payload Integration & Basic Handling (3.0 hours)

### Objective
Validate basic control and hover performance without the payload and with payload mounted. Observe any mechanical or control issues due to added weight.

### Pilot Instructions

- Ensure the dispenser is physically and electronically secured.
- Use conservative throttle inputs during initial hover.
- Activate the dispenser manually while on the ground before flight.

### Tests

| Test                             | Time   | Description |
|----------------------------------|--------|-------------|
| Hover Tests (Stabilize mode)     | 0.5 hr | Hover at various altitudes (1–5 m), observe drift, stability, power draw. |
| Translational Maneuvers          | 0.5 hr | Move forward/backward/left/right in AltHold. Monitor response lag. |
| Yaw Control                      | 0.5 hr | Rotate CW/CCW. Evaluate smoothness and stability with payload. |
| Manual Dispenser Activation      | 0.5 hr | Activate the dispenser while flying low. Ensure drone stability. |
| Hover + Payload Power Profile    | 0.5 hr | Log current draw during hover with full payload weight. |
| Pre-Flight Logging               | —      | Monitor `RCOUT`, `CTUN.ThO`, `BATT.Curr`, `IMU`, and vibrations. |

###  Post-Flight
- Tune `ATC_ANG_PIT_P`, `ATC_RAT_PIT_P`, etc., if instability observed.
- Inspect vibration logs (`VIBE`, `IMU`).
- Ensure secure payload mounting after each flight.

---

## Phase 2: PID Tuning & Stabilization with Payload (4.0 hours)

### Objective
Optimize stability and responsiveness using PID tuning and assess control under different flight modes with the payload.

###  Pilot Instructions

- Begin with default gains and use Autotune.
- Maintain high altitude (5–10 m) to allow recovery.
- Focus on smooth transitions and yaw precision.

###  Tests

| Test                         | Time   | Description |
|------------------------------|--------|-------------|
| Autotune - Roll & Pitch      | 1.0 hr | Use Autotune in calm conditions. Let ArduPilot adjust gains. |
| Manual Yaw PID Tuning        | 1.0 hr | Observe yaw response. Adjust `ATC_RAT_YAW_P`, `D`, `FF` as needed. |
| Autonomous Loiter & Transitions | 1.0 hr | Fly in Loiter and AltHold. Check mode switching latency and stability. |
| Emergency Maneuvers          | 1.0 hr | Try GPS loss (simulate) and RTL. Monitor failsafe smoothness. |

###  Post-Flight
- Analyze `ATT.Des*` vs `ATT.Act*` for accuracy.
- Review `RCOUT.*`, `BATT.Curr`, and `RATE.*` for responsiveness and control margin.

---

## Phase 3: Automated Waypoint Mission with Payload (4.0 hours)

### Objective
Test precise waypoint navigation and dispenser activation during autonomous missions.

###  Pilot Instructions

- Upload pre-planned waypoint mission with target coordinates.
- Include Do-Set-Servo commands for dispenser triggering.
- Ensure GPS HDOP < 1.5 before flight.

###  Tests

| Test                              | Time   | Description |
|-----------------------------------|--------|-------------|
| Full Auto Waypoint Mission        | 1.5 hr | 6–10 waypoints with altitude changes and RTL. Monitor path accuracy. |
| Dispenser Activation During Mission | 1.0 hr | Trigger payload drop at designated waypoints. Observe altitude, GPS offset. |
| Dispensing Accuracy               | 0.5 hr | Validate hit accuracy (visually or via ground markers). |
| Geofence & RTL Test               | 0.5 hr | Trigger fence breach. Confirm automatic RTL activation. |

### 🔧 Post-Flight
- Check `NAV`, `CMD`, `CTUN.DSAlt`, Dispenser Relay
- Log hit accuracy per waypoint vs GPS logs.
- Verify mission repeatability with same path.

---

## Phase 4: Performance Envelope & Final System Validation (3.5 hours)

### Objective
Test operational performance under stress: payload, speed, long range, and dispensing under flight extremes.

### Pilot Instructions

- Use Auto mode for consistent paths.
- Stay within legal altitude and range limits.
- Be ready to switch to Stabilize in case of failure.

### Tests

| Test                              | Time   | Description |
|-----------------------------------|--------|-------------|
| Max Payload Flight                | 1.0 hr | Fly at full load (bullet + dispenser). Check climb rate, power. |
| High-Speed Flight                 | 1.0 hr | Auto mode at 15–20 m/s. Monitor speed accuracy and vibration. |
| Long-Range Mission                | 1.0 hr | Max distance with multiple waypoints and RTL. Track GPS errors. |
| Final Dispenser Activation        | 0.5 hr | Drop payload at max speed and range. Ensure stability. |

###  Post-Flight
- Analyze current draw vs flight phase (`BATT`, `CTUN.ThO`).
- Assess path tracking (`POS.X`, `POS.Y`, `NAV`).
- Document hit accuracy, battery usage, temperature.

---

## Phase 5: Emergency Handling & Safety Tests (2.0 hours)

### Objective
Validate failsafe actions for GPS/RF/Battery failure while carrying a payload.

### Pilot Instructions

- Ensure logs are active before test.
- Test in open space with no GPS drift zones.
- Stay ready on transmitter to recover control manually.

### Tests

| Test                             | Time   | Description |
|----------------------------------|--------|-------------|
| GPS Loss Simulation              | 1.0 hr | Mask GPS or disconnect. Drone should switch to Land/Stabilize or return safely. |
| RC Signal Loss                   | 1.0 hr | Turn off transmitter. Ensure RTL or Land triggers. Verify it returns to Home and lands safely. |

### Post-Flight
- Check `FS_GPS`, `FS_GCS_ENABL`, `FS_THR` behavior in logs.
- Measure RTL timing and descent quality with payload.
- Log all emergency responses and recommend safety thresholds.

---

##  Notes & Deliverables

- Full flight logs (`.bin` or `.log`)
- Pilot logs and videos if available
- Dispenser test records (accuracy log)
- Tuning parameter snapshots (`.param`)
- Battery and ESC temperature records
- Dispenser system validation document
