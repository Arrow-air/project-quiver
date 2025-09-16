# Obstacle Avoidance Proximity Sensors (LiDAR + Radar)

# Status

`Valid`

`Revision History: v1`

`Replacement Log: None`


# Project Description

## **Purpose** 
Choose and integrate a **top-mounted 360° LiDAR** and a **forward mmWave radar** for Quiver PT3/PT4 (chassis-integrated; side/belly payload mounts remain free).

## **Decision** 
Proceed with **Slamtec RPLIDAR S2L** (top) + **Nanoradar MR82** (forward). **Integration order for MR82:** attempt **direct CAN** with ArduPilot first; only if that’s unviable, use a **companion-computer MAVLink bridge**.

# Methodology

## Shortlist — Direct-to-ArduPilot LiDARs

| Model                                     | FOV    |     Range | Mass (approx) | Typical price | ArduPilot integration               |
| ----------------------------------------- | ------ | --------: | ------------: | ------------: | ----------------------------------- |
| **LightWare SF45/B**                      | \~320° |  0.2–50 m |        \~59 g |         \$449 | Direct (serial; driver)             |
| **Slamtec RPLIDAR S Series** *(e.g., S1)* | 360°   |   to 40 m |       \~100 g |         \$649 | Direct (USB/UART; driver)           |
| **Slamtec RPLIDAR A Series**              | 360°   |   to 25 m |       \~190 g |   \$599–\$645 | Direct (USB/UART; note baud)        |
| **Slamtec RPLIDAR C1**                    | 360°   |   to 12 m |       \~110 g |          \$69 | Direct (UART 460800; Lidar360)      |
| **LightWare SF40/C (EOL)**                | 360°   | 0.2–100 m |       \~258 g |   \$639–\$799 | Direct (serial; driver)             |
| **Slamtec RPLIDAR S2L** *(selected)*      | 360°   | 0.05–18 m |       \~190 g |     **\$299** | **Direct** (UART **1 M**; Lidar360) |

## Shortlist — LiDARs via Companion → MAVLink

| Model                 | FOV     |     Range | Mass (approx) | Typical price | ArduPilot integration              |
| --------------------- | ------- | --------: | ------------: | ------------: | ---------------------------------- |
| **Benewake CE30-C/D** | 132°×9° |     \~4 m |       \~230 g |         \$839 | Companion → `OBSTACLE_DISTANCE_3D` |
| **YDLIDAR G6**        | 360°    | 0.12–16 m |       \~160 g |       €374.40 | Companion → `DISTANCE_SENSOR`      |
| **Hokuyo UST-10LX**   | 270°    |   to 10 m |       \~130 g |     \~\$1,200 | Companion (Ethernet → MAVLink)     |

## Shortlist — mmWave Obstacle-Detection Radars

| Model                           | Band      | Range (typ)     | FoV (approx)  | I/O          | Mass         | ArduPilot integration                          |
| ------------------------------- | --------- | --------------- | ------------- | ------------ | ------------ | ---------------------------------------------- |
| **TI IWR6843AOPEVM** (AoP)      | 60–64 GHz | short–mid       | wide (AoP)    | USB/UART     | EVM-class    | Companion → `OBSTACLE_DISTANCE(_3D)`           |
| **TI AWR1843AOP**    | 76–81 GHz | mid–long        | wide (AoP)    | SPI/UART/CAN | module-class | Companion → `OBSTACLE_DISTANCE(_3D)`           |
| **Nanoradar MR82** | 77–80 GHz | **0.2–40/80 m** | dual-beam fan | **UART/CAN** | **\~92 g**   | **Direct (CAN)** attempt first; else Companion |
| **InnoSenT IMD-2000**           | 24 GHz    | to \~50 m       | \~98°×48°     | UART         | 25×20×12 mm  | Companion → `OBSTACLE_DISTANCE(_3D)`           |
| **Nanoradar MR72**     | 77 GHz    | 0.2–80 m        | fan beams     | **CAN**      | module-class | **Direct (CAN)** on Copter 4.5+                |


# Results and Deliverables

## Selected PT3/4 Configuration

### Top (chassis, under radome): **Slamtec RPLIDAR S2L**

* **Why:** 360°, IP65, strong-light tolerance, compact, \$299.
* **Electrical:** 5 V; UART **1,000,000 bps** TTL.
* **ArduPilot (Lidar360 family):**

  * `SERIALx_PROTOCOL = 11`
  * `SERIALx_BAUD = 1000000`
  * `PRX1_TYPE = 5`, `PRX1_ORIENT = 0` (top)
* **Mounting:** Horizontal; cable aft; exclude mast/prop sectors if needed.

### Forward (nose): **Nanoradar MR82 — Direct CAN first**

* **Why:** All-weather arc sensing; **0.2–40/80 m** dual-beam; IP66; \~92 g; UART/CAN.
* **ArduPilot direct (attempt):** Configure MR82 for **CAN**; use NanoRadar CAN protocol settings.

  * Example (CAN2):

    * `CAN_P2_DRIVER = 2`
    * `CAN_P2_BITRATE = 500000`
    * `CAN_D2_PROTOCOL = 14` *(NanoRadar)*
    * `PRX1_TYPE = 17` *(MR72\_CAN)*
    * `PRX1_ORIENT = 0/1`, `PRX1_YAW_CORR = <deg>`
  * Verify in **Proximity** viewer.
* **Fallback (only if needed):** Companion computer runs vendor SDK; publish MAVLink `OBSTACLE_DISTANCE_3D`.

## Integration Notes (Pixhawk 6X / Pix32 v6)

* **LiDAR (S2L) → TELEM UART.**

  * Wiring: TELEM **5 V → VCC**, **TX↔RX**, **GND → GND**; disable RTS/CTS on that port.
  * Params: as above; confirm 360° returns in Proximity.

* **Radar (MR82) → CAN.**

  * Use **CAN2**; bus terminated 120 Ω at both ends; set bitrate to match sensor.
  * **Not DroneCAN**: keep this CAN port isolated from DroneCAN nodes while testing NanoRadar protocol.

## Assumptions — “Family pattern” rationale (and risks)

* **NanoRadar MR-series (MR72 ⇄ MR82).**
  *Assumption:* Common **CAN message set** for proximity/object-list across MR-series → MR82 parseable by ArduPilot’s NanoRadar CAN protocol.
  *Why reasonable:* Same vendor family, same role, shared UART/CAN options.
  *Risk:* Frame IDs/scales/rates may differ; ArduPilot may not decode.
  *Mitigation:* Quick bench on CAN; if no returns, switch to companion bridge.

* **RPLIDAR S-family (S1 ⇄ S2/S2L).**
  *Assumption:* **Lidar360** serial protocol continuity across S-family at vendor baud (e.g., **1 M**).
  *Why reasonable:* Same interface, framing, and bring-up as documented family members.
  *Risk:* Minor report-code differences.
  *Mitigation:* Bench at 1 M; verify 360° plot; keep S1 as documented fallback.

## Test & Acceptance

**Bench (MR82 direct CAN):**

1. Set MR82 → **CAN**, **500 kbps**.
2. Apply FC params; reboot; open **Proximity**.
3. Walk a target across the forward arc; confirm sector changes.
4. Check DataFlash for **PROX/RNGFND** entries.

**Bench (S2L UART):**

1. Wire TELEM; `SERIALx_PROTOCOL=11`, `SERIALx_BAUD=1000000`.
2. Confirm 360° returns.

**Flight (incremental):**

* Low-speed OA trials (Simple/BendyRuler); increase speed after consistent detection at range.
* Ensure no FC brownouts; stable CAN errors; consistent timestamps.

# References

1. [ArduPilot — Nanoradar MR72 (Copter): setup, CAN protocol, non-DroneCAN note, Copter 4.5+](https://ardupilot.org/copter/docs/common-rangefinder-mr72.html)
2. [Nanoradar MR82 product page: range, IP rating, interfaces, mass, power](https://www.nanoradar.com/Products_1/7.html#c_navigation_199-17399536465290)
3. [DFRobot — Slamtec RPLIDAR S2L (SKU DFRobot #2617): specs, IP, UART 1 M, pricing](https://www.dfrobot.com/product-2617.html)
4. [ArduPilot — RPLIDAR (C1/A2/S1) setup: parameters, wiring, Lidar360 notes](https://ardupilot.org/copter/docs/common-rangefinder-lidar360.html)
5. [LightWare SF45/B product page: specs, weight, range](https://lightwarelidar.com/shop/sf45-b-50-m/)
6. [LightWare SF40/C product page / EOL notice: specs, range](https://lightwarelidar.com/shop/sf40-c-100-m-lidar-scanner/)
7. [YDLIDAR G6: specs and pricing](https://www.ydlidar.com/products/view/33.html)
8. [Hokuyo UST-10LX: specs overview](https://www.hokuyo-aut.jp/search/single.php?serial=167)
9. [Benewake CE30 series: specs overview](https://www.benewake.com/en/CE30.html)
10. [TI IWR6843AOPEVM: overview and SDK](https://www.ti.com/tool/IWR6843AOPEVM)
11. [TI AWR1843AOP: overview and SDK](https://www.ti.com/product/AWR1843AOP)
12. [InnoSenT IMD-2000: module overview](https://www.innosent.de/en/products/imd-2000/)
13. [Project Quiver - Obstacle Avoidance Options](https://docs.google.com/presentation/d/1X6TMNxwQzu4THHaNy2OxhHWF6RLIMKWR-6mM7jSrwQQ/edit?slide=id.p#slide=id.p)
