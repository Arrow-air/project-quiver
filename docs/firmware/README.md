# Quiver Firmware

This directory contains the custom ArduCopter firmware build for the Quiver dev kit, along with standard parameter configurations and documentation.

## Firmware File

**`arducopter-pixhawk6c-arrow.apj`** — flash this file onto the Pixhawk 6C.

## Custom Build

The Quiver dev kit runs a custom ArduCopter build for the **Pixhawk 6C** with the following additions over the standard release:

### RPLidar S2 Support
- Cherry-picks PR [#31663](https://github.com/ArduPilot/ardupilot/pull/31663) from the ArduPilot upstream
- Adds the RPLidar S2 as a proximity sensor option (`PRX1_TYPE = 5`)
- Reuses the existing RPLidar A2 serial protocol with an additional dense-express scan mode
- Serial config: `SERIALx_PROTOCOL = 11`, `SERIALx_BAUD = 1000` (1 Mbaud), `PRX1_TYPE = 5`

### PPP Networking (Raspberry Pi Ethernet over UART)
- Enables PPP protocol on SERIAL2 to bridge Ethernet from the Raspberry Pi
- Allows Mission Planner / MAVProxy to connect to the Pixhawk via the RPi's network interface
- Config: `SERIAL2_PROTOCOL = 48`, `SERIAL2_BAUD = 12500000` (12.5 Mbaud)

### Temperature Sensors
- Enables support for: MCP9600, MLX90614, TSYS01, TSYS03
- Useful for monitoring ESC and battery temperatures via I2C

## Flashing

1. Open **Mission Planner** → `Setup` → `Install Firmware` → `Load custom firmware`  
   **or** open **QGroundControl** → `Vehicle Setup` → `Firmware` → `Advanced settings` → `Custom firmware`
2. Select **`arducopter-pixhawk6c-arrow.apj`**
3. After flashing, do a full parameter reset, then load the parameter files below

## Parameters

See [`parameters/`](./parameters/) for:

| File | Purpose |
|------|---------|
| `standard-params.param` | **Base config** — load this first. Networking and object avoidance disabled. Per-drone calibration values stripped. |
| `params-ethernet.param` | **Add-on** — layer on top of base to enable PPP networking via SERIAL2 |
| `params-object-avoidance.param` | **Add-on** — layer on top of base to enable RPLidar S2 + object avoidance |
| `PARAMETER_NOTES.md` | Explanation of key parameters and differences from stock Pixhawk 6C |

### Loading Order

1. Load `standard-params.param` (base)
2. If using ethernet: also load `params-ethernet.param`
3. If using RPLidar: also load `params-object-avoidance.param`

> ⚠️ Parameters **not** included (must be calibrated per-drone):
> compass calibration, IMU calibration, RC calibration, baro ground pressure, PID gains, hover thrust
