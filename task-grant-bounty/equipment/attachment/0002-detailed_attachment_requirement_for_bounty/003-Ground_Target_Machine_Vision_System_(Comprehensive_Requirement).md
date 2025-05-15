# Comprehensive Requirement
### 003 - Ground Target Machine Vision System
Version: 16.05.25-1 Beef Noodle

## General Objective Description:
An airborne image processing system mainly composed of computing units, which uses machine vision method to extract and classify objects from input image frames. The main source of the images is other airborne cameras. The system can be used for animal detection or regional analysis.

## Optional Functions:
- OF-1: May support special target early warning function.
- OF-2: May support on-ground wireless data download functions.

## Architecture & Boundary:
- AB-1: Must accept 12~60V DC power supply and include anti-spark and voltage regulating design.
- AB-2: Must connect to other camera to acquire static image or video frames.
- AB-3: Must support RTSP or USB video input and RSTP video output.
- AB-4: The system must be controllable and communicate via Ethernet, and with a power and reset control via CAN.

## Performance:
- P-1: May sort targets by different size, shape, visible colors, or custom signal format.
- P-: Shall have 1080p 60fps video rated computing power.
- P-: Shall have performance and latency level as real-time system.
- P-: Must have dust and water splash proof ablility.


## Manufacturing & Maintenance Process Technology:
- M-1: Uses of off-shelf computer are encouraged (e.g. Raspberry Pi, Nvidia Jetson).
- M-: Shall support raster-to-vector conversion function for survey data output.
- M-: Shall output with standardized or universal data format (e.g.  KML / KMZ) for survey data archiving and exchanging (e.g. Google Earth, ArcGIS, QGIS, etc.).

## Safety:
- S-1: Must include heatsink or active heat removal design for computing unit.


## Revision:
15.05.25-1 Beef Noodle: Initial public release. WIP


  

 

