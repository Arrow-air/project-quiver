# Comprehensive Requirement
### 002 - General Aerial LiDAR Scanning Device
Version: 12.06.25-2 Powered Glider

## General Objective Description:
An airborne LiDAR system designed to acquire high-precision point cloud data of terrestrial objects. The system integrates inertial navigation, onboard point cloud processing, and embedded data storage subsystems. Color data fusion is not required at this stage of deployment.

## Optional Functions:
- OF-1: May support forward-look flight path safety scan.
- OF-2: May support multiple mounting location mode for different survey mission profile.
- OF-3: May support on-ground wireless point cloud and log download functions.

## Architecture & Boundary:
- AB-1: Must accept 12V DC power supply (Or 48~60V DC via external power connection) and include anti-spark and voltage regulating design.
- AB-2: May include an isolated power supply design for minimize the EMI and noise.
- AB-3: Must include a high-precision navigation subsystem integrating GNSS, AHRS, PPS synchronization, and logging capabilities.
- AB-4: Must design with a dedicated companion computer with ≥ 128 GB of data storage for subsystem architecture.
- AB-5：The LiDAR sensor shall be mounted in a location maximizing ground coverage.
- AB-6: May be able to pair with 3-axis gimbal via standard UNC 1/4"-20 or custom mating interface, excluding power supply wiring integration, for improved pose accuracy and repeatability.
- AB-7: Must include a state machine interface for subsystem status feedback.
- AB-8: The subsystem must be controllable and communicate via Ethernet, and with a limited control via CAN.

## Performance:
- P-1: Shall have ideal detecting range ≥ 100 m.
- P-2: LiDAR sensor must include (1) ≥ 32 laser channels @ ≥ 20 Hz of scan rate, with (2) ≤ 1 cm @ 100 m of accuracy.
- P-3: Must have dust and water splash proof ability.
- P-4: Must be able to resist and filter normal operating vibration that comes from aircraft's propulsion system.
- P-5: Shall have optimized aerodynamic enclosure shape to reduce the form drag.

## Manufacturing & Maintenance Process Technology:
- M-1: Uses of off-shelf LiDAR sensor are encouraged.
- M-2: The LiDAR sensor must be rigidly aligned with the navigation subsystem to preserve calibration integrity.
- M-3: LiDAR sensor must have an rigid structure and dimension relation with all high precision navigation subsystem.
- M-4: Aluminum alloys and composite materials are encouraged.
- M-5: Modern design approaches such as 3D printing, thin skins, hollow frames, and non-standard shapes or mount directions are encouraged.
- M-6: Shall include sensor system storage and protection equipment.
- M-7: Shall include on-ground companion software for LiDAR sensor and subsystem configuration and data output.

## Safety:
- S-1: Must include heat sink or active heat removal design for LiDAR sensor and companion computer.
- S-2: Shall include a full-weight-rated safety tether for structural fail-safe.
- S-3: Must include laser safety warning signs.

## Revision:
- 15.05.25-1 Glide: Initial public release.
- 12.06.25-2 Powered Glider: Fix power limit in AB-1. Fix standard description in AB-6.
