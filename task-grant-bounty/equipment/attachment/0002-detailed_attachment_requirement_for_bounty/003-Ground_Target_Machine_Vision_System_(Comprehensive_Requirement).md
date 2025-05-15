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
- AB-: Must connect to other camera to acquire static image frames.


## Performance:
- P-: May sort targets by different size, shape, visible colors, or custom signal format.


## Manufacturing & Maintenance Process Technology:
- M-1: Uses of off-shelf computer are encouraged (e.g. Raspberry Pi, Nvidia Jetson).
- M-: Shall support raster-to-vector conversion function for survey data output.
- M-: Shall output with standardized or universal data format (e.g.  KML / KMZ) for survey data archiving and exchanging (e.g. Google Earth, ArcGIS, QGIS, etc.).

## Safety:
- S-1: Must include heatsink or active heat removal design for computing unit.


## Revision:
15.05.25-1 Beef Noodle: Initial public release. WIP


  

 

