# Status  

`Valid`

# Project Description

This test plan is designed for the third prototype of Project Quiver. PT3 introduces structural refinements, an updated internal PCB layout, possible CG/inertia changes due to brush and attachment configuration, and a Raspberry Pi onboard interface. Unlike PT1 and PT2, PT3 is expected to be stable from the outset, allowing for a leaner and more targeted test process.

The plan is modular and time-efficient, built to cover critical performance areas, quickly validate new hardware and interfaces, and spend time on improvements or anomalies only when necessary.

# Methodology

All tests are performed using Pixhawk + ArduPilot. Full `.bin` flight logs are recorded, including:
- Flight controller data (`RATE`, `ATT`, `POS`, `IMU`, `VIBE`, `CTUN`, etc.)
- ESC telemetry and temperature
- Battery voltage/current
- Payload activation logs and Raspberry Pi telemetry

PID tuning is handled via **QuickTune** or **AutoTune**, depending on observed flight quality.

Each module defines:
- Flight mode
- Pilot directives
- Key parameters to monitor
- Exit criteria for continuing

Performance metrics such as rate tracking error, yaw authority, thrust margin, vibration levels, and waypoint accuracy are extracted using Mission Planner, MAVExplorer, and post-processing scripts.

---

## Test Modules

### Summary Table

| **Test Module**                      | **Min Time** | **Goal**                                                                 | **Exit Criteria**                                                                                         | **Extend If...**                                                |
|-------------------------------------|--------------|-------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| 1. Initial Hover                    | 0.5 hr       | Verify flight-worthiness, log vibration, motor sync, stability          | Stable hover in Stabilize/Loiter; VIBE.X/Y/Z < 30; ESC temps nominal                                      | Drift, vibration spikes, desync                                  |
| 2. Pitch/Roll Rate Steps            | 0.5 hr       | Assess control quality & rate response                                  | Smooth tracking, low RMS error (<10°/s), minimal overshoot                                                 | Jitter, large overshoot or delay                                 |
| 3. Yaw Axis Check                   | 0.5 hr       | Confirm tracking and authority under new inertia                        | Accurate yaw steps ±90° with clean RATE.YOut tracking                                                      | Overshoot, oscillation, slow tracking                           |
| 4. PID/Quicktune                    | 1.0 hr       | Adjust tuning if needed post-inertia change                             | Acceptable loop gains, stable hover, no PIDs saturated                                                     | Instability or oscillations observed                             |
| 5. Hover w/ Dispenser On            | 0.5 hr       | Verify EMI, vibration or yaw instability from payload                    | Hover with payload ON; logs normal, no power anomalies                                                     | VIBE/BATT/ATT disturbance when brush is active                   |
| 6. Mission Accuracy & Dispense      | 1.0 hr       | Test nav accuracy, auto dispense, yaw alignment                         | 5-point mission w/ drop, <1.5m waypoint error, correct yaw at drop                                        | Path deviation, yaw drift, drop delay                            |
| 7. Speed/Stress Flight              | 0.5 hr       | Observe high-speed control + thermal response                           | 10–15 m/s straight flight; vibration and temp within safe range                                           | ESC heating, FFT spikes, loss of control                         |
| 8. Emergency / Failsafe             | 0.5 hr       | Check GPS loss, RC signal loss behavior                                 | RTL/Land executes correctly; drone maintains control                                                       | Spiral/descent issues, delay in failsafe trigger                |
| 9. Attachment Vibration Test        | 0.5 hr       | Ensure structural mods or mounts don’t introduce vibration or resonance | VIBE < 30; no abnormal oscillations or ESC overdraw                                                       | Rattling, oscillation, FFT peaks                                |
| 10. Raspberry Pi Comms Interface    | 0.5 hr       | Validate Pi-FC link, telemetry, GPIO, MAVLink integration                | Commands and telemetry execute reliably under flight                                                       | Data loss, delayed trigger, CPU overload                        |
| 11. Performance Metric Maneuvers    | 1.5 hr       | Collect data for rate error, climb rate, glide, waypoint error, etc.    | Clean data from controlled maneuvers collected for comparison table                                       | Noise, loss of signal, need for repetition                       |
| Optional: Decel / Glide             | 0.5 hr       | Measure glide time, decel behavior                                      | From 10 m, throttle to 0, log velocity decay                                                               | If new frame significantly impacts aero                          |

## Detailed Test Modules

### 1. Initial Hover (0.5 hr)
**Goal:** Verify flight-worthiness and basic system health. 
**Flight Mode:** Stabilize → Loiter  
**Pilot Directives:**
- Hover at 3 m AGL for 1 minute
- Observe motor sync, hover attitude, and log VIBE/ESC/BATT

**Check:**
- VIBE.X/Y/Z < 30 m/s²
- No visible oscillation or drift
- ESC temps within nominal limits

### 2. Pitch/Roll Rate Steps (0.5 hr)
**Goal:** Assess control quality and response delay.  
**Flight Mode:** Stabilize  
**Pilot Directives:**
- Command ±100 °/s roll and pitch step inputs (manually or via guided commands)
- Record RATE.R/P/YDes vs RATE.R/P/YOut

**Check:**
- RMS rate error < 10 deg/s
- Overshoot < 25%
- Response time to 90% < 0.5 s

### 3. Yaw Axis Check (0.5 hr)
**Goal:** Confirm yaw control under new CG/inertia.  
**Flight Mode:** Stabilize or Guided  
**Pilot Directives:**
- Perform ±90° yaw steps at constant altitude
- Observe RATE.YDes vs RATE.YOut, yaw drift, oscillation

**Check:**
- Clean tracking, minimal overshoot or lag

### 4. PID/QuickTune or AutoTune (1.0 hr)
**Goal:** Optimize pitch/roll/yaw tuning if needed  
**Flight Mode:** AutoTune or QuickTune  
**Pilot Directives:**
- Run pitch/roll AutoTune in calm conditions
- Run yaw QuickTune after observing yaw behavior

**Check:**
- Gains reasonable, stable response
- No oscillations in RATE logs

### 5. Hover with Payload Active (0.5 hr)
**Goal:** Check for interference or instability from running payload  
**Flight Mode:** Loiter  
**Pilot Directives:**
- Hover at 3 m with brush running
- Record BATT.Curr, VIBE.Z, ATT

**Check:**
- No anomalies introduced by payload
- No yaw drift or vibration rise

### 6. Mission Accuracy & Dispense (1.0 hr)
**Goal:** Confirm nav accuracy and dispenser reliability  
**Flight Mode:** Auto  
**Pilot Directives:**
- Upload 5-point square mission (60×60 m)
- Include Do-Set-Servo commands at 3 waypoints
- Log path, drop accuracy, GPS HDOP

**Check:**
- Waypoint error < 1.5 m
- Correct yaw at drop
- No delayed triggers

### 7. Speed / Stress Flight (0.5 hr)
**Goal:** Test high-speed behavior and vibration  
**Flight Mode:** Auto  
**Pilot Directives:**
- Fly straight at 10–15 m/s
- Monitor speed, VIBE, ESC temp

**Check:**
- Smooth tracking, minimal rise in VIBE or ESC temp
- No power surges

### 8. Emergency / Failsafe (0.5 hr)
**Goal:** Ensure failsafe triggers behave correctly  
**Flight Mode:** Auto + Manual  
**Pilot Directives:**
- Simulate GPS loss (GPS_DISBALE or physical masking)
- Simulate RC loss (turn TX off)

**Check:**
- RTL or Land executes smoothly
- Controlled descent

### 9. Attachment Vibration Test (0.5 hr)
**Goal:** Check structural interaction from new mounts  
**Flight Mode:** Loiter  
**Pilot Directives:**
- Hover and do 3 × directional transitions
- Record VIBE.X/Y/Z and ESC currents

**Check:**
- No vibration spikes > 30 m/s²
- No induced oscillations

### 10. Raspberry Pi Comms Check (0.5 hr)
**Goal:** Validate payload communication and MAVLink integration  
**Flight Mode:** Any  
**Pilot Directives:**
- Boot up Pi and monitor MAVLink over serial
- Trigger GPIO pins and verify FC response
- Repeat while hovering

**Check:**
- Pi-to-FC communication reliable
- No data loss, command lag

### 11. Performance Metric Maneuvers (1.5 hr)
**Goal:** Collect standardized data for prototype comparison  
**Flight Mode:** Stabilize, Auto, Loiter  
**Pilot Directives:**
- Hover for FFT (IMU/VIBE)
- Step inputs for RATE response
- Auto circle for yaw authority
- Mission for waypoint error
- Full-throttle climb for CTUN.CRt
- Cut throttle in cruise for glide test  

**Check:**
- Clean logs for each performance domain
- Valid data for metric calculations


# Results and Deliverables

- `.bin` logs for each flight
- Pass/fail tracker table with notes
- PID gain record before/after tuning
- Raspberry Pi communication test logs
- Waypoint accuracy vs GPS logs
- ESC and power draw summary
- FFT spectrum plots (IMU vibration)
- Performance metric summary table for prototype comparison

# Remarks

- PT3 introduces better structure and integration; this test plan reflects that with conditional logic.
- If no issues are observed during each stage, testing may proceed with minimal repetition.
- Attachments and Raspberry Pi are now part of core validation.
- Environmental conditions (e.g., wind) must be recorded.
- Use consistent mission paths and PID strategies for comparison with PT1/PT2.
- Performance metrics enable quantitative comparisons between prototypes.
