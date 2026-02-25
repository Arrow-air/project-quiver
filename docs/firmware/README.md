# Quiver Firmware

This directory contains the custom ArduCopter firmware build for the Quiver dev kit, along with standard parameter configurations and documentation.

## Custom Build

The Quiver dev kit runs a custom ArduCopter build for the **Pixhawk 6C** with the following additions over the standard release:

### RPLidar S2 Support
- Cherry-picks PR [#31663](https://github.com/ArduPilot/ardupilot/pull/31663) from the ArduPilot upstream
- Adds the `RPLidar S2` as a proximity sensor option (`PRX1_TYPE = 5`)
- Reuses the existing RPLidar A2 serial protocol with an additional dense-express scan mode
- Serial config: `SERIAL3_PROTOCOL = 11`, `SERIAL3_BAUD = 1000` (1 Mbaud), `PRX1_TYPE = 5`

### PPP Networking (Raspberry Pi Ethernet over UART)
- Enables `PPP` protocol on SERIAL2 to bridge Ethernet from the Raspberry Pi
- Allows Mission Planner / MAVProxy to connect to the Pixhawk via the RPi's network interface
- Serial config: `SERIAL2_PROTOCOL = 48`, `SERIAL2_BAUD = 12500000` (12.5 Mbaud)

### Temperature Sensors
- Enables support for: MCP9600, MLX90614, TSYS01, TSYS03
- Useful for monitoring ESC and battery temperatures via I2C

### DroneCAN / CAN Bus
- CAN port 1 configured for DroneCAN (GPS, ESCs)
- CAN port 2 configured for protocol 14 (reserved/alternate)

## Flashing

1. Download the `.apj` firmware file from the [releases](../../releases) or request a build from the Arrow team
2. Open **Mission Planner** → `Setup` → `Install Firmware` → `Load custom firmware`  
   **or** open **QGroundControl** → `Vehicle Setup` → `Firmware` → `Advanced settings` → `Custom firmware`
3. Select the `.apj` file and follow the prompts

> ⚠️ After flashing, always do a full parameter reset and re-load the standard parameter file before flying.

## Parameters

See [`parameters/`](./parameters/) for:
- `standard-params.param` — standard Quiver parameter set (load after firmware flash)
- `PARAMETER_NOTES.md` — explanation of key parameters and differences from stock Pixhawk 6C defaults
