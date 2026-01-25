## Project Description  
This test plan defines a repeatable, quantitative framework for evaluating any two Project Quiver prototypes by measuring how their airframe, mass distribution, and sensor suites affect flight mechanics across seven performance domains: control & maneuverability, stability & oscillations, energy efficiency, vertical performance, yaw authority & heading stability, navigation accuracy, and aerodynamic effectiveness.

---

## Methodology  
All metrics derive from ArduPilot `.bin` flight logs processed via Mission Planner, MAVExplorer, PyMAVLink, and custom scripts. For each test:  
1. **Extract** the relevant channels (e.g. `RATE.*`, `IMU.*`, `BAT.*`, `CTUN.*`, `ATT.*`, `POS.*`)  
2. **Compute** RMS errors, response times, FFT peaks, power-to-thrust ratios, peak rates, waypoint deviations, etc., according to the recipes below  
3. **Visualize** results with time-series overlays, histograms, bar/line charts, FFT spectra, and map-scatter plots  

---

## Flight Tests & Pilot Directives

### 1. Control & Maneuverability  
- **Test:** From hover at 3 m AGL, perform:  
  - 5 pitch-rate steps of ±100 °/s  
  - 5 roll-rate steps of ±100 °/s  
  - 3 yaw-rate steps of ±90 °/s  
- **Directive:** Use guided mode or exact RC inputs to command precise steps; keep throttle constant.  

### 2. Stability & Oscillations  
- **Test:** Loiter (or AltHold) hover at 3 m AGL for 60 s.  
- **Directive:** Minimize stick inputs; maintain position within 1 m.  

### 3. Energy Efficiency  
- **Hover Endurance:** Hover at 3 m AGL until battery reaches 20 % reserve.  
- **Waypoint Mission:** Fly a square mission (e.g. 50 m × 50 m² at 5 m/s), land at mission end.  
  > ²Distances can be changed based on test-site limitations but must be identical for both prototypes.  

### 4. Vertical Performance  
- **Test:** From hover at 3 m, full-throttle climb to 10 m³ (repeat 3×).  
  > ³Altitudes can be adjusted to local airspace restrictions but must match between tests.  
- **Directive:** After reaching target, center sticks for level flight.  

### 5. Yaw Authority & Heading Stability  
- **Test:** Auto-mode circle of 20 m radius⁴ at 3 m/s for 3 laps.  
  > ⁴Radius customizable but identical across prototypes.  
- **Directive:** Upload a simple circular mission; observe drift and correction.  

### 6. Navigation Accuracy  
- **Test:** Auto mission through 5 waypoints forming a 60 m square, hover 5 s at each.  
- **Directive:** Ensure waypoint coordinates are entered precisely.  

### 7. Aerodynamic Effectiveness  
> _Perform only after structural sign-off._  
- **Deceleration Rate:** Cruise at 5 m/s, cut throttle, record deceleration.  
- **Glide Capability:** From 10 m, neutral throttle, measure time to 3 m AGL⁵.  
  > ⁵Start/end altitudes adjustable but consistent across tests.  

---

## Metrics & Calculations

| **Domain**                      | **Metric**                       | **Source**                              | **Calculation**                                                                                   |
|---------------------------------|-----------------------------------|-----------------------------------------|---------------------------------------------------------------------------------------------------|
| **Control & Maneuverability**   | Rate Tracking Error (deg/s)      | `RATE.R/P/YDes` vs. `RATE.R/P/Yout`     | RMS & peak of `(Des−Out)` during rate steps                                                      |
|                                 | Response Time (s)                | same                                    | Time to 90 % of step amplitude in `RATEOut`                                                      |
|                                 | Overshoot (%)                    | same                                    | `(max(RATEOut)−step)/step×100`                                                                    |
| **Stability & Oscillations**    | IMU Vibration RMS (m/s²)         | `VIBE.X/Y/Z` or `IMU.AccX/Y/Z`          | RMS of raw vibration data during hover                                                            |
|                                 | Oscillation Frequency (Hz)       | same                                    | FFT of hover IMU data; dominant frequency peak                                                    |
| **Energy Efficiency**           | Hover Throttle (%)               | `RCOU.*`                                | Average servo output during steady hover                                                         |
|                                 | Power-to-Thrust Efficiency (N/W) | `BAT.Curr`, `BAT.Volt`, mass            | `(mass×g)/(Iavg×Vavg)`                                                                            |
|                                 | Flight Time (min)                | takeoff/landing timestamps              | Difference between airborne start and end                                                         |
| **Vertical Performance**        | Max Climb Rate (m/s)             | `CTUN.CRt`                              | Peak value during full-throttle ascent                                                           |
|                                 | Thrust Margin (%)                | `RCOU` hover throttle                   | `(1−hover_throttle)×100`                                                                          |
| **Yaw Authority & Heading**     | Yaw Tracking Error (deg)         | `ATT.DesYaw` vs. `ATT.Yaw`              | RMS and peak error during yaw steps and auto-turns                                               |
|                                 | Turn Coordination (deg)          | `GPS.GCrs` vs. `ATT.Yaw`                | Mean angular difference between ground track and heading                                          |
| **Navigation Accuracy**         | Waypoint Tracking Error (m)      | `POS.X/Y` vs. waypoints                 | Euclidean distance at each waypoint arrival                                                      |
|                                 | Yaw Misalignment (deg)           | `ATT.Yaw` vs. velocity vector           | Angular difference at waypoint arrivals                                                          |
| **Aerodynamic Effectiveness**   | Deceleration Rate (m/s²)         | `PSCN/PSCE Vel`, `CTUN.ThO`             | Slope of velocity vs. time after throttle cut                                                    |
|                                 | Glide Capability (s/m)           | `PSCD Vel`, `CTUN.ThO`                  | Time/distance sustained at zero throttle until target altitude                                    |

---

## Results & Deliverables  

| **Metric**                        | **Proto A** | **Proto B** | **Better** | **Notes**                            |
|-----------------------------------|-------------|-------------|------------|---------------------------------------|
| Hover Throttle (%)                |             |             |            |                                       |
| IMU Vibration RMS (AccZ, m/s²)    |             |             |            | Use `VIBE.Z` for consistency          |
| FFT Peak Frequency (Hz)           |             |             |            | Hover FFT of AccZ                     |
| Rate Tracking RMS (deg/s)         |             |             |            | Average of pitch/roll/yaw errors      |
| Response Time (s)                 |             |             |            | 10–90 % rise time                     |
| Overshoot (%)                     |             |             |            | Peak overshoot in rate steps          |
| Power-to-Thrust (N/W)             |             |             |            | mass·g/(I×V)                          |
| Flight Time (min)                 |             |             |            | Hover to 20 % battery                 |
| Max Climb Rate (m/s)              |             |             |            | Peak `CTUN.CRt`                       |
| Thrust Margin (%)                 |             |             |            | (1–hover_throttle)×100                |
| Yaw Tracking Error (deg)          |             |             |            | RMS during auto-turn                  |
| Turn Coordination (deg)           |             |             |            | Mean heading vs. track error          |
| Waypoint Error (avg, m)           |             |             |            | Mean radial error at waypoints        |
| Yaw Misalignment at WP (deg)      |             |             |            | Mean across all waypoints             |
| Deceleration Rate (m/s²)          |             |             |            | After throttle cut cruise             |
| Glide Time (s)                    |             |             |            | Time from start to end altitudes      |

---

## Next Steps  
- Automate log processing to populate this table for each new prototype pair.  
- In later rounds, conduct back-to-back flights under identical PID settings to isolate airframe effects.  
- Use insights to guide structural, CG, and damping improvements for PTₙ.  
