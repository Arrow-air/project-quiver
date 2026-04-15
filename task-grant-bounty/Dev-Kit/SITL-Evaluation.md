# SITL Obstacle Avoidance Evaluation

# Status

`Author: Zeynep`

`Status: Valid`

`Revision History: None`

`Replacement Log: None`

`Reference: None` 

# Project Description

This information note covers the Software-In-the-Loop (SITL) simulation environment established for safe and rapid exploration of obstacle avoidance (OA) parameters on Project Quiver. The SITL setup uses the standard ArduPilot SITL framework and is configured to resemble the physical and control characteristics of the Quiver airframe. The primary objective of this activity is behavioral exploration and parameter sensitivity analysis, not final performance validation.

# Methodology

## Simulation Environment Overview

The SITL environment is based on the same ArduPilot source code and branch currently used on Project Quiver flight hardware. The following aspects were aligned with the real vehicle:
- Airframe configuration (quadcopter)
- Approximate physical dimensions (arm length, propeller size)
- Mass and inertia estimates
- Control gains and parameter set identical to the current Quiver configuration
- Obstacle avoidance enabled using the same OA parameters as flight tests

This approach allows relative comparison of parameter effects while maintaining consistency with the flight-tested configuration.

## Sensor Simulation

### Top-Mounted LiDAR
The top-mounted 360° LiDAR used on Quiver is not directly available as a native SITL sensor model. To approximate its behavior:
- The SF45 LiDAR model was used in simulation.
- The model was configured to reflect the operational limitations of Quiver's top-mounted LiDAR (range and horizontal-only awareness).
- The simulated sensor feeds obstacle data into the ArduPilot proximity framework in the same manner as the real system.

This substitution provides a functional approximation suitable for studying avoidance logic and parameter interactions, while acknowledging that it does not replicate exact sensor physics or noise characteristics.

## Simulation Startup Configuration

The SITL environment is launched using the following command:

```bash
../Tools/autotest/sim_vehicle.py --map --console \
  -A "--serial5=sim:sf45b --serial6=sim:obstacle"
```

Key elements:
- `sim:sf45b` is used to simulate the top-mounted LiDAR input.
- `sim:obstacle` enables the obstacle simulation backend.
- The simulation is visualized and monitored using QGroundControl.

## Obstacle and Fence Interaction

Within the SITL environment, virtual obstacles and fences can be dynamically introduced. Obstacle geometry and placement can be modified, and vehicle response to parameter changes can be observed in real time.

This capability allows rapid iteration on obstacle margin behavior, BendyRuler lookahead effects, continuity and direction-change constraints, and general avoidance responsiveness.

## Scope and Limitations

While SITL provides a valuable and low-risk environment for experimentation, the following limitations apply:
- Sensor models are simplified and do not capture real-world noise, dropouts, or environmental effects.
- Aerodynamic effects (prop wash, wind interaction, inertia coupling) are approximated.
- Timing and latency characteristics differ from real hardware.
- Avoidance performance observed in SITL must not be considered flight-validated.

SITL results are therefore used to identify promising parameter ranges, eliminate clearly unsafe configurations, and inform flight test planning. Final validation of any obstacle avoidance behavior must be performed on real hardware under controlled flight test conditions.

# Results and Deliverables

At the time of writing:
- The SITL environment is operational.
- Obstacle avoidance behavior can be exercised and visualized.
- Parameter sensitivity studies are ongoing.
- Findings from SITL are being used to guide subsequent real-world flight testing.

QGroundControl screenshots showing the SITL obstacle avoidance simulation:

![SITL QGroundControl View 1](/task-grant-bounty/Dev-Kit/images/SITL/sitl1.jpeg)

![SITL QGroundControl View 2](/task-grant-bounty/Dev-Kit/images/SITL/sitl2.jpeg)

The SITL setup provides a controlled and repeatable environment for early-stage obstacle avoidance tuning on Project Quiver. By closely matching firmware, parameters, and high-level vehicle characteristics, it enables safe exploration of avoidance behavior while clearly separating simulation insights from flight-validated performance.

# Remarks


