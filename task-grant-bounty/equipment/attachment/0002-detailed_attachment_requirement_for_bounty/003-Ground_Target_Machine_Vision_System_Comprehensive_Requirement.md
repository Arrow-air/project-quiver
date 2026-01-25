# Comprehensive Requirement
### 003 - Ground Target Machine Vision System
Version: 03.09.25-5 Deer Noodle

## General Objective Description:
An airborne image processing system mainly composed of computing units, designed to uses machine vision or AI method to extract and classify objects from input image frames. The main source of the images is other airborne cameras. The system can be used for animal detection or regional analysis.

## Optional Functions:
- OF-1: May support custom target early warning functionality based on predefined rules or AI models.
- OF-2: May support on-ground wireless data transfer functions.

## Architecture & Boundary:
- AB-1: Must accept 12V DC power supply and include anti-spark and voltage regulating design.
- AB-2: Must support interface-level integration with other airborne camera to acquire static image or video frames.
- AB-3: Shall include GNSS and AHRS synchronization and logging capability.
- AB-4: Must support RTSP or USB video input and RTSP video output.
- AB-5: Shall support image frame source switching function.
- AB-6: The system must be fully controllable and communicate via Ethernet, and with mode, power, reset control via CAN.

## Performance:
- P-1: May sort targets by different size, shape, visible colors, or custom signal format.
- P-2: Shall have 1080p 60fps video rated computing power.
- P-3: Must have performance and latency level as real-time system.
- P-4: Shall support analysis result overlay and RTSP video output function.
- P-5: Shall support analysis result logging function.
- P-6: Must have dust and water splash proof ability.

## Manufacturing & Maintenance Process Technology:
- M-1: Use of off-shelf computer are encouraged (The core components may consist of highly integrated modules(e.g., Raspberry Pi, Nvidia Jetson) available on the market for better design).
- M-2: Shall support raster-to-vector conversion function for survey data output.
- M-3: Shall output with standardized format (e.g. KML / KMZ) for compatibility with survey data archiving and exchanging (e.g. Google Earth, ArcGIS, QGIS, etc.).
- M-4: Shall include on-ground companion software for system configuration and data output.
- M-5: Design approaches of baseboard or extension board are encouraged.
- M-6: Shall be able to import and work with user predefined rules or AI model.

## Safety:
- S-1: Must include heat sink or active heat removal design for computing unit.

## Revision:
16.05.25-1 Beef Noodle: Initial public release.
19.05.25-2 Egg Noodle: Added M-5.
24.05.25-3 Pork Noodle: Added M-6.
12.06.25-4 Dragon Noodle: Fix power limit in AB-1.
03.09.25-5 Deer Noodle: CHANGE M-1 for components source clarification.
