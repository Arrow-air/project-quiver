# Quiver Parameter Notes

This document explains the most important parameter differences between the Quiver standard configuration and the default Pixhawk 6C out-of-box settings.

---

## CAN Bus

| Parameter | Value | Notes |
|-----------|-------|-------|
| `CAN_P1_DRIVER` | `1` | Enables CAN port 1 driver |
| `CAN_P1_BITRATE` | `1000000` | 1 Mbit/s — required for DroneCAN |
| `CAN_D1_PROTOCOL` | `1` | DroneCAN (formerly UAVCAN) on CAN1 |
| `CAN_D2_PROTOCOL` | `14` | Reserved for secondary CAN bus use |

DroneCAN is used for the GPS modules (Here3+) and ESCs. The GPS units are assigned node IDs 124 and 125 (`GPS1_CAN_NODEID = 124`, `GPS2_CAN_NODEID = 125`).

---

## Ethernet / Networking (PPP over UART)

| Parameter | Value | Notes |
|-----------|-------|-------|
| `NET_ENABLE` | `0` (base) / `1` (ethernet) | Enables MAVLink networking stack |
| `NET_P1_PORT` | `5760` | Standard MAVLink TCP port |
| `NET_P1_PROTOCOL` | `1` | MAVLink 1 on network port 1 |
| `SERIAL2_PROTOCOL` | `48` | PPP — bridges Ethernet from Raspberry Pi |
| `SERIAL2_BAUD` | `12500000` | 12.5 Mbaud — required for PPP throughput |

The PPP link connects the Pixhawk to the Raspberry Pi's network stack. This allows Mission Planner or MAVProxy to connect to the Pixhawk via the RPi's IP address on port 5760, without needing a separate telemetry radio.

---

## RPLidar S2 (Proximity Sensor)

| Parameter | Value | Notes |
|-----------|-------|-------|
| `PRX1_TYPE` | `5` | RPLidar A2/S2 (serial) |
| `PRX1_YAW_CORR` | `180` | Rotates scan to match drone forward direction |
| `SERIAL3_PROTOCOL` | `11` | Lidar serial protocol |
| `SERIAL3_BAUD` | `1000` | 1 Mbaud for S2 |

Used for obstacle avoidance. The S2 connects to SERIAL3 on the Pixhawk 6C. The `PRX1_YAW_CORR = 180` corrects for the physical mounting orientation (cable pointing forward).

---

## Motors & ESCs

| Parameter | Value | Notes |
|-----------|-------|-------|
| `MOT_PWM_TYPE` | `10` | DShot600 |
| `MOT_PWM_MIN` | `1050` | Minimum motor command |
| `MOT_PWM_MAX` | `1950` | Maximum motor command |
| `MOT_SPIN_ARM` | `0.07` | Low spin on arm — drone twitches slightly when armed |
| `MOT_SPIN_MIN` | `0.1` | Minimum throttle to keep motors spinning in flight |
| `MOT_SPIN_MAX` | `0.95` | Leave headroom for control authority |
| `MOT_THST_EXPO` | `0.74` | Motor thrust curve — calibrated for T-Motor MN501S |
| `CAN_D1_UC_ESC_BM` | `15` | ESC bitmask: motors 1–4 on DroneCAN (binary 1111) |

> ⚠️ `MOT_THST_HOVER` is drone-specific (auto-learned). Do not copy this value between drones.

---

## Battery

| Parameter | Value | Notes |
|-----------|-------|-------|
| `BATT_MONITOR` | `9` | Smart battery via I2C (Tattu Plus) |
| `BATT_CAPACITY` | `30000` | 30Ah — matches Tattu 30Ah pack |
| `BATT_ARM_VOLT` | `42` | Minimum voltage to arm (~3.5V/cell on 12S) |
| `MOT_BAT_VOLT_MAX` | `60.9` | Full charge voltage (12S @ 4.2V/cell) |
| `MOT_BAT_VOLT_MIN` | `46.2` | Minimum cell voltage threshold (12S @ 3.85V/cell) |
| `BATT_FS_LOW_ACT` | `2` | Low battery → RTL |
| `BATT_FS_CRT_ACT` | `1` | Critical battery → Land immediately |

---

## GPS

| Parameter | Value | Notes |
|-----------|-------|-------|
| `GPS1_TYPE` / `GPS2_TYPE` | `9` | DroneCAN GPS (Here3+) |
| `GPS1_GNSS_MODE` | `77` | GPS + GLONASS + Galileo + BeiDou |
| `GPS2_GNSS_MODE` | `69` | GPS + GLONASS + BeiDou |
| `AHRS_ORIENTATION` | `4` | Pixhawk rotated 180° yaw in enclosure |

---

## EKF & Attitude

| Parameter | Value | Notes |
|-----------|-------|-------|
| `AHRS_EKF_TYPE` | `3` | EKF3 (recommended) |
| `EK3_SRC1_POSXY` | `3` | Primary XY position source: GPS |
| `EK3_SRC1_VELXY` | `3` | Primary XY velocity source: GPS |
| `EK3_SRC1_VELZ` | `3` | Primary Z velocity source: GPS |
| `EK3_SRC_OPTIONS` | `1` | Fuse all sources when available |

---

## Obstacle Avoidance

| Parameter | Value | Notes |
|-----------|-------|-------|
| `AVOID_ENABLE` | `3` | Obstacle avoidance enabled (stop + slide) |
| `AVOID_DIST_MAX` | `5` | Start slowing at 5m from obstacle |
| `AVOID_MARGIN` | `4` | Hard stop at 4m |
| `OA_TYPE` | `1` | BendyRuler path planning |
| `OA_BR_LOOKAHEAD` | `12` | Look 12m ahead for obstacles |

---

## Parameters to Set Per-Drone (Not in Standard File)

The following **must be calibrated individually** and are not included in `standard-params.param`:

| Parameter Group | Why it's drone-specific |
|-----------------|------------------------|
| `COMPASS_OFS_*`, `COMPASS_DIA_*`, `COMPASS_ODI_*`, `COMPASS_SCALE_*` | Compass calibration — unique to each drone's magnetic environment |
| `COMPASS_DEV_ID*`, `COMPASS_PRIO*_ID` | Hardware IDs assigned during calibration |
| `COMPASS_DEC` | Magnetic declination — location-specific |
| `INS_ACC*OFFS_*`, `INS_ACC*SCAL_*` | Accelerometer calibration |
| `INS_GYR*OFFS_*` | Gyro bias compensation |
| `INS_ACC*_ID`, `INS_GYR*_ID` | Hardware IDs |
| `INS_*CALTEMP` | Temperature calibration reference points |
| `RC*_MIN`, `RC*_MAX`, `RC*_TRIM` | Radio calibration |
| `BARO*_GND_PRESS` | Ground pressure at calibration site |
| `BARO*_DEVID` | Hardware IDs |
| `MOT_THST_HOVER` | Auto-learned hover throttle — varies with payload |
| `ATC_RAT_*`, `ATC_ANG_*`, `ATC_ACCEL_*` | Autotune PID results — vary between airframes |
| `STAT_*` | Flight statistics — per-drone counters |
| `GPS*_CAN_NODEID` | CAN node IDs assigned during first boot |
