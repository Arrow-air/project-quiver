# Initial Configuration Guide
Quiver Dev-Kit

> [!NOTE]
>
> This guide covers **first-time configuration of an unconfigured aircraft**. It is the counterpart to Pilot Handbook §2.5, which assumes the aircraft already shipped pre-configured and asks the pilot only to *verify*. Use this document when the build was completed but no firmware, parameters, calibrations, networking, or companion computer setup were performed.
>
> Work top to bottom. Each section ends with a verification step. Do not move on until the verification passes.

## 0. Scope and Hardware Baseline

This procedure assumes the following Dev-Kit configuration:

| Subsystem | Hardware | Bus / Port |
|---|---|---|
| Flight controller | Holybro Pix32 V6 (Pixhawk6C firmware target) | — |
| ESCs | 4× Hobbywing XRotor X6-Plus-G2 | DroneCAN, CAN1 @ 1 Mbit |
| GNSS primary | Holybro F9P Rover Mini (RTK) | DroneCAN, CAN1 |
| GNSS secondary | Mateksys M9N-G4-3100 | DroneCAN, CAN1 (verify, see §5) |
| Obstacle LiDAR (360°) | RPLidar S2 (`S2M1-R2`) | SERIAL5 (TELEM3) @ 1 Mbaud, `PRX1_TYPE=5` (see §9.1) |
| Forward radar | NanoRadar MR82 | CAN2 RadarCAN, `PRX2_TYPE=17` |
| Radar altimeter (down) | NanoRadar NRA15 | CAN2 RadarCAN, `RNGFND1_TYPE=39` (NRA24_CAN) |
| Networking | 2× GigaBlox Nano switches + CubeNode ETH (PPP2ETH module) | CAN1 + SERIAL2 (PPP) |
| Companion computer | Raspberry Pi 5 on Main PCB (40-pin) | eth0 + CAN |
| Battery telemetry | DroneCAN ESC monitor (Bat1) + the pack's native smart BMS (Bat2, node 125). No RPi Tattu bridge, see §7 | CAN1 |
| Remote ID | DroneBeacon db201 (ArduRemoteID on ESP32) | DroneCAN, CAN1 |
| Battery | Tattu 14S LiHV (3.5 / 4.0 series) | — |

### Motor numbering and orientation (read before touching any ESC)

The aircraft flies the **ArduPilot QuadX** mixer (`FRAME_CLASS = 1`, `FRAME_TYPE = 1`). Motor numbers, arm positions, and rotation directions are fixed by ArduPilot and are the single source of truth for ESC ThrottleID/NodeID assignment (§10.2), motor test verification, prop handedness, and LED colors (§10.4):

```
        nose
   M3 CW    M1 CCW
      \      /
       \    /
       /    \
      /      \
   M2 CCW   M4 CW
```

| Motor / ThrottleID / NodeID | Position (nose forward, pilot's view from behind) | Rotation | Motor test letter |
|---|---|---|---|
| 1 | Front-right | CCW | A |
| 2 | Rear-left | CCW | C |
| 3 | Front-left | CW | D |
| 4 | Rear-right | CW | B |

> [!WARNING]
>
> **The Main PCB silkscreen motor numbering does NOT match this table — never use it for ESC ID assignment.** The silkscreen follows the Betaflight pattern (1 rear-right, 2 front-right, 3 rear-left, 4 front-left). The first Dev-Kit unit was ID'd off the silkscreen and motor test commanded the wrong motors — the aircraft would have flipped on takeoff. PT2's first flight carried the same defect class (motors 1 and 3 swapped, `pt2/flight-test/0001`), misread as CG imbalance. Always verify with motor test: A = front-right, B = rear-right, C = rear-left, D = front-left.

Source material this guide consolidates (historical sources, so where one conflicts with this guide, the guide reflects the newer verified state):
- `docs/Operations/firmware/index.md` and `docs/Operations/firmware/parameters/` (firmware image and parameter overlays, source of truth for param values)
- `task-grant-bounty/Dev-Kit/Ethernet-Setup-Guide.md` (CubeNode ETH + RPi + Tattu bridge)
- `task-grant-bounty/pt3/flight-controller/0002-flight-controller-setup` (CAN, serial, sensor params)
- `task-grant-bounty/pt3/flight-controller/0003-compass-setup` (compass calibration and MagFit)
- `docs/Engineering-Reports/Dev-Kit-Engineering-Report.md` §Remote ID Integration

### Network Topology (drone subnet 192.168.144.x)

Flat `192.168.144.0/24`, all static (no DHCP — SIYI firmware conflicts with a DHCP server). Source: Engineering Report §Network and Quiver SDK/Hub Developer Guide (canonical). The older `task-grant-bounty/Dev-Kit/Ethernet-Setup-Guide.md` is a **superseded test scheme** (FC .11, Pi .20, /20, gateway .10) and its addresses collide with SIYI — do not use it.

| Device | IP | Notes |
|---|---|---|
| CubeNode ETH (PPP2ETH) | 192.168.144.**50** | Static, set in CubeNode params. The FC's PPP peer and gateway. |
| Raspberry Pi (companion) | 192.168.144.**49** | Static on eth0 |
| Flight controller | 192.168.144.**51** | PPP-assigned by the CubeNode (`.50` + 1). The FC has no IP params of its own. |
| Payload C1 (bottom) | 192.168.144.100 | Fixed |
| Payload C2 / C3 (side) | 192.168.144.101 / .102 | Defaults, reassignable, range .100–.199 |
| Ground stations / dev machines | 192.168.144.200–254 | — |

> [!CAUTION]
>
> **`192.168.144.0/24` is a single flat network shared with the SIYI hardware**, and these SIYI addresses are hardcoded in firmware and cannot be changed, so every other device must avoid them: **`.11` air unit, `.12` ground unit, `.20` Android GCS, `.25` A8 Mini camera, `.60` reserved.** The flight controller has no IP of its own. It is PPP-assigned the CubeNode's address + 1. The first unit originally booted at `.11` (CubeNode `.10` + 1), colliding with the SIYI air unit. **Resolved 2026-06-19 by moving the CubeNode to `.50`, which puts the FC at `.51`** (clear of every reserved address), with the Pi at `.49`. Always verify the FC's live IP from the boot banner before powering the SIYI link.

> [!IMPORTANT]
>
> **Tattu 4.0 battery power-up.** The Tattu 4.0 pack has its own internal SSR/output that must be enabled before the drone push button does anything. On the battery's power button: **short press, then long press** to activate the output. Only then will the drone push button power the aircraft. (Tattu 3.5 packs have no output control and are always live.) This battery-internal SSR is in series with the aircraft's own main SSR (§11), so both must close for the HV bus to reach the ESCs.

### Tools and software needed

- USB-C cable for the Pix32 V6
- Mission Planner (primary GCS) on a Windows laptop
- DroneCAN GUI Tool v1.2.25+ for ESC node configuration
- Raspberry Pi Imager
- A microSD card for the RPi, plus the FC SD card for logging
- An RJ45 cable you can cut (the spare SIYI 4-wire RJ45 works) for the RPi to Main PCB Ethernet link
- Class D fire extinguisher and the battery handling discipline from Pilot Handbook §1.3

---

## 1. Firmware Flash

The Quiver firmware is ArduCopter built from current ArduPilot master on the upstream `Pixhawk6C` target, with the Arrow feature set restored: PPP networking, RPLidar S2 support, OpenDroneID (Remote ID), and the extra temperature sensors. A stock Pixhawk6C build will not work for Ethernet or Remote ID. Because this build now uses the upstream board target rather than the old `Pixhawk6C-arrow` hwdef, the boot banner alone no longer tells you the Arrow features are present. Confirm by feature, see **Verify** below.

1. Power the FC over USB only for flashing.
2. Mission Planner → **Setup → Install Firmware → Load custom firmware**.
3. Select `docs/Operations/firmware/arducopter-pixhawk6c.apj`.
   - The Pix32 V6 uses the Pixhawk6C target. This file is correct for the board even though the board silk says Pix32 V6.
   - **Confirm the file is current before flashing.** The `.apj` is JSON and its `git_identity` field must read `20622a39` (the PR #230 image, `summary` = `Pixhawk6C`). A stale checkout of `main` can still hold the older `977fd8e` image, which lacks the S2 lidar driver. Sync with `origin/main` if it does not match.
4. Let the flash complete and the FC reboot.

> [!WARNING]
>
> Flash on USB power. For all configuration *after* flashing, power the FC from the main power module, not USB alone, so peripherals on CAN and serial are powered and enumerate correctly.

> [!NOTE]
>
> The Pix32 V6 enumerates over USB as a **composite device with two COM ports**. One is MAVLink, the other is SLCAN. Connect Mission Planner to the **lower-numbered** port (the MAVLink endpoint). Connecting to the SLCAN port produces a "Sequence contains no elements" error because there is no heartbeat there. If the COM number shifts after a replug, refresh the port list and reselect.

**Verify:** Mission Planner connects and the Messages tab boot banner shows the master-based build. Confirmed on the first unit:

```
ArduCopter V4.8.0-dev (20622a39)
ChibiOS: 73f152d3
Pixhawk6C 002F0039 33335101 31313837
```

The git hash `20622a39` identifies this Arrow-equivalent build, and the APJ `summary` reads `Pixhawk6C`. The version string may differ slightly with the master snapshot, so treat the git hash as the marker.

> [!IMPORTANT]
>
> The board string is now `Pixhawk6C`, the same as a stock build, so it no longer proves the Arrow features are present. A bare upstream Pixhawk6C build has the same banner but no Ethernet, Remote ID, or temperature sensors. The real confirmation is **functional**. On a fresh board these signals only appear as the matching sections are configured, so treat them as a running checklist rather than a flash-time gate:
> - Lidar (once §2 loads the SERIAL5 params): boot prints `RPLidar S2 hw=18 fw=1.1`. `RPLidar UNKNOWN hw=18 fw=1.1` means an **older Arrow build** without the S2 driver (the pre-PR-230 image prints exactly this), so recheck the `.apj` provenance in step 3. Current stock builds also detect the S2, so `UNKNOWN` points at the old image, not a stock one.
> - Ethernet (once §2 and §4 are done): boot prints `NET: IP 192.168.144.51` and `TCP[21]: bound to 0.0.0.0:5760` (the `NET_P1` server, §4). A stock image prints no `NET:` lines at all. (The first unit initially booted at `.11` under the old CubeNode address, resolved in §4.4.)
> - Remote ID (once §2 loads the Remote ID overlay): `ODID:` messages and `PreArm: OpenDroneID: UA_TYPE required` (§8). A stock image shows neither.
> - Scripting (once §11.4 installs the SSR Lua): `Relay 1 closed (SSR enabled) after 12s delay`.
>
> If the Ethernet and Remote ID signals never appear after their sections are configured, you flashed a stock image. If they appear but the lidar reads `UNKNOWN`, you flashed the old `977fd8ec` Arrow build.

For historical reference, the previous build banner was `ArduCopter V4.8.0-dev (977fd8ec)` with board string `Pixhawk6C-arrow` (the old custom hwdef, git `977fd8e`).

`Frame: UNSUPPORTED` and `PreArm: Check frame class and type` at this stage are expected, the board has blank params until §2.

### 1.1 Bench-testing an alternate firmware build (revert-safe)

Sometimes you want to flash a different build to isolate one subsystem, for example a stock or master-based image to confirm an RPLidar S2 fix. This is safe and fully reversible if you treat it as a throwaway test and keep the Arrow build as the flight image.

> [!WARNING]
>
> A **stock / official `Pixhawk6C`** build is not a flight image for this airframe. ArduPilot's published feature manifest (`firmware.ardupilot.org/Copter/latest/Pixhawk6C/features.txt`) shows the official target ships with `!AP_NETWORKING_ENABLED`, `!AP_NETWORKING_BACKEND_PPP`, `!AP_OPENDRONEID_ENABLED`, and the `!AP_TEMPERATURE_SENSOR_*` drivers all disabled. So Ethernet, the CubeNode PPP link, the `NET_P1` MAVLink TCP server, Remote ID, and the temperature sensors are gone. The RPLidar driver is enabled, so the lidar still works. Only the Arrow build (the upstream Pixhawk6C target with the Arrow feature defines restored, PR #230, formerly the `Pixhawk6C-arrow` hwdef) turns the other features back on. Use a stock build for diagnostics only.

What a reflash does and does not touch:

- It does **not** wipe parameters. ArduPilot keeps stored params across a reflash, so frame, compass, GPS, battery, and the SERIAL5 lidar params all carry over.
- Params for features the test build lacks (all `NET_*`, `DID_*`, `TEMP*_*`) have no home in that build and can be dropped from storage. They revert to defaults, which is why you reload the full HOU file after going back.
- The SD card is untouched, so `relay_delayed_close.lua` and logs survive. ESC node/throttle IDs and LED colors live in the ESCs themselves over DroneCAN, so motor mapping is unaffected.

Procedure:

1. **Back up first, on the current build.** Mission Planner → Config → Full Parameter Tree → Save. For the first unit, `parameters/params-HOU-713.param` (2026-07-13, battery power, post M9N replacement) is the current restore point, superseding `params-HOU.param` (2026-07-08, predates the swap and the first-flight deviations) and the earlier `params-HOU-2.param`. Make sure the file reflects the current state. Do **not** restore from `params-HOU-625.param`: that 2026-06-25 snapshot contains `ARMING_SKIPCHK,-1`, which skips every arming check.
2. **Flash the test build** the same way as §1 (Load custom firmware → its `.apj`). Do not reconfigure anything. The SERIAL5 lidar params carry over.
3. **Test only the target subsystem, props off.** For the lidar the S2 is powered from avionics 5 V on TELEM3, not the HV bus, so SSR / Relay 1 state does not matter. Watch for a stable lock rather than the spin-up then coast-down loop. Ethernet and Remote ID will be dead on a stock build, which is expected.
4. **Revert** by loading the Arrow `.apj` again (`docs/Operations/firmware/arducopter-pixhawk6c.apj`).
5. **Reload HOU after reverting.** Load `parameters/params-HOU.param` → Write → reboot → confirm `NET_P1_TYPE`, the CAN sub-parameters, and the AVOID / PRX params are back. If any driver-dependent params are missing, run the two-pass from §2 (load → Write → reboot → load again).

> [!CAUTION]
>
> Going **back** to an older build (for example master back to `977fd8ec`) is the riskier direction, because downgrade parameter conversions are not always clean. Do not trust the automatic restore. Always reload the known-good HOU file in step 5. Worst case is a short param reload, never a from-scratch rebuild.

---

## 2. Load Base Parameters

> [!CAUTION]
>
> After flashing, do a **full parameter reset** before loading the base file, so no stale defaults survive. Mission Planner → Config → Full Parameter Tree → reset to default, then reboot.

Load the parameter overlays **in this order**. Each is additive and only sets the keys it lists. It does not reset others, so order matters.

| Order | File | Purpose | Load when |
|---|---|---|---|
| 1 | `parameters/standard-params.param` | Base config: CAN, ESC, GPS, EKF, battery, failsafes, RPLidar present but avoidance off, Ethernet off | Always |
| 2 | `parameters/params-ethernet.param` | Enables PPP networking via the CubeNode ETH / RPi | This unit (has Ethernet) |
| 3 | `parameters/params-remoteid.param` | Enables DroneBeacon db201 over DroneCAN | This unit (has Remote ID) |
| 4 | `parameters/params-object-avoidance.param` | Enables RPLidar S2 BendyRuler avoidance | Optional, see §9 |

Load via Mission Planner → Config → Full Parameter Tree → **Load from file**, then **Write Params**, then reboot after each file.

> [!IMPORTANT]
>
> **Load each file twice (two-pass).** CAN, NET, and other driver-dependent sub-parameters do not exist until their parent driver is enabled *and the FC has rebooted*. On the first write, Mission Planner silently skips them. So: load → Write → reboot → **load the same file again** → Write → reboot. Confirmed needed on the first unit, where `CAN_D1_UC_ESC_BM`, `CAN_P2_DRIVER`, and `CAN_P2_BITRATE` did not take until the second pass.

**Verify after step 1:** Spot-check that the base values match the airframe:

| Parameter | Expected | Meaning |
|---|---|---|
| `CAN_P1_DRIVER` / `CAN_P1_BITRATE` | `1` / `1000000` | DroneCAN bus 1 at 1 Mbit (ESC, GPS, db201, CubeNode) |
| `CAN_P2_DRIVER` / `CAN_P2_BITRATE` | `2` / `500000` | DroneCAN bus 2 at 500 kbit (NanoRadar) |
| `CAN_D1_UC_ESC_BM` | `15` | Motors 1–4 over DroneCAN |
| `GPS1_TYPE` / `GPS2_TYPE` | `9` / `9` | Both GNSS over DroneCAN |
| `BATT_MONITOR` | `9` | Bat1 = DroneCAN ESC telemetry |
| `BATT_ARM_VOLT` | `47.5` | ~3.4 V/cell on 14S |
| `MOT_BAT_VOLT_MAX` / `MIN` | `60.9` / `46.2` | 14S LiHV range |
| `PRX1_TYPE` | `5` | RPLidar S2 proximity sensor present |

If `BATT_*` or `MOT_BAT_*` show 12S-style values, stop and report. The aircraft is 14S LiHV.

---

## 3. Per-Drone Calibrations

The parameter files deliberately exclude calibration values because they are unique to each airframe. Perform all of the following before flight.

### 3.1 Accelerometer and Level

1. Mission Planner → **Setup → Mandatory Hardware → Accel Calibration**.
2. Follow the six-orientation prompts on a flat, stable surface.
3. Run **Level Horizon** with the aircraft sitting level on its landing gear.

### 3.2 Compass

The Pix32 V6 internal magnetometer is disabled. The two external compasses are the magnetometers inside the GNSS units (both on DroneCAN).

On the first unit, **Setup → Mandatory Hardware → Compass** detected three:

| Priority | DevID | Bus | Addr | Device | Action |
|---|---|---|---|---|---|
| 1 | 96003 | UAVCAN | 119 | Mateksys M9N magnetometer (external) | keep (primary) |
| 2 | 96515 | UAVCAN | 121 | Holybro F9P magnetometer (external) | keep |
| 3 | 658433 | I2C | 12 | Pix32 V6 internal IST8310 | **disable** |

The DevID encodes the DroneCAN node ID, so it changes whenever a GNSS module is replaced. The original M9N was node 122 (DevID 96771). Its 2026-07-13 replacement enumerated at node 119 (DevID 96003), and the table above shows the current unit. After any GNSS swap, the new magnetometer appears as a new uncalibrated device at the bottom of the priority list and the old one shows as missing: remove the missing entry, promote the new module back to its priority slot, reboot, and re-run the outdoor calibration below.

> [!NOTE]
>
> **Priority number and parameter index are two different things.** `COMPASS_PRIO1/2/3_ID` and `COMPASS_USE/USE2/USE3` follow the **priority** order above. The offset, external, and device-ID parameters (`COMPASS_OFS*`, `COMPASS_EXTERN*`, `COMPASS_DEV_ID*`) follow the **detection slot**, which is whatever order the drivers registered in. After the 2026-07-13 M9N swap the slots reshuffled: slot 1 = internal IST8310, slot 2 = F9P, slot 3 = Mateksys. So the primary compass's offsets now live in `COMPASS_OFS3_*`, not `COMPASS_OFS_*`. When reading offsets back after a calibration, match the slot to the device through `COMPASS_DEV_ID1/2/3` first. Stale offsets left on a disabled slot (the old Matek values now sitting on the internal's slot 1) are harmless and are skipped by the calibration.

**Indoor config (done on first unit):**
1. **Setup → Mandatory Hardware → Compass.** Uncheck **"Use Compass 3"** to disable the internal IST8310 (DevID 658433). Leave Use Compass 1 and 2 checked. Click **Reboot** to apply. (Optional: "Remove Missing" to clear the disabled row.) The slot numbers come from this unit's enumeration, so on another airframe disable whichever slot shows the I2C IST8310, it is not always Compass 3.
2. Leave **Orientation = None** on all — `COMPASS_AUTO_ROT = 2` auto-detects orientation during calibration. (If the IST8310 ever needs manual fixing, `COMPASS_ORIENT = 6` / Yaw270.)

**Outdoor (the actual calibration).** Pick the method by whether you can physically rotate the airframe:

3a. **Onboard Mag Calibration (the Start button)** is the better baseline *if* you can rotate the aircraft through all six orientations — a small vehicle, a rotating stand, or a second person tilting and spinning it. Run it outdoors, well away from buildings, vehicles, rebar, and tools. On a prior, lighter build this beat LVMC.

3b. **Large Vehicle MagCal (LVMC)** for the fully assembled 25 kg Dev-Kit, which you cannot hand-flip on the gear with the battery in. The aircraft stays still: sit it level on its landing gear in normal attitude, point the nose at a known heading, and run LVMC. It computes offsets from the World Magnetic Model in one shot, no rotation. Enter the **true** heading (magnetic + declination; Houston ≈ +1° E, so a nose at magnetic north is true heading 1°).

   **In Mission Planner:**
   1. Confirm a GPS 3D fix first (§5) — LVMC needs the vehicle's lat/lon to look up the expected field. Sit the aircraft level on its gear.
   2. Point the nose at a known heading. Read it off a phone compass held about a meter from the airframe so the aircraft's own steel and magnets do not pull it. Convert to true (add the local declination).
   3. **Setup → Mandatory Hardware → Compass** → click **Large Vehicle MagCal**.
   4. A prompt appears: **"Enter current heading in degrees — NOTE: gps lock is required. Heading is true, not magnetic."** Type the nose's **true** heading in degrees, click OK.
   5. Mission Planner computes, writes, and autosaves the new offsets to the FC. It does **not** pop them up in a dialog. Read them back from **Config → Full Parameter Tree** (Refresh Params first), search `OFS`. The instance digit goes after `OFS`: Compass 1 = `COMPASS_OFS_X/_Y/_Z`, Compass 2 = `COMPASS_OFS2_X/_Y/_Z`, Compass 3 = `COMPASS_OFS3_X/_Y/_Z`. No reboot needed.

   Equivalent over MAVLink (used on the first unit's 2026-06-20 run, with Mission Planner disconnected so the COM port was free): `MAV_CMD_FIXED_MAG_CAL_YAW` — param1 = true yaw, param2 = 0 (all compasses), param3/param4 = 0 (use the live GPS position).

In both cases **MagFit (§3.3) from a flight log is the real refinement**, so the ground cal only needs to be good enough to fly safely.

First-unit result, MP Large Vehicle MagCal (nose at 350° magnetic, true heading 351°):

| Compass | Offsets (x, y, z) mGauss | Magnitude |
|---|---|---|
| 1 (Matek, primary) | −91, 61, 256 | ~279 |
| 2 (F9P) | 9, 111, 57 | ~125 |

Both are well under the ~400 healthy ceiling. Verified immediately after: with the nose still at 351° true the HUD heading read **348°** (3° error, within tolerance — a static offset this small is what MagFit refines out). This run is consistent with the earlier 2026-06-20 MAVLink run on the same unit (Matek −54, 36, 247 / ~255; F9P 40, 79, 51 / ~102; heading read 4° vs 1° expected, EKF compass variance 0.055) — same Z-dominant Matek and smaller F9P, the spread is heading and magnetometer noise.

Re-run 2026-07-13 after the M9N replacement (new module = node 119, so its offsets landed in `COMPASS_OFS3_*` per the slot note above):

| Compass | Param slot | Offsets (x, y, z) mGauss | Magnitude |
|---|---|---|---|
| Matek (new unit, primary) | `COMPASS_OFS3_*` | −29, 19, 226 | ~229 |
| F9P | `COMPASS_OFS2_*` | 28, 40, 24 | ~55 |

Verified by readback over MAVLink: both enabled magnetometers reported 463 and 464 mGauss field strength, agreeing within 2 counts, with no compass pre-arm messages. The new Matek shows the same Z-dominant signature as the old unit in the same mount location. The disabled internal IST8310 read 620 mGauss, which is the expected uncalibrated in-hull value and does not matter.

4. Quick check in LOITER or POSHOLD after calibration: no toilet-bowling, no yaw drift, no mag warnings.

### 3.3 MagFit (recommended)

For best heading performance, collect a MagFit dataset and run it through WebTools.

- Dataset: either a manual 6-minute flight with step inputs, throttle sweeps, 360° turns, and circles, or an auto figure-8 mission from the MagFit helper script.
- The dataset must be flown on the compass hardware currently installed. A log recorded before a compass or GNSS module swap fits the old magnetometer and cannot be used. On the first unit, the 2026-07-09 logs predate the 2026-07-13 M9N replacement for exactly this reason. Valid datasets: log 63 (2026-07-23, full 360° heading coverage, §17.6 finding 3) and log 72 (2026-07-24, after the field LVMC). Whether the refinement run is needed on this unit is with Zeynep (2026-07-27), since in-flight compass behavior looks good.
- Run MagFit via WebTools with Battery1 current offsets + scale enabled.
- Assign compass priority based on the MagFit error metrics. On prior builds the Mateksys gave lower mean Gaussian error and was set primary.

See `task-grant-bounty/pt3/flight-controller/0003-compass-setup` for the full procedure.

### 3.4 RC Calibration

1. Bind the receiver and confirm input in Mission Planner. On this aircraft the transmitter is the MK32 talking to the HM30 air unit, so if it has never been bound, do **§16.3 (firmware match) and §16.4 (bind) now**, then come back here. §16.5 records the finished channel map.
2. **Setup → Mandatory Hardware → Radio Calibration.** Move all sticks and switches to extremes.
3. Apply **no trims or sub-trims**.
4. Map the mandatory controls per Pilot Handbook §2.7.1: Arm/Disarm, a 3-position flight mode switch (LOITER / AUTO / STABILIZE), a dedicated RTL switch, and a guarded Kill Switch. The as-built map on the first unit is in §16.5 (ch9 = mode, ch10 = RTL, ch5 = arm, ch8 = kill). An earlier first-unit map put RTL on the third mode-switch position with no AUTO. It was re-mapped 2026-07-08 to match the Handbook. Since 2026-07-09 the first unit flies a documented deviation, STABILIZE / ALTHOLD / LOITER with AUTO off the switch while no auto missions are flown (decided 2026-07-20, see the §16.5 note).
5. Verify each switch produces the intended mode and the kill switch is protected against accidental activation.

### 3.5 Barometer

Barometer ground pressure is auto-calibrated on boot. Confirm a sane altitude reading at rest before flight.

**Verify:** No calibration-related pre-arm errors remain in Mission Planner.

### 3.6 Outdoor calibration field session

These outdoor steps cannot be completed on the bench, because they need open sky for a GPS fix or distance from rebar, vehicles, and tools for clean magnetometer data. Steps 1 and 2 are also re-run after every shipment or relocation to a new operating site, per Pilot Handbook §2.5.5 (Post-Shipment Recalibration). The accel, level, barometer, and RC steps above are bench work and stay indoors. Take the aircraft to an open area away from buildings, parked cars, and structural steel, and run these four in order. Each depends on the one before it. Steps 1 and 2 complete on the first outdoor session. Step 3 needs a flight, so it only happens after the entire bench configuration (§4 through §12) is done and the aircraft is cleared to fly. Plan on two outdoor sessions.

| Step | Calibration | Depends on | Detail |
|---|---|---|---|
| 1 | GPS 3D fix + HDOP check | sky view | §5.2 |
| 2 | Compass mag-cal (LVMC on the assembled airframe, or onboard if you can rotate it) | a good 3D fix | §3.2, "Outdoor" |
| 3 | MagFit refinement (flight log → WebTools) | a completed mag-cal to fly safely | §3.3 |
| 4 | F9P RTK base-station survey-in (not used on this drone) | sky view | §5.2, step 3 |

1. **Get a GPS fix first (§5.2).** Power up outdoors and wait for satellite counts to climb and the EKF to reach a 3D fix with HDOP settling. The mag-cal in the next step wants a good fix, and you cannot fly the MagFit log without one.
2. **Run the compass mag-cal (§3.2).** On the fully assembled 25 kg airframe, use **Large Vehicle MagCal** — the aircraft sits level on its gear, point the nose at a known heading and enter the **true** heading (Houston declination ≈ +1° E). Use the onboard **Start**-button cal instead only if you can rotate the airframe through all six orientations. Stay well clear of buildings, vehicles, rebar, and tools. The cal covers the two GNSS magnetometers (the internal IST8310 is disabled). For the onboard method leave orientation at None and let `COMPASS_AUTO_ROT = 2` resolve it. Quick check in LOITER or POSHOLD afterward: no toilet-bowling, no yaw drift, no mag warnings.
3. **Collect a MagFit log and run it (§3.3).** Fly either a 6-minute manual flight with step inputs, throttle sweeps, 360° turns, and circles, or the auto figure-8 from the MagFit helper script. Run the log through WebTools **with Battery1 current offsets + scale enabled** — that current compensation is the modern replacement for a separate CompassMot run, so you do not need CompassMot. Assign compass priority from the MagFit error metrics (the Mateksys gave lower mean Gaussian error and was set primary on prior builds).
4. **RTK base survey-in — not used on this drone, skip.** This aircraft does not fly RTK. For reference on a future RTK build: Mission Planner → Setup → RTK/GPS Inject, SurveyIn Acc = 2 m, Survey Time = 60 s+, Restart, then save the surveyed position for reuse.

> [!NOTE]
>
> There is no separate **CompassMot** step. Compass/motor-current interference is corrected by the current-compensated MagFit in step 3, not by a standalone CompassMot run.

**Verify (first session):** Mag-cal passes with low offsets and the EKF holds a 3D fix with stable heading in LOITER. **Verify (after the first flight):** MagFit assigns a sensible primary.

---

## 4. Ethernet: Switches and CubeNode ETH

This is the dev-kit Main PCB path using the CubeNode ETH (PPP2ETH) module on **CAN1** and **SERIAL2 (PPP)**, with the cables on **J35 / J36 / J41**.

> [!CAUTION]
>
> **The FC has no IP of its own. It is PPP-assigned the CubeNode's address + 1.** The aircraft uses **CubeNode `.50` → FC `.51`**, so the FC's gateway is the CubeNode at `.50`, and the Pi is at `.49`. The values in §4.4 below reflect this. The first unit originally booted at `.11` from the old test scheme (CubeNode `.10`), which collided with the SIYI air unit. That was resolved on 2026-06-19 by moving the CubeNode to `.50`.

### 4.1 Ethernet switches

1. Plug each GigaBlox Nano switch into its connector on the Main PCB.
2. Secure each with 2× M2x6 screws. Dev-kit PCBs have the spacers pre-soldered.

> [!WARNING]
>
> **The two GigaBlox switches are now prime suspects for the M9N GNSS degradation (hypothesis, 2026-08-13).** The second unit produced the first clean before/after evidence in the interference thread: it flew before its Ethernet install with strong sat counts on both the M9N and the F9P, and after this section's install (switches, CubeNode PPP, RPi) the M9N stopped working. The switches mount directly beside the M9N. This fits the first unit's history (§5.1, §17.6, §17.7), where the failure followed the position rather than the module: it survived a full M9N replacement and only eased with constellation mitigation.
>
> To confirm: first rule out the §5.2 receiver wedge with a cold start. Then A/B outdoors, static: log GPS 2 sat count and HDOP with the switches powered, then depower or unplug both switches with everything else running and watch for recovery. If the switches are confirmed, the options are shielding, relocating the M9N, or relocating the switches. Flag the result to the team either way.

### 4.2 CubeNode ETH physical connection (dev-kit PCB)

Connect all three included cables to the CubeNode ETH, then to the Main PCB:

| Cable | Main PCB connector |
|---|---|
| 6-pin UART | J41 |
| 5-pin Ethernet | J36 |
| 4-pin CAN | J35 |

> [!WARNING]
>
> A dedicated mount for the CubeNode ETH ships on the floating module plate inside the main enclosure. Secure it so exposed pins and pads cannot short against the airframe or other boards.

### 4.3 Flight controller parameters (dev-kit PCB)

These come from the `params-ethernet.param` overlay loaded in §2, plus the CAN settings already in the base file. Confirm:

```
CAN_P1_DRIVER   = 1
CAN_P1_BITRATE  = 1000000
CAN_D1_PROTOCOL = 1
NET_ENABLE      = 1
NET_P1_TYPE     = 4          ; TCP Server (see warning below)
NET_P1_PORT     = 5760
NET_P1_PROTOCOL = 1
SERIAL2_PROTOCOL = 48        ; PPP
SERIAL2_BAUD     = 12500000  ; 12.5 Mbaud
```

> [!WARNING]
>
> **`NET_P1_TYPE` and the load order.** ArduPilot does not create the `NET_P1_PORT` and `NET_P1_PROTOCOL` parameters until `NET_P1_TYPE` is set to a non-zero value and the FC is rebooted. `params-ethernet.param` now sets `NET_P1_TYPE,4` (patched 2026-06-25), so the two-pass load in §2 instantiates the port and protocol on the second pass. On a unit flashed from the **older** overlay (which omitted `NET_P1_TYPE`), those two lines are silently skipped on every load, so set it manually:
> 1. Confirm `NET_ENABLE = 1`, reboot if you just set it.
> 2. Set `NET_P1_TYPE = 4` (TCP Server, because the GCS connects *to* the FC at `192.168.144.51:5760`). Write, reboot.
> 3. `NET_P1_PORT` and `NET_P1_PROTOCOL` now exist. Set `5760` and `1`. Write, reboot.
>
> The overlay file has been patched to include `NET_P1_TYPE,4` (Open Item 4, 2026-06-25).

### 4.4 CubeNode ETH parameters

The CubeNode ETH appears on the CAN bus. Open Mission Planner → **Setup → Optional Hardware → DroneCAN/UAVCAN**, connect to **MAVLinkCAN1**, query the node, then **Menu → Parameters**. Set and **Write**:

```
NET_DHCP    = 0
NET_ENABLE  = 1

NET_GWADDR0 = 192
NET_GWADDR1 = 168
NET_GWADDR2 = 144
NET_GWADDR3 = 1

NET_IPADDR0 = 192
NET_IPADDR1 = 168
NET_IPADDR2 = 144
NET_IPADDR3 = 50

NET_NETMASK = 24
NET_OPTIONS = 1
NET_P1_TYPE = 0
```

This gives the CubeNode ETH the static IP `192.168.144.50`. The FC then receives `192.168.144.51` from the adapter automatically (the CubeNode address + 1), with its gateway set to the CubeNode at `.50`.

> [!WARNING]
>
> **Two gotchas when changing the CubeNode IP, both hit on the first unit (2026-06-19):**
>
> 1. **Confirm the write committed.** After editing `NET_IPADDR3`, re-fetch the node's parameters and check it reads back `50`. The MP DroneCAN parameter grid does not always commit an edited value on the first attempt.
> 2. **Fully power the aircraft down and back up.** The CubeNode is a separate DroneCAN node and keeps its running IP until it loses power. An FC reboot (the MP reboot button) is **not** enough, because the FC re-negotiates PPP against the still-running old CubeNode and comes back unchanged. On the first unit, after setting `NET_IPADDR3 = 50`, an FC reboot still showed `NET: IP 192.168.144.11`. Only a full power cycle brought the FC up at `.51` with gateway `.50`.

**Verify:** With the FC on USB, check the **Messages** tab during boot. You should see (the `/32` mask is normal for the PPP point-to-point link):

```
NET: IP      192.168.144.51
NET: Mask    255.255.255.255
NET: Gateway 192.168.144.50
```

Full detail and photos: `task-grant-bounty/Dev-Kit/Ethernet-Setup-Guide.md` §2–4. Use it only for the photos and physical steps. Its IP addressing is the superseded test scheme (§0) and must not be followed.

---

## 5. GNSS Verification

Both GNSS units are configured as DroneCAN (`GPS1_TYPE = 9`, `GPS2_TYPE = 9`).

### 5.1 GPS role assignment (F9P primary)

The design intent (Engineering Report, with background in GNSS note 0006 and FC setup note 0002) is **F9P = primary** (the multi-band RTK unit) and **Mateksys M9N = backup** (non-RTK). On the first unit the DroneCAN instances enumerated **flipped** — GPS 1 = Mateksys (then node 122), GPS 2 = F9P (node 121). Pin them with `CAN_OVRIDE` so the F9P is GPS 1:

```
GPS1_CAN_OVRIDE = 121   ; F9P node → GPS 1 (primary)
GPS2_CAN_OVRIDE = 119   ; Mateksys node → GPS 2
```

Write, reboot. Verify `GPS1_CAN_NODEID` and `GPS2_CAN_NODEID` read back the same node IDs after reboot, on battery power (the CAN peripherals are unpowered on USB alone, so the `NODEID` fields read 0 there). Confirmed working on the first unit.

The node IDs are assigned by the flight controller's dynamic node allocation (DNA) server and are unit-specific. The first unit's original M9N sat at node 122. Its 2026-07-13 replacement came up at **node 119**, because the DNA server keeps the old ID reserved against the dead unit's hardware serial and hands a new module the next free slot. So after any GNSS swap: read the new node ID off the DroneCAN screen, point the matching `CAN_OVRIDE` at it, and do not expect the old number to come back. Do not clear the DNA database to force a reuse, since that would re-allocate every dynamic node on the bus and break the other override and both compass device IDs.

Keep `GPS_AUTO_SWITCH = 1` (**Use Best**) — do **not** blend an RTK unit with a non-RTK one. (FC note 0002 suggests blending. That advice is superseded, do not follow it.) `GPS_INJECT_TO = 127` sends RTCM to both, so RTK reaches the F9P regardless of instance.

### 5.2 Verification

1. In the DroneCAN/UAVCAN screen, confirm both GPS nodes enumerate on CAN1.
2. Confirm satellite counts climb outdoors and the EKF reaches a 3D fix. **In Mission Planner**, read per-instance status on the **Flight Data → Status** subtab (use the search box to filter): `satcount` / `gpsstatus` / `gpshdop` for GPS 1, and `satcount2` / `gpsstatus2` / `gpshdop2` for GPS 2. `gpsstatus` fix codes: **0 No GPS, 1 No Fix, 2 2D, 3 3D, 4 DGPS, 5 RTK Float, 6 RTK Fixed.** The HUD's "GPS A / B" labels are ambiguous and can disagree with the instance numbers, so trust the numbered Status fields. Target outdoors: 12+ sats and HDOP ≤ 1.0 per working unit.
3. **RTK is not used on this drone, so skip the base station.** For reference on a future RTK build: Mission Planner → **Setup → RTK/GPS Inject**, SurveyIn Acc = 2 m, Survey Time = 60 s+, then Restart, and save the surveyed position for reuse.

> [!NOTE]
>
> **GPS 2 (Mateksys M9N) stuck at `No Fix` with 0 satellites? Run a cold start before considering a return.** If the M9N sits at `No Fix` with 0 sats in open sky while the F9P fixes normally, the most likely cause is a wedged u-blox receiver state (a stale almanac or corrupted configuration held in the receiver's battery-backed RAM), not faulted hardware. On the first unit this persisted across two outdoor sessions and looked like a dead module, but a cold start recovered it fully.
>
> **Why a cold start rather than a return.** The DroneCAN node stays healthy on the bus and its magnetometer publishes a normal field the whole time, which proves power, CAN, and the AP_Periph firmware are all fine. Only the receiver's internal GNSS state is stuck, and a cold start clears it. The receiver also reports `No Fix` (status 1), not `No GPS` (status 0), so it is powered and running and simply not acquiring.
>
> Do not rely on the node's `gnss.Auxiliary.sats_visible` field for this diagnosis. On this MatekG474 firmware it reads 0 even with a healthy 3D fix. Use the FC's GPS 2 fix type and sat count on the **Flight Data → Status** screen, plus the HDOP value, which sits at 100 when there is no solution and drops to a real number such as 2 once the receiver locks.
>
> **Cold start procedure:**
> 1. **Power the whole aircraft from the main battery, not the flight controller USB alone.** The M9N draws its power from the DroneCAN bus, so it is only alive when the aircraft is fully powered. Connecting the flight controller over USB by itself does not power the CAN peripherals, and the module cannot acquire if it is not powered.
> 2. Take the aircraft outdoors with the M9N antenna under clear, open sky.
> 3. Bridge the **`M9N-RST` pad to ground for at least 100 ms**. This triggers a u-blox cold start, which erases the receiver's stored almanac, ephemeris, and configuration and forces a fresh acquisition. AP_Periph re-applies its own configuration automatically on the next boot (`GPS_AUTO_CONFIG = 1`), so nothing needs to be set by hand afterward.
> 4. **Re-soak.** Leave the aircraft powered and stationary, antenna facing open sky, for several minutes. "Re-soak" means giving the freshly reset receiver uninterrupted sky time to download a new almanac and ephemeris and reacquire satellites from scratch. A basic 3D fix usually appears within a few minutes. Full timing alignment can take up to 12.5 minutes while the leap second downloads, but a position fix comes well before that.
> 5. Re-check GPS 2 on **Flight Data → Status**. `gpsstatus2` should climb from 1 (No Fix) to 3 (3D) or 4 (DGPS), `satcount2` should rise from 0, and `gpshdop2` should fall from 100 toward 1.
>
> On the first unit, a cold start took GPS 2 from `No Fix` / 0 sats / HDOP 100 to a **3D fix with 6 satellites and climbing, HDOP 2**, within minutes.
>
> **The wedge can recur.** On the first unit it returned days later and needed the cold start repeated. When it does not recover immediately, confirm the `M9N-RST` bridge actually made solid contact for a full second or two, then give it a full open-sky soak of 10 to 12 minutes before treating it as recovered or as failed. The recovery is repeatable, so a recurrence is not by itself evidence of a hardware fault.
>
> **Only if a cold start plus a re-soak under clear sky still yields 0 satellites** should you treat the module as faulted hardware and pursue an RMA. RMA stands for Return Merchandise Authorization, the vendor's warranty return process: contact Mateksys or the reseller, obtain an RMA number, and ship the unit back for repair or replacement. A faulted GNSS RF front end or antenna is the remaining cause once a cold start is ruled out. The M9N also carries **Compass 1 (the primary, the one LVMC ran on)**, so a replacement means re-running **LVMC** and reassigning compass priority on the new module. Either way this is not a flight blocker on its own: the F9P alone is flyable, and you only lose GPS redundancy.
>
> **How the first unit ended.** The cold start recovered it twice, but the module kept degrading: it produced an in-flight velocity glitch (22.7 m/s reported while stationary, §17.3 finding 3) and then dropped off the CAN bus entirely, and it was **replaced on 2026-07-13**. So the cold start is the right first move, but a module that needs repeated cold starts and then starts glitching in flight is on its way out.
>
> **Replacing the M9N (done on the first unit 2026-07-13):**
> 1. Swap the module (J9, CAN1), mounted in the same orientation as the old one.
> 2. Power up on battery and read the new node ID off the DroneCAN screen. Expect a **new** node ID, not the old one (§5.1 explains the DNA allocation). The replacement came up at node 119 with Mode OPERATIONAL, Health OK, and a steadily climbing uptime.
> 3. Set `GPS2_CAN_OVRIDE` to the new node ID, reboot, and confirm `GPS2_CAN_NODEID` reads it back on battery power.
> 4. Compass cleanup (§3.2): remove the missing old magnetometer, promote the new one to priority 1, reboot, then re-run LVMC outdoors.
> 5. Acceptance before trusting it: 3D fix held, 12+ sats in open sky after a 10 minute soak, HDOP at or under ~1.5, and reported ground speed staying in the noise (under 0.5 m/s stationary, no sustained ramps). The 07-13 bench readback showed fix 3, 11 sats, HDOP 2.08 under a partial sky view, velocity peak 0.30 m/s.
> 6. `GPS_AUTO_SWITCH` stays at 4 (pinned to the F9P, §17.2) until the new unit's velocities track the F9P through a real flight log, then restore 1 (Use Best). **First attempt FAILED 2026-07-23: the replacement unit reproduced the old unit's velocity glitch in log 63 (§17.6 finding 2), so the pin stays and the cause now looks systemic to the M9N position rather than the module.** Update 2026-08-13: the second unit adds before/after evidence pointing at the adjacent GigaBlox Ethernet switches, see the §4.1 warning.

> [!NOTE]
>
> One FC setup note described the Mateksys M9N on a UART (`GPS_TYPE2 = 1`). The current baseline puts both units on DroneCAN. Trust the baseline, but if the secondary GPS does not enumerate on CAN, confirm whether your M9N is wired to a UART and adjust `GPS2_TYPE` accordingly.

**Verify:** Two GPS instances reporting, EKF happy, HDOP improving outdoors.

---

## 6. Raspberry Pi Setup

### 6.1 Image the SD card

Use Raspberry Pi Imager for a headless setup:

1. Choose your Pi model, **Raspberry Pi OS Lite (64-bit)**.
2. Set hostname (e.g. `quiver`), timezone, keyboard.
3. Create the user and password. **Record the username**, the Tattu service file needs it later.
4. Enter WiFi credentials so you never need a monitor.
5. Enable **SSH** with password auth.
6. Write the image and insert the card into the RPi.

### 6.2 Physical installation

1. Seat the RPi on the 40-pin connector on the Main PCB.
2. Prepare an Ethernet cable: RJ45 on one end, a 4-pin Phoenix connector on the other to fit **J2**. The spare SIYI 4-wire RJ45 cable works.
3. Use only the two pairs, keeping each twisted pair intact: TX+ / TX- and RX+ / RX-. T568A colors are white-green / green and white-orange / orange, but a SIYI 4-wire cable differs, see the as-built mapping below.

**J2 pinout (Main PCB, switch-side labels) and the as-built cable.** RJ45 100 Mbps Ethernet uses pins 1 = TX+, 2 = TX-, 3 = RX+, 6 = RX-. Ethernet crosses TX to RX, so the Pi's TX pair lands on J2's RX pins:

| J2 Phoenix pin | J2 signal | ← RJ45 pin | first-unit SIYI cable |
|---|---|---|---|
| 1 | `ETH_RX1+` | 1 (TX+) | red |
| 2 | `ETH_RX1-` | 2 (TX-) | white |
| 3 | `ETH_TX1+` | 3 (RX+) | green |
| 4 | `ETH_TX1-` | 6 (RX-) | black |

Keep red + white together (the TX pair) and green + black together (the RX pair). A split pair gives `NO-CARRIER` while the IP still shows set. On the first unit the Phoenix order **red, white, green, black** (pins 1–4) brought eth0 up and pinged `.50` and `.51`.

> [!NOTE]
>
> Main PCB note 0007 labels J2 the "A8 camera Ethernet port for when the HM30 is not installed," but it is electrically a GigaBlox switch port and works for the RPi with the HM30 installed (verified on the first unit).

> [!WARNING]
>
> **Do not connect the RPi Ethernet cable yet.** Configure the static IP first, then plug it in.

> [!IMPORTANT]
>
> **This is a permanent connection, not a setup-only cable.** Once configured, the Pi reaches the drone network only through J2, so it stays plugged in for all operations. The Pi's WiFi cannot see the `192.168.144.x` wired net. **Secure both ends against vibration.** The 4-pin Phoenix at J2 can back out, and losing it in flight drops every companion function (telemetry forwarding, OTA, camera, FC log and MAVLink access). Strain-relief the cable and route it per the harness guide. The only time J2 can be left unplugged is flying without the Pi entirely (pure FC + RC + SIYI), which is not the standard configuration.

### 6.3 Static IP on eth0 (NetworkManager)

Boot the drone, let the RPi come up on WiFi, find its IP in your router, and SSH in. Update first:

```bash
sudo apt update && sudo apt full-upgrade
sudo apt autoremove && sudo apt clean
```

Configure eth0 with a static IP and no gateway, so only 192.168.144.x traffic uses Ethernet and everything else uses WiFi or cellular:

```bash
sudo nmcli con add type ethernet con-name "Drone-Net" ifname eth0
sudo nmcli con modify "Drone-Net" ipv4.addresses 192.168.144.49/24
sudo nmcli con modify "Drone-Net" ipv4.method manual
sudo nmcli con up "Drone-Net"
```

The Pi is **`.49`**, a companion host on the drone subnet. The FC's gateway is the CubeNode at `.50`, not the Pi. Avoid the SIYI-reserved `.20` (Android GCS).

**Now plug in the Ethernet wire between the RPi and the Main PCB.**

**Verify:**

```bash
ip a show eth0          # expect inet 192.168.144.49/24
ping 192.168.144.50     # CubeNode ETH
ping 192.168.144.51     # Flight controller
```

To reach the FC from your laptop over the wired drone net, add the laptop to the Drone-Net network and Mission Planner → TCP connect to `192.168.144.51:5760`. To reach it over WiFi or the internet with no cable, set up the RPi as a Tailscale subnet router (§6.5).

### 6.4 WiFi networks (add and switch)

The Pi reaches the internet over WiFi (`wlan0`), which is what `tailscaled` needs to phone home and what gives you SSH access at the bench. Add a second SSID for a different site or a phone hotspot, and the Pi picks whichever is in range. This uses the same NetworkManager (`nmcli`) as the static eth0 in §6.3, and does **not** touch the `Drone-Net` eth0 connection, which carries the `192.168.144.x` drone net independent of any WiFi.

**Add an SSID.** Scan, connect, and save a profile in one command:

```bash
sudo nmcli device wifi list                                  # SSIDs in range
sudo nmcli device wifi connect "NEW_SSID" password "PASSWORD"
```

For a hidden network add `hidden yes`. To pre-load a profile **without** connecting now (e.g. stage a field hotspot at the bench):

```bash
sudo nmcli connection add type wifi con-name "field" ifname wlan0 ssid "NEW_SSID"
sudo nmcli connection modify "field" wifi-sec.key-mgmt wpa-psk wifi-sec.psk "PASSWORD"
```

**Switch between them.** List the saved profiles, then bring one up:

```bash
nmcli connection show
sudo nmcli connection up "field"        # switch to it now
sudo nmcli connection up "home"         # switch back
```

**Make it automatic (preferred).** All saved WiFi profiles autoconnect. When more than one is reachable, NetworkManager picks the **highest** `autoconnect-priority`:

```bash
sudo nmcli connection modify "home"  connection.autoconnect-priority 10
sudo nmcli connection modify "field" connection.autoconnect-priority 20
```

So the Pi grabs `field` in the field and falls back to `home` at the bench, no manual switching.

> [!WARNING]
>
> **Switching off the SSID you are connected through drops your SSH session.** Do it one of three ways: set `autoconnect-priority` and reboot so the Pi lands on the right one, or switch while you also have a path in over `Drone-Net` / Tailscale, or use a console. After a manual switch, reconnect on the new network's IP. Tailscale (§6.5) keeps working across a switch as long as the new SSID has internet.

### 6.5 Remote access to the FC over WiFi (Tailscale subnet router)

The Pi already has eth0 on the drone subnet and WiFi for internet. Run Tailscale on the Pi and have it **advertise the drone subnet** to your tailnet. Your laptop, on the same tailnet, then routes to the FC through the Pi, so Mission Planner connects to `192.168.144.51:5760` from anywhere, no Ethernet cable to the laptop.

> [!NOTE]
>
> **Confirmed working 2026-06-22.** Tailscale runs on the Pi and Mission Planner on the laptop connects to the FC at `192.168.144.51:5760` over the tailnet. Treat this as the **remote** access path. Its latency is the internet round-trip, so it is not the low-latency link for field monitoring. At the field, connect the PC to the MK32 locally instead (§16.6).

> [!NOTE]
>
> **This does not conflict with QGC on the MK32.** QGC on the MK32 talks to the FC over the SIYI HM30 link (FC SERIAL1 / TELEM1, surfaced at the SIYI ground unit `192.168.144.12:19856`, see §16.6). Tailscale reaches the FC's separate Ethernet TCP server (`NET_P1`, `192.168.144.51:5760`). They are different FC links and ArduPilot serves multiple GCS at once. Tailscale uses `100.64.0.0/10` for tailnet addresses and only *advertises* `192.168.144.0/24`, so it touches none of the SIYI-reserved addresses. The only rule is operational: treat one GCS as the active control station at a time so two stations do not write params or modes on top of each other.

**On the Pi.** Enable IP forwarding (needed for subnet routing), install Tailscale, and bring it up advertising the drone subnet:

```bash
# IP forwarding for the subnet router
echo 'net.ipv4.ip_forward = 1' | sudo tee /etc/sysctl.d/99-tailscale.conf
echo 'net.ipv6.conf.all.forwarding = 1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
sudo sysctl -p /etc/sysctl.d/99-tailscale.conf

# install and start
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up --advertise-routes=192.168.144.0/24 --accept-dns=false
```

`--accept-dns=false` keeps MagicDNS from touching the Pi's own resolver. The `tailscale up` command prints a login URL the first time. Open it and authenticate the Pi into your tailnet.

> [!IMPORTANT]
>
> **Advertising the whole `/24` also routes the SIYI addresses (`.12/.20/.25`) through the Pi for any tailnet client that accepts the route.** That is fine when the laptop is remote. If the laptop is ever *also* on the SIYI network directly at the same time, advertise only the FC instead to avoid a routing overlap: `--advertise-routes=192.168.144.51/32`.

**In the Tailscale admin console** (`login.tailscale.com/admin/machines`):

1. Open the Pi's machine, **Edit route settings**, and **approve** the advertised `192.168.144.0/24` (or `.51/32`) route. Routes are not live until approved.
2. On the same machine, **Disable key expiry** so the Pi stays on the tailnet without a periodic re-login. It is an unattended companion.

**On the laptop (Windows).**

1. Install Tailscale and sign in to the **same tailnet**.
2. Tailscale tray icon → **Preferences → Use Tailscale subnets** (accept routes). On the CLI this is `tailscale up --accept-routes`.
3. Mission Planner → top-right connection dropdown → **TCP** → Connect → Host `192.168.144.51`, Port `5760`.

**Verify:**

```bash
# from the laptop, with Tailscale up
ping 192.168.144.51          # FC, routed through the Pi
```

Then Mission Planner connects over TCP and the full parameter tree downloads (a TCP link is bidirectional, unlike the view-only UDP forward in §16.6). If the ping works but MP does not connect, confirm `NET_P1` is a TCP server on the FC (§4.3: `NET_P1_TYPE = 4`, `NET_P1_PORT = 5760`).

> [!NOTE]
>
> This is the same Tailscale relay the remote flight engineer needs (§16.6). The difference is the source: here the Pi advertises the *Ethernet* path to the FC (`NET_P1` TCP), whereas the §16.6 field-PC pattern relays the *SIYI* MAVLink (`192.168.144.12:19856`). Either can feed a remote MP. The Pi subnet router is simpler because it needs no field PC on the SIYI network, but it depends on the CubeNode PPP link and the FC TCP server being up.

---

## 7. Battery Monitoring

Two monitor instances, reading **different** DroneCAN message types (so they cannot silently swap):

| Instance | Param | Source | Reads |
|---|---|---|---|
| **Bat1** | `BATT_MONITOR = 9` | DroneCAN **ESC** telemetry | HV bus voltage/current as seen by the ESCs (after the SSR) |
| **Bat2** | `BATT2_MONITOR = 8` | DroneCAN **BatteryInfo** | The pack's own smart **BMS**, ahead of the SSR |

On the first unit, **Bat2 is the battery pack's native smart BMS** (DroneCAN node 125, `GBMS063E12`). Confirmed via the UAVCAN Inspector: it reports **14 individual per-cell voltages**, `cell_count = 14`, `design_capacity = 30000` (30 Ah), `state_of_charge`, `state_of_health`, `cycle_count`, and serial — data only the pack's internal BMS can produce. Messages are CUAV format (`cuav_equipment_power_CBAT` + `ardupilot…BatteryInfoAux` + `uavcan…BatteryInfo`), i.e. the pack speaks DroneCAN **natively**.

> [!IMPORTANT]
>
> **The pack's native BMS already provides full battery telemetry on Bat2, so the RPi Tattu bridge (§7.2) is very likely redundant.** `tattu_bridge.py` exists to translate a pack that speaks the *raw* Tattu protocol (CAN ID `0x01109216`) into DroneCAN — this pack does not need that. Confirm with the Quiver team whether the bridge is still required (and whether the deployed pack is Tattu or a CUAV smart battery) before building it. If the bridge is added later, give it its own instance (`BATT3_MONITOR = 8`) and pin both with `BATTx_SERIAL_NUM` so the two BatteryInfo sources do not collide on Bat2.

> [!NOTE]
>
> On a fresh unit, Bat1 has no data until the ESCs are configured (§10) and the SSR is closed (§11). Set the §7.3 parameters now, but expect the §7.1 mapping check and the section Verify to pass only after §10 and §11 are complete.

### 7.1 Verify the Bat1 / Bat2 mapping

Because both read ~55–56 V at idle they look alike — confirm which is which physically:

- **Pull the Battery-PCB↔Main-PCB CAN telemetry cable** (with ESCs powered, SSR closed): `battery_voltage2` (Bat2) drops to 0, `battery_voltage` (Bat1) stays → Bat2 = BMS, Bat1 = ESC. Reconnect.
- **Or open the SSR** (Relay 1 OFF, disarmed, briefly): Bat1 (ESC) drops as the ESCs depower, Bat2 (BMS) stays (it measures the pack ahead of the SSR) → confirms Bat1 = ESC. Re-close Relay 1.
- **Tell-tale:** only Bat2 (the BMS) carries per-cell voltages, SOC %, SOH, and cycle count. Bat1 (ESC) has voltage + current only.

### 7.2 Tattu DroneCAN bridge on the RPi (only if the team confirms it is needed)

Skip this if the pack's native BMS (Bat2 above) is the battery source. Install only for a pack that speaks the raw Tattu protocol rather than DroneCAN.

Install Python and the CAN libraries:

```bash
sudo apt install python3-pip python3-venv -y
mkdir -p ~/tattu_can_bridge
python3 -m venv ~/venv
source ~/venv/bin/activate
pip install python-can dronecan
deactivate
```

Copy `docs/Operations/firmware/tattu-bridge/tattu_bridge.py` to `~/tattu_can_bridge/tattu_bridge.py` on the RPi (SFTP). The script runs as DroneCAN node 110, listens for the Tattu pack, and rebroadcasts `BatteryInfo` on `can0`.

Create the CAN interface service:

```bash
sudo nano /etc/systemd/system/can-setup.service
```

```ini
[Unit]
Description=Setup CAN Interface
After=sys-subsystem-net-devices-can0.device
Requires=sys-subsystem-net-devices-can0.device

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/sbin/ip link set can0 type can bitrate 1000000
ExecStart=/sbin/ip link set can0 txqueuelen 1000
ExecStart=/sbin/ip link set can0 up
ExecStop=/sbin/ip link set can0 down

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable can-setup
```

Create the bridge service (**replace USER with your RPi username**):

```bash
sudo nano /etc/systemd/system/tattu-bridge.service
```

```ini
[Unit]
Description=Tattu Battery to DroneCAN Bridge
After=network.target can-setup.service
Requires=can-setup.service

[Service]
Type=simple
User=USER
WorkingDirectory=/home/USER/tattu_can_bridge
ExecStart=/home/USER/venv/bin/python /home/USER/tattu_can_bridge/tattu_bridge.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable tattu-bridge
sudo systemctl start tattu-bridge
systemctl status tattu-bridge
journalctl -u tattu-bridge -f
ip -details link show can0   # confirm bitrate 1M, no errors
```

### 7.3 Flight controller battery monitor parameters

Bat1 is the ESC monitor; Bat2 is the pack's smart BMS. Recommended Bat2 settings:

| Param | Set to | Base default | Why |
|---|---|---|---|
| `BATT2_MONITOR` | `8` | `9` | DroneCAN BatteryInfo (the pack BMS, node 125) |
| `BATT2_CAPACITY` | `30000` | `3300` | **Fix:** match the 30 Ah pack (BMS reports `design_capacity = 30000`). The `3300` default corrupts Bat2 SoC / mAh. |
| `BATT2_LOW_VOLT` | `46.2` | `48` | 3.3 V/cell, consistent with Bat1 |
| `BATT2_CRT_VOLT` | `44.8` | `0` | 3.2 V/cell, consistent with Bat1 |
| `BATT2_OPTIONS` | `0` | `0` | Leave **"Ignore DroneCAN SoC" (bit 0) CLEAR** so ArduPilot uses the BMS's accurate reported state-of-charge instead of estimating its own. Already `0` — do not set bit 0. |
| `BATT2_SERIAL_NUM` | `-1` | `-1` | Accept any BatteryInfo source; pin to the pack's battery ID only if a second source (e.g. a node-110 bridge) is ever added |

Reboot after changing `BATT2_MONITOR`.

**On `BATT2_OPTIONS` and SoC:** the pack's BMS coulomb-counts and models the cells internally to report a true state-of-charge. `BATT2_OPTIONS` bit 0 ("Ignore DroneCAN SoC"), if set, makes ArduPilot discard the BMS value and estimate its own (less accurate). Keep it clear (`OPTIONS = 0`) to use the real BMS SoC — the reason for having a smart battery.

**Bonus the BMS gives you:** per-cell voltages, SOC %, SOH, cycle count, and **battery temperature** (the Pilot Handbook §1.2.1 ≤56 °C limit) — all visible on Bat2 / in the UAVCAN Inspector, none of which the ESC monitor can produce.

### 7.4 Low-battery failsafe source (decision — align with the Quiver team)

The documented baseline drives the low-battery failsafe from **Bat1 (ESC, voltage-based)** with **Bat2 (BMS) monitor-only** (`BATT2_FS_LOW_ACT = 0`, `BATT2_FS_CRT_ACT = 0`). The first unit's live config currently runs voltage failsafes on **both** instances (`BATT_FS_LOW_ACT = BATT2_FS_LOW_ACT = 2` RTL at 46.2 V, `BATT_FS_CRT_ACT = BATT2_FS_CRT_ACT = 1` Land at 44.8 V, see `params-HOU.param`). But the Pilot Handbook §4.2.1 failsafe is **"≤ 20% → RTL"**, a *state-of-charge* rule, and the BMS reports true SoC while the ESC monitor only coulomb-counts. So the BMS is the more accurate source for that exact rule.

Two options, to be decided with the team (do not flip unilaterally — it changes the documented baseline):
- **Keep baseline:** Bat1 voltage failsafe, Bat2 rich monitor.
- **Move failsafe to Bat2 (BMS, SoC-based):** `BATT2_LOW_MAH = 6000` (20% of 30 Ah) → `BATT2_FS_LOW_ACT = 2` (RTL), `BATT2_CRT_MAH = 3000` (10%) → `BATT2_FS_CRT_ACT = 1` (Land), and set Bat1 monitor-only so they do not double-trigger.

**Verify (§7.3):** Mission Planner Status tab shows two instances; Bat1 (ESC) and Bat2 (BMS) voltages are close when the SSR is closed. Confirm which is which using §7.1 before relying on them.

---

## 8. Remote ID (DroneBeacon db201)

The db201 runs ArduRemoteID on an ESP32 and connects over DroneCAN on CAN1 (shared 1 Mbit bus). The `params-remoteid.param` overlay loaded in §2 sets:

```
DID_ENABLE    = 1
DID_CANDRIVER = 1
DID_MAVPORT   = -1
DID_OPTIONS   = 1     ; bit 0 = EnforcePreArmChecks (see below)
DID_BARO_ACC  = -1
```

> [!NOTE]
>
> **Module board and firmware.** The first unit's module reports its board as **BlueMark db200** running **ArduRemoteID** firmware (the db201 is the same family). Keep the module firmware current. Stale firmware can leave the module healthy on its own WiFi but silent on DroneCAN, which presents as `ODID: lost transmitter` on the flight controller. Update it over the web interface (see §8.3). When working, the module enumerates as a normal DroneCAN node on CAN1 (it came up as **node 123** on the first unit, alongside the GNSS nodes 121 / 119 and the BMS at 125).

### 8.1 Per-operator identity (required before flight / shipment)

Configure in Mission Planner → **DATA → DroneID** tab:

- **UA_TYPE** (aircraft type in BasicID): set to **multirotor**. This is mandatory.
- **UAS ID**: the aircraft's registered serial number.
- **Operator ID**: the operator's CAA / FAA registration number.

Both FAA Part 107 (US) and EASA Open Category (EU) require these to be set. They are per-operator and are not stored in the param files.

> [!IMPORTANT]
>
> `DID_OPTIONS` bit 0 is **EnforcePreArmChecks** (verified against the AP_OpenDroneID source). With `DID_OPTIONS = 1` the FC enforces the full Remote ID arming gate: `UA_TYPE` set in BasicID, operator location received, and a healthy transmitter reporting good-to-arm. So the aircraft pre-arm-fails with `PreArm: OpenDroneID: UA_TYPE required in BasicID` until `UA_TYPE` is set. This is expected and appears on the bench as soon as the overlay is loaded. Setting `DID_OPTIONS = 0` would bypass every Remote ID arming check, which is not an option for compliant flight.

### 8.2 Operator location pre-arm

Remote ID broadcasts **two** independent positions, and they come from different sources:

1. **Drone (UA) location** is the aircraft's own position. The flight controller takes it from its GPS and sends it to the module automatically over DroneCAN, so once the module is on CAN and the FC has a 3D fix there is nothing to set. On the module's web status page the Location line stops reading `REMOTE_ID_SYSTEM_FAILURE (missing location message)` once this is flowing.
2. **Operator location** is where the control station is. It does **not** come from the drone. A GCS with its own position sends it to the flight controller in the `OPEN_DRONE_ID_SYSTEM` MAVLink message, and the FC relays it to the module. Until a GCS supplies it, the FC repeats `ODID: lost operator location`.

So the operator-location pre-arm is cleared by giving your GCS a position source.

**Mission Planner as the operator-location source.** Mission Planner reads a GPS that provides NMEA `GPGGA` / `GNGGA` and sends operator location through its OpenDroneID panel: **DATA → Drone ID** tab (if the tab is missing, right-click the Data view, choose **Customize**, and enable `tabDroneID`, which needs the MP beta). Enter the GPS COM port and baud (`9600`) in the **GCS GPS** fields and click **Connect to Base GPS**. The indicator runs red (no link) to orange (link, no fix) to yellow (fix) to green (DGPS). GPS sources:

- A USB GPS dongle on the laptop, which enumerates directly as a COM port.
- An Android phone over Bluetooth SPP running an NMEA app, which presents a Bluetooth serial COM port.
- An Android phone over **USB**: enable USB tethering, run an app that serves NMEA over TCP (for example Share GPS as a TCP server, or BlueNMEA with `adb forward`), then bridge that TCP stream to a virtual COM port (HW VSP or com0com / com2tcp) and point the GCS GPS field at that COM port. USB needs the bridge because a phone over USB appears as a network interface, not a serial port.

**MK32 (QGC) as the operator-location source.** The MK32 has a built-in GPS, so QGC on it can supply operator location with no tether. Two requirements:

- QGC must have Android **Location permission** and the MK32's location turned on.
- **Application Settings → General → Stream GCS Position = `Always`**, and QGC must have the **Remote ID** feature, shown as an **Application Settings → RemoteID** tab. Only the Remote ID feature emits `OPEN_DRONE_ID_SYSTEM`. Generic position streaming alone does not populate the operator location.

> [!WARNING]
>
> **Stream GCS Position can stall the QGC parameter download on a slow SIYI link.** The first unit's SIYI telemetry link (FC `SERIAL1`, the HM30) runs at **57600 baud** (`SERIAL1_BAUD = 57`). With Stream GCS Position set to `Always`, the continuous outbound position stream saturates that slow link during the bulk parameter download (ArduPilot has ~1300 parameters), so QGC reports it cannot load all parameters. Two fixes:
> - **Quick:** set Stream GCS Position to `Never`, connect and let parameters finish loading, then set it back to `Always`. The steady-state position stream is light and coexists fine once the bulk download is done, but the conflict returns on every reconnect.
> - **Permanent (preferred):** raise the link to **115200** on both ends. Set the SIYI air unit UART to 115200 in the SIYI FPV app, then set FC `SERIAL1_BAUD = 115` to match. Change both ends together, or the link drops. With the faster link, Stream GCS Position can stay `Always` and parameters still load. **This was applied on the first unit (SIYI app to 115200, then `SERIAL1_BAUD = 115` and reboot) and the QGC parameter load completed cleanly afterward.** Note that on the SIYI side, changing the datalink baud reconfigures both the ground unit and the air unit UART over the air, so you set it once.
>
> Also keep only one GCS on the link during a parameter download. Mission Planner connected at the same time contends for the link and produces the same incomplete load.

> [!CAUTION]
>
> **The SIYI MK32 QGC build does not include Remote ID (confirmed on the first unit).** Its Application Settings has **no RemoteID tab**, so it never emits `OPEN_DRONE_ID_SYSTEM` and cannot supply operator location, regardless of Stream GCS Position or the MK32's own GPS fix. The operator-location error came only from Mission Planner, and `ODID: lost operator location` returned the moment the PC disconnected from MP. **Use Mission Planner with a GPS as the operator-location source**, run on a laptop alongside the MK32. MP connects to the FC over Ethernet TCP (`192.168.144.51:5760` via the Pi / tailnet, or the SIYI ground-unit Ethernet) at the same time the MK32 flies, since ArduPilot serves multiple GCS at once. The simplest GPS is a USB u-blox dongle, which enumerates directly as a COM port with no tether or bridge.
>
> Operator location is an **arming requirement** enforced by `DID_OPTIONS = 1` (bit 0 = EnforcePreArmChecks), so this must be working before flight.

There are two ways to supply operator location. Pick by whether you need the SIYI camera in the flying app.

**Laptop-free (SIYI's own recommendation, done on the first unit).** SIYI support confirmed the MK32 apps do not support Remote ID and recommended loading **mainline QGroundControl** on the MK32. Mainline QGC has the Remote ID feature and sends operator location from the MK32's own GPS. This is the sanctioned path on the first unit.

1. Sideload the official QGroundControl Android APK onto the MK32. It installs alongside the SIYI apps.
2. In the **SIYI TX** app (the settings app, not QGC): **Datalink** → set **Connection = `UDP`**, **Flight Controller = `PIX / PX4 / Ardupilot`**, and **baud = `115200`** to match the FC's `SERIAL1_BAUD`. Connection must be `UDP`, otherwise the internal app holds the link and QGC sees nothing.
3. In QGC, **Application Settings → Comm Links → Add**: Type `UDP`, **Port `19856`**, leave Server Addresses empty, check Automatically Connect on Start. The SIYI datalink pushes telemetry to UDP `19856`. Mainline QGC only auto-listens on `14550`, so the default link finds nothing. **Delete or disable QGC's default 14550 link** so it does not fight the connection, then Connect the new one.
4. Grant QGC **Location** permission, then Application Settings → **RemoteID** and set Region, UAS ID, and Operator ID.
5. Bench-check with props off: the sticks still fly the aircraft, because the MK32 sends RC over the SIYI radio link independent of the GCS app. Confirm QGC shows a GCS GPS fix.

The trade-off is that mainline QGC does not have SIYI's in-app A8 Mini video and gimbal control.

> [!NOTE]
>
> **Confirmed on the first unit (2026-07-07):** with mainline QGC connected over the SIYI datalink and **Application Settings → General → Stream GCS Position = `Always`**, `ODID: lost operator location` clears. The RemoteID feature that the SIYI QGC fork lacks is what makes this work. The full Remote ID chain is now closed: transmitter (db200 on CAN1), drone location (FC GPS over DroneCAN), and operator location (mainline QGC on the MK32).

**With SIYI camera integration.** Fly on the SIYI QGC or UniGCS app for the camera, and run **Mission Planner with a GPS** on a laptop at the same time for operator location, using the steps above. ArduPilot serves both ground stations at once.

> [!NOTE]
>
> **The satellite count shown on the QGC screen is the drone's GPS, not the controller's.** QGC's toolbar sat count is the vehicle GPS reported over telemetry from the FC. The operator location uses the control station's *own* GPS, a separate receiver. On the MK32 that is the handheld's internal GPS, and on a laptop it is the GCS GPS in §8.2. Seeing satellites on screen confirms the drone is located, not the operator.

**Verify:** A BLE scan with a Remote ID scanner app (OpenDroneID / DroneScanner) shows UAS ID, Operator ID, and operator location broadcasting. The "Unknown" manufacturer field is expected and has no compliance impact.

### 8.3 Module not communicating over DroneCAN (`lost transmitter`)

If the flight controller repeats `ODID: lost transmitter` while the module is reachable and healthy on its own RID WiFi access point, the module is powered but not on the CAN bus. On the first unit the cause was stale module firmware (db200 firmware 1.13) whose CAN was not working: the module showed no DroneCAN node in Mission Planner's DroneCAN/UAVCAN list and put no DroneCAN frames on the bus, even though it was on a CAN port and powered.

**Fix that worked on the first unit:**

1. Connect to the module's RID WiFi access point (SSID `RID_xxxx`, password `ArduRemoteID`) and open its web interface at `http://192.168.4.1`.
2. Download the current release from <https://github.com/ArduPilot/ArduRemoteID/releases>. The file for the web updater is **`ArduRemoteID_BLUEMARK_DB200_OTA.bin`** (the `_OTA` variant is the app image the web updater expects, the plain `ArduRemoteID-BLUEMARK_DB200.bin` is the full image for serial flashing below). The first unit went from 1.13 to 1.14 this way on 2026-06-29. Use the web **Firmware Update** box to flash it.
3. **Power-cycle the aircraft.** A DroneCAN node only brings up its CAN interface at boot.

**Untested fallback (not yet done on any unit).** If the web interface does not respond (the AP hands out a DHCP lease and `192.168.4.1` pings but port 80 times out, which the first unit showed on 2026-06-25 before the web UI came back on its own), the documented recovery per the BlueMark manual and the ArduRemoteID README is a serial reflash: remove it from the airframe, connect a 3.3 V USB-UART, hold the download button while connecting (pogo-pin clamp, see the BlueMark manual at <https://download.bluemark.io/db200.pdf>, Fig. 4), and flash the full image `ArduRemoteID-BLUEMARK_DB200.bin` (not the `_OTA` file) with esptool (chip `esp32c3`). A serial reflash also wipes a corrupt config and restores the web server. If neither path brings back the web UI and node 123, contact BlueMark (`info@bluemark.io`) for RMA.

Reseating the cable or power-cycling alone did **not** fix it. The firmware update did. After the update and power cycle the module joined CAN1 (node 123) and `ODID: lost transmitter` cleared, leaving only the operator-location item in §8.2.

> [!NOTE]
>
> When chasing a module that is healthy on WiFi but silent on CAN, update its firmware before chasing wiring. Confirm the connector is on a CAN port and not the UART port (the module has two CAN ports and a UART port in identical JST-GH housings), but if frames are still absent after a confirmed CAN connection, suspect the firmware.

Detail: `docs/Engineering-Reports/Dev-Kit-Engineering-Report.md` §Remote ID Integration.

---

## 9. Obstacle Avoidance (optional)

Load `parameters/params-object-avoidance.param` to enable BendyRuler avoidance. Key behavior: slow-down at 5 m, hard stop at 4 m.

This unit carries **two** obstacle sensors:

| Sensor | Param | Bus | Notes |
|---|---|---|---|
| RPLidar S2 (360°, top) | `PRX1_TYPE = 5` | SERIAL5 (TELEM3) @ 1 Mbaud | `SERIAL5_PROTOCOL = 11`, `SERIAL5_BAUD = 1000`, `PRX1_YAW_CORR = 180` for cable-forward mounting. (Older copies of the base file said SERIAL3, patched to SERIAL5 2026-06-25, see §9.1.) |
| NanoRadar MR82 (forward) | `PRX2_TYPE = 17`, `PRX2_RECV_ID = 2` | CAN2 RadarCAN | Radar set to **CAN ID 2**. RadarCAN already enabled via `CAN_D2_PROTOCOL2 = 14`. See §9.2. |

The downward **NanoRadar NRA15** altimeter shares the same RadarCAN bus (CAN2) as the MR82 and is the rangefinder, set to **CAN ID 1**: `RNGFND1_TYPE = 39` (NRA24_CAN), `RNGFND1_RECV_ID = 1`, `RNGFND1_ORIENT = 25` (down).

> [!IMPORTANT]
>
> The MR82 and NRA15 ship from the factory **both at CAN ID 0**, so they transmit identical CAN message IDs and **collide on the bus**. On ArduPilot, the proximity driver claims every RadarCAN frame it sees and starves the rangefinder, so the down rangefinder reads nothing whenever the forward radar is enabled. You **must** give the two devices distinct CAN IDs and matching receive-ID filters. The one-time procedure is in **§9.2**. After it is done: `RNGFND1_RECV_ID = 1` (NRA15) and `PRX2_RECV_ID = 2` (MR82).

> [!NOTE]
>
> The intermittent RPLidar behavior (turret spin-up then coast-down, `RPLidar UNKNOWN`) was traced to **two** causes, both now fixed: the wrong serial port (§9.1) and a firmware gap missing the S2 driver (resolved by PR #230, see §1 and §15). The lidar now holds a steady scan. Avoidance is still unflown on this airframe, so treat it as experimental and never rely on it as a primary safety layer until validated in flight.

**Verify:** Mission Planner proximity radar view shows returns from both the 360° RPLidar and the forward MR82, and the Status tab shows `rangefinder1` tracking ground distance from the NRA15.

### 9.1 Bench-check log — RESOLVED 2026-06-17

**The 360° lidar holds a stable scan.** There were **two** root causes, both fixed: (1) a wrong serial-port assignment (the lidar is on SERIAL5, not SERIAL3 — see below), and (2) a firmware gap (the shipped build lacked the RPLidar S2 driver from ArduPilot PR #31663 — fixed by PR #230, see §1 and §15). The sensor itself was always healthy. Several intermediate theories during the debug (MOTOCTL, S2-vs-S2L) were wrong and are listed at the end so they are not repeated.

**Lidar:** RPLidar **S2** (base label `S2M1-R2`) — the full 30 m (white) / 10 m (black) S2, not an S2L or C1. TTL UART 1 Mbaud 8N1, XH2.54-5P connector.

#### Root cause: the lidar is on SERIAL5, not SERIAL3

The lidar is physically wired to the **TELEM3 connector**, which on the Pix32 V6 / Pixhawk6C target is **USART2 = ArduPilot SERIAL5**. But the loaded params (and the firmware docs) put Lidar360 on **SERIAL3**, which is `USART1` = the **GPS1** connector — empty on this aircraft because the GPS runs on DroneCAN. So the scan command went out a connector with nothing on it, and the lidar never received it.

Pix32 V6 / Pixhawk6C serial map (verified against the ArduPilot hwdef and the Holybro baseboard doc):

| ArduPilot | STM32 | Connector |
|---|---|---|
| SERIAL1 | UART7 | TELEM1 |
| SERIAL2 | UART5 | TELEM2 (PPP to CubeNode) |
| SERIAL3 | USART1 | GPS1 |
| SERIAL4 | UART8 | GPS2 |
| **SERIAL5** | **USART2** | **TELEM3 ← lidar is here** |
| SERIAL6 | USART3 | FMU debug |

**Fix (pure param, no rewiring):**

```
SERIAL5_PROTOCOL = 11      Lidar360
SERIAL5_BAUD     = 1000    1,000,000 baud
SERIAL3_PROTOCOL = -1      free the empty GPS1 port
```

Leave `PRX1_TYPE = 5`, `PRX1_ORIENT = 0`, `PRX1_YAW_CORR = 180`.

> [!WARNING]
>
> **The firmware docs originally had this wrong.** `standard-params.param` was corrected 2026-06-25 (SERIAL5 with `SERIAL3_PROTOCOL,-1`), and the prose in `docs/Operations/firmware/index.md` now says SERIAL5, but as of 2026-07-07 the index.md parameter table still lists `SERIAL3_PROTOCOL,11`. For this hardware the lidar is on **SERIAL5** (the TELEM3 connector). Any unit configured from an old copy of those files hits this blocker, so if the lidar is silent, check which serial port carries `SERIALx_PROTOCOL = 11` first.

#### U5 connector is mirrored, and the pinout for this unit

The Quiver FC-PCB lidar connector (**U5**) pinout is **mirrored** relative to the RPLidar's standard connector, so the cable must be **flipped / re-pinned** to mate. Pinout as read off this unit's cable — note RX/TX map to the opposite colors from the generic datasheet:

| Pin | Wire | Signal | Connects to |
|---|---|---|---|
| 1 | Red | VCC (5 V) | VCC |
| 2 | Yellow | **RX** (lidar in) | **FC TX** |
| 3 | Green | **TX** (lidar out) | **FC RX** |
| 4 | Black | GND | GND |
| 5 | Blue | MOTOCTL | **leave NC** |

Working crossover: **FC TX → Yellow, FC RX → Green.**

> [!NOTE]
>
> **MOTOCTL (pin 5, blue) is left unconnected and the lidar works fine.** It does not need to be tied high. The S2's motor follows the host scan command, not MOTOCTL — once the scan command reaches the lidar on SERIAL5, it spins and streams with pin 5 floating.

#### How it was found

Voltmeter readings at the connector were unreliable and led to several wrong conclusions. What worked was sniffing the FC's serial TX directly with the SLAMTEC USB-TTL adapter and `pyserial` at 1 Mbaud: set a candidate `SERIALn_PROTOCOL = 2` (MAVLink), `SERIALn_BAUD = 1000`, reboot, and find which physical connector pin streams `fd` packets — that is the live port. The baud must match (`1000` = 1 Mbaud) or the bytes read as garbage `00`s. Validate the adapter with a loopback first (short its own TX to RX).

#### Corrected wrong theories (do not repeat)

- *"Params are correct on SERIAL3."* No — the lidar is on SERIAL5.
- *"MOTOCTL must be tied high to spin."* No — left NC works fine; the motor follows the scan command.
- *"The firmware predates the S2 patch."* ✅ **This suspicion was correct — CONFIRMED and FIXED.** The shipped build (git `977fd8e`) did not include PR #31663's S2 support, so a standard S2 (model byte `0x71`, fw 1.1) was detected as `RPLidar UNKNOWN hw=18 fw=1.1` and never locked: the turret spun up, streamed briefly, then coasted down on a loop. Proven by flashing the rebuilt firmware (PR #230, git `20622a39`, built from current master which carries #31663) — the same hardware then boots `RPLidar S2 hw=18 fw=1.1` and holds a steady scan. The SERIAL5 fix above was necessary but **not sufficient on its own**; both fixes were needed. (Earlier in the debug this was wrongly dismissed, then over-asserted before it was actually verified — it is now confirmed on hardware.) See §1 and §15.

#### Forward + down radars

With the lidar up, verify the other two OA sensors: the forward **MR82** (`PRX2_TYPE = 17`) shows a forward arc in the proximity viewer, and the down **NRA15** (`RNGFND1_TYPE = 39`, `RNGFND1_ORIENT = 25`, range 0.7–90 m) shows on the Status tab as `rangefinder1`. Both share CAN2 RadarCAN (`CAN_P2_DRIVER = 2`, `CAN_P2_BITRATE = 500000`, `CAN_D2_PROTOCOL = 1`, `CAN_D2_PROTOCOL2 = 14`) with **distinct CAN IDs: NRA15 = 1, MR82 = 2** (see §9.2 for how they were assigned). Note `PRX2_TYPE` gets set to `0` during lidar-isolation testing — set it back to `17`.

---

### 9.2 Assigning distinct CAN IDs to the two NanoRadar sensors

The forward **MR82** (proximity) and the downward **NRA15** (rangefinder) both ship at **CAN ID 0**, so they broadcast on identical CAN message IDs and collide on CAN2. ArduPilot's shared-CAN dispatch hands each frame to the first driver that accepts it, and the proximity driver with `PRX2_RECV_ID = 0` accepts *every* frame — so it swallows the rangefinder's data and `rangefinder1` reads nothing. The fix is to give each radar a unique CAN ID and set each driver to listen only for that ID:

- **NRA15 → CAN ID 1** → `RNGFND1_RECV_ID = 1`
- **MR82 → CAN ID 2** → `PRX2_RECV_ID = 2`

The CAN IDs are stored in each radar's own flash (not in ArduPilot parameters). You set them by sending raw CAN frames to each device once. This is a one-time hardware setup.

> [!NOTE]
>
> A NanoRadar's message IDs are `base + (CAN_ID × 0x10)`. Status `0x60A`, target-status `0x70B`, target-info `0x70C` at ID 0 become `0x61A / 0x71B / 0x71C` at ID 1, `0x62A / 0x72B / 0x72C` at ID 2, and so on. The two product lines also use **different configuration protocols** (NRA-series vs MR-series), so the set-ID command differs between them.

#### Step 1 — open a writable SLCAN port on the flight controller

Raw CAN writes require a real SLCAN port. (CAN-over-MAVLink forwarding can read the bus but cannot transmit on this board.)

```
SERIAL7_PROTOCOL = 22      dedicate the second USB serial endpoint to SLCAN
CAN_SLCAN_CPORT  = 2       bridge SLCAN to CAN2 (the radar bus)
```

Reboot. The flight controller now enumerates **two USB COM ports**: the lower number stays MAVLink (Mission Planner), the higher number is a dedicated SLCAN port. Connect your SLCAN tool (a pyserial script, or the DroneCAN GUI Tool's interactive console) to the SLCAN port at the CAN2 bitrate (500 kbit). The radars are not DroneCAN, so they will not appear in any node list — that is expected; you are sending raw frames.

#### Step 2 — set the NRA15 to CAN ID 1 (NRA-series protocol)

The NRA24/NRA15 config message is at `0x200`, and **the device's config address moves with its ID**, so the *save* command must go to the new address:

| Action | CAN ID | Data (8 bytes) |
|---|---|---|
| Set Sensor ID = 1 | `0x200` | `81 01 00 00 00 00 00 00` |
| Save to flash | `0x210` | `FF 00 00 00 00 00 00 00` |

The radar acknowledges on `0x410` with byte 0 bit 7 = 1 on success. **Power-cycle the NRA15** (unplug its connector briefly), then confirm on the bus that its frames now appear at `0x61A / 0x71B / 0x71C` (ID 1).

#### Step 3 — set the MR82 to CAN ID 2 (MR-series protocol)

The MR72/MR76/MR82 use a Continental-style `RadarCfg` message at `0x200`: Sensor ID is byte 4 bits 0–2, gated by the `SensorID_valid` bit (byte 0 bit 1); writing to flash is the `StoreInNVM` bit (byte 4… see below) gated by `StoreInNVM_valid` (byte 0 bit 7). Send one frame to the MR82's current config address (`0x200`, since it is still at ID 0):

| Action | CAN ID | Data (8 bytes) | Meaning |
|---|---|---|---|
| Set Sensor ID = 2 + store | `0x200` | `82 00 00 00 02 80 00 00` | byte0 `0x82` = SensorID_valid + StoreInNVM_valid; byte4 `0x02` = Sensor ID 2; byte5 `0x80` = StoreInNVM |

Only the two `*_valid` bits are set, so no other radar setting (output type, power, max range) is touched. **Power-cycle the MR82**, then confirm its frames now appear at `0x62A / 0x72B / 0x72C` (ID 2).

> [!TIP]
>
> To test the MR82 ID change without writing flash first, send `02 00 00 00 02 00 00 00` to `0x200` (SensorID_valid only, no store). The ID changes in RAM and reverts on power-cycle — useful to confirm the frame is correct before persisting.

#### Step 4 — restore the serial port and set the ArduPilot filters

```
SERIAL7_PROTOCOL = 2       return the USB port to MAVLink (releases SLCAN)
CAN_SLCAN_CPORT  = 0
RNGFND1_RECV_ID  = 1       rangefinder listens only to the NRA15 (ID 1)
PRX2_TYPE        = 17      forward proximity = MR82
PRX2_RECV_ID     = 2       proximity listens only to the MR82 (ID 2)
```

> [!IMPORTANT]
>
> **`PRX2_RECV_ID` only takes effect after a reboot.** Write it, confirm it reads back as `2`, then reboot. If it is left at `0`, the proximity driver reverts to accept-any and starves the rangefinder again.

#### Verify

On the Status tab, `rangefinder1` tracks ground distance from the NRA15 **and** the proximity viewer shows the forward MR82 arc **at the same time**. Both now coexist on CAN2 with no collision.

---

## 10. ESC Node Configuration (if motors were never set up)

> [!CAUTION]
>
> **ROOT CAUSE on the first unit was CAN bus termination, not protocol.** The X6-Plus-G2 ESCs are DroneCAN devices and need **no DataLink box and no protocol conversion**. They have **no internal 120 Ω terminator** (Hobbywing manual: "CAN terminal resistor: None… should be added on the FC side"), so without proper bus termination the 1 M CAN signals reflect and corrupt, and the ESCs never enumerate — even though other CAN devices (GPS, CubeNode, GBMS) happen to work. **If the ESCs do not show up, check CAN termination first.**

> [!IMPORTANT]
>
> **Two prerequisites live in other sections. Do them before starting §10:**
> 1. **Manual SSR control (§11.3).** Every step below needs the SSR closable (the ESCs are unpowered until it closes), and every reboot reopens it. Configure `RELAY1_FUNCTION` / `RELAY1_PIN` / `RELAY1_DEFAULT` per §11.3 first.
> 2. **An SLCAN port on CAN1 for the DroneCAN GUI Tool.** Set `SERIAL7_PROTOCOL = 22` (the FC's second USB COM port becomes a dedicated SLCAN endpoint) and `CAN_SLCAN_CPORT = 1` (bridge to CAN1), then reboot. §9.2 uses the same bridge with `CAN_SLCAN_CPORT = 2` for the radar bus. When all CAN work is finished, restore `SERIAL7_PROTOCOL = 2` and `CAN_SLCAN_CPORT = 0`.

### 10.1 Fix CAN bus termination first (do this before anything else)

CAN requires a 120 Ω terminator at **each** end of the bus, so a healthy bus measures **~60 Ω** across CAN-H / CAN-L (two 120 Ω in parallel). The X6-Plus-G2 ESCs have **no internal terminator**, so if the bus is under-terminated their high-speed signals reflect and corrupt and they never enumerate.

1. **Power down. Measure resistance across CAN1 H–L** with a multimeter.
   - **~60 Ω** → correctly terminated, good.
   - **~120 Ω** → only one terminator present.
   - **Open / very high** → no termination.
2. **If it is not ~60 Ω, enable the termination resistor on the Main PCB** for the CAN1 segment until the bus measures ~60 Ω. On the first unit the ESCs would not enumerate at all until this was added (diagnosed by Julius).
3. Power back up, SSR closed — the ESCs are now reachable.

> [!NOTE]
>
> **Earlier misdiagnosis (corrected):** the symptoms — ESCs powered, wiring correct, FC transmitting `com_hobbywing_esc_GetEscID`/`RawCommand` but zero ESC reply at 1 M and 500 k — were wrongly blamed on a "HWCAN default needing a DataLink box." With termination fixed, the ESCs enumerate normally over DroneCAN. The G2 manual's `HWCAN + DroneCAN` refers to telemetry data formats, not a throttle protocol you must switch. **No box is required.**

### 10.x Reference: the original (wrong) diagnostic ladder

On the first unit the ESCs were powered but never appeared on CAN. The following was eliminated but led to the wrong conclusion (the real cause was termination, above):

| Checked | Result |
|---|---|
| Power | SSR closed (BC PCB LED 5), ESC beep gets louder at full voltage = powered |
| Wiring | Verified correct; the GBMS shares the same Bat_PCB→J43 segment and enumerates fine, so the CAN segment is electrically healthy |
| Baud | Tested at both 1 M and 500 k (factory default) |
| FC side | UAVCAN Inspector shows the FC transmitting `com_hobbywing_esc_GetEscID` (1 Hz) and `com_hobbywing_esc_RawCommand` (394 Hz) — correctly hailing Hobbywing DroneCAN ESCs |
| ESC reply | **None.** No `uavcan.protocol.NodeStatus`, no `com_hobbywing_esc_StatusMsg` at either baud, with SSR closed |

The reasoning "no `NodeStatus` therefore not DroneCAN therefore needs conversion" was **wrong**. With bad termination the ESC replies were corrupted on the wire, so nothing valid reached the FC. The continuous beep was the "throttle signal lost" alarm because the ESC never received clean throttle frames. Fixing termination (§10.1) resolved all of it — no protocol change, no box.

### 10.2 Configure the ESCs (DroneCAN GUI Tool, no box)

With termination fixed, the factory ESCs are DroneCAN devices reachable at their default **500 kbaud, node/throttle ID 1**.

> [!IMPORTANT]
>
> **The golden rule: only the ONE ESC you are configuring may be on CAN1.** All four ship at node ID 1, so any two un-configured ESCs on the bus together collide and **flicker in and out** of the Hobbywing panel — and a save attempted while it is flickering will not stick. Disconnect everything else from CAN1: the other three ESCs' CAN leads (yellow/gray/green), **`J43`** (the Bat_PCB connector that carries the other ESCs and the GBMS onto CAN1), and the other CAN1 devices (J7, J9, J20, J35). The ESC being configured must be the only node-1 device on the bus.
>
> **This rule applies to RE-configuration too, not just first setup.** The Hobbywing panel's Set buttons **broadcast to every ESC on the bus** — they do not target the selected row. Attempting to renumber ESCs on a shared bus (confirmed on the first unit, 2026-06-11) assigns the same ID to all four at once, putting them all back in node-1 collision. Recovery is this same one-at-a-time procedure.

**Motor numbering:** assign ThrottleID/NodeID strictly per the **§0 Motor numbering and orientation** table (ArduPilot QuadX: 1 front-right, 2 rear-left, 3 front-left, 4 rear-right). **Not** the Main PCB silkscreen — see the §0 warning.

**Per ESC, for motors 1–4:**

1. **Power down.** Connect **only this ESC's** CAN leads to CAN1; leave the other three ESCs' CAN leads, `J43`, and the other CAN1 devices unplugged.
2. Set `CAN_P1_BITRATE = 500000` (factory baud), Write, reboot, **re-close Relay 1 (LED 5)**.
3. DroneCAN GUI Tool v1.2.25+ → SLCAN → **Panels → Hobbywing ESC Panel**. Confirm the ESC shows **steadily** (not flickering). If it flickers, another node-1 device is still on the bus — fix that first.
4. Set **Node ID = Throttle ID = this motor's number**, **Baudrate = 1,000,000**. **Save** — only while it is showing steadily. `ThrottleID` **must** match the ArduCopter quad-X motor number for this ESC's physical position.
5. Power down, unplug this ESC's CAN, move to the next ESC, repeat.

**After all four are configured:**

6. Reconnect **all four** ESC CAN leads, `J43`, and the other CAN1 devices (J7, J9, J20, J35).
7. Set `CAN_P1_BITRATE = 1000000`, Write, reboot, **re-close LED 5**.
8. All four enumerate on CAN1 as nodes 1–4 with telemetry, `Bat1` (ESC) comes alive on the Status tab, and the beeping stops (each ESC now receives throttle addressed to its ID).
9. Mission Planner → **Setup → Motor Test** (props OFF, SSR closed) — each test letter spins one motor. Verify the **correct physical motor and rotation direction**. Wrong motor → fix that ESC's `ThrottleID`; wrong direction → reverse it in the ESC settings.

> [!NOTE]
>
> **Recurring trap:** every reboot reopens the SSR (`RELAY1_DEFAULT = 0`), browning out the ESCs and dropping their telemetry. **Re-close Relay 1 (LED 5) after every reboot** until the auto-engage Lua script (§11.4) is installed. Also: telemetry showing but the ESC **still beeping** means it has comms but no throttle addressed to it yet — that clears once its `ThrottleID` is set.

### 10.3 G2-specific tuning (apply once on DroneCAN)

All three are manufacturer recommendations from the **Hobbywing XRotor X6-Plus-G2 manual**.

- **`MOT_SPOOL_TIME = 2`** and **`TKOFF_SLEW_TIME = 2`** — the G2 holds a ~400 ms low-speed startup delay to fling the folding props open. Per the manual (*Protection Functions → Startup delay protection*): *"the automatic delay of the flight controller needs to be adjusted. Otherwise, it may lead to issues such as catapult takeoff of the UAV. For example, for the open-source Ardupilot, modify the MOT_SPOOL_TIME and TKOFF_SLEW_TIME to 2s."* The base file ships `MOT_SPOOL_TIME = 0.5` — **bump to 2** (this is a safety item). `TKOFF_SLEW_TIME` is already 2.
- **CAN idle throttle ~6%** (`MOT_SPIN_ARM ≈ 0.06`) — manual (*Precautions*): *"When using CAN digital throttle, it is recommended to set the idle throttle of the flight controller to 6%."* The base file's `MOT_SPIN_ARM = 0.07` (7%) is effectively already there.
- The G2 has **no internal CAN terminal resistor** (manual: *"CAN terminal resistor: None… should be added on the FC side"*) — see the §10.1 termination check.

The note `task-grant-bounty/pt3/flight-controller/0002-flight-controller-setup` covers the DroneCAN GUI Hobbywing config, but it predates the one-ESC-at-a-time golden rule. Where the note and §10.2 differ, follow §10.2.

### 10.4 LED color (orientation lighting)

**Confirmed working on the first unit (2026-06-11).** The X6-Plus-G2 has no physical LED switch and ships **green** on all four arms, which gives the pilot no orientation cue. On Quiver the ESCs run CAN throttle, so the manual's throttle-stick procedure (manual §11.1) cannot reach them, and there is no DataLink V2 box on the bench. None of the GUI front ends work either:

- Mission Planner's DroneCAN screen shows the ESC nodes but cannot write Hobbywing parameters.
- The DroneCAN GUI Tool **Hobbywing ESC Panel** exposes Baudrate/IDs/Direction/MsgRates only, no LED field.

The LED is set with Hobbywing's custom DroneCAN service **`com.hobbywing.esc.SetLED`** (service ID 212, in the standard DSDL set, so pydronecan already knows it), sent from the DroneCAN GUI Tool's **interactive console**.

**Color scheme — aviation navigation lights.** No LED convention exists in the Pilot Handbook, so Quiver uses nav-light colors judged from the pilot's perspective (standing behind the aircraft, facing the same direction as the nose): **port (left) arms red, starboard (right) arms green.**

The `color` field is an **RGB bitmask** (R=4, G=2, B=1 — so white=7, off=0), *not* the 1–5 enum in the Hobbywing manual's transmitter table:

| Node | Position | Color | `color` value |
|---|---|---|---|
| 1 | Front-right | Green | 2 |
| 2 | Rear-left | Red | 4 |
| 3 | Front-left | Red | 4 |
| 4 | Rear-right | Green | 2 |

**Procedure (all four ESCs stay on the bus, they have unique node IDs after §10.2):**

1. DroneCAN GUI Tool → SLCAN COM port → 1000000 baud → **Tools → Interactive console**.
2. If the console floods with `TransferError: Toggle bit value 32 incorrect` (the Hobbywing status frames trip pydronecan's parser, harmless), silence it first:

   ```python
   import logging; logging.getLogger('dronecan_gui_tool.main').setLevel(logging.CRITICAL)
   ```

3. Enter these one line at a time (multi-line pastes lose their indentation in the console):

   ```python
   cb = lambda nid, e: print(nid, e.transfer.payload if e else 'timeout')
   request(dronecan.com.hobbywing.esc.SetLED.Request(option=1, color=2, blink=0), 1, partial(cb, 1))
   request(dronecan.com.hobbywing.esc.SetLED.Request(option=1, color=4, blink=0), 2, partial(cb, 2))
   request(dronecan.com.hobbywing.esc.SetLED.Request(option=1, color=4, blink=0), 3, partial(cb, 3))
   request(dronecan.com.hobbywing.esc.SetLED.Request(option=1, color=2, blink=0), 4, partial(cb, 4))
   ```

   `option=1` saves to the ESC's flash, `blink=0` is solid. Each request prints an echo of the accepted settings and the arm LED changes immediately.

4. Power-cycle and confirm the colors held: left arms red, right arms green, judged facing the same direction as the nose.

> [!NOTE]
>
> LED colors are stored per ESC and travel with the physical unit, not with the node ID. If ESCs are ever renumbered (§10.2), re-check the colors afterward.

---

## 11. SSR and Relay Output Configuration (CRITICAL — before any motor load)

The high-voltage main power path is gated by a Solid State Relay (SSR). Until the SSR closes, the aircraft runs only through the pre-charge resistor, which cannot carry motor current. **Do not run motor test or any sustained load until the SSR is configured, closable, and confirmed closed.**

### 11.1 How it works

1. The BC PCB pre-charge pushbutton brings up the Main PCB 5V/12V regulators and boots the FC. The pre-charge resistor partially fills the ESC bulk capacitors to limit inrush, but cannot carry motor current.
2. The SSR (Main PCB U3 plus the BC PCB main-power SSR) bypasses the pre-charge resistor to connect the full HV bus. Its control input is the FC signal **IO_CH5 (`SSR_S`)**, with `IO_CH6` / `SSR_S2` as a redundant path.
3. ArduPilot maps `RELAY1` to the GPIO pin driving that signal. Setting Relay 1 high closes the SSR. In Mission Planner this is the **Servo/Relay** page button.
4. The auto-engage Lua script automates step 3: on boot it waits a short delay then calls `relay:on(0)` to close the SSR so the pilot does not press the button manually.

### 11.2 Current state on the first unit (must fix)

The baseline param set ships with the SSR control unconfigured. This is a baseline defect: the handbook assumes auto-engage works, but the published config does not enable it.

- `SCR_ENABLE = 0` — scripting is disabled, so no script can run.
- `RELAY1_FUNCTION` … `RELAY6_FUNCTION` all `= 0` — no relay outputs configured, so neither manual nor automatic SSR control exists yet.
- The auto-engage script `relay_delayed_close.lua` is now committed at `docs/Operations/firmware/scripts/relay_delayed_close.lua`. It closes Relay 1 (index 0) 12 seconds after boot.

### 11.3 Configure manual SSR control (do this first)

```
RELAY1_FUNCTION = 1     ; Relay
RELAY1_PIN      = 105   ; IO_CH5 (SSR_S), confirmed correct for the Dev-Kit Main PCB
RELAY1_DEFAULT  = 0     ; SSR starts open
```

Set `RELAY1_FUNCTION = 1` first and reboot, then `RELAY1_PIN` and `RELAY1_DEFAULT` (dependent params that only appear after the relay is enabled). `SERVO_GPIO_MASK = 65520` already includes output 5 (IO_CH5), so pin 105 is GPIO-capable with no further change.

**Verify (powered, props off):** On the Mission Planner Servo/Relay page, toggle Relay 1.

- **Most reliable early indicator:** **LED 5 (`SSR Signal`)** on the Battery Control PCB toggles with the SSR control signal. Confirmed on the first unit — watch BC PCB LED 5 change state as you toggle Relay 1.
- The Bat1-vs-Bat2 voltage method (Bat1 `ESC` rises to meet Bat2 when the SSR closes) **only works once ESC DroneCAN telemetry is alive** (after §10 ESC configuration). Before the ESCs are configured, `BATT_MONITOR = 9` has no data and Bat1 will not reflect SSR state, so use the BC PCB LED or a multimeter on the HV bus instead.

Watch the avionics PCB / pre-charge resistor temperature if the SSR is left open while the ESCs draw from pre-charge.

### 11.4 Auto-engage script (after manual control works)

**Confirmed installed and working on the first unit (2026-06-10).** The SSR now closes automatically ~12 s after every boot, with no manual Relay 1 toggle.

The script is `docs/Operations/firmware/scripts/relay_delayed_close.lua`. It calls `relay:on(0)` (Relay 1 = SSR) 12 seconds after boot, which gives the FC time to boot and pre-charge to settle. The script only acts on `RELAY1`, so §11.3 must be done first or it does nothing.

Once Relay 1 reliably closes the SSR manually:
1. Set `RELAY1_DEFAULT = 0` so the SSR starts open and the script is what closes it.
2. Copy `relay_delayed_close.lua` into `APM/scripts/` on the FC SD card (pull the card and copy, or upload via MAVFTP).
3. Set `SCR_ENABLE = 1`, reboot.
4. Confirm ~12 s after boot: GCS prints `Relay 1 closed (SSR enabled) after 12s delay` and LED 5 closes, with no manual relay toggle. Reboot once more without touching Relay 1 to confirm it auto-closes every boot.

> [!NOTE]
>
> Do not set `SCR_ENABLE = 1` until the `.lua` file is actually on the SD card, or the FC logs a script-not-found error each boot. This is why the baseline keeps `SCR_ENABLE = 0`. Once the script ships on every unit's SD card, the baseline should set `RELAY1_FUNCTION = 1`, `RELAY1_PIN`, `RELAY1_DEFAULT = 0`, and `SCR_ENABLE = 1`.

The remaining relay outputs (Relay 2–6: Bypass, Add HV, P1 Sig, P1 12V, 12V Pay per Pilot Handbook §2.8.5) also need `RELAYx_FUNCTION` and `RELAYx_PIN` set against the PCB pinout if those functions are used.

### 11.5 Kill switch (RC → SSR)

The Quiver kill switch opens the SSR to cut HV (Handbook §4.1). It is mapped to the SSR's Relay 1:

- **`RC8_OPTION = 28`** (Relay 1 On/Off) — kill switch on RC channel 8 (a 3-position switch on the MK32).
- **Direction reversed on the MK32 transmitter side** (SIYI TX → Channel Settings → channel 8 → Reverse), **not** via `RC8_REVERSED` — `RCx_REVERSED` only affects control channels, not aux switch functions. Result: **switch up = SSR closed (run), switch down = SSR open (kill).** Verify by LED 5.

> [!IMPORTANT]
>
> **Kill-switch ↔ auto-engage Lua interaction (design decision):** the auto-engage script (§11.4) **always** closes the SSR ~12 s after boot, regardless of the kill-switch position. This is **intentional** — if the SSR stayed open while the avionics and companion computer draw power, that load would run through the pre-charge resistor, which is not rated for it and would overheat (Pilot Handbook §2.4). The trade-off: the kill switch is an **in-flight kill**, not a boot-time lockout. In flight it works correctly (the Lua fires only once at 12 s, so flipping kill afterward opens the SSR and it stays open). Booting with the kill engaged will still close the SSR at 12 s. The Lua was deliberately **not** modified to read the kill channel, to keep pre-charge protection.

### 11.6 Payload port PWM (FMU AUX channels)

Each payload port carries one FMU AUX channel (see the payload port pinout in the Engineering Report). The mapping, confirmed on the second unit's bench session (2026-08-12):

| Payload port | FC pin | Servo output | HOU baseline state |
|---|---|---|---|
| Bottom | FMU_CH1 | 9 | GPIO (mask bit set), function 0 |
| Side 1 | FMU_CH7 | 15 | GPIO (mask bit set), function 0 |
| Side 2 | FMU_CH8 | 16 | GPIO (mask bit set), function 0 |

The HOU baseline ships `SERVO_GPIO_MASK = 65520`, which claims every output 5 through 16 as a GPIO at boot. A channel claimed by the mask cannot generate PWM even with its `SERVOx_FUNCTION` at 0, so all three payload channels boot as GPIO by default.

**To enable PWM on a payload channel** (Mission Planner: Config → Full Parameter List):

1. Clear that channel's bit from `SERVO_GPIO_MASK`:

   | Channels made PWM | New `SERVO_GPIO_MASK` |
   |---|---|
   | Bottom only | 65264 |
   | Side 1 only | 49136 |
   | Side 2 only | 32752 |
   | Side 1 + Side 2 | 16368 |
   | All three | 16112 |

   (Each value is 65520 minus the bits for output 9 = 256, output 15 = 16384, output 16 = 32768. Combine as needed.)

2. Write and **reboot**. Pin allocation between the PWM and GPIO drivers happens once at boot, so the mask change does nothing until then.

3. Set the output range for the payload device: `SERVOx_MIN` / `SERVOx_MAX` (baseline 1100 / 1900, trim 1500). These are FC-side clamps on everything that commands the channel.

4. Leave `SERVOx_FUNCTION = 0` for manual control. With function 0 the channel accepts `MAV_CMD_DO_SET_SERVO`, which in Mission Planner is the **Servo 9 / 15 / 16 row on the Flight Data → Servo/Relay page**. The Low/High boxes on that page are MP-side button values, so type the same numbers you set in `SERVOx_MIN`/`MAX`. Assign a real function instead if a driver (mount, gripper, sprayer) should own the channel.

**Verify (powered, payload connected or scope on the port pin):** command Low / Mid / High from the Servo/Relay page and confirm the output follows. `SERVO_OUTPUT_RAW` readback proves the FMU side, the scope proves the harness.

> [!NOTE]
>
> `BRD_SAFETY_MASK = 16368` covers outputs 5 through 14 only, so outputs 15 and 16 sit outside it. With `BRD_SAFETY_DEFLT = 0` (baseline) this has no effect, but if a safety switch is ever enabled, Side 1 and Side 2 PWM would be held until safety is released. Revisit the mask at that point.

Worked example, second unit 2026-08-12: that unit shipped with mask 61168 (outputs 9 and 13 already excluded, a deviation from the 65520 baseline). Side 1 and Side 2 were enabled by writing the mask to 12016, then `SERVO15_MIN/MAX = 1315/1750` and `SERVO16_MIN/MAX = 1000/2000`. All three channels tracked a DO_SET_SERVO sweep after reboot.

---

## 12. Safety, Failsafe, and Logging Verification

Before first flight, confirm (Pilot Handbook §2.5.3):

- [ ] All arming checks enabled. **On 4.8-dev this is `ARMING_SKIPCHK = 0`** (skip-none bitmask), not the legacy `ARMING_CHECK = 1`, which was removed. `standard-params.param` ships `ARMING_SKIPCHK,0` since the 2026-06-25 patch. Read the live value back and confirm it is `0`: one first-unit snapshot (`params-HOU-625.param`) captured `-1`, which skips **every** arming check. Never fly that way.
- [ ] Battery failsafes: `BATT_FS_LOW_ACT = 2` (RTL), `BATT_FS_CRT_ACT = 1` (Land), thresholds correct for 14S LiHV. **Confirm `BATT_LOW_VOLT` reads `46.2`.** It ships in `standard-params.param` since the 2026-06-25 patch. The firmware default (about 10 V) never triggers on a 14S pack, so a unit configured from an older base file flies with no working voltage-based low-battery RTL.
- [ ] RC and GCS failsafe behavior understood and configured.
- [ ] RTL altitude appropriate for the site. This unit uses `RTL_ALT_TYPE = 1` (terrain-relative), which requires `TERRAIN_ENABLE = 1` plus terrain data, or a working downward rangefinder (used when `WPNAV_RFND_USE = 1`). The `above-terrain` pre-arm warning clears once terrain data is available.
- [ ] Geo-fence set for the test site: `FENCE_ENABLE = 1`, `FENCE_RADIUS`, `FENCE_ALT_MAX`.
- [ ] Kill switch mapped and tested with props removed or motors disabled.
- [ ] Onboard logging enabled and SD card installed. **Flight without logging is not permitted.** Install the FC SD card before §11.4, it hosts both `APM/scripts/` and the dataflash logs. Confirm a `.bin` log actually appears after an arm or a forced log. (Verified on the first unit 2026-07-07.)
- [ ] Mission Planner Servo/Relay labels set for relays 1–6 (`SSR`, `Bypass`, `Add HV`, `P1 Sig`, `P1 12V`, `12V Pay`), per Pilot Handbook §2.8.5.

---

## 13. Final Verification Checklist

| Area | Check | Pass |
|---|---|---|
| Firmware | Quiver build flashed (git `20622a39`, PR #230); Arrow features confirmed by boot (S2 lidar, NET IP, ODID) | ☐ |
| Params | standard + ethernet + remoteid (+ OA) loaded in order | ☐ |
| Accel/Level | Calibrated, no errors | ☐ |
| Compass | External cals done outdoors, MagFit applied, internal disabled | ☐ |
| RC | Calibrated, no trims, mode switch (LOITER / AUTO / STABILIZE), RTL switch, kill switch mapped | ☐ |
| GNSS | Both units enumerate, 3D fix on both (RTK not used on this drone) | ☐ |
| Ethernet FC | Boot shows IP 192.168.144.51 (NOT .11 — SIYI air unit) | ☐ |
| RPi | eth0 = .49, pings .50 (CubeNode) and .51 (FC) | ☐ |
| Battery | Bat1 (ESC) + Bat2 (pack BMS) both reporting | ☐ |
| Remote ID | UAS ID + Operator ID set, BLE broadcast confirmed | ☐ |
| SSR / Relay | `RELAY1_FUNCTION/PIN` set, Relay 1 closes SSR (Bat1 rises to Bat2), auto-engage script installed if available | ☐ |
| ESCs | Nodes 1–4 at 1 Mbaud, motor test order + direction correct | ☐ |
| Failsafe | Battery, RC, GCS, fence, RTL configured | ☐ |
| Logging | Enabled, SD card present, a log confirmed written | ☐ |
| Props | Reinstalled after motor test, handedness matches the §0 rotation table | ☐ |

When every row passes and no unexplained pre-arm warnings remain, the aircraft is ready for the Pilot Handbook §3 Power Up Procedure and first flight.

---

## 14. Parameter Deviations from the Repo Baseline

This unit's live configuration differs from the repo param files (`docs/Operations/firmware/parameters/`) in the ways below. **Use this as the diff when syncing changes to other aircraft or back into the baseline.** Calibration values (accel, compass, RC, baro, hover throttle, autotune) are per-drone and excluded by design — they are not listed here.

### 14.1 Baseline defects — should be patched into the repo `.param` files

| Parameter | Repo baseline | Set on this unit | Why | Repo action |
|---|---|---|---|---|
| `NET_P1_TYPE` | *(absent)* | `4` | `params-ethernet.param` omits it, so `NET_P1_PORT`/`NET_P1_PROTOCOL` never instantiate and the FC opens no MAVLink TCP server | **Patched 2026-06-25** — `NET_P1_TYPE,4` added to `params-ethernet.param` |
| `BATT_LOW_VOLT` | *(absent → default ~`10`)* | `46.2` | not in the old `standard-params.param`; the ~10 V default never triggers on 14S, so voltage-based low-battery RTL was effectively off | **Patched 2026-06-25** — `BATT_LOW_VOLT,46.2` added to `standard-params.param` |
| `RELAY1_FUNCTION` | `0` | `1` | baseline leaves all relays unconfigured, so the SSR has no control path | Add once the SSR Lua ships on the SD card |
| `RELAY1_PIN` | *(absent)* | `105` | IO_CH5 (`SSR_S`) drives the main SSR | Add with `RELAY1_FUNCTION` |
| `RELAY1_DEFAULT` | *(absent)* | `0` | SSR starts open; the Lua script closes it after boot | Add with `RELAY1_FUNCTION` |
| `ARMING_CHECK` | `1` | *(removed in 4.8)* | replaced by `ARMING_SKIPCHK`; the line is silently ignored on 4.8-dev | **Patched 2026-06-25** — `standard-params.param` now uses `ARMING_SKIPCHK,0` |
| `AVOID_ANGLE_MAX` | `1000` | *(removed in 4.8)* | the "missing 1 param" on load; gone in 4.8-dev | **Patched 2026-06-25** — dropped from `params-object-avoidance.param` |
| `MOT_SPOOL_TIME` | `0.5` | `2` | Hobbywing G2 folding-prop startup delay, catapult-takeoff risk (§10.3, manufacturer instruction) | Still `0.5` in the base file. Candidate to patch, safety item |

### 14.2 Hardware / config values applied this unit

| Parameter | Repo baseline | Set on this unit | Why |
|---|---|---|---|
| `BATT2_MONITOR` | `9` | `8` | Bat2 = pack DroneCAN smart BMS (node 125), not a second ESC monitor |
| `BATT2_CAPACITY` | `3300` | `30000` | match the 30 Ah pack (default corrupts Bat2 SoC) |
| `BATT2_LOW_VOLT` | `48` | `46.2` | 3.3 V/cell, consistent with Bat1 |
| `BATT2_CRT_VOLT` | `0` | `44.8` | 3.2 V/cell, consistent with Bat1 |
| `PRX2_TYPE` | `0` | `17` | NanoRadar MR82 forward proximity (RadarCAN) |
| `PRX2_RECV_ID` | `0` | `2` | listen only to the MR82 (set to CAN ID 2) so it does not swallow the rangefinder's frames — see §9.2. **Needs a reboot to take effect.** |
| `MOT_SPOOL_TIME` | `0.5` | `2` | Hobbywing X6-Plus-G2 manual — avoid catapult takeoff from the 400 ms folding-prop delay |
| `SERIAL1_BAUD` | `57` | `115` | HM30 link raised to 115200 on 2026-06-30 so the QGC parameter download survives Stream GCS Position (§8.2). Change the SIYI side together with it. Recorded in the exports since `params-HOU.param` (2026-07-08) |
| `GPS1_CAN_OVRIDE` | `0` | `121` | pin the F9P (RTK) as GPS 1 — **node ID is unit-specific, will differ per aircraft** |
| `GPS2_CAN_OVRIDE` | `0` | `119` | pin the Mateksys as GPS 2 — **unit-specific node ID** (was `122` until the M9N was replaced 2026-07-13, §5.1) |

`TERRAIN_ENABLE,1` and `RNGFND1_RECV_ID,1` were merged into `standard-params.param` on 2026-06-25 and are no longer deviations.

> [!WARNING]
>
> `GPS1/2_CAN_OVRIDE` values (`121`/`119`) are **specific to this airframe's DroneCAN node IDs** and will not be correct on another aircraft, or even on this aircraft after a GNSS module swap (the first unit's M9N slot went `122` → `119` when the module was replaced, §5.1). Re-read the node IDs per unit (§5.1). Do not copy these two verbatim into the baseline.

### 14.3 Not parameter-file items (device-side / per-drone)

- **ESC node/throttle IDs (1–4) and baud 1 M** — set on the Hobbywing ESCs themselves (§10), not FC params.
- **CubeNode ETH network params** — set on the CubeNode device (§4.4), not the FC param file.
- **Compass `COMPASS_USE3 = 0`** (internal disabled) and all calibration offsets — per-drone (§3.2), set via the compass screen.
- **NanoRadar CAN IDs (NRA15 = 1, MR82 = 2)** — stored in each radar's own flash, not in the FC param file. Set once over SLCAN (§9.2). The FC-side filters that pair with them (`RNGFND1_RECV_ID = 1`, `PRX2_RECV_ID = 2`) *are* params and are listed in §14.2.
- **Pending team decision:** low-battery failsafe source (Bat1 voltage vs Bat2 BMS SoC), see §7.4.

---

## 15. Configuration Status & Gaps

Burn-down of the full initial configuration against the Pilot Handbook. Updated as work completes.

> [!IMPORTANT]
>
> **Next session, start here (updated 2026-07-07).**
>
> **Last session (2026-06-19):** resolved the network IP conflict. The FC has no IP of its own (PPP-assigned by the CubeNode), so it was stuck at `.11`, the SIYI air-unit address. Team-approved fix applied and verified: moved the CubeNode to `.50`, which puts the FC at `.51` (Pi `.49`), confirmed on the boot banner after a full power cycle (an FC reboot is not enough, see §4.4). Synced the addressing across the Engineering Report, this guide (§0 / §4 / §4.4 / §6.3), and the SDK guide. Closed out the relay labels and the SIYI check (HM30 telemetry on SERIAL1, A8 video in the FPV app and QGC). Then brought the **Raspberry Pi up on the network**: imaged, static `.49`, eth0 verified, pings `.50` and `.51`. The J2 Ethernet Phoenix pinout is now in §6.2.
>
> **Resume here — MagFit refinement (needs the first flight log, §3.3) and the Pi Hub/SDK services (telemetry forwarder, OTA puller from `.49:8080`, camera).** **Remote ID is fully complete 2026-07-07**: transmitter (db200 node 123), drone location (FC GPS over DroneCAN), operator location (mainline QGC on the MK32, §8.2), and identity (UA_TYPE, UAS ID, Operator ID). No RID pre-arm gates remain. **Logging is verified 2026-07-07** (FC dataflash log to SD confirmed). The Raspberry Pi network is up (static `.49`, eth0 verified) and Tailscale remote access to the FC is confirmed working (§6.5). No Tattu bridge.
>
> **Do at the bench (no external dependency, roughly in order):**
> 1. **OA sensors — DONE (2026-06-18).** All three work: 360 RPLidar S2 (steady scan), forward MR82 proximity, and the down NRA15 rangefinder. The NRA15 and MR82 were colliding on CAN2 (both at CAN ID 0); resolved by assigning distinct CAN IDs (NRA15 = 1, MR82 = 2) and matching receive-ID filters — see §9.2. Remaining (tuning, not blocking): confirm the intermittent `Proximity 337 deg, 0.00m` is a real return, not a spurious near-zero.
> 2. **Remote ID identity (§8): DONE 2026-07-07.** UA_TYPE = multirotor, UAS ID, and Operator ID set. Operator location supplied by mainline QGC on the MK32 (§8.2). No RID pre-arm remains.
> 3. **Logging + SD verify (§2.5.3): DONE 2026-07-07.** FC dataflash logging to SD confirmed working.
> 4. **Servo/Relay labels 1 to 6 (§2.8.5): DONE 2026-06-19.** Six MP labels set (cosmetic, per-PC). Relays 2–6 intentionally left unconfigured (enable only when an attachment needs one).
> 5. **Base param-file defects (§14, Open Items 4–5): PATCHED 2026-06-25 in the overlays.** `params-ethernet.param` now carries `NET_P1_TYPE,4`; `standard-params.param` uses `ARMING_SKIPCHK,0` (was `ARMING_CHECK,1`) and adds `BATT_LOW_VOLT,46.2`; `params-object-avoidance.param` drops `AVOID_ANGLE_MAX`. Reload the overlays on the unit to confirm they take.
> 6. **SIYI check: DONE 2026-06-19.** HM30 telemetry on SERIAL1 (TELEM1 / UART7, §16.2). A8 video confirmed in the FPV app and in QGC RTSP on the MK32 (gotcha: the MK32 Chinese keyboard typed a full-width colon in the URL, now fixed, §16.6).
>
> **Outdoor, clear sky (§2.5.2):** GPS 3D fix / HDOP and compass LVMC **DONE 2026-06-22 via Mission Planner** (GPS1/F9P DGPS 20 sats HDOP 0.72; LVMC offsets Matek ~279, F9P ~125, heading verified; §3.2, §5.2 click-paths validated). GPS2 Matek M9N No-Fix was recovered twice by cold start but the module kept degrading and was **REPLACED 2026-07-13** (new module = DroneCAN node 119, `GPS2_CAN_OVRIDE` updated, compass re-prioritized, LVMC re-run, all verified by readback; §5.1, §5.2, §3.2). Remaining: MagFit refinement (needs a flight log), and restore `GPS_AUTO_SWITCH` 4 → 1 once the new M9N tracks the F9P through a flight log (§17.5). RTK is not used on this drone.
>
> **Blocked on the team (do not work around):**
> - **Network IP (§0 and Open Item 3), RESOLVED 2026-06-19.** The FC has no IP of its own (no `NET_IPADDR`, confirmed by direct query). It is PPP-assigned the CubeNode's address + 1, so it booted at `.11` (CubeNode `.10` + 1), colliding with the SIYI air unit. Team-approved fix: move the CubeNode to `.50`, which puts the FC at `.51` (clear of all SIYI-reserved addresses), with the Pi at `.49`. Applied and verified 2026-06-19: a full power cycle (not an FC reboot, see §4.4) brought the FC up at `.51` with gateway `.50`. Keep clearing the SIYI-reserved addresses before powering the HM30.
> - **Low-battery failsafe source (§7.4).** Bat1 voltage vs Bat2 BMS SoC. Delegated to Zeynep, who sets it from the shared param file.
>
> **Hub/SDK services (after the Pi is on the network):** telemetry forwarder, the OTA puller (the FC pulls from `.49:8080`), and camera streaming. These come once the Pi is imaged and on `.49`. No Tattu bridge.

### Done (verified on the first unit)
Firmware flash (PR #230, git `20622a39`, S2 + Arrow features confirmed) · **360 lidar fixed (RPLidar S2, steady scan, §9.1)** · all param overlays (+ §14 deltas) · accel + level cal · all 4 ESCs (nodes 1–4, directions, `MOT_SPOOL_TIME=2`) · SSR manual control + auto-engage Lua · GPS F9P set primary · internal compass disabled + externals prioritized · battery telemetry (Bat1 ESC, Bat2 pack BMS) · CubeNode ETH link up · **MK32 bound to HM30 (after firmware match) · RC cal + channel map (modes/arm/kill, §16.5) · kill switch on SSR (§11.5) · MK32 telemetry + A8 video working · Remote ID complete (identity + operator location via mainline QGC, 2026-07-07) · SD logging verified (2026-07-07)**.

### Remaining — indoor / bench
| Gap | Ref (this guide or Handbook) | Notes |
|---|---|---|
| GCS link to PC | §2.8 | **Decided 2026-06-22.** MK32 = sole control; PC MP = telemetry view, screen-shared to the remote engineer over Discord (engineer is view-only, no own MP, no VPN relay). Open task: set the **low-latency MK32 → PC link** — wired USB-C Datalink USB COM preferred, or PC on the SIYI net → UDP `192.168.144.12:19856` (§16.6). |
| OA sensor data clean | §9 | **RESOLVED.** 360 RPLidar S2 fixed 2026-06-17 (firmware PR #230 + SERIAL5, §9.1). Forward MR82 + down NRA15 fixed 2026-06-18: both were at CAN ID 0 and colliding on CAN2; assigned distinct CAN IDs (NRA15 = 1, MR82 = 2) with matching `RNGFND1_RECV_ID`/`PRX2_RECV_ID` filters (§9.2). All three OA sensors now report together. Remaining (tuning, not blocking): confirm the intermittent `Proximity 337 deg, 0.00m` is a real return. |
| SIYI camera / video | §2.8.4 | **DONE 2026-06-19.** A8 video confirmed in the FPV app and QGC RTSP. (MK32 Chinese keyboard had typed a full-width colon in the URL, see §16.6.) |
| Remote ID IDs | §8 | **DONE 2026-07-07.** Identity (UA_TYPE, UAS ID, Operator ID) plus operator location (mainline QGC on the MK32). No RID pre-arm remains. |
| Servo/Relay labels 1–6 | §2.8.5 | **DONE 2026-06-19.** Six MP labels set (cosmetic, per-PC). Relays 2–6 left unconfigured by choice, not needed (enable per attachment). |
| Logging + SD verify | Handbook §2.5.3 | **DONE 2026-07-07.** Dataflash log to SD confirmed. |
| Raspberry Pi | §6 / SDK | **Network up 2026-06-19.** Imaged (OS Lite 64-bit), static `.49` on eth0, link verified (pings `.50` and `.51`, 0% loss). Tailscale remote access to the FC **confirmed working 2026-06-22** (§6.5). Remaining: Hub/SDK services. No Tattu bridge. |
| Network IP to final scheme | §0 / §4.4 | **DONE 2026-06-19.** CubeNode moved to `.50`, FC verified at `.51` / gateway `.50` after a full power cycle. |

### Remaining — outdoor (clear sky)
Compass LVMC + GPS 3D fix / HDOP **DONE 2026-06-22 via MP** (§3.2, §5.2), and **redone 2026-07-13** on the replacement M9N (node 119, offsets in `COMPASS_OFS3_*`, §3.2). The original M9N's No-Fix was cold-start recoverable (§5.2 note) but the module later failed for good and was **replaced 2026-07-13** (§5.1, §5.2). Remaining: MagFit refinement (dataset acquired 2026-07-23, log 63, WebTools run pending, §3.3), and `GPS_AUTO_SWITCH` 4 → 1, blocked since the replacement unit failed its 2026-07-23 flight validation with the same velocity glitch (§17.6 finding 2). RTK is not used on this drone.

### Remaining — ops / per-flight
Geo-fence site values (§2.5.3) · flight-tracking-platform registration (§6) · pre-flight checklist (§5.1) · first-flight authorization gate (§2.5.4).

### Decisions for the team
Low-battery failsafe source, Bat1 voltage vs Bat2 BMS SoC (§7.4), delegated to Zeynep · (resolved: network IP = CubeNode `.50` / FC `.51` / Pi `.49`, RID display, IP target = canonical, Tattu bridge skipped, RTK not used on this drone, **remote engineer = view-only via Discord with MK32 as sole control**).

---

## 16. MK32 / SIYI HM30 Link Setup

### 16.1 Topology
- The aircraft carries the **HM30 air unit** (powered from `Main_PCB J14`).
- The **MK32 binds directly to the HM30 air unit** — the MK32 is its own ground unit. The standalone HM30 ground box is **not needed** (only for repeater / dual-operator, which require the "dual & repeater combo").

### 16.2 Wiring (from the harness guide)
- **RC:** HM30 SBUS → `Main_PCB J17` (pin 1 = `IO_PPM_INPUT_AND_SBUS_INPUT`) → FC dedicated SBUS input. `RC_PROTOCOLS = 1` auto-detects SBUS — no serial param needed.
- **Telemetry:** HM30 UART → `Main_PCB J15` → FC **UART7 = SERIAL1 (TELEM1)**, MAVLink2. Shipped at 57600, raised to **115200 on both ends 2026-06-30** (SIYI app plus `SERIAL1_BAUD = 115`, see §8.2). Confirmed 2026-06-19 (J15 is wired to UART7). Note `SERIAL4` (GPS2) is also MAVLink @ 57600 but is an unused spare, the HM30 is on SERIAL1.
- **Video / network:** A8 camera + network ride the HM30 LAN (ethernet).

### 16.3 Firmware MUST match (the blocker we hit)

The MK32 (ground) firmware and the HM30 air unit firmware must be a **matched release set**. They carry different version numbers on purpose — ground `0.x`, air `5.x` on the N32 chip — but must come from the same release. If they don't match, the **air unit blinks Slow Red** ("firmware does not match ground unit") and binding silently fails (MK32 stays Solid Red).

Confirmed on the first unit: MK32 was `RC 0.2.3`, air unit was `(N32) 5.3.1` — incompatible releases. **Fix: flash BOTH devices from the same pack** (the MK32 Firmware Pack):

| Device | File flashed |
|---|---|
| MK32 | `MK32 Ground Unit Firmware v0.1.6` |
| Air unit | `…Air Unit Firmware (N32) v5.2.8` |

Rules that matter:
- **Use the firmware pack for the ground station you are actually using** (the MK32 here), and flash **both** its ground and air firmware — they are the matched pair. The HM30 pack is only for the standalone HM30 ground box.
- **Chip variant:** the air unit boot-loader's first digit selects the chip. Boot loader `5.x` = **(N32)** firmware. **Never flash (GD) `3.x` or (ST) `0.x` on an N32 air unit** — wrong MCU, it will brick.
- Flash via **SIYI PC Assistant** → Upload page → Select File → Upgrade to 100%. Air unit first (its USB-C), then the MK32 (USB-C upgrade port).
- MK32 Firmware Pack download (confirmed working): <https://siyi.biz/siyi_file/MK32/MK32%20Firmware%20Pack.zip>
- Read current versions on the MK32 at **SIYI TX → Device Info** (`RC Firmware Version` = ground, `AU Firmware Version` = air; `AU 0.0.0` means "not linked / can't read", not a real version).

### 16.4 Bind procedure (confirmed working)
1. MK32: **SIYI TX app → System → Bind – Start** (MK32 LED → Red Fast Blink, menu shows "Binding").
2. Air unit bind button unreachable → **wireless bind: power-cycle the air unit 3×** (LED → Fast Green-Red).
3. Both LEDs → **Solid Green** = bound and linked.

### 16.5 RC channel mapping (done)

RC calibration done (radio bars move with the MK32 sticks). Channel map on the first unit:

| Channel | Function | Params | Notes |
|---|---|---|---|
| ch9 | 3-pos flight mode | `FLTMODE_CH = 9`; Pos1 LOITER, Pos2 AUTO, Pos3 STABILIZE | Handbook §2.7.1 map. Set on the **Setup → Flight Modes** page (it highlights the active position as you flip the switch) |
| ch10 | RTL | `RC10_OPTION = 4` | Dedicated 2-pos switch (Handbook §2.7.1). Set in **Config → Full Parameter Tree**. Switch high = RTL. Returning it low hands control back to whatever mode ch9 selects |
| ch5 | Arm / Disarm | `RC5_OPTION = 153` | **Reversed on the MK32 transmitter side** |
| ch8 | Kill (SSR / Relay 1) | `RC8_OPTION = 28` | **Reversed on the MK32 transmitter side**; up = SSR closed, down = kill (§11.5) |

> [!WARNING]
>
> **Re-mapped 2026-07-08 to match Pilot Handbook §2.7.1.** The original first-unit map was Pos1 STABILIZE, Pos2 LOITER, Pos3 RTL with no AUTO and no separate RTL switch. Two consequences of the new map to internalize before flying it:
>
> - **The middle position is now AUTO.** A fast LOITER ↔ STABILIZE flip transits it. With no mission loaded ArduPilot refuses the change and stays in the current mode, but with a mission loaded, resting on the middle position starts the mission. Flip through it deliberately and quickly.
> - **Pos3, which used to command RTL, now commands STABILIZE.** On a self-centering throttle that is close to a mid-throttle demand, a very different aircraft response than the old RTL. Retrain the muscle memory before flight, and use the ch10 switch for RTL.

> [!NOTE]
>
> **Reverse aux switches on the MK32 (SIYI TX → Channel Settings → channel → Reverse), not with `RCx_REVERSED`.** `RCx_REVERSED` only affects control channels (roll/pitch/throttle/yaw), not aux switch functions — confirmed it has no effect on ch5/ch8. On the first unit both **ch5 (arm) and ch8 (kill)** had to be reversed on the transmitter. Check **ch10 (RTL)** direction the same way when mapping its switch: props off, flip it high and confirm the HUD mode changes (or the refusal message appears when there is no GPS fix), and reverse it on the transmitter if it engages in the intended off position.

> [!NOTE]
>
> **Operating deviation (decided 2026-07-20).** The aircraft currently flies **Pos1 STABILIZE / Pos2 ALTHOLD / Pos3 LOITER** (`FLTMODE1/3/4/5/6 = 0/2/2/5/5`, set at the field 2026-07-09, §17.2). AUTO is off the switch because no auto missions are flown yet, which also removes the mid-position mission-start trap in the warning above. The table above remains the documented standard map and is restored when auto missions enter the program. RTL stays on ch10 in both maps.

The Flight Modes page is under the **Setup** tab in Mission Planner (not Config).

### 16.6 GCS, telemetry, and the remote flight engineer

**Telemetry + video work on the MK32.** Confirmed in the **SIYI FPV app** (telemetry + A8 video). Switching `SIYI TX → Datalink → Connection = UDP` routes MAVLink to UDP (which stops the FPV app's telemetry — expected, since the FPV app does not read the UDP output). To use **QGroundControl** on the MK32 instead of the FPV app: QGC → Comm Links → UDP, **`192.168.144.12:19856`** (the SIYI ground unit), and video via QGC → Video → RTSP `rtsp://192.168.144.25:8554/main.264`.

**SIYI Datalink output modes** (one at a time): UART, USB COM, Bluetooth, **Type-C upgrade port** (telemetry-only virtual COM to a Windows PC, the wired USB-C path below), and **UDP**. The MK32 outputs **video** only via HDMI, its WiFi hotspot, or a LAN port — **not** over the Type-C port. So a single USB cable to the MK32 gives telemetry only.

**GCS roles (decided 2026-06-22).**

- **The MK32 is the sole control of the drone** — RC sticks over SBUS, plus the in-field video screen (SIYI FPV app or QGC).
- **The PC runs Mission Planner as the telemetry view**, screen-shared to the remote flight engineer over Discord.
- **The remote flight engineer is view-only.** They watch the MP screen on the Discord stream and do **not** run their own MP or hold any link to the drone. This supersedes the earlier plan of giving the engineer a bidirectional MP over a VPN relay, so no relay to the engineer is needed.

So the link that matters is **MK32 → the PC's Mission Planner**, and it needs **low latency** because it is what the engineer watches live. Ranked best first:

1. **Wired USB-C (lowest latency), but see the Remote ID warning below.** SIYI TX → **Datalink → Connection = USB COM**, plug the MK32 USB-C into the PC, then Mission Planner → connect on that COM port. A direct wire adds essentially no latency and gives a clean bidirectional MAVLink. The MK32 keeps **video** (HDMI / WiFi hotspot / LAN are separate from the Datalink output) and only loses its own telemetry HUD while Datalink is on USB COM, which is fine because the PC's MP is the telemetry GCS.
2. **Local WiFi or LAN — the field-validated setup (2026-07-23).** Put the PC on the **SIYI network** (USB WiFi dongle to the MK32 hotspot, or Ethernet to the ground LAN), then MP → **UDP `192.168.144.12:19856`** (the SIYI ground unit), or TCP to the FC at `192.168.144.51:5760` directly. A local hop, low latency, and it leaves the MK32 Datalink free. The PC's built-in WiFi keeps internet for the Discord stream. **Confirmed working at the field 2026-07-23: MP over the FC TCP server at `.51:5760` alongside QGC on the MK32 over UDP, both live through two flights.**
3. **Remote only, Tailscale (§6.5).** Use when the PC is **not** at the field. Latency is the internet round-trip, so it is not the low-latency field path.

> [!WARNING]
>
> **USB COM and QGC-based Remote ID are mutually exclusive (field finding, 2026-07-23).** The SIYI Datalink outputs **one** mode at a time, so switching Connection to USB COM stops the UDP push to `19856` and dark-screens QGC on the MK32. With QGC down, no `OPEN_DRONE_ID_SYSTEM` operator location reaches the FC and **arming is blocked** by the Remote ID gate (§8). While QGC on the MK32 is the operator location source, use option 2 (Datalink stays UDP, PC on the SIYI network). Option 1 becomes viable only if the PC's Mission Planner has its own GPS and supplies operator location itself.

> [!WARNING]
>
> **Do not use the MK32-forwards-to-PC pattern for this.** Forwarding MAVLink out of the MK32's own QGC to the PC (MK32 QGC → Application Settings → MAVLink → Forward to `<PC-IP>:14550`, PC MP listening on UDP `14550`) is a lossy one-way double hop. Mission Planner hangs on the full param download (`getting param STAT_RUNTIME`), so it is fine only for a throwaway glance. Connect the PC **directly** instead (USB COM, or `192.168.144.12:19856`), not through the MK32's GCS.

**Confirmed 2026-06-19:** the HM30 telemetry is on **SERIAL1 (TELEM1 = UART7)**, MAVLink2 (`J15` → FC UART7), at 115200 since 2026-06-30 (was 57600, see §8.2). `SERIAL4` (GPS2/UART8) was a spare MAVLink @ 57600 until 2026-07-27, when it became the A8 gimbal port via J12 (§16.7). **A8 video confirmed** working both in the SIYI FPV app and in QGC on the MK32 via RTSP `rtsp://192.168.144.25:8554/main.264`.

> [!WARNING]
>
> **MK32 keyboard gotcha.** If QGC sits at "waiting for video" with a URL that looks correct, check the colon. The MK32's Chinese input mode types a full-width colon `：` (U+FF1A) instead of the ASCII `:` (U+003A), which silently breaks the RTSP URL with no error. Switch the keyboard to English and re-type the `:` before the port. This, not codec or network, was the actual cause on the first unit.

---

### 16.7 A8 mini gimbal control from the MK32 (set up 2026-07-27)

The A8 mini accepts control on three independent inputs (spec sheet: S.Bus / UART / UDP), and knowing which is which saves a day of confusion:

- **UDP over Ethernet.** What the SIYI FPV app touchscreen uses (slide for pitch/yaw, double tap to center). Works with no control wiring at all, because it rides the same network path as the video. Always available as a fallback.
- **S.Bus.** The gimbal listens to RC channels directly through its control-signal port, wired to the air unit RC port via a Y cable. Not used on this aircraft (it would splice the flight-critical RC line). Note the A8 still holds a channel config from a brief attempt (Yaw = ch15, Pitch = ch16, set via SIYI PC Assistant), inert without the wire.
- **UART + ArduPilot mount driver (the installed path).** The FC drives the gimbal over serial using the SIYI protocol, and the MK32 dials reach it as RC options through the FC. This integrates the gimbal with ArduPilot (missions, ROI, GCS gimbal control, camera commands) and needs one additive wire.

**Wiring (as built).** The Main PCB has a dedicated **J12 "Gimbal UART"** connector on **UART8 = SERIAL4** (the port §16.2 previously listed as a spare MAVLink at 57600, repurposed 2026-07-27). The A8's control-port lead (6-pin connector, three wires populated) carries: **green = gimbal TX** (idles ~3.3 V, that's how to identify it with a DMM), **white = gimbal RX**, **black = GND**. Working arrangement: **green → J12 pin 1, white → J12 pin 2, black → pin 3**. The schematic nets (`UART8_TX_GPS2` on pin 1, `UART8_RX_GPS2` on pin 2) read device-side, pin 2 is electrically the FC's transmit (proven in operation, commands flow through white on pin 2). Nothing connects to pin 4. When in doubt, trust a meter over the labels: a UART transmit pin idles ~3.3 V, and the gimbal's TX (green) must land on a pin that does **not** idle high.

**MK32 setup** (SIYI TX app → Channel Settings): assign **ch15 = LD2** (left dial) and **ch16 = RD2** (right dial). Assignments commit when you back out of the Channel Settings screen cleanly. They were observed to drop once when the screen was left without backing out, so re-open the page and confirm the rows survived.

**FC parameters** (Mission Planner → Config → Full Parameter Tree, reboot after):

| Parameter | Value | Meaning |
|---|---|---|
| `SERIAL4_PROTOCOL` | 8 | SIYI gimbal serial driver on UART8/J12 |
| `SERIAL4_BAUD` | 115 | 115200, the A8 UART rate |
| `MNT1_TYPE` | 8 | SIYI mount (driver instantiates on reboot) |
| `MNT1_PITCH_MIN` / `MAX` | −135 / 45 | A8 mini pitch travel |
| `MNT1_YAW_MIN` / `MAX` | −160 / 160 | A8 mini yaw travel |
| `MNT1_RC_RATE` | 90 | dial full deflection = 90°/s |
| `RC15_OPTION` | 214 | left dial = Mount1 yaw |
| `RC16_OPTION` | 213 | right dial = Mount1 pitch |
| `CAM1_TYPE` | 4 | camera commands (photo/record) via the mount driver |

**Behavior:** the dials are rate control, deflection sets speed, center stops, full deflection 90°/s. The gimbal boots in Follow mode every power-up, so yaw follows the airframe and dial yaw steers relative to it. Verified working 2026-07-27: right dial tilts, left dial pans, touch control remains active in parallel (both paths command the same gimbal, last input wins, avoid driving both at once).

**Post-setup export:** `parameters/params-HOU-727.param` (2026-07-27, battery power, 1214 of 1214 params) is the **restore point**, superseding 724. Enabling the mount grew the tree by the `MNT1_*`/`CAM1_*` subtrees (31 params, including `MNT1_DEFLT_MODE = 3`, RC targeting, the mode the dials use). `MNT1_DEVID` reads 0 in it, which is the parameter-level marker of the open return-path item below (it populates when the driver identifies the gimbal).

> [!WARNING]
>
> **Open item (as of 2026-07-27): the gimbal-to-FC return path is not working.** Dial control is fully functional (FC → gimbal proven), but the FC's device-information handshake fails, so the gimbal's responses are not arriving on UART8 RX. Until fixed there is no gimbal health or attitude telemetry (nothing in dataflash logs, no angle feedback to the GCS, no photo/record acknowledgment). Discriminating test: with everything powered and connected, measure J12 pin 1 to ground. ~3.3 V means the gimbal's signal reaches the board and the fault is board-side (check the J12 pin-1 net, and remember the U5 lidar connector was mirrored on this board). ~0 V means the green crimp is not making contact (the lead was re-pinned repeatedly during setup). Verification once fixed: a `GIMBAL_DEVICE_INFORMATION` request returns the camera model and firmware instead of failing.

## 17. Initial Flight Tuning (first flights, 2026-07-09)

The first unit flew its first four flights on 2026-07-09. This section records how the flights were conducted, what the log review found, and the tuning and inspection actions that came out of it. It is the bridge between the bench configuration above and a validated flight tune. Dataflash logs: `00000057` through `00000060`, one armed cycle each (log 57 was retrieved from the SD card afterward over MAVLink log download on COM6). The post-flight parameter state is captured in `parameters/params-HOU-709.param` (§17.4).

> [!NOTE]
>
> The stats counters reconcile exactly with the four logs. `STAT_FLTCNT` advanced 25 → 29, one per takeoff. `STAT_FLTTIME` advanced 622 s, which matches the summed **airborne** time (49 + 169 + 143 + 263 ≈ 624 s), not the armed time, so the counter tracks time in the air. Logs 55 and 56 also exist on the SD from earlier that morning (~07:34 and ~08:05, ~11 MB each), consistent with ground arms or checks before the first hop. They were not analyzed.

### 17.1 Flight summary

Times are local (log GPS time). Altitudes are AGL from the downward NRA15 rangefinder, which is the trustworthy reference at these heights (the EKF altitude datum sat below zero for parts of the day, a baro origin offset, not a sensor fault).

| # | Log | Armed | Airborne | Mode(s) | Max AGL | Max lean (R/P) | Bat1 start → min | Used |
|---|---|---|---|---|---|---|---|---|
| 1 | 00000057 | 08:06:09 | 49 s | ALTHOLD | 1.8 m | 5.8° / 4.5° | 57.7 → 56.2 V | 583 mAh |
| 2 | 00000058 | 08:12:40 | 169 s | ALTHOLD | 2.8 m | 5.7° / 7.7° | 57.3 → 54.7 V | 2389 mAh |
| 3 | 00000059 | 08:58:28 | 143 s | LOITER | 2.8 m | 5.3° / 8.8° | 55.8 → 53.3 V | 2058 mAh |
| 4 | 00000060 | 09:13:11 | 263 s | LOITER | 7.4 m | 8.7° / 10.5° | 54.6 → 51.1 V | 3901 mAh |

All four flights were gentle hover and low-speed position work: ground speed held under ~1 m/s for 90% of samples, with small translations. Flight 1 was a short shakedown hop to ~1.8 m. Flight 4 climbed to about 7.4 m AGL and worked the climb and descent rates (−1.5 to +1.3 m/s). Hover current ran roughly 45 to 50 A with a session peak of 82.5 A (flight 4). One battery pack across the session, ending at 51.1 V minimum under load (~3.65 V/cell).

All flights were flown by Erick at the Hockley, TX field (zip 77447) between 07:00 and 10:00 local, in calm wind with no real gusts (historical weather for 77447 corroborates). Takeoffs were a manual throttle-up in the active mode and landings a manual throttle-down, in both ALTHOLD and LOITER. The session plan was two flights per mode: a hover with light maneuvering, then a prolonged hover with maneuvering, first in ALTHOLD and then repeated in LOITER, all to characterize how the aircraft flies and responds. No oscillations were felt in flight. Before the final flight a wobble was noticed in the **rear-right (M4) arm** on the ground, and it flew fine afterward. Post-flight, the **rear-right (M4) and front-left (M3) motors were both noticeably warmer** than the other two. Both observations feed directly into the §17.3 yaw imbalance finding: M3 and M4 are the CW pair the logs show running ~13% harder.

### 17.2 Field configuration deviations

The live post-flight params differ from the 2026-07-08 baseline (`params-HOU.param`) in three deliberate settings, changed at the field for the first flights:

| Parameter | Baseline | Flown | Meaning |
|---|---|---|---|
| `FLTMODE1/3/4/5/6` | 5 / 0 / 3 / 0 / 0 | 0 / 2 / 2 / 5 / 5 | Mode switch remapped for first flights: Pos1 **STABILIZE**, Pos2 **ALTHOLD**, Pos3 **LOITER**. Supersedes the §3.4 / §16.5 map (LOITER / AUTO / STABILIZE) for now. AUTO removed from the switch entirely. |
| `AVOID_ENABLE` | 3 | 1 | Proximity avoidance disabled for the first flights, fence avoidance only. The OA sensor stack (§9) is unvalidated in flight, so this was the conservative choice. |
| `GPS_AUTO_SWITCH` | 1 (UseBest) | 4 (Use primary if 3D fix) | Pins navigation to the F9P unless it loses fix, instead of letting the EKF switch on quality. |

All three were deliberate team decisions for the first flights. The M9N that motivated the `GPS_AUTO_SWITCH` pin (off CAN, `GPS2_CAN_NODEID` reading 0 on battery power, the velocity glitch in §17.3 finding 3) was **replaced 2026-07-13** (§5.1, §5.2), but the pin stays until the new unit's velocities track the F9P through a real flight log. The FLTMODE deviation was **adopted as the operating map on 2026-07-20**: keep STABILIZE / ALTHOLD / LOITER while no auto missions are flown, with the Handbook map restored when they begin (deviation noted in §3.4 and §16.5, overlay files unchanged). The AVOID_ENABLE deviation and the final baseline treatment for it remain pending Zeynep's review.

One parameter changed itself, and it is a keeper:

- `MOT_THST_HOVER` learned 0.35 → **0.28** in flight (hover throttle learn). Mean throttle output in a hover ran 0.24 to 0.27, so the aircraft hovers at roughly a quarter of motor range with the current pack and no payload. Healthy thrust margin. Do not reset it.

### 17.3 Log review findings

**1. CW motor pair runs ~130 PWM high (open item, with Zeynep for review).** In every flight the CW motors (M3 front-left, M4 rear-right) averaged well above the CCW pair (M1, M2), 120 to 140 PWM in the three full flights, while the front/rear and left/right splits stayed within ±7 PWM:

| Flight | M1 (CCW) | M2 (CCW) | M3 (CW) | M4 (CW) | CW − CCW | Mean yaw output |
|---|---|---|---|---|---|---|
| 1 | 1283 | 1260 | 1344 | 1359 | +80 | −0.149 |
| 2 | 1441 | 1446 | 1583 | 1582 | +139 | −0.154 |
| 3 | 1423 | 1434 | 1550 | 1548 | +121 | −0.128 |
| 4 | 1449 | 1459 | 1591 | 1591 | +137 | −0.141 |

(Flight 1's PWM means are diluted by its large share of ground idle time, but its yaw output matches the others.) The rate controller held a steady yaw output of −0.13 to −0.15 (13 to 15% of motor range) from the very first takeoff through the last landing. Read: the airframe carries a constant nose-right yaw disturbance, and the controller counters it by running the CW pair faster. Because the split is purely diagonal (CW vs CCW) and not front/back or left/right, this is a yaw torque imbalance, **not** a CG problem.

Working hypothesis (team-confirmed, with precedent): motor arm alignment. The same CW/CCW output split has appeared on a prior build and was resolved by realigning the motor arms. Two field observations back it up. First, a wobble was noticed in the **rear-right (M4) arm** on the ground before the final flight, so start the inspection there. Second, the predicted thermal signature was observed: **M3 (front-left) and M4 (rear-right), the CW pair, were both noticeably warmer post-flight** than the CCW motors, confirming the extra output in the logs is real mechanical load and not a logging artifact. Check motor mount and arm twist on all four (a ~1° thrust-line tilt is enough to produce this) and verify prop seating while in there. Consequences while unfixed: reduced yaw authority in one direction, extra load and heat on M3/M4, and wasted hover current. After realignment, re-fly and confirm the mean yaw output drops toward zero.

[TBD Zeynep: log review feedback and the corrective action.]

**2. Vibration and EKF are clean.** Vibe peaks under 14 m/s² on all axes across all four flights, zero accel clipping, EKF in-flight yaw alignment completed normally. No ERR records, no failsafes. Two one-time messages in flight 1, both benign and both expected behavior: a `PreArm: OpenDroneID: LOC` gate at the first arm of the day (the Remote ID operator location had not arrived from the GCS yet, §8), and `EKF3 ground mag anomaly, yaw re-aligned` at the first liftoff (the EKF detected local magnetic interference at the takeoff spot and corrected yaw once airborne). Neither recurred in flights 2 through 4.

**3. RESOLVED: the GPS speed spike in log 59 is an M9N velocity glitch.** Between T+27 and T+32 s after arming (about 8 to 13 s after liftoff), GPS instance 1 (the M9N) reported a smooth ground speed ramp to 22.7 m/s while its satellite count degraded from 12 to 8. The F9P (instance 0, 22 to 24 satellites) read ~0.1 m/s throughout, so the aircraft was stationary in hover and nothing was physically wrong. This is the M9N's degrading solution, the same unit that later dropped off CAN entirely, and it independently validates both `GPS_AUTO_SWITCH 4` (navigation pinned to the F9P) and the M9N replacement plan. With `GPS_AUTO_SWITCH 1` (UseBest) this glitch would have been a candidate for an EKF lane disturbance, so keep the pin until the M9N is replaced and verified.

### 17.4 Post-flight parameter snapshot (`params-HOU-709.param`)

Exported over COM6 after the flights, 1194 params, zero missing. First pulled on USB bench power, then re-exported the same day on battery power with the CAN peripherals up. (Superseded as the restore point by `params-HOU-713.param`, exported 2026-07-13 on battery power after the M9N replacement. Its diff against 709 contains only the swap params from §5.1 / §3.2, per-boot volatiles, and `MAV1_EXTRA2` 4 → 2, a benign GCS rate renegotiation, not the `MAV*_*` zeroing signature.) Findings from the two pulls:

- The auto-detected device IDs (`COMPASS_DEV_ID`, `COMPASS_DEV_ID2`, `COMPASS_EXTERNAL`, `COMPASS_EXTERN2`, `GPS1_CAN_NODEID`) read 0 on USB power and re-populated on battery power, confirming they are a bench-power artifact. Rule for future exports: **pull param snapshots on battery power**, or the CAN device IDs in the file will be zeroed.
- **`GPS2_CAN_NODEID` stayed 0 even on battery power: the M9N is no longer enumerating on CAN.** This is real, consistent with its velocity glitch in flight (§17.3 finding 3) and its cold-start history (§5.2). The unit was **replaced 2026-07-13** (new module = node 119, §5.1), so this snapshot predates the swap. `GPS_AUTO_SWITCH 4` stays until the replacement is flight-validated.
- The `MAV2_*` stream rates read 0 on both pulls, where the baseline recorded 10/10/3/2/3/2/2 from earlier network GCS sessions. Same signature as the 2026-07-08 `MAV1_*` zeroing (cause never confirmed). Working hypothesis from the field, unconfirmed: it happens when Mission Planner over TCP and QGC on the MK32 are connected at the same time. A notice about MAV1 and MAV2 compatibility appeared on the MK32 during the session but was not recorded. [TBD: capture that message verbatim next time it appears.] Benign on MAV2 (a connecting GCS re-requests its rates), but if the same thing ever hits `MAV1_*` the SIYI FPV telemetry HUD goes blank, so re-read `MAV1_*` first if that happens.

Everything else that differs from `params-HOU.param` is per-boot volatile (gyro offsets and cal temps, baro ground pressure, `STAT_*` counters) plus the deliberate deviations in §17.2 and the learned `MOT_THST_HOVER`.

### 17.5 Actions before the next flight session

1. Realign the motor arms (§17.3 finding 1, working hypothesis with precedent), starting with the rear-right (M4) arm that wobbled before the final flight. Re-fly and confirm the yaw output offset drops toward zero. **DEFERRED 2026-07-22:** no reliable way to measure and correct the arm alignment is on hand, so the imbalance stays for now. The aircraft has flown four flights in this state. Known costs while unfixed (§17.3): reduced yaw authority in one direction, extra load and heat on M3 and M4, and wasted hover current. Until the fix lands, keep yaw demands gentle, check M3 and M4 temperature between flights, and check the M4 arm for wobble at every inspection. Keep running the post-flight log report so the CW/CCW output delta has a continuous baseline for when the realignment happens.
   **Alignment measured and ADJUSTED 2026-07-23, after flight session 2.** A digital level was calibrated against the airframe structure, then read at the motor attachment interface at the end of each CF motor beam, all four arms measured. Out of tolerance before adjustment: front-left (M3) **−1.7°** and front-right (M1) **−1.5°**, both tilted in the CCW direction viewed from the drone side. The rear arms measured within tolerance and were left alone. The two front arms were realigned to **within ±0.1° of zero**. This is the first quantified alignment data for the imbalance and it confirms thrust-line tilt on the order the §17.3 hypothesis predicted (~1° is enough to produce the logged CW/CCW split). Remaining gate: re-fly and confirm the mean yaw output and the CW/CCW PWM delta drop toward zero (session 2 pre-adjustment baseline in §17.6).
   **★ VERIFIED 2026-07-24 (flight 7, log 72, §17.7): CW − CCW delta +19 PWM (was +135/+144) and mean yaw output −0.024 (was −0.13 to −0.18). The yaw torque imbalance tracked since the first flights is closed.** The front arm thrust-line misalignment was the dominant cause, as the precedent predicted.
2. Get Zeynep's log review and fold her feedback into this section. [TBD]
3. **Replace the M9N GPS: DONE 2026-07-13.** New module enumerated at **DroneCAN node 119** (DNA assigns a fresh ID, the old 122 stays reserved, §5.1). `GPS2_CAN_OVRIDE` set to 119 and `GPS2_CAN_NODEID` confirmed reading 119 on battery power. Compass priority reassigned (new Matek mag = priority 1, DevID 96003) and LVMC re-run, offsets in `COMPASS_OFS3_*` (§3.2). Bench readback: 3D fix, 11 sats, HDOP 2.08 under a partial sky view, ground speed peak 0.30 m/s over 15 s, no compass or DroneCAN pre-arm messages. Remaining from this item: restore `GPS_AUTO_SWITCH` 4 → 1 after the new unit's velocities track the F9P in a flight log (§5.2 step 6). **VALIDATION FAILED 2026-07-23: the replacement unit reproduced the velocity glitch in log 63 (§17.6 finding 2). `GPS_AUTO_SWITCH` stays 4. The cause now looks systemic to the M9N position rather than a defective module, raise with the team.**
   - Bench observation during the 07-13 verification, worth a check: the pre-arm run reported `OpenDroneID: UA_TYPE required in BasicID` even though identity was set 2026-07-07 (§8.1). Hypothesis, unconfirmed: no RID-capable GCS was connected to feed BasicID at the time, same as the pre-07-07 bench state. Confirm it clears next time mainline QGC on the MK32 is up. If it persists with QGC connected, the db200's stored identity needs a re-check.
4. **Mode map: DECIDED 2026-07-20.** Keep the flown STABILIZE / ALTHOLD / LOITER as the operating map while no auto missions are flown. Documented as a deviation in §3.4 and §16.5 (the Handbook map stays the standard and returns with auto missions). No parameter change needed.
5. Capture the MK32 MAV1/MAV2 compatibility message verbatim if it reappears, and test the dual-GCS hypothesis for the `MAV2_*` zeroing (§17.4) on the bench. **CAPTURED 2026-07-23** (mainline QGC on the MK32, UDP 19856 link, at connect): "MAVLink V1 traffic detected on 'Siyi'. QGroundControl Daily only supports MAVLink2. Please Ensure your vehicle is configured to use MAVLink v2." The FC's SIYI link runs MAVLink2 (`SERIAL1_PROTOCOL 2`, verified live 2026-07-22), so the V1 frames are not the vehicle's own telemetry. **Field observation, same day: the notice appears only at the moment Mission Planner connects to the FC's Ethernet TCP server at `.51:5760` (which worked, §16.6 option 2 confirmed in the field), and never otherwise.** Leading hypothesis, revised to fit that correlation: Mission Planner opens its connection with MAVLink1 framed packets before it detects the vehicle speaks MAVLink2 and switches, and ArduPilot routes GCS traffic between its links, so those first V1 frames reach the SIYI link where QGC flags them. A SIYI datalink injecting V1 status packets on its own was the earlier guess, but it does not fit, since that would trigger the notice with no MP session at all. QGC discards V1 frames and MP switches to V2 after the handshake, so the warning is cosmetic as long as telemetry and parameters flow and the RemoteID panel works. This MP-over-TCP plus QGC-on-UDP combination is also the suspected trigger for the `MAV2_*` zeroing (§17.4), so re-read the `MAV1_*` and `MAV2_*` rates after the session. **Post-session readback 2026-07-23: `MAV2_*` all zeroed again, `MAV1_*` healthy (§17.6 finding 4). The dual-GCS combination was the only GCS configuration used that day, so the correlation is now strong, though the mechanism is still unconfirmed.**
6. **Bench verification PASSED 2026-07-22** (read-only over COM6, aircraft on battery power) ahead of the second flight session. Every First-Flight-Checklist §1 authorization gate parameter read back at its expected value, and a full pull (1194 of 1194) matched `params-HOU-713.param` in every configuration parameter. The only diffs were per-boot volatiles, `MAV1_EXTRA2` renegotiated back to 4, and a benign compass detection slot swap (the Matek 96003 moved to slot 1 with its offsets intact, the disabled internal to slot 3, priorities unchanged, expect slot order to vary between boots). Bench health: Bat1 58.17 V (4.15 V per cell), BMS at 94%, SSR closed with ESC telemetry alive, 60 logs listed on SD, all ten expected CAN1 nodes present including the new M9N (119) and the db200 (123). The `UA_TYPE required in BasicID` pre-arm appeared again with no GCS connected, so the item 3 hypothesis is still untested. Check it first at the field with mainline QGC up, and treat it as a flight blocker if it survives with QGC connected.
7. **Fly the MagFit dataset (§3.3) in this session if a slot allows.** Logs 57 to 60 predate the 2026-07-13 compass replacement and fit the old magnetometer, so they cannot be used. The first valid dataset is a flight on the new Matek. One §3.3 profile flight closes MagFit, the M9N velocity validation (item 3), and the yaw baseline check (item 1) in a single session. **DATASET FLOWN 2026-07-23: log 63 covers all 24 fifteen-degree yaw bins on the new Matek (§17.6), and log 72 (2026-07-24) also qualifies. Whether the run is needed is Zeynep's call (2026-07-27), since in-flight compass behavior looks good.**

### 17.6 Second flight session (2026-07-23)

Two flights at the Hockley field, both LOITER throughout, flown by Erick with the dual-GCS field setup from §16.6 option 2 (QGC on the MK32 over UDP for Remote ID operator location, Mission Planner on the field PC over the FC TCP server at `.51:5760`, validated this session). Flight 5 was gentle pitch and roll work with deliberately minimal yaw (known imbalance, §17.3). Flight 6 flew a square pattern and assorted maneuvers with full 360° heading coverage. Times local, altitudes AGL from the NRA15 (the EKF altitude datum again sat low, same baro origin offset as the first session).

| # | Log | Armed | Airborne | Mode | Max AGL | Max lean (R/P) | Bat1 start → min | Used |
|---|---|---|---|---|---|---|---|---|
| 5 | 00000062 | 07:49:07 | 169 s | LOITER | 5.9 m | 5.3° / 7.5° | 57.8 → 55.2 V | 2345 mAh |
| 6 | 00000063 | 08:18:30 | 581 s | LOITER | 10.6 m | 9.6° / 12.5° | 56.3 → 50.3 V | 8639 mAh |

`STAT_FLTCNT` 29 → 31 and `STAT_FLTTIME` +749 s reconcile with the two logs. Both logs are on the flight tracking platform (anonymized, log 63 with the raw IMU batches stripped to fit the bucket limit). A post-flight full pull on battery power (1194 of 1194) showed **zero configuration diffs against `params-HOU-713.param`**, only per-boot volatiles, the benign compass slot swap, and the `MAV1_EXTRA2` renegotiation, so nothing changed at the field and **713 remains the restore point** (no new export committed, same call as 2026-07-22). Findings:

1. **Yaw imbalance baseline held, pre-adjustment.** CW − CCW delta +135 PWM (flight 5) and +144 PWM (flight 6), mean yaw output −0.182 and −0.167 (airborne samples, throttle output above 0.15). Same signature and direction as the 07-09 band (−0.13 to −0.15, deltas 121 to 139). These are the last flights before the arm realignment (§17.5 item 1), so they close out the pre-fix baseline. The next flight is the realignment verdict: expect the delta and the mean yaw output to drop toward zero.
2. **★ M9N flight validation FAILED: the replacement unit (node 119) reproduced the old unit's velocity glitch.** In log 63, GPS instance 1 reported ground speeds up to 20.8 m/s (87 samples above 6 m/s) while the F9P read 0.1 to 0.3 m/s, with M9N satellites sagging from ~12 to 7 and HDOP reaching 2.8. The F9P (19 to 29 sats, HDOP ≤ 0.66) never exceeded 2.1 m/s, which matches the actual maneuvering. No flight impact because navigation stayed pinned to the F9P. **Keep `GPS_AUTO_SWITCH = 4`.**
   Deeper characterization (same day, both logs): **the glitch is fully gated by the motors running.** With motors off (310 samples across both logs, including 187 in log 63) the M9N never exceeded 0.92 m/s, zero samples above 1 m/s. With motors on, 25% of log 63 samples read above 1 m/s across 23 spike windows, all at ordinary hover current (43 to 60 A), so it tracks propulsion being active rather than a current excursion. It is also not a velocity-only artifact: **the M9N's reported position wanders with the velocity** (one 11.6 s window walked 92 m of reported position while the F9P held under 1.01 m/s), and the receiver flags its own degradation (speed accuracy estimate ballooning from ~0.3 to 9.0 m/s). That is a genuine signal-domain disturbance while motors run, an interference signature rather than random receiver scatter. The clean F9P does not contradict this: it is a dual-band receiver on a different antenna at a different location, and single-band L1 patch receivers are the standard canary for RF interference. Two different modules with the same signature makes a defective unit unlikely. Leading hypothesis (unconfirmed): ESC or power-stage RF coupling into the M9N antenna or supply at its mounting position. Discriminating tests: outdoor static run comparing SSR-open vs motors spinning props-off vs throttle sweep, then a temporary antenna relocation and repeat. Also worth asking whether the German build's M9N shows Spd above 1 m/s while stationary in their logs, and checking the module's u-blox firmware level. Raise with the team before buying a third module.
3. **MagFit dataset acquired.** Log 63 is the first flight on the replacement Matek compass and covers all 24 fifteen-degree yaw bins. Run WebTools MagFit on it and apply the compensation (§3.3).
4. **`MAV2_*` zeroing recurred, trigger correlation now strong.** Post-session readback: all seven `MAV2_*` stream rates 0 again (`MAV1_*` healthy at 2/4/4/2/2/2/2, FPV HUD unaffected). This session ran exactly the suspected combination (MP over TCP plus QGC on UDP), and the MK32 notice fired at the MP connect (§17.5 item 5). Still benign on MAV2.
5. **Clean otherwise.** Vibes ≤ 10.7 m/s² all axes, zero clipping, no ERR records, no failsafes, EKF in-flight yaw alignment normal on both flights. One benign arming retry on flight 6 (`Arm: Yaw (RC4) is not neutral`). `MOT_THST_HOVER` stable at 0.28. Weather (Open-Meteo, interpolated to takeoff times): 27.9 to 28.4 °C, RH 76%, wind NNE to NE 12 to 14 km/h gusting to ~29 km/h, no precipitation.

### 17.7 Realignment verdict and GPS2 relocation test (2026-07-24)

Third field session at Hockley, the morning after the front arm realignment. Session sequence: a static GPS2 relocation test (log 65), GNSS constellation experiments and a compass recalibration during the middle of the session (logs 66 to 71, which also contain two brief hops totaling ~164 s airborne per the STAT deltas, not analyzed), then the realignment verdict flight with everything reverted and GPS2 back in its original mount (flight 7, log 72). Logs 65 and 72 are on the flight tracking platform (anonymized, log 65 with raw IMU batches stripped).

| # | Log | Armed | Airborne | Mode | Max AGL | Max lean (R/P) | Bat1 start → min | Used |
|---|---|---|---|---|---|---|---|---|
| 7 | 00000072 | 09:13:53 | 142 s | LOITER | 5.9 m | 10.8° / 10.2° | 57.1 → 54.9 V | 1919 mAh |

1. **★ REALIGNMENT VERIFIED (closes §17.3 finding 1).** CW − CCW motor output delta **+19 PWM** against the pre-fix band of +121 to +144, and mean yaw output **−0.024** against −0.13 to −0.18 across all six pre-fix flights. The residual is near the noise floor for a short flight in gusty wind. Consequences recovered: symmetric yaw authority, no more chronic extra load on M3/M4. Keep the delta in the routine post-flight report to confirm it stays down over longer flights.
2. **★ GNSS constellation change (standing config change, not an experiment).** `GPS1_GNSS_MODE` 77 → **0** and `GPS2_GNSS_MODE` 69 → **0**, kept through flight 7 and recorded in `params-HOU-724.param`. The old values date to the baseline overlays: 69 on the M9N meant GPS + Galileo + GLONASS with **BeiDou disabled**, 77 on the F9P included BeiDou. 0 hands constellation selection back to the receiver defaults (all four constellations plus SBAS and QZSS on an M9-generation u-blox). So the M9N gained BeiDou, QZSS, and SBAS, while the F9P gained only QZSS/SBAS, and the sat counts moved accordingly (M9N up ~5 sats, F9P roughly unchanged).
3. **GPS2 relocation ground test (log 65, no flight).** The M9N was temporarily mounted on top of the lid, rotated 180° from its original orientation, and left to collect ~6 minutes of static data. It was never armed: the rotation flipped its magnetometer and the compass consistency pre-arm checks blocked arming, as expected. Result: **12 to 23 sats, mean 18.5** vs 12.3 (min 9) in the original position the day before. The comparison is confounded by item 2 (the constellation change was active on the lid, not in the day-before baseline). The cleaner position read: lid static mean 18.5 vs original position in flight the same day at 16.9, a modest gap attributable to position, motors, or both. **The log contains no motors-on data (arming was blocked), so the §17.6 motors-on interference correlation is still untested.** The static armed throttle-sweep test remains open.
4. **M9N in flight 7 (original position): markedly healthier than the day before.** 13 to 21 sats with motors on (mean 16.9 vs 11.5 in log 63), a single 2.2 s divergence to 5.2 m/s while the F9P read 1.14 m/s of real motion. The only large excursions (9 to 11 m/s at 6 sats) came 42 s after disarm with the F9P stationary, consistent with post-flight handling rather than a solution fault. **Leading explanation, revised after item 2 was identified: the constellation change.** More satellites in the solution makes it more robust against the same motors-on RF degradation, so this looks like effective **mitigation** rather than proof the interference is gone. The underlying disturbance may still be present with a deeper margin before it shows. A longer flight with maneuvering decides, then `GPS_AUTO_SWITCH` 4 → 1.
5. **Compass work mid-session.** LVMC was re-run at the field (confirmed by Erick), new offsets Matek −93/−8/249, F9P −13/58/36, both legitimate current cal states, and log 72 remains MagFit-usable. During log 65 `COMPASS_ORIENT2 = 4` (Yaw180) was set, but detection slot 2 that boot was the F9P mag (96515) by DEV_ID, the rotated M9N mag (96003) sat in slot 1, so the correction landed on the wrong physical device. That boot the correct param was `COMPASS_ORIENT` (instance 1). This is the §3.2 slot-vs-priority trap extended to orientations: **`COMPASS_ORIENTx` indexes by detection slot, and slot order varies boot to boot on this FC, so check `COMPASS_DEV_IDx` in the same boot before setting any per-compass param.** With the module back in its original orientation, all `COMPASS_ORIENT*` correctly read 0 again.
6. **Housekeeping.** `MOT_THST_HOVER` re-learned 0.28 → **0.318** during flight 7 (gusty southerly day, learned value, do not reset, watch where it settles on the next longer flight). The in-between logs 66 to 71 were a deliberate test hop to verify motor outputs before the extended flight (per Erick, nothing to record). **`params-HOU-724.param` (exported at the field post-flight, on battery, 1194 params) is the new restore point**, superseding 713 (and itself superseded 2026-07-27 by `params-HOU-727.param` after the gimbal setup, §16.7). Its real content diffs vs 713: the GNSS_MODE change (item 2), the new LVMC offsets, `MOT_THST_HOVER`, a benign compass slot swap, and `MAV5_*` stream rates newly populated (a GCS session landed on a fifth MAVLink channel this session, benign, but note the channel numbering shifts between sessions when chasing the `MAV2_*` zeroing). Post-session live readback: `COMPASS_ORIENT*` 0, `LOG_DISARMED` 0, gate params intact (`ARMING_SKIPCHK` 0, `GPS_AUTO_SWITCH` 4, `AVOID_ENABLE` 1, node 119 up). One oddity: **flight 7 never registered in AP_Stats at all**: the post-flight export from the same boot already showed `STAT_FLTCNT`/`STAT_FLTTIME` at their pre-takeoff values (33 / 1957 s), so this is not a failed save, the counters never incremented in RAM, while the same morning's test hop did count (+2 / +164 s). Cause unknown, cosmetic. **Verify the counters increment after the next flight, and investigate AP_Stats if they miss again** (checklist §9 row added).
7. Weather (Open-Meteo, interpolated): log 65 session 26.9 °C, RH 92%, wind S 14 km/h gusting 31. Flight 7 at 14:14 UTC, 28.1 °C, RH 91%, wind S 17 km/h gusting 32. No precipitation. Vibes ≤ 13.5 m/s² (gusty day), zero clipping, no errors or failsafes.

### 17.8 Fifth field session: endurance record and first autonomous mode engagement (2026-07-30)

Flights 10 and 11 at Hockley. (The fourth session, flights 8 and 9 on 2026-07-28, is not yet written up here. Its GPS2 finding, the worst M9N performance to date with kilometer scale position disagreement at arm, is reflected in §5.2 and the §17.6 systemic interference hypothesis.) Flight 10 set the platform endurance record at **20.7 minutes** and ended when the Battery 2 capacity failsafe commanded RTL, working as configured (§7 posture). Full log review is pending. Logs are uploaded to the flight tracking platform.

1. **★ First autonomous mode engagement, and the OA path planner came with it.** The BendyRuler object avoidance path planner (`OA_TYPE = 1`, loaded with the object avoidance overlay, §9) runs only in autonomous modes: AUTO, GUIDED, and RTL. Every flight in the campaign had been flown manually on the deviation mode map (STABILIZE / ALTHOLD / LOITER, §17.2), so the failsafe RTL in flight 10 was the first time an autonomous mode had ever engaged on this aircraft, and with it came the first live activation of the path planner. It detected the trees off the left side and steered the aircraft up and away from them instead of flying a straight line back to home. Note the distinction from simple proximity avoidance (`AVOID_ENABLE`, held at 1, fence only, §17.2), which was and remains inactive: the path planner is a separate subsystem and arrives automatically with any autonomous mode, including a failsafe triggered one. Internalize this before flying: anything that commands RTL enables avoidance path planning even when simple avoidance is disabled, so the aircraft may take an indirect route home.
2. **Pilot recovery procedure (Handbook item).** Erick recovered by switching out of RTL from the mapped mode switch and landed normally. On this unit's map a ch9 edge exits RTL and ch10 high re-commands it (§16 mode map, ch10 RTL switch). Both the recovery procedure and the path planner note above go to the Pilot's Handbook.
3. **Battery failsafe posture change.** The first battery failsafe stage has been reconfigured to warn instead of commanding RTL, so a capacity warning no longer takes the aircraft autonomous without pilot action. Parameter readback and a fresh restore point export are pending, and the change belongs in the §7.4 failsafe source design review (Zeynep).
4. **★ Orientation item closed in full.** The HM30 air unit and the MR82 forward radar were physically flipped 180° after the session, closing the hardware half of the long deferred orientation item. The CAD model was updated and the radar orientation parameters verified 2026-08-06, closing the item completely.

---

## Open Items to Confirm With the Quiver Team

These are unresolved conflicts in the source documentation found while writing this guide. Confirm before treating any as settled:

1. **GNSS secondary bus — RESOLVED.** Both GNSS enumerate on DroneCAN on the first unit (§5). The FC note showing the M9N on a UART was historical.
2. **Battery monitor instance mapping — RESOLVED.** Bat2 is the pack's native smart BMS (node 125). No Tattu bridge (node 110) is installed, so nothing collides (§7). If a bridge is ever added, pin the instances with `BATTx_SERIAL_NUM`.
3. **Network IP plan — RESOLVED 2026-06-19.** The FC has no `NET_IPADDR` of its own (confirmed by direct query: `NET_IPADDR0-3`, `NET_NETMASK`, `NET_GWADDR`, `NET_DHCP` all absent). It is PPP-assigned the CubeNode's address + 1, so CubeNode `.10` gave FC `.11`, the SIYI air unit's address. The team approved moving the **CubeNode to `.50`**, which makes the FC `.51` by the same +1 (clear of all SIYI-reserved addresses), with the Raspberry Pi at `.49` as a companion host and the CubeNode as the FC's gateway. This keeps the existing harness with no rewiring. The alternative (the FC PPP terminating at the Pi, `.50` → `.51`, with the CubeNode bridging payloads only) was not taken because it needs the FC PPP UART rewired from the CubeNode to the Pi, against the PPP2ETH harness (HAR-0025 carries the UART, HAR-0023 is its CAN cable). Apply via the CubeNode `NET_IPADDR3` `10` → `50` (§4.4), then verify `NET: IP 192.168.144.51` on the boot banner before powering the SIYI HM30. **Applied and verified on the first unit 2026-06-19:** the FC boots at `.51` with gateway `.50` after a full power cycle (an FC reboot alone is not enough, see §4.4). **The SIYI-reserved `.11` / `.12` / `.20` / `.25` / `.60` remain hardcoded, so keep avoiding them.**
4. **`params-ethernet.param` is missing `NET_P1_TYPE`. PATCHED 2026-06-25.** Without it, `NET_P1_PORT` and `NET_P1_PROTOCOL` are never created, so the FC never opens its MAVLink TCP server. `NET_P1_TYPE,4` (TCP Server) has been added to the overlay file. Confirmed on the first unit (§4.3).
5. **`standard-params.param` references parameters removed in ArduCopter 4.8-dev. PATCHED 2026-06-25.** Verified against the first unit's full param export:
   - `ARMING_CHECK` no longer exists. Replaced by `ARMING_SKIPCHK` (skip bitmask). The base file's `ARMING_CHECK,1` was silently ignored. `standard-params.param` now sets `ARMING_SKIPCHK,0` (skip nothing = all checks active).
   - `AVOID_ANGLE_MAX` (in `params-object-avoidance.param`) no longer exists. This was the "missing 1 param" reported on load. The line has been dropped from the overlay.
6. **Sensor loadout corrected.** This unit does NOT use the Ainstein US-D1 or Benewake TF03 (older memory/eng-report listed those). Actual sensors: downward **NanoRadar NRA15** altimeter (`RNGFND1_TYPE = 39`, NRA24_CAN, correct) and forward **NanoRadar MR82** for avoidance. Both NanoRadar devices share CAN2 RadarCAN (`CAN_D2_PROTOCOL2 = 14`). The MR82 needs `PRX2_TYPE = 17` added (was unset); the 360° RPLidar S2 stays on `PRX1_TYPE = 5`. The two NanoRadar devices now carry distinct CAN IDs (NRA15 = 1, MR82 = 2, done 2026-06-18, §9.2). Note `EK3_RNG_USE_HGT = -1`, so the EKF does not use the rangefinder for height (baro-primary).
7. **Bat2 failsafe posture — superseded by §7.** Bat2 turned out to be the pack's native BMS, and its leftover defaults were real defects: `BATT2_CAPACITY = 3300` corrupts the Bat2 SoC and was set to `30000` (§7.3). The live config currently runs voltage failsafes on both instances (`BATT2_FS_LOW_ACT = 2`, `BATT2_FS_CRT_ACT = 1`), which differs from the documented Bat1-only baseline. Zeynep owns the final failsafe-source design (§7.4).
8. **SSR control is unconfigured in the baseline; auto-engage script now committed.** `SCR_ENABLE = 0` and all `RELAY*_FUNCTION = 0` on the first unit, so the SSR had no control path (manual or automatic). The auto-engage script is now at `docs/Operations/firmware/scripts/relay_delayed_close.lua`. To enable: set `RELAY1_FUNCTION = 1` / `RELAY1_PIN = 105` (IO_CH5, confirmed working on the first unit) / `RELAY1_DEFAULT = 0`, put the script on the SD card, then `SCR_ENABLE = 1`. The baseline param file should adopt these once the script ships on every unit's SD card. See §11.
