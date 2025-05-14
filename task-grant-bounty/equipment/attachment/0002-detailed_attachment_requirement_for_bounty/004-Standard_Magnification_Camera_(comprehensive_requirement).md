# Comprehensive Requirement
### 004 - Standard Magnification Camera
Version: 14.05.25-1 Boar

## General Objective Description:

A dual-sensor camera module, it integrates one normal main lens and one high magnification lens, both are fixed focus. 
Instead of controlling a complex mechanical optical zooming lens, the camera can switch between two different optical path via digital video switching mechanism. 
The camera module can be attached or detached from a gimbal stablizer or other structures through standardized mounting interface and connectors.

## Optional Functions:
- OF-1: May support point tracking, flight heading alignment, or 3-axis locking functions.
- OF-2: May include onboard logging for camera triggering, pose or GNSS data.
- OF-3: May support on-ground wireless imagery and log download functions.

## Architecture & Boundary:
- AB-1: Shall accept 12~60V DC power supply and include an anti-spark design.
- AB-2: Must include real-time video stream switching mechanism that can be controlled by flight controller via any supported control signals.
- AB-3: Must include a state machine interface for video stream routing status feedback, and be able to communicate with aircraft's telemetry system.
- AB-4: Must be able to pair with 3-axis gimbal via standard 1/4 mounting interface or non-standard mounter.
- AB-5: Shall support H.264 and MJPEG encoding for balanced image quality and latency.
- AB-6: Shall use Ethernet over UDP protocol for video stream output.

## Performance:
- P-1: Image sensors shall have diagonal size ≥ 1/2 inch and refresh rate ≥ 30 FPS.
- P-2: May select global shutter sensor for components. 
- P-3: Main lens shall have effective focus length of approximately 24 mm (35 mm equivalent).
- P-4: Magnified lens may have effective focus length ≥ 85 mm (35 mm equivalent).
- P-5: Must include still image capture, video recording and SD card storage functions.
- P-6: Must have dust and water splash proof ability.

## Manufacturing & Maintenance Process Technology:
- M-1: Structure parts must be designed using materials with a thermal softening point above 110 degress Celsius.
- M-2: Structure parts must provide rigid support and connections to all connected parts.
- M-3: Shall not include any kind of non-functional decorative features.
- M-4: May include on-ground companion software for video encoding configuration and log output.

## Safety:
- S-1: Must include over temperature protection mechanism.
- S-2: Must include at least a passive heatsink design.
- S-3: Must include EMI and power line noise filtering mechanism.
  
## Revision:
- 14.05.25-1 Boar: Initial public release.
