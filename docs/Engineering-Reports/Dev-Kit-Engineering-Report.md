---
title: Dev-Kit Engineering Report
sidebar_position: 3
description: Engineering report for Project Quiver Dev-Kit
---

# Project Quiver Dev Kit Engineering Report

## Executive Summary



## Introduction

### Block Diagrams



## Evolution of Project Quiver

### Prototype Comparison

| Feature                      | PT1                             | PT2                   | PT3                                            |
| ---------------------------- | ------------------------------- | --------------------- |:---------------------------------------------- |
| **Airframe Material**        | Aluminum/CF/3D prints           | Aluminum/CF/3D prints | Aluminum/CF/3D prints                          |
| **Weatherproofing**          | No                              | No                    | Yes                                            |
| **Payload Interfaces**       | One                             | One                   | Three                                          |
| **GNSS System**              | Basic                           | Initial RTK           | Holybro F9P Rover Mini & Mateksys M9N-G4-3100  |
| **Flight Controller**        | Pixhawk 6X                      | Mateksys H743         | Pix32 V6 with plans for Pixhawk 6X/Cube Orange |
| **PCB Strategy**             | Repurposed from Feather Testbed | Custom main PCB       | Multiple custom PCBs                           |
| **Battery Management**       | Contactor controlled by Arduino | SSR & Pre-charge      | Battery PCB w/ temp monitoring and kill switch |
| **Altimeter Sensors**        | Radar altimeter                 | LiDAR                 | Ainstein US-D1 Radar, Benewake TF03-180 LiDAR  |
| **Communication**            | CAN, Serial, Analog             | CAN, Serial, Analog   | CAN, Serial, Analog, & Ethernet                |
| **Raspberry Pi Integration** | None                            | Optional              | Optional                                       |
| **Testing sites**            | US                              | Germany               | US & Germany                                   |



## Detailed Technical Improvements 

This portion of the report will highlight and summarize the modifications to PT3. For additional details please refer to the appendix of the report. 

### Airframe & Structural Improvements

The PT3 structural design is an evolution of the PT2 airframe, preserving core geometries while incorporating modifications to resolve limitations observed during PT2 operations. These enhancements address environmental sealing, increased payload mounting provisions, structural mass optimization, additional cable routing provisions, and mitigations for electromagnetic interference.  The following sections will cover the various airframe modifications targeted for PT3.

**Weather Proofing** 

Total|Explode 
:-:|:-:
![] | ![]


**Weight Reduction Study**



**Transport Case** 




**Cable Routing Anchors**

**Detachable Landing Gear** 


### Electronics Integration

Summary of updates and upgrades to electrical systems

#### Battery PCB Updates

![]()


[KiCAD Files](https://github.com/Arrow-air/project-quiver/tree/main/task-grant-bounty/pt3/electronics/0002-Battery-PCB/KiCAD-Files)

#### Main PCB Updates

![](g)



[KiCAD Files](https://github.com/Arrow-air/project-quiver/tree/main/task-grant-bounty/pt3/electronics/0007-Main-PCB/KiCAD-Files)


#### RPI Integration


#### Ethernet Integration

#### RemoteID Integration


### Software Upgrades

#### Quiver Payload SDK
#### Obstacle Avoidance Selection, Tuning, and SITL Simulation


## Performance Metrics & Endurance Testing 

The Dev Kit performance evaluation follows a standardized methodology for comparing prototypes across control behavior, stability, efficiency, and navigation accuracy. Metrics are extracted from ArduPilot flight logs using Mission Planner, MAVExplorer, and custom scripts. Tests cover rate tracking error, vibration analysis, power efficiency, climb performance, yaw authority, waypoint tracking, and glide capability. Results are collected under consistent environmental and configuration conditions to ensure fair comparisons. 

**PENDING TEST RESULTS**

## Beta Testing 

## Conclusions & Future Recommendations



## Appendices (PENDING NEW INFORMATION NOTES)

### Electronics
- [Battery PCB Information Note](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/pt3/electronics/0002-Battery-PCB/information-note.md)
- [Attachment Interface PCB Information Note](https://github.com/Arrow-air/project-quiver/tree/main/task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB)
- [Rangefinder Information Note](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/pt3/electronics/0005-Rangefinder/information-note.md)
- [GNSS Information Note](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/pt3/electronics/0006-GNSS/information-note.md)
- [Main PCB Information Note](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/pt3/electronics/0007-Main-PCB/information_note.md)
- [FC Information Note](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/pt3/electronics/0008-FC-PCB/information_note.md)

### Flight Controller
- [FC Roadmap Information Note](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/pt3/flight-controller/0001-fc-roadmap/information-note.md)
- [FC Setup Guide](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/pt3/flight-controller/0002-flight-controller-setup/information-note.md)

### Airframe
- [PT3 Airframe Modifications Information Note](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/pt3/structural/0001-comprehensive_airframe_modification/information-note.md)
- [Airframe CAD Architecture Information Note](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/pt3/structural/0002-Airframe-CAD-Architecture.md)

### Assembly Guides
- [All](https://github.com/Arrow-air/project-quiver/tree/main/docs/pt3-assembly-guides)

### Misc
- [Performance Metrics Information Note](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/Tools/Performance-Metrics/information-note.md)
