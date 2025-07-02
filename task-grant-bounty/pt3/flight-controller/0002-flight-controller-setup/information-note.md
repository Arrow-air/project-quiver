# Status  

`Valid`

# Project Description

This project involves the development of a high-performance multicopter platform utilizing the Holybro Pix32 V6 flight controller. The vehicle is designed for advanced autonomous operations with precise altitude control, accurate positioning, and real-time telemetry. It integrates DroneCAN-based ESCs, RTK-capable GPS modules, a radar altimeter, and a long-range LiDAR for optimal performance in outdoor and semi-structured environments. The architecture emphasizes redundancy, modular communication, and tunable flight behavior using the ArduPilot open-source firmware.

The aim is to ensure seamless interoperability between all components, robust logging and diagnostics, and a configuration that can serve both development and production environments with minimal modification.


# Methodology

The integration process followed a structured and iterative approach to ensure hardware compatibility, optimal firmware configuration, and field readiness:

### 1. Component Selection & Compatibility Mapping

- Selected components were verified to support ArduPilot 4.4+ firmware and interface via either CAN** or UART.
- All components were checked for update rate, operating voltage, supported parameters, and physical connector types.
- Pix32 V6 port mapping was referenced to ensure optimal allocation of UART and CAN peripherals.

### 2. Firmware & Initial Setup

- The Pix32 V6 flight controller was flashed with the latest ArduCopter firmware under Pixhawk6x category (compatible with Pix32 V6).
- USB connection was used for initial setup, followed by full power-up using the main power module to avoid low voltage on peripherals.
- All required peripherals were connected (ESCs, GPS modules, LiDAR, radar) using verified wiring for JST-GH and CAN connectors.

### 3. CAN and Serial Configuration

- **CAN1** and **CAN2** ports were activated using:
  - `CAN_P1_DRIVER = 1`
  - `CAN_P2_DRIVER = 1`
  - `CAN_D1_PROTOCOL = 1` (DroneCAN for ESCs, GPS, radar, etc.)
- Unique **DroneCAN Node IDs** and baud rates were assigned where needed.
- **Serial ports** were enabled and configured with:
  - Correct `SERIALx_PROTOCOL`, `SERIALx_BAUD`
  - Rangefinder and RTK telemetry settings based on manufacturer recommendations

### 4. Parameter Configuration by Component

Each component was configured in detail:
- **ESCs (Hobbywing X6 Plus)**:
  - CAN communication enabled, ESC ID set via DroneCAN GUI
  - `CAN_D1_UC_ESC_BM = 15`, `CAN_D1_UC_OPTION = 128`
  - Telemetry for RPM, current, temperature validated
- **GPS (Holybro F9P Rover + secondary)**:
  - RTK and GPS blending configured
  - `GPS_AUTO_SWITCH = 2`, `GPS_BLEND_MASK = 7`, `GPS1_TYPE = 9`
  - Survey-in setup on base module through Mission Planner
- **Radar Altimeter (Ainstein US-D1)**:
  - Configured via CAN or Serial (depending on version)
  - `RNGFND1_TYPE = 33`, `RNGFND1_MAX = 45`, `RNGFND1_GNDCLR` tuned based on mounting
- **LiDAR (Benewake TF03)**:
  - Serial setup on `SERIAL4`
  - `RNGFND2_TYPE = 27`, `RNGFND2_MAX = 35`, `RNGFND2_GNDCLR` measured

### 5. System Calibration & Testing

- Compass orientation corrected via `COMPASS_ORIENT` and external compass prioritized
- ESC function and direction verified via Mission Planner Motor Test
- Rangefinder values checked via Mission Planner “Status” tab
- GPS signal confirmed via RTK FIX and RTCM data injection monitoring
- Logs reviewed to confirm all sensor data is present and properly timestamped

### 6. Redundancy & Fail-Safe Planning

- Dual GPS blending used for positioning robustness
- Both radar and LiDAR configured for rangefinding fallback
- Battery voltage and current monitoring calibrated using `BATT_*` parameters
- Fail-safe behaviors (e.g. RTL, Land) configured based on GNSS and altitude sensor status

### 7. Documentation and Verification

- All parameter settings exported and stored for reproducibility
- Reference links embedded for each component’s ArduPilot setup documentation
- A summary “quick setup table” created for field engineers

# Results and Deliverables


## Hobbywing DroneCAN ESC Integration Details

Hobbywing ESCs with CAN interfaces support DroneCAN. This allows the autopilot to control the ESC/motor via CAN and also retrieve RPM, voltage, current, and temperature per motor.


###  Connection and Configuration

- Connect ESCs (using 4-pin I2C splitter if needed) to **CAN1** port.
- **Wire Note**: `CAN_H` wire color may vary between **red** and **gray** depending on model.

#### Required Parameters:

```ini
CAN_P1_DRIVER      = 1        ; First CAN driver
CAN_D1_PROTOCOL    = 1        ; DroneCAN
CAN_D1_UC_ESC_BM   = 15       ; Send outputs 1-4 over CAN
CAN_D1_UC_OPTION   = 128      ; Check 'Hobbywing ESC' manually or set value
```

---

###  Configuring ESCs

By default, ESCs are set to:
- **Baudrate**: 500,000 (incorrect)
- **Node IDs**: All set to 1 (conflict)

#### To test ESCs before reconfiguration:
1. Disconnect all other DroneCAN devices from CAN1
2. Set:
   ```ini
   CAN_P1_BITRATE = 500000
   ```
3. Reboot autopilot and power ESCs
4. Motors should stop beeping
5. Go to **Mission Planner → Setup → Motor Test** and test motor spin

#### Permanent configuration steps:
1. Keep `CAN_P1_BITRATE = 500000`
2. Download [DroneCAN GUI Tool (v1.2.25+)](https://github.com/dronecan/gui_tool/releases)
3. Determine **SLCAN or MAVLink COM port**
4. Open DroneCAN GUI and connect to port
5. Set `Local Node ID`, open **Panels → Hobbywing ESC Panel**
6. For each ESC:
   - Set **Baudrate** to `1,000,000`
   - Set **ThrottleID** and **NodeID** to motor number (1–4)
   - Optionally:  
     - `Msg1Rate` (RPM)  
     - `Msg2Rate` (voltage/current/temp)

7. Repeat for each ESC
8. Set:
   ```ini
   CAN_P1_BITRATE = 1000000
   ```

---

###  Testing and Telemetry

Once setup:
- ESCs report **RPM**, **voltage**, **current**, and **temperature**
- Data available in:
  - **Mission Planner → Status tab**
  - **Onboard logs (BIN files)**
- Perform motor spin test using **Motor Test** in Mission Planner

For full documentation:  
[ArduPilot Hobbywing ESC Setup](https://ardupilot.org/copter/docs/common-dronecan-hobbywing-esc.html)


---

## Ainstein US-D1 Radar Altimeter Integration

The **Ainstein US-D1** is a compact, high-precision radar altimeter with the following specs:

- **Range**: up to 50 meters
- **Update Rate**: 100 Hz
- **Weight**: 110g

> 📄 [Ainstein US-D1 Manual](https://ainstein.ai/product/us-d1/)

---

###  Connecting to Autopilot

The US-D1 is available in two versions: **Serial** and **CAN**.

---

###  Serial Version (example using SERIAL4)

```ini
SERIAL4_PROTOCOL = 9         ; Rangefinder (Lidar)
SERIAL4_BAUD     = 115       ; 115200 baud
RNGFND1_TYPE     = 11        ; USD1 Serial
RNGFND1_MIN      = 0.5       ; Minimum range in meters
RNGFND1_MAX      = 45        ; Maximum range in meters
RNGFND1_GNDCLR   = 0.1       ; Distance from sensor to ground when landed
```

---

###  CAN Version

```ini
CAN_P1_DRIVER    = 1         ; Enable CAN1
CAN_D1_PROTOCOL  = 7         ; USD1 Protocol
RNGFND1_TYPE     = 33        ; USD1_CAN
RNGFND1_MIN      = 0.5
RNGFND1_MAX      = 45
RNGFND1_GNDCLR   = 0.1
```

---

###  Testing the Sensor

- View output via **Mission Planner → Status tab**
- Look for field: `rangefinder1`

---

###  Using with AP_Periph CAN Node

If your flight controller lacks an available UART or CAN port, the **Serial version** of USD1 can be used with an **AP_Periph CAN Node** (e.g., Matek L431).

1. Flash the AP_Periph with firmware supporting rangefinders.
2. Connect USD1 Serial to UART2 (TX2/RX2) of the node.
3. On AP_Periph, set:

```ini
RNGFND_BAUDRATE = 115
RNGFND_MAX_RATE = 50
RNGFND_PORT     = 1      ; UART2 (TX2, RX2)
RNGFND1_TYPE    = 11
RNGFND1_ORIENT  = 0
```

> 🔧 RNGFND_PORT = 0 → RX1/TX1  
> RNGFND_PORT = 1 → RX2/TX2

4. On autopilot:

```ini
RNGFND1_TYPE    = 24     ; DroneCAN
RNGFND1_ORIENT  = 25     ; Downward
RNGFND1_ADDR    = 0      ; For sensor_id 0
```

Check `CAN Inspector` in Mission Planner for:

```
uavcan_equipment_range_sensor_Measurement
```

Use this to verify `sensor_id`.

---

For more:  
[Ainstein US-D1 Product Page](https://ainstein.ai/product/us-d1/)  
[ArduPilot USD1 Integration](https://ardupilot.org/copter/docs/common-ainstein-usd1.html)


---

## Benewake TF03 LiDAR Integration

The **Benewake TF03** is a robust time-of-flight LiDAR sensor capable of operating in outdoor conditions with long-range measurements. It is suitable for terrain following, obstacle detection, and precision landing applications.

###  Specifications

- **Range**: 50–180 meters (depending on surface reflectivity)
- **Update Rate**: 100 Hz
- **Weight**: 77 g
- **Interface**: UART (default), can be configured for CAN

>  [Benewake Downloads](https://www.benewake.com/en/download)  
>  Other models: TF02 (20–40m), TF-Luna (3–8m), also supported

---

###  Connecting to Autopilot (UART Mode)

The TF03 can be connected to any free UART (e.g., SERIAL4 or SERIAL5).

#### Example (using SERIAL5):

```ini
SERIAL5_PROTOCOL = 9
SERIAL5_BAUD     = 115
RNGFND1_TYPE     = 27       ; Benewake TF03
RNGFND1_MIN      = 0.1
RNGFND1_MAX      = 180      ; adjust based on environment
RNGFND1_GNDCLR   = 0.1      ; sensor height from ground when landed
RNGFND1_ORIENT   = 25       ; downward
```

>  **Note**: UART TX/RX wires may be color-coded differently — refer to manufacturer’s datasheet

---

###  Using TF03 with DroneCAN

TF03 supports **CAN mode** if configured via Benewake’s configuration tool.

#### CAN Setup Parameters:

```ini
RNGFND1_TYPE     = 34       ; Benewake DroneCAN
CAN_P1_DRIVER    = 1
CAN_D1_PROTOCOL  = 1
RNGFND1_MIN      = 0.1
RNGFND1_MAX      = 180
RNGFND1_ORIENT   = 25
```

Follow DroneCAN setup instructions after flashing the correct firmware and verifying node IDs.

---

###  Sensor Testing

To verify the TF03 is working:
- Open **Mission Planner → Flight Data → Status tab**
- Look for: `rangefinder1`
- Move object in front of sensor and check if distance changes

---

For more:  
[ArduPilot Benewake Integration](https://ardupilot.org/copter/docs/common-benewake-tfmini.html)


---

##  Recommended Configuration Summary

This section summarizes the best practices and optimal port/protocol configuration for all components used in the multicopter build. Decisions are based on interface stability, bandwidth, compatibility with ArduPilot, and ease of integration.

| Component               | Interface | Port (Pix32 V6)     | Protocol / Type       | Baud Rate / Notes                          |
|------------------------|-----------|---------------------|------------------------|---------------------------------------------|
| **Hobbywing X6 Plus**  | CAN       | CAN1                | DroneCAN ESC (UC)     | 1,000,000 bps (requires configuration)     |
| **Holybro H-RTK F9P**  | CAN       | CAN1                | DroneCAN GPS + Compass| Auto-config (GPS_TYPE = 9)                 |
| **Mateksys M9N-G4-3100** | UART     | SERIAL4 (GPS2/UART8)| NMEA GPS              | 115200 bps                                 |
| **Ainstein US-D1**     | CAN       | CAN1                | USD1_CAN              | Use CAN_D1_PROTOCOL = 7                    |
| **Benewake TF03**      | UART      | SERIAL5 (Telem3)    | TF03 UART             | 115200 bps – stable & avoids CAN bus load  |
| **RC Receiver (CRSF)** | UART      | SERIAL6 (USER/UART3)| RCIN                  | 420000-115200 bps (usually 115200 default) |

> ⚙️ **Why this configuration?**
> - CAN1 is used for all DroneCAN devices (ESC + GPS + US-D1), keeping them on a dedicated, high-speed bus.
> - TF03 remains on UART to reduce CAN bus congestion and avoid node ID conflicts.
> - M9N GPS provides redundancy via UART without competing for CAN bandwidth.
> - CRSF or FPort receivers require a true UART and work reliably on SERIAL6.

---

## Updated Parameter Set

### General CAN & Serial Setup

```ini
CAN_P1_DRIVER      = 1
CAN_D1_PROTOCOL    = 1        ; For DroneCAN ESC & GPS
CAN_D1_UC_ESC_BM   = 15       ; Outputs 1–4 to CAN
CAN_D1_UC_OPTION   = 128      ; Hobbywing ESC

SERIAL4_PROTOCOL   = 5        ; GPS (Mateksys)
SERIAL4_BAUD       = 115200

SERIAL5_PROTOCOL   = 9        ; Rangefinder (TF03 UART)
SERIAL5_BAUD       = 115200

SERIAL6_PROTOCOL   = 23       ; RC input (CRSF)
SERIAL6_OPTIONS    = 0

SERIAL7_PROTOCOL   = 10       ; SLCAN diagnostics (optional)
```

### GPS Configuration

```ini
GPS_TYPE           = 9        ; DroneCAN (F9P)
GPS_TYPE2          = 1        ; UART (M9N)
GPS_AUTO_CONFIG    = 1
GPS_AUTO_SWITCH    = 1
```

### Rangefinder Configuration

```ini
RNGFND1_TYPE       = 33       ; Ainstein US-D1 CAN
RNGFND1_MIN        = 0.5
RNGFND1_MAX        = 45
RNGFND1_GNDCLR     = 0.1
RNGFND1_ORIENT     = 25

RNGFND2_TYPE       = 27       ; Benewake TF03 UART
RNGFND2_MIN        = 0.1
RNGFND2_MAX        = 180
RNGFND2_GNDCLR     = 0.1
RNGFND2_ORIENT     = 25
```

### EKF3 Height Source

```ini
EK3_SRC1_POSZ      = 2        ; Rangefinder
EK3_RNG_USE_HGT    = 70
EK3_ALT_SOURCE     = 0        ; Baro default
```

### Compass Setup

```ini
COMPASS_USE        = 0        ; Disable internal
COMPASS_USE2       = 1        ; Enable external
COMPASS_AUTO_ROT   = 2
```

---

This configuration prioritizes clean bus separation, reduces cross-talk, and ensures high-priority rangefinders and GPS units are given the bandwidth they need.


---

## H-RTK F9P (RTK GPS) Integration & Best Practices

The **Holybro H-RTK F9P** provides centimeter-level accuracy using **RTK (Real Time Kinematic)** positioning. It requires two GPS modules: a **rover (on the UAV)** and a **base station** for correction data. RTK significantly improves GPS accuracy.

###  Recommended Setup Overview

| Module         | Interface | Port (Pix32 V6)     | Type      | Baud Rate / Notes |
|----------------|-----------|---------------------|-----------|--------------------|
| H-RTK Rover    | CAN       | CAN1                | DroneCAN  | Auto Baud, GPS_TYPE = 9 |
| H-RTK Base     | UART      | via Telemetry Radio | RTCM Out  | 57600 or 115200 typical |

> Use **Holybro SiK Telemetry Radio v3** or any MAVLink-compatible telemetry set.

---

###  Best Configuration

#### Parameters for Rover (DroneCAN version):

```ini
CAN_P1_DRIVER     = 1
CAN_D1_PROTOCOL   = 1
GPS_TYPE          = 9       ; DroneCAN
NTF_LED_TYPES     = 231     ; Enable DroneCAN LED status
COMPASS_USE2      = 1
COMPASS_AUTO_ROT  = 2
```

> If using two GPSs, use:
```ini
GPS_TYPE2         = 1       ; Secondary GPS (UART)
GPS_AUTO_SWITCH   = 2       ; Use blending
GPS_BLEND_MASK    = 7       ; Blend horizontal, vertical, and speed
```

#### Disable safety switch if no external switch is present:
```ini
BRD_SAFETY_DEFLT  = 0
```

---

###  RTK Base Station Setup in Mission Planner

1. Open **Mission Planner → Setup → RTK/GPS Inject**
2. Choose correct COM port and connect
3. Enter `SurveyIn Acc` = 2 (meters or better)
4. Enter `Survey Time` = 60 seconds or more
5. Click **Restart** to begin surveying

**Survey Status:**
- *In Progress*: Surveying ongoing
- *Position is valid*: Survey complete
- *Use FixedLLA*: Store current position as fixed base location

> After survey, click “Save Current Pos”, name it, and click “Use” next time for instant setup.

---

###  RTK Status Indicators

- **RTK Float**: Intermediate accuracy (centimeter-level with correction)
- **RTK Fixed**: Best accuracy (millimeter-level)
- **Orange LED on F9P**:
  - *Blinking*: Receiving RTCM data
  - *Solid*: RTK Fixed solution achieved

---

###  F9P Internal Configuration via DroneCAN

1. Go to **Mission Planner → Setup → Optional Hardware → DroneCAN**
2. Click **MAVLink CAN1** to query node
3. Select **Menu → Parameters**
4. Modify internal F9P parameters as needed
5. Click **Commit Params** to save

---

###  Compass Setup (F9P with IST8310)

If compass calibration fails:
```ini
COMPASS_ORIENT = 6  ; Yaw270 (orientation fix for IST8310)
```

> Calibrate compass via **Setup → Mandatory Hardware → Compass**, set external GPS compass as priority = 1

---

### Notes

- Make sure **autopilot is powered by a power module**, not USB-only, during setup.
- **Firmware**: Use **ArduCopter 4.1.5+** to allow auto node ID allocation for multiple CAN GPS units
- **Multiple aircraft using same base station** must use consistent RTCM protocol/rates


# References

- [Hobbywing DroneCAN ESC Setup — ArduPilot Documentation](https://ardupilot.org/copter/docs/common-hobbywing-dronecan-esc.html)
- [Ainstein US-D1 Radar Altimeter Setup — ArduPilot Documentation](https://ardupilot.org/copter/docs/common-aerotenna-usd1.html)
- [Benewake TF02/TF03 LiDAR Setup — ArduPilot Documentation](https://ardupilot.org/copter/docs/common-benewake-tf02-lidar.html)
- [Holybro H-RTK F9P GPS Setup — Holybro Documentation](https://docs.holybro.com/gps-and-rtk-system/zed-f9p-h-rtk-series/setup-and-getting-started-ardupilot)

- [Holybro H-RTK F9P Product](https://www.holybro.com/product/h-rtk-f9p-rover/)
- [ArduPilot RTK Inject Guide](https://ardupilot.org/copter/docs/common-gps-inject.html)
- [ArduPilot GPS Blending](https://ardupilot.org/copter/docs/common-dual-gps.html)
- [ArduPilot Moving Baseline (Yaw)](https://ardupilot.org/copter/docs/common-gps-for-yaw.html)
