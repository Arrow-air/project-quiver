# Quiver Parameter Notes

Documentation for the Quiver standard parameter configuration and key differences from the stock Pixhawk 6C defaults.

## Parameter File Structure

| File | Purpose |
|------|---------|
| `standard-params.param` | Load first — base config with ethernet and OA disabled |
| `params-ethernet.param` | Layer on to enable PPP networking via Raspberry Pi |
| `params-object-avoidance.param` | Layer on to enable RPLidar S2 obstacle avoidance |

---

## CAN Bus

| Parameter | Value | Notes |
|-----------|-------|-------|
| `CAN_P1_DRIVER` | `1` | Enables CAN port 1 |
| `CAN_P1_BITRATE` | `1000000` | 1 Mbit/s — required for DroneCAN |
| `CAN_D1_PROTOCOL` | `1` | DroneCAN (formerly UAVCAN) on CAN1 |
| `CAN_D2_PROTOCOL` | `14` | Reserved for secondary CAN bus |
| `CAN_D1_UC_ESC_BM` | `15` | ESC bitmask: motors 1–4 on DroneCAN (binary 1111) |

---

## Ethernet / PPP Networking (params-ethernet.param)

Disabled in `standard-params.param`. Load `params-ethernet.param` to enable.

| Parameter | Value | Notes |
|-----------|-------|-------|
| `NET_ENABLE` | `1` | Enables MAVLink networking stack |
| `NET_P1_PORT` | `5760` | Standard MAVLink TCP port |
| `NET_P1_PROTOCOL` | `1` | MAVLink 1 on network port 1 |
| `SERIAL2_PROTOCOL` | `48` | PPP — bridges Ethernet from Raspberry Pi |
| `SERIAL2_BAUD` | `12500000` | 12.5 Mbaud — required for PPP throughput |

Connect Mission Planner or MAVProxy to `RPi_IP:5760` over TCP.

---

## RPLidar S2 (Proximity Sensor)

The proximity sensor is always configured in `standard-params.param`, but obstacle avoidance is disabled by default. Load `params-object-avoidance.param` to enable.

| Parameter | Value | Notes |
|-----------|-------|-------|
| `PRX1_TYPE` | `5` | RPLidar A2/S2 (serial) |
| `PRX1_YAW_CORR` | `180` | Corrects for cable-forward mounting orientation |
| `SERIAL3_PROTOCOL` | `11` | Lidar serial protocol |
| `SERIAL3_BAUD` | `1000` | 1 Mbaud (required for S2) |

---

## Motors & ESCs

| Parameter | Value | Notes |
|-----------|-------|-------|
| `MOT_PWM_TYPE` | `10` | DShot600 |
| `MOT_SPIN_ARM` | `0.07` | Low spin on arm |
| `MOT_SPIN_MIN` | `0.1` | Minimum throttle in-flight |
| `MOT_SPIN_MAX` | `0.95` | Leaves headroom for control |
| `MOT_THST_EXPO` | `0.74` | Calibrated for T-Motor MN501S |

> ⚠️ `MOT_THST_HOVER` is auto-learned and drone-specific. Not included in standard file.

---

## Battery

| Parameter | Value | Notes |
|-----------|-------|-------|
| `BATT_MONITOR` | `9` | Smart battery via I2C (Tattu Plus) |
| `BATT_CAPACITY` | `30000` | 30Ah — matches Tattu 30Ah pack |
| `BATT_ARM_VOLT` | `42` | Minimum voltage to arm (~3.5V/cell on 12S) |
| `MOT_BAT_VOLT_MAX` | `60.9` | Full charge (12S × 4.2V) |
| `MOT_BAT_VOLT_MIN` | `46.2` | Low threshold (12S × 3.85V) |
| `BATT_FS_LOW_ACT` | `2` | Low battery → RTL |
| `BATT_FS_CRT_ACT` | `1` | Critical battery → Land |

---

## GPS

| Parameter | Value | Notes |
|-----------|-------|-------|
| `GPS1_TYPE` / `GPS2_TYPE` | `9` | DroneCAN GPS (Here3+) |
| `GPS1_GNSS_MODE` | `77` | GPS + GLONASS + Galileo + BeiDou |
| `GPS2_GNSS_MODE` | `69` | GPS + GLONASS + BeiDou |

---

## IMU Orientation

| Parameter | Value | Notes |
|-----------|-------|-------|
| `AHRS_ORIENTATION` | `0` | Default — no rotation |

> Note: Earlier param files used `AHRS_ORIENTATION = 4` (Yaw 180°) specific to one airframe's mounting. Standard config uses `0` (default). Set per-drone if your flight controller is mounted at a different rotation.

---

## EKF

| Parameter | Value | Notes |
|-----------|-------|-------|
| `AHRS_EKF_TYPE` | `3` | EKF3 |
| `EK3_SRC1_POSXY` | `3` | Primary XY position: GPS |
| `EK3_SRC1_VELXY` | `3` | Primary XY velocity: GPS |
| `EK3_SRC1_VELZ` | `3` | Primary Z velocity: GPS |
| `EK3_SRC_OPTIONS` | `1` | Fuse all sources when available |

---

## Parameters NOT Included (Calibrate Per-Drone)

| Parameter Group | Reason |
|-----------------|--------|
| `COMPASS_OFS_*`, `COMPASS_DIA_*`, `COMPASS_ODI_*`, `COMPASS_SCALE_*` | Compass calibration — unique per drone |
| `COMPASS_DEV_ID*`, `COMPASS_PRIO*_ID` | Hardware IDs set during calibration |
| `COMPASS_DEC` | Magnetic declination — location-specific |
| `INS_ACC*OFFS_*`, `INS_ACC*SCAL_*` | Accelerometer calibration |
| `INS_GYR*OFFS_*` | Gyro bias |
| `INS_ACC*_ID`, `INS_GYR*_ID` | Hardware IDs |
| `RC*_MIN`, `RC*_MAX`, `RC*_TRIM` | Radio calibration |
| `BARO*_GND_PRESS`, `BARO*_DEVID` | Barometer calibration |
| `MOT_THST_HOVER` | Auto-learned hover throttle |
| `ATC_RAT_*`, `ATC_ANG_*`, `ATC_ACCEL_*` | Autotune PID results |
| `AHRS_ORIENTATION` | Review if flight controller is not mounted in default orientation |
| `GPS*_CAN_NODEID` | CAN node IDs assigned on first boot |
| `STAT_*` | Flight statistics counters |
