---
title: First Flight Sequence & Checklist
sidebar_position: 3
---

# First Flight Sequence & Checklist
Quiver Dev-Kit

> [!NOTE]
>
> **Approved by Zeynep 2026-07-30 (July 20 version). Revised 2026-08-25, 2026-09-30, and 2026-11-07 (T-20 review).** Drafted 2026-07-20 from the Initial Configuration Guide (§12, §13, §16.5, §17), Pilot Handbook (§2.5, §3, §5), and the 2026-07-09 first flight session at Hockley, TX (logs 57–60).

**Scope.** This document covers the **first flight of a newly configured aircraft** and any **first flight after major maintenance** (motor, arm, ESC, GNSS, or flight controller work). For routine flights, the Pilot Handbook §5.1 pre-flight checklist alone is sufficient. This checklist is a superset of it.

**Format.** Work top to bottom. Every checkbox is a gate. If a box cannot be checked, stop and resolve before continuing.

---

## 1. Authorization Gate (before scheduling a flight)

The aircraft is not authorized for a first flight until all of the following hold (Pilot Handbook §2.5.4, Configuration Guide §13):

- [ ] Configuration Guide **§13 Final Verification Checklist** passes every row, no unexplained pre-arm warnings.
- [ ] **All arming checks active:** `ARMING_SKIPCHK = 0`. Read the live value back. One first-unit snapshot carried `-1`, which skips every check. Never fly that way.
- [ ] **Stick arming off:** `ARMING_RUDDER = 0`. The ch5 switch is the only RC arming path (Handbook §2.5.3).
- [ ] **Battery failsafes verified for 14S LiHV:** `BATT_LOW_VOLT = 46.2` and `BATT_CRT_VOLT = 44.8` on Bat1 (both in the baseline, read them back), `BATT_FS_CRT_ACT = 1` (Land). On a pack without CAN telemetry `BATT_FS_LOW_ACT = 2` (RTL). On a smart pack `BATT_FS_LOW_ACT = 0` (warn) and Bat2 carries the stages: `BATT2_MONITOR 8`, `BATT2_CAPACITY 30000`, `BATT2_LOW_MAH 7500`, `BATT2_CRT_MAH 4500`, `BATT2_ARM_MAH 9000`, `BATT2_FS_LOW_ACT 0`, `BATT2_FS_CRT_ACT 1`, `BATT2_LOW_VOLT 46.2`, `BATT2_CRT_VOLT 44.8` (Handbook §4.2.1, approved 2026-09-30). The mAh stages are remaining capacity computed against `BATT2_CAPACITY`, so they mean nothing without it.
- [ ] **Unit open items reviewed** (Configuration Guide §17 or the unit record on the flight tracking platform) and none blocks this flight.
- [ ] **Logging verified.** SD card installed, a `.bin` log confirmed written on a bench arm. Flight without logging is not permitted.
- [ ] **Remote ID complete.** UA_TYPE, UAS ID, and Operator ID set, operator location source available (mainline QGC on the MK32, not the SIYI-bundled build, which blocks arming).
- [ ] **Kill switch mapped and tested** with props removed (ch8 on the first unit, reversed on the transmitter side).
- [ ] **Regulatory:** aircraft registered, PIC certificated (Part 107 in the US), airspace checked (LAANC / B4UFLY or national equivalent), VLOS plan.
- [ ] **Ground risk buffer planned** per Handbook §1.4: clear zone ≥ flight altitude (1:1 rule), zero uninvolved persons inside it.
- [ ] Propellers reinstalled after the last motor test, handedness matching the §0 rotation table (M1/M2 CCW, M3/M4 CW).

---

## 2. Day Before

- [ ] **Weather within limits** (Handbook §1.2.1): sustained wind ≤ 15 kt, gusts ≤ 18 kt, no precipitation, ambient −10 °C to +35 °C, Kp ≤ 4. The 2026-07-09 session flew 07:00–10:00 local specifically for calm morning air. Plan the same window.
- [ ] **Battery fully charged:** Bat2 state of charge 95 % or more on a smart pack, otherwise resting voltage at the charger's full value. 56.0 V (4.0 V/cell) is the Handbook §5.1 minimum, not a charged pack (on the 2026-07-22 bench 58.17 V read 94 % on the BMS). One pack covered all four first flights (~9 Ah used) but bring a second pack if available.
- [ ] **Charged: MK32, GCS laptop, phone.** Class D extinguisher packed (fire blanket recommended).
- [ ] **MK32 location settings verified** (one-time, config guide §8.2 tip): Location on, High accuracy, WiFi scanning on, QGC location permission Allow all the time with precise location, QGC battery Unrestricted.
- [ ] **Site confirmed:** open area, clear of buildings, vehicles, rebar (compass), with the site parameters ready (`FENCE_ENABLE = 1`, `FENCE_RADIUS`, `FENCE_ALT_MAX`, `RTL_ALT_M`). The pilot sets these within the Handbook §2.6.1 limits and logs them per §2.6.3.
- [ ] **Crew briefed.** MK32 is the sole control. The PC runs Mission Planner as a telemetry view, screen-shared over Discord to the remote flight engineer, who is view-only. Connect the PC on the SIYI network (UDP `192.168.144.12:19856` or TCP `192.168.144.51:5760`), not the USB COM Datalink, which stops QGC on the MK32 and blocks arming (Handbook §2.8.6).
- [ ] **Flight plan reviewed:** the flight profile in §6 below, plus abort criteria (§7).

---

## 3. Pre-Flight Inspection (aircraft cold, no power)

Standard airframe inspection (Handbook §5.1) plus first-flight additions.

**Airframe**

- [ ] Visual check: no deformation, cracks, loose fasteners, damage. Photograph the airframe.
- [ ] **Motor arm screws and latches — check ALL, every flight.** Standing rule from 2026-07-13: arm connector screws loosen even with red Loctite (hand tighten only), and a latch was found closing suspiciously easily after the 07-09 flights and may not have been locked in flight. Confirm each latch is rotated to full engagement and immobile, and each arm has zero wobble. A wobble was observed on the rear-right (M4) arm during the first flight session and is implicated in the yaw imbalance finding.
- [ ] Landing gear quick-release joints fully seated, screws tight, light-pull test passed.
- [ ] Battery and payload mounting points secure.
- [ ] Antennas upright, connectors tight, not facing each other.

**Propulsion**

- [ ] Propellers securely fastened, free of damage, tips and leading edges clean.
- [ ] Props match rotation direction per position (front-right/rear-left CCW, front-left/rear-right CW).
- [ ] Motors turn freely by hand, no grinding.

**Avionics**

- [ ] All accessible connectors seated. Strain relief intact on the RPi J2 Ethernet Phoenix (losing it in flight drops all companion functions).
- [ ] FC SD card installed. RPi SD card installed (if flying with companion functions).

---

## 4. Power-Up and Link Checks

Follow Handbook §3 exactly. Condensed with first-unit expectations:

- [ ] **MK32 on the field WiFi with internet, then QGC open, at least 10 minutes before aircraft power.** Outdoors, screen to the sky for the first minute. Assisted GNSS needs the internet connection to make the fix fast. Confirm QGC → RemoteID shows operator location before continuing (config guide §8.2 tip).
- [ ] Aircraft level, nose reference heading noted, inside the safety zone.
- [ ] **Switches safe before power:** ch5 DISARM, ch8 RUN (up) with the guard closed, ch10 RTL low, ch9 on LOITER. The flight controller does not act on ch5 or ch8 at boot, only when they move, and the SSR closes at ~12 s whatever ch8 says (Handbook §3.2 step 5).
- [ ] **Install and latch battery.** Light-pull test.
- [ ] **Battery wake** (Tattu 4.0: short press then long press to enable output; 3.5 packs are always live).
- [ ] **Drone push button.** Expect fan spin and LEDs, then 30–60 s for FC boot and GPS acquisition.
- [ ] **SSR auto-engage confirmed.** The Lua script closes Relay 1 (`SSR`) after a ~12 s delay (boot message `Relay 1 closed (SSR enabled)`). Verify Bat1 (ESC) and Bat2 (pack BMS) voltages read nearly equal. If Bat1 sits several volts low, the SSR is open. Do not fly until confirmed closed.
- [ ] **MK32 link up** (solid green), telemetry live in the FPV app or QGC, A8 video if fitted.
- [ ] **GCS link up:** PC Mission Planner connected on the SIYI network (UDP `192.168.144.12:19856` or TCP `192.168.144.51:5760`), not USB COM, Discord screen share running for the remote engineer.
- [ ] **GPS:** 3D fix on both instances. Gate: 14+ sats and HDOP ≤ 1.6 per unit in open sky (Handbook §3.3) (first-session benchmark: F9P at DGPS, 20+ sats, HDOP 0.72). GPS 1 must be the F9P (`GPS1_CAN_OVRIDE` pinned).
- [ ] **EKF stable**, no compass variance warnings, heading matches the noted nose reference within 5°. More than 5° is a recalibration trigger (Handbook §2.5.5).
- [ ] **No critical pre-arm messages.** A one-time `OpenDroneID: LOC` gate at the first arm of the day is expected until the GCS supplies operator location, and `EKF3 ground mag anomaly, yaw re-aligned` at first liftoff is benign. Anything else: resolve before flight.
- [ ] **Geo-fence loaded for this site** and verified on the GCS.
- [ ] **Relay labels** visible on the Mission Planner Servo/Relay page (`SSR`, `Bypass`, `Add HV`, `P1 Sig`, `P1 12V`, `12V Pay`).

---

## 5. Mode and Switch Verification (disarmed, before arming)

- [ ] Flight mode switch positions verified on the HUD, one by one.

> [!IMPORTANT]
>
> **Mode map (one map for every unit, Handbook §2.7.1).** ch9 **Pos1 ALTHOLD / Pos2 LOITER / Pos3 AUTO**, RTL on the dedicated ch10 switch. AUTO sits at the end of the switch so no mode change passes through it, and the aircraft refuses to arm with the switch in AUTO. Brief the map at the field and confirm every position on the HUD before arming. For first flights the profile in §6 stays manual: ALTHOLD then LOITER, AUTO not used.

- [ ] RTL switch (ch10) verified while disarmed: flip high, confirm the mode change or the no-fix refusal message, flip back low and confirm the ch9 mode returns.
- [ ] Arm/disarm (ch5) direction verified.
- [ ] Kill switch (ch8) location confirmed with the PIC and the flip-up guard closed over the run position (Handbook §2.8.6). Up = SSR closed, middle and down = kill. Confirmed in RUN (up) for flight. Kill acts only on movement: if the switch was ever down at power-up it takes a flip up and back down to kill. Kill is a deliberate crash, ballistic free fall (Handbook §4.1).
- [ ] **Avoidance posture confirmed.** First flights flew `AVOID_ENABLE = 1` (fence only), proximity avoidance off, because the OA sensor stack is unvalidated in flight. Confirm the intended value for this flight and brief it.
- [ ] **GPS switching posture confirmed.** `GPS_AUTO_SWITCH = 4` (pinned to the F9P) is the current standing value until the replacement M9N's velocities track the F9P through a full flight log, then revert to `1` (Use Best). Confirm which state applies to this flight.

---

## 6. First Flight Profile

The 2026-07-09 session structure worked well and is the recommended template. Two flights per mode, manual throttle-up takeoffs and throttle-down landings:

| # | Profile | Mode | Target |
|---|---|---|---|
| 1 | Shakedown hop | ALTHOLD | ~2 m AGL, under 60 s. Confirm control response, no oscillation, then land |
| 2 | Prolonged hover + light maneuvering | ALTHOLD | ~3 m AGL, 2–3 min. Small translations, gentle yaw inputs |
| 3 | Repeat flight 1–2 profile | LOITER | Confirm position hold, no toilet-bowling |
| 4 | Extended envelope | LOITER | Higher AGL (first session used ~7 m), work climb and descent rates gently |

Session expectations from the first unit (healthy baselines to compare against):

- Hover current ~45–50 A, hover throttle ~0.25–0.28 of range (`MOT_THST_HOVER` learns in flight, do not reset it).
- Vibration under 14 m/s² all axes, zero accel clipping.
- Lean angles under ~10° for this profile.

**Between flights, every time:**

- [ ] Feel all four motors. Report any pair noticeably warmer (on the first unit the CW pair M3/M4 ran warm, matching the logged yaw imbalance).
- [ ] Re-check arm latches and arm wobble by hand.
- [ ] Battery state: land the session at or before `BATT_LOW_VOLT` margins, do not push a pack below ~3.6 V/cell under load for first flights.

---

## 7. Abort Criteria

Abort the flight (land immediately, minimum maneuvering) if any of the following occur (Handbook §3.5, §4.2):

- Electrical arcing, smoke, or any battery warning (temperature > 56 °C: land now).
- Persistent critical errors or EKF instability.
- Uncommanded roll, pitch, yaw, thrust loss, or motor warnings. Quadcopter motor failure has no in-flight recovery: land immediately, and if heading toward people, kill.
- Rapid voltage sag, oscillating or frozen battery telemetry.
- Toilet-bowl or drift in LOITER: switch to ALTHOLD, counter wind manually, land.
- Anything unexplained. First flights earn no benefit of the doubt.

---

## 8. Post-Flight (after each session)

- [ ] Power down in order: motors disarmed → push button off → battery output off → battery removed (Handbook §5.2).
- [ ] Motor temperature check across all four, propeller tips and leading edges, chassis, overall shape.
- [ ] Arm latch and screw re-check (informs the wear pattern, not just safety).
- [ ] **Download all dataflash logs** before leaving the field if possible.
- [ ] **Export a parameter snapshot on battery power**, not USB. On USB the CAN device IDs read zero and the snapshot is not a valid restore point.
- [ ] Upload logs + metadata to the flight tracking platform (https://flights.arrowair.com/): date, location, weather, mission type, pilot notes with any abnormal behavior.
- [ ] Hand logs to the assigned reviewer. First flights are not validated until the log review is complete (the 07-09 session's review produced the yaw imbalance finding and the M9N replacement, both invisible from the ground).
- [ ] Record any parameter changes made at the field in the maintenance log: date, parameter, old/new values, reason, affected flights.
- [ ] Battery to storage: cool 15–30 min before charging, storage voltage if idle > 14 days.
