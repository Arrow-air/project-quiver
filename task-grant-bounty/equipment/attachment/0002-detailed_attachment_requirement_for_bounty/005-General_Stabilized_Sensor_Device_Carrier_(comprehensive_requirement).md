# Comprehensive Requirement
### 005 - General Stabilized Sensor Device Carrier (aka. Arrow Gimbal)
Version: 15.05.25-1 Ranch Grill

## General Objective Description:
A 3-axis gimbal stabilizer with mounting interface and control signal connector outlet. Serves as a universal carrier platform for various cameras and imagery payload. Optional with addtional angle lock and POI tracking functions.

## Optional Functions:
- OF-1: May support location point tracking, flight heading alignment, or 3-axis locking functions.
- OF-2: May support GNSS data injection or integration.

## Architecture & Boundary:
- AB-1: Shall accept 12~60V DC power supply and include an anti-spark design.
- AB-2: Must include on board IMU and AHRS system for attitude correction.
- AB-3: Must provide standard 1/4 or custom adapter mounting interface for payload devices.
- AB-4: Shall reserve CAN, Ethernet and analog control signal interface connectors for payload devices coordination.

## Performance:
- P-1: Shall have angular operating range with (1) ± 360° yaw (2) ± 90° pitch and (3) ± 90° roll.
- P-2: Shall have angular resolution ≤ 0.02° and dynamic stabilization accuracy ≤ 0.1°.
- P-3: Must be able to resist and filter normal operating vibration that comes from aircraft's propulsion system.

## Manufacturing & Maintenance Process Technology:
- M-1: Flexible PCBs for signal routing design are encouraged.
- M-2: Aluminum alloys and composite materials are encouraged.
- M-3: Must not use ferromagnetism material for main structural parts.
- M-4: Structure parts must be designed using materials with a thermal softening point above 110 ℃.
- M-5: Structure parts must provide mechanical rigidity and dimensional accuracy to all connected parts, except motor rotations.

## Safety:
- S-1: Must include mechanical multi-rotation end-stop design to prevent cable damage.
- S-2: Shall include heatsink design for motor driver subsystem. 

## Revision:
15.05.25-1 Ranch Grill: Initial public release.
