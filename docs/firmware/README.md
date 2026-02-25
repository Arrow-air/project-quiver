# Quiver Firmware

Custom ArduCopter build for the Quiver dev kit (Pixhawk 6C).

## Custom Build Features

This firmware adds the following on top of the standard ArduCopter release:

### RPLidar S2 Support
Cherry-picks [PR #31663](https://github.com/ArduPilot/ardupilot/pull/31663) from ArduPilot upstream.
- Adds RPLidar S2 as a proximity sensor (`PRX1_TYPE = 5`)
- Reuses the RPLidar A2 serial protocol with an additional dense-express scan mode
- Connect to SERIAL3: `SERIAL3_PROTOCOL = 11`, `SERIAL3_BAUD = 1000` (1 Mbaud)

### PPP Networking (Raspberry Pi Ethernet over UART)
- Enables PPP protocol on SERIAL2 to bridge Ethernet from the Raspberry Pi
- Allows Mission Planner / MAVProxy to connect to the Pixhawk over the RPi network
- Enable via `parameters/params-ethernet.param` (disabled by default)

### Temperature Sensors
Enables support for: MCP9600, MLX90614, TSYS01, TSYS03 (I2C).

## Firmware File

| File | Description |
|------|-------------|
| `arducopter-pixhawk6c.apj` | Compiled firmware — flash via Mission Planner or QGroundControl |

## Flashing

1. Open **Mission Planner** → `Setup` → `Install Firmware` → `Load custom firmware`  
   **or** open **QGroundControl** → `Vehicle Setup` → `Firmware` → `Advanced settings` → `Custom firmware`
2. Select `arducopter-pixhawk6c.apj`
3. After flashing: **full parameter reset**, then load parameter files below

## Parameters

Load in order:

| File | Purpose |
|------|---------|
| `parameters/standard-params.param` | Base configuration — load this first on every drone |
| `parameters/params-ethernet.param` | *(optional)* Enable PPP networking via Raspberry Pi |
| `parameters/params-object-avoidance.param` | *(optional)* Enable RPLidar S2 obstacle avoidance |

See [`parameters/PARAMETER_NOTES.md`](./parameters/PARAMETER_NOTES.md) for full documentation.

> ⚠️ After loading parameters, perform compass calibration, accelerometer calibration, and RC calibration — these are drone-specific and not included in the standard file.
