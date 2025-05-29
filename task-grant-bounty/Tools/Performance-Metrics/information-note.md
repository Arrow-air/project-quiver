# Status  

`Valid`


# Project Description

This document defines a methodology for comparing different Project Quiver prototypes from a flight mechanics perspective. The objective is to establish a quantitative, repeatable framework for assessing control behavior, stability, efficiency, and navigation accuracy using flight log data.

The metrics listed below will guide performance comparisons throughout prototype development and testing phases.

---

# Methodology

All metrics are derived from ArduPilot flight logs (.bin) using custom tools, log analysis software (e.g., Mission Planner, MAVExplorer, PyMAVLink), and post-processing scripts.

## 1. **Control & Maneuverability**

- **Rate Tracking Error (deg/s)**  
  - **Source:** `RATE.R/P/YDes` vs. `RATE.R/P/Yout`  
  - **How to Calculate:**  
    Compute RMS and peak error between desired and actual angular rates during dynamic maneuvers.

- **Response Time (s)**  
  - **Source:** Same as above  
  - **How to Calculate:**  
    Time for the actual rate to reach 90% of a step change in the commanded rate.

- **Overshoot (%)**  
  - **Source:** Same  
  - **How to Calculate:**  
    `(max actual rate - commanded rate) / commanded rate × 100`


## 2. **Stability & Oscillations**

- **IMU Vibration Levels (RMS, m/s²)**  
  - **Source:** `IMU.AccX/Y/Z`, `IMU.GyrX/Y/Z`  
  - **How to Calculate:**  
    Root mean square of raw accelerometer and gyro values during hover or cruise. Can be compared between axes.

- **Oscillation Frequency (Hz)**  
  - **Source:** Same  
  - **How to Calculate:**  
    Apply FFT (Fast Fourier Transform) to vibration signals. Identify dominant frequency peaks (frame resonance or instability).


## 3. **Energy Efficiency**

- **Hover Throttle (`RCOU`)**  
  - **Source:** `RCOU`  
  - **How to Calculate:**  
    Average servo output value during hover at steady altitude.

- **Power-to-Thrust Efficiency (N/W)**  
  - **Source:** `BAT.Curr`, `BATT.Volt`, known aircraft mass  
  - **How to Calculate:**  
    `mass × g / (average current × voltage)`

- **Flight Time (min)**  
  - **Source:** Timestamps of takeoff and landing events  
  - **How to Calculate:**  
    Difference between airborne start and end times under a standard battery and payload.

## 4. **Vertical Performance**

- **Maximum Climb Rate (m/s)**  
  - **Source:** `CTUN.CRt`  
  - **How to Calculate:**  
    Maximum value recorded during full-throttle ascents.

- **Thrust Margin Estimate (%)**  
  - **Source:** `RCOU`  
  - **How to Calculate:**  
    `(1 - hover throttle) × 100`

## 5. **Yaw Authority & Heading Stability**

- **Yaw Tracking Error (deg)**  
  - **Source:** `ATT.DesYaw` vs. `ATT.Yaw`  
  - **How to Calculate:**  
    RMS and peak error during yaw commands and auto-turns.

- **Turn Coordination**  
  - **Source:** `GPS.GCrs`, `ATT.Yaw`  
  - **How to Calculate:**  
    Check alignment of heading vs. ground track during horizontal turns.

## 6. **Navigation Accuracy**

- **Waypoint Tracking Error (m)**  
  - **Source:** `POS.X/Y` and mission waypoints  
  - **How to Calculate:**  
    Euclidean distance between actual and desired positions during autonomous flight.

- **Yaw Misalignment at Waypoints (deg)**  
  - **Source:** `ATT.Yaw`, velocity vector direction  
  - **How to Calculate:**  
    Compute angular difference between drone heading and intended path.

## 7. **Aerodynamic Effectiveness**

These tests have higher risks and should be done in the later stages of testing. 

- **Deceleration Rate (m/s²)**  
  - **Source:** `PSCN and PSCE Vel`, `CTUN.ThO`  
  - **How to Calculate:**  
    Record deceleration after throttle cut in forward flight to estimate drag.

- **Glide Capability**  
  - **Source:** `PSCD Vel`, `CTUN.ThO`  
  - **How to Calculate:**  
    Time and distance sustained at zero throttle before stall or descent begins.


# Results and Deliverables

Each prototype should be evaluated under consistent conditions (weather, payload, battery). The results will be presented in a structured table:

| **Metric**                        | **Prototype A** | **Prototype B** | **Better** | **Notes**                             |
|----------------------------------|-----------------|-----------------|------------|----------------------------------------|
| Hover Throttle (%)               |                 |                 |            |                                        |
| IMU Vibration RMS (AccZ, m/s²)   |                 |                 |            |                                        |
| Max Climb Rate (m/s)             |                 |                 |            |                                        |
| Yaw Tracking Error (deg)         |                 |                 |            |                                        |
| Waypoint Error (avg, m)          |                 |                 |            |                                        |
| Power Efficiency (N/W)           |                 |                 |            |                                        |
| Flight Time (min)                |                 |                 |            |                                        |
| FFT Peak Frequency (Hz)          |                 |                 |            |                                        |


# Remarks

- **Control Tuning Impact:**  
  Many metrics (especially rate tracking, yaw authority, overshoot) depend on PID tuning quality. To ensure a fair comparison:
  - Use the same tuning strategy (e.g., Autotune or identical manual PID tuning)
  - Document tuning parameters used in each test

- **Filtering & Logging Consistency:**  
  Make sure harmonic notch filters, EKF settings, and logging rates are identical across all prototypes.

- **Environmental Conditions:**  
  Note any significant differences in wind, temperature, or air density. These may influence climb rate, power draw, and glide performance.

- **Next Steps:**  
  - Automate metric extraction with log analysis scripts  
  - Validate key metrics under repeatable flight patterns (hover, climb, auto mission)  
  - Use findings to inform design iterations and tuning refinements
