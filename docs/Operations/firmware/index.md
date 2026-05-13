---
title: Firmware & Parameters
slug: /Operations/Firmware-Parameters
sidebar_position: 2
description: Firmware files and parameter sets for configuring a Quiver Dev-Kit.
---

# Firmware & Parameters

This page collects the firmware file and parameter sets used to configure a Quiver Dev-Kit flight controller.

Use this when you are setting up or re-flashing a Quiver Dev-Kit. The supporting firmware and parameter files live alongside this page so they can be downloaded directly from the docs.

## Firmware File

| File | Description |
|------|-------------|
| [`arducopter-pixhawk6c.apj`](./arducopter-pixhawk6c.apj) | Compiled firmware — flash via Mission Planner or QGroundControl |
| [`arducopter-pixhawk6c.abin`](./arducopter-pixhawk6c.abin) | Alternate firmware artifact for compatible tooling |

## Flashing

1. Open **Mission Planner** → `Setup` → `Install Firmware` → `Load custom firmware`
   **or** open **QGroundControl** → `Vehicle Setup` → `Firmware` → `Advanced settings` → `Custom firmware`
2. Select [`arducopter-pixhawk6c.apj`](./arducopter-pixhawk6c.apj)
3. After flashing: **full parameter reset**, then load parameter files below

## Parameters

Load in order:

| File | Purpose |
|------|---------|
| [`standard-params.param`](./parameters/standard-params.param) | Base configuration — load this first on every drone |
| [`params-ethernet.param`](./parameters/params-ethernet.param) | *(optional)* Enable PPP networking via Raspberry Pi |
| [`params-object-avoidance.param`](./parameters/params-object-avoidance.param) | *(optional)* Enable RPLidar S2 obstacle avoidance |
| [`params-remoteid.param`](./parameters/params-remoteid.param) | *(optional)* Enable DroneBeacon db201 Remote ID via DroneCAN |

See [Parameter Notes](#parameter-notes) below for full parameter documentation.

> ⚠️ After loading parameters, perform compass calibration, accelerometer calibration, and RC calibration — these are drone-specific and not included in the standard file.

## Custom Build Features

This firmware adds the following on top of the standard ArduCopter release.

### RPLidar S2 Support

Cherry-picks [PR #31663](https://github.com/ArduPilot/ardupilot/pull/31663) from ArduPilot upstream.

- Adds RPLidar S2 as a proximity sensor (`PRX1_TYPE = 5`)
- Reuses the RPLidar A2 serial protocol with an additional dense-express scan mode
- Connect to SERIAL3: `SERIAL3_PROTOCOL = 11`, `SERIAL3_BAUD = 1000` (1 Mbaud)
- Enable via [`params-object-avoidance.param`](./parameters/params-object-avoidance.param) when needed

### PPP Networking (Raspberry Pi Ethernet over UART)

- Enables PPP protocol on SERIAL2 to bridge Ethernet from the Raspberry Pi
- Allows Mission Planner / MAVProxy to connect to the Pixhawk over the RPi network
- Enable via [`params-ethernet.param`](./parameters/params-ethernet.param) (disabled by default)

### Temperature Sensors

Enables support for MCP9600, MLX90614, TSYS01, and TSYS03 I2C temperature sensors.

### OpenDroneID (Remote ID)

Enables ArduPilot's OpenDroneID support (`AP_OPENDRONEID_ENABLED`) for use with the DroneBeacon db201 or any external Remote ID transponder.

- Connects via **DroneCAN** (CAN1, already configured)
- The standard Pixhawk 6C bootloader is unchanged — firmware can still be updated freely
- Enable via [`params-remoteid.param`](./parameters/params-remoteid.param) (disabled by default)

## Supporting Scripts

| File | Purpose |
|------|---------|
| [`tattu_bridge.py`](./tattu-bridge/tattu_bridge.py) | Tattu smart battery bridge helper script |

## Parameter Notes

Documentation for the Quiver standard parameter configuration and key differences from the stock Pixhawk 6C defaults.

### Parameter File Structure

| File | Purpose |
|------|---------|
| `standard-params.param` | Load first — base config with ethernet and OA disabled |
| `params-ethernet.param` | Layer on to enable PPP networking via Raspberry Pi |
| `params-object-avoidance.param` | Layer on to enable RPLidar S2 obstacle avoidance |


### CAN Bus

| Parameter | Value | Notes |
|-----------|-------|-------|
| `CAN_P1_DRIVER` | `1` | Enables CAN port 1 |
| `CAN_P1_BITRATE` | `1000000` | 1 Mbit/s — required for DroneCAN |
| `CAN_D1_PROTOCOL` | `1` | DroneCAN (formerly UAVCAN) on CAN1 |
| `CAN_D2_PROTOCOL` | `14` | Reserved for secondary CAN bus |
| `CAN_D1_UC_ESC_BM` | `15` | ESC bitmask: motors 1–4 on DroneCAN (binary 1111) |


### Ethernet / PPP Networking (params-ethernet.param)

Disabled in `standard-params.param`. Load `params-ethernet.param` to enable.

| Parameter | Value | Notes |
|-----------|-------|-------|
| `NET_ENABLE` | `1` | Enables MAVLink networking stack |
| `NET_P1_PORT` | `5760` | Standard MAVLink TCP port |
| `NET_P1_PROTOCOL` | `1` | MAVLink 1 on network port 1 |
| `SERIAL2_PROTOCOL` | `48` | PPP — bridges Ethernet from Raspberry Pi |
| `SERIAL2_BAUD` | `12500000` | 12.5 Mbaud — required for PPP throughput |

Connect Mission Planner or MAVProxy to `RPi_IP:5760` over TCP.


### RPLidar S2 (Proximity Sensor)

The proximity sensor is always configured in `standard-params.param`, but obstacle avoidance is disabled by default. Load `params-object-avoidance.param` to enable.

| Parameter | Value | Notes |
|-----------|-------|-------|
| `PRX1_TYPE` | `5` | RPLidar A2/S2 (serial) |
| `PRX1_YAW_CORR` | `180` | Corrects for cable-forward mounting orientation |
| `SERIAL3_PROTOCOL` | `11` | Lidar serial protocol |
| `SERIAL3_BAUD` | `1000` | 1 Mbaud (required for S2) |


### Motors & ESCs

Quiver uses DroneCAN ESCs. Motor outputs 1–4 are mapped via `CAN_D1_UC_ESC_BM = 15`; PWM/DShot output settings are not the primary ESC control path for the standard dev-kit configuration.

| Parameter | Value | Notes |
|-----------|-------|-------|
| `CAN_D1_UC_ESC_BM` | `15` | DroneCAN ESC bitmask for motors 1–4 |
| `MOT_SPIN_ARM` | `0.07` | Low spin on arm |
| `MOT_SPIN_MIN` | `0.1` | Minimum throttle in-flight |
| `MOT_SPIN_MAX` | `0.95` | Leaves headroom for control |
| `MOT_THST_EXPO` | `0.74` | Calibrated for T-Motor MN501S |

> ⚠️ `MOT_THST_HOVER` is auto-learned and drone-specific. Not included in standard file.


### Battery

| Parameter | Value | Notes |
|-----------|-------|-------|
| `BATT_MONITOR` | `9` | DroneCAN ESC voltage/current monitor |
| `BATT_CAPACITY` | `30000` | 30Ah — matches Tattu 30Ah pack |
| `BATT_ARM_VOLT` | `42` | Minimum voltage to arm (~3.5V/cell on 12S) |
| `MOT_BAT_VOLT_MAX` | `60.9` | Full charge (12S × 4.2V) |
| `MOT_BAT_VOLT_MIN` | `46.2` | Low threshold (12S × 3.85V) |
| `BATT_FS_LOW_ACT` | `2` | Low battery → RTL |
| `BATT_FS_CRT_ACT` | `1` | Critical battery → Land |


### GPS

| Parameter | Value | Notes |
|-----------|-------|-------|
| `GPS1_TYPE` / `GPS2_TYPE` | `9` | DroneCAN GPS (Here3+) |
| `GPS1_GNSS_MODE` | `77` | GPS + GLONASS + Galileo + BeiDou |
| `GPS2_GNSS_MODE` | `69` | GPS + GLONASS + BeiDou |


### IMU Orientation

| Parameter | Value | Notes |
|-----------|-------|-------|
| `AHRS_ORIENTATION` | `0` | Default — no rotation |

> Note: Earlier param files used `AHRS_ORIENTATION = 4` (Yaw 180°) specific to one airframe's mounting. Standard config uses `0` (default). Set per-drone if your flight controller is mounted at a different rotation.


### EKF

| Parameter | Value | Notes |
|-----------|-------|-------|
| `AHRS_EKF_TYPE` | `3` | EKF3 |
| `EK3_SRC1_POSXY` | `3` | Primary XY position: GPS |
| `EK3_SRC1_VELXY` | `3` | Primary XY velocity: GPS |
| `EK3_SRC1_VELZ` | `3` | Primary Z velocity: GPS |
| `EK3_SRC_OPTIONS` | `1` | Fuse all sources when available |


### Parameters NOT Included (Calibrate Per-Drone)

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
