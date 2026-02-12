Author: Zeynep

## Software-In-the-Loop (SITL) Obstacle Avoidance Evaluation

### Purpose
To enable safe and rapid exploration of obstacle avoidance (OA) parameters without risking hardware, a Software-In-the-Loop (SITL) simulation environment was established using the standard ArduPilot SITL framework. The primary objective of this activity is behavioral exploration and parameter sensitivity analysis, not final performance validation.

---

### Simulation Environment Overview

The SITL environment is based on the same ArduPilot source code and branch currently used on Project Quiver flight hardware. The simulation is configured to resemble the physical and control characteristics of the Quiver airframe as closely as practical within the limitations of SITL.

The following aspects were aligned with the real vehicle:
- Airframe configuration (quadcopter)
- Approximate physical dimensions (arm length, propeller size)
- Mass and inertia estimates
- Control gains and parameter set identical to the current Quiver configuration
- Obstacle avoidance enabled using the same OA parameters as flight tests

This approach allows relative comparison of parameter effects while maintaining consistency with the flight-tested configuration.

---

### Sensor Simulation

#### Top-Mounted LiDAR
The top-mounted 360° LiDAR used on Quiver is not directly available as a native SITL sensor model. To approximate its behavior:

- The SF45 LiDAR model was used in simulation.
- The model was configured to reflect the operational limitations of Quiver’s top-mounted LiDAR (range and horizontal-only awareness).
- The simulated sensor feeds obstacle data into the ArduPilot proximity framework in the same manner as the real system.

This substitution provides a functional approximation suitable for studying avoidance logic and parameter interactions, while acknowledging that it does not replicate exact sensor physics or noise characteristics.

---

### Simulation Startup Configuration

The SITL environment is launched using the following command:

```bash
../Tools/autotest/sim_vehicle.py --map --console \
  -A "--serial5=sim:sf45b --serial6=sim:obstacle"
```
  
Key Elements:
- `sim:sf45b` is used to simulate the top-mounted LiDAR input.
- `sim:obstacle` enables the obstacle simulation backend.
- The simulation is visualized and monitored using QGroundControl.

### Obstacle and Fence Interaction

Within the SITL environment:
- Virtual obstacles and fences can be dynamically introduced.
- Obstacle geometry and placement can be modified.
- Vehicle response to parameter changes (e.g., margin, lookahead, continuity) can be observed in real time.

This capability allows rapid iteration on:
- Obstacle margin behavior
- BendyRuler lookahead effects
- Continuity and direction-change constraints
- General avoidance responsiveness

---

### Scope and Limitations

While SITL provides a valuable and low-risk environment for experimentation, the following limitations apply:

- Sensor models are simplified and do not capture real-world noise, dropouts, or environmental effects.
- Aerodynamic effects (prop wash, wind interaction, inertia coupling) are approximated.
- Timing and latency characteristics differ from real hardware.
- Avoidance performance observed in SITL must not be considered flight-validated.

SITL results are therefore used to:
- Identify promising parameter ranges
- Eliminate clearly unsafe configurations
- Inform flight test planning

Final validation of any obstacle avoidance behavior must be performed on real hardware under controlled flight test conditions.

---

### Current Status

At the time of writing:
- The SITL environment is operational.
- Obstacle avoidance behavior can be exercised and visualized.
- Parameter sensitivity studies are ongoing.
- Findings from SITL are being used to guide subsequent real-world flight testing.

---

### Summary

The SITL setup provides a controlled and repeatable environment for early-stage obstacle avoidance tuning on Project Quiver. By closely matching firmware, parameters, and high-level vehicle characteristics, it enables safe exploration of avoidance behavior while clearly separating simulation insights from flight-validated performance.
