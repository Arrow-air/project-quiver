# **Project Quiver PT2 Engineering Report**

Project Quiver PT1 Engineering Report: Insert Link

---

## Introduction

The purpose of Project Quiver is to design and manufacture a practical multi-purpose multi-rotor unmanned aerial vehicle. Its purpose is to promote Arrow's decentralized organization to explore the commercial aviation service market and generate new concepts for the manufacturing process of subsequent unmanned and manned aircraft models, to explore new materials, new structures, new communication protocol and other related technologies. And try to break the current lack of innovation in the drone market around the United States and even the world by Internet collaborate and decentralized finance (DeFi).

This aircraft is designed to perform typical light UAV missions. The design concept is: compact and portable, easy to manufacture, easy to maintenance, highly reliable, highly adaptable, and expandable.

The PT2 prototype of this Project Quiver will contain the following features:

- Having a common quadcopter layout to ensure energy efficiency and structure simplified.
- The designated maximum mission load is 25 kg. Considering the safety margin, the designated maximum thrust force is about 45 to 50 kg.
- The motor beams and propellers can be folded to the side of the cockpit for optimized storage and transportation.
- Standardized, quick-release mission equipment pylon (Attachment interface).
- Has the functions supported by the digital autopilot system, such as GNSS-assisted hovering, waypoint missions, altimeter, etc.
- Has FPV camera and video transmission to assist piloting and various mission actions.
- Use 14-cells LiHV smart batteries and advanced main power connectors commonly used by heavy drones.
- Partially use CAN bus for communication to avoid electromagnetic interference that traditional non-differential signals such as PWM may be subject to.
- Has digitalized sensor communication to monitor more component parameters, such as battery cell temperature and ESC temperature.
- Using integrated thrust terminal to improve the reliability and design convenience of the thrust system, and for easier sourcing, installing and initial testing.
- Use a PCB and Solid State Relay (SSR) that incorporate power and signal management to improve the safety and controllability of the power distributing system.
- Features a lid that protects from dust and enables easy maintenance
- Optional Raspberry Pi for additional computing power on the drone

Based on the above characteristics, Project Quiver will also try to compete with other UAVs on the market in terms of parameters such as endurance, empty weight ratio, open source level, and mission equipment options. It's also expected to gradually introduce more advanced designs including but not limited to the following in future prototypes:

- Real-Time Kinematic (RTK) high-precision GNSS positioning
- Dedicated battery pack
- Dedicated thrust system ESC
- Integrated 3D printing structure
- Hazard protection airframe
- Multiple mission attachment interface
- Retractable landing gear
- Emergency ballistic parachute
- LiDAR navigation
- Dedicated ground control telemetry software
- ...

This second version does not have a waterproof design, the only attachment interface of the aircraft is located on the belly of the cockpit, and flight controller unit (FCU) is on the top of the main PCB for easy accessibility.

The current first mission equipment is the herbicide dispenser "Brush Pod" (or "Brush bullet dispenser"), and the first experimental commercial project is corresponding vegetation analysis and aerial dispensing services. "Brush Pod" will be installed through the standardized attachment interface on the cockpit.

The common design process of Project Quiver will use Onshape and Fusion 360 for CAD/CAM software. They will mainly used for overall layout, structure design and finite element method (FEA) analysis.\
Since the project does not specify the use of industrial design software, the design personnel could use any software and workflow they are familiar with. Therefore, when working between multiple software, STEP or other similar formats could be used as data exchange formats.

# 2. Project Requirements

### 2.1 Flight-Critical Systems

Project Quiver PT2 MUST incorporate robust and reliable flight-critical systems to ensure safe and predictable flight performance. The UAV SHALL feature advanced flight-control electronics that maintain stable operation under varying flight conditions and payload configurations. These systems will allow the drone to safely land even if certain critical components fail during flight operations.

##### Flight Controller:

The aircraft SHALL be equipped with a flight controller compatible with ardupilot software.

##### GPS Module:

The aircraft SHALL have high-accuracy GPS antennas to support reliable navigation.

##### Radar Altimeter:

The aircraft SHALL include an altimeter for precise altitude measurements, particularly during low-altitude operations.

##### Telemetry:

The aircraft SHALL support real-time telemetry data transmission with a range of 2 km.

##### Motors:

The aircraft’s motors SHALL be capable of providing sufficient thrust to maintain hover with a full payload.

##### Propellers:

- The propellers SHALL be large and efficient to maximize lift and minimize power consumption.

- The propellers SHOULD be foldable, if feasible, to support ease of storage and transport.

##### ESCs:

The aircraft’s ESCs SHALL be compatible with up to a 14S power supply, integrate with the CAN bus for precise motor control, and provide sufficient current to meet motor requirements.

### 2.2 Structural Integrity and Components

The structural frame shall leverage commercially available, off-the-shelf, or easily manufacturable components to enable rapid assembly and ease of replacement. The chosen materials must be lightweight yet strong enough to sustain heavy lift operations, accommodating considerable payload capacities without compromising durability or structural safety. Additionally, the structural configuration must allow flexibility for modifications and additions in future iterations.

##### Airframe:

The aircraft SHALL incorporate a durable carbon fiber or aluminum frame capable of supporting a maximum take-off weight (MTOW) of 25 kg and SHALL be designed to accommodate various payload configurations.

The airframe SHALL be constructed using:

- Commonly available off-the-shelf components.

- Common material processing methods.

The aircraft’s motor arms **SHALL** be foldable to enhance portability and ease of deployment.

##### Landing Gear:

The aircraft’s landing gear SHALL be shock-absorbing and support the full MTOW during landing, including in hard-landing scenarios.

##### Modular Design:

The aircraft SHALL be designed with modular, easily replaceable arms, motors, and ESCs to facilitate streamlined maintenance.

### 2.3 Electrical Systems and Power Management

A simplified and robust electrical system shall be designed, ensuring reliability and ease of troubleshooting. Commercially available battery packs must support adequate flight durations, providing sufficient power for continuous flight under maximum payload conditions. The power system should include protective features such as circuit breakers or fuses, mitigating the risk of electrical overload or failures.

##### Battery:

The aircraft SHALL use a 12S or 14S LiPo or Li-ion battery with sufficient capacity to meet endurance requirements.

##### Battery Management System (BMS):

The BMS SHALL monitor battery health, temperature, and charge/discharge rates to ensure optimal battery performance and safety.

##### HV Kill Switch:

The aircraft SHALL have a kill switch for the high-voltage electrical network.

##### LV Kill Switch:

The aircraft SHALL have a kill switch for the low-voltage electrical network.

##### Power Distribution Board (PDB):

The PDB SHALL provide stable 12S or 14S power distribution to all critical components.

##### Battery Case:

The battery SHALL be housed in a case permitting easy swap for rapid replacement in the field.

##### Charging:

The aircraft SHALL NOT require in-aircraft battery charging capabilities.

##### Hover Time Without Payload:

The aircraft SHALL provide at least 25 minutes of hover endurance without payload.

##### Battery Reserve:

The aircraft SHALL ensure a 20% battery reserve upon landing for safety considerations.

##### Cooling System:

The aircraft SHALL incorporate an effective cooling system for motors, ESCs, and the battery, if necessary, to maintain consistent performance during prolonged flights.

##### Health Monitoring:

The aircraft SHALL provide real-time monitoring of ESC and battery health.

##### Pre-Flight Diagnostics:

The aircraft SHALL include a pre-flight diagnostics system to battery levels, GPS accuracy, radar altimeter functionality, and sensor health before each flight.

##### Heading Indicator LEDs:

The aircraft SHALL include LEDs with predefined colors around it to indicate its direction.

### 2.4 Payload Integration and Imaging

The UAV prototype shall integrate a stabilized camera system mounted on a gimbal, providing steady, high-quality video feeds to ground operators. An adaptable payload attachment mechanism must enable rapid payload swaps in-field, thus maximizing versatility across various mission profiles.

##### Payload Capacity:

The aircraft SHALL be capable of carrying at least 7 kg of payload during any mission.

##### Quick-Release Mounting:

The payload attachment system SHALL incorporate a modular quick-release mechanism, allowing for the attachment of various payloads with minimal setup time.

##### CAN Integration:

The payload system SHALL support CAN bus integration to facilitate seamless data communication between the payload and the flight controller.

##### 12V Power Feed:

The aircraft SHALL provide a dedicated 12V power line for powering payloads, adaptable to a variety of equipment.

##### Video Telemetry Range:

The video telemetry SHALL have 1 km of range.

### 2.5 Flight Testing and Verification

A comprehensive testing program is required for PT2, verifying core flight performance, structural strength, electrical reliability, and payload handling capabilities. Testing should document essential parameters and establish baseline operational limits, providing valuable data to inform subsequent design iterations.

### 2.6 Regulatory Compliance

PT2, and all subsequent Quiver systems shall be built to comply with CFR Part 107 Small Unmanned Aircraft Systems standards and requirements.

---

# 3. Prototype Specifications

Image 1: Rendering of the Quiver PT2 CAD assembly

![](https://holocron.so/uploads/e7103ee3-quiver-pt2-render.png)

### 3.1 Flight-Critical Systems

- Flight Controller: Utilizes a Mateksys H743-SLIM V3 flight controller with precision navigation, and autonomous flight modes.

- Navigation Sensors: Utilizes Mateksys AP DroneCAN M10Q-3100 GNSS module, providing high accuracy positioning.

### 3.2 Structure and Geometry

- Frame Material: Employ carbon fiber tubes interconnected with aluminum joints for strength-to-weight optimization. The frame main frame is made out of laser cut aluminum plates and laser cut aluminum rectangular tube.

- Maximum Takeoff Weight (MTOW): Prototype must support a total weight exceeding 25 kg.

- Payload Capacity: Minimum payload capability of 7 kg is required to validate heavy-lift capabilities.

- Structural Safety Factor: Structural integrity must ensure a safety factor of at least 2.5 times the maximum anticipated operational loads.

### 3.3 Propulsion and Power

- Motors and ESCs: Select commercial-grade brushless DC motors rated for 12S to 14S battery configurations, paired with ESCs capable of sustaining at least 80A continuous current, ensuring sufficient thrust-to-weight performance.

- Battery System: LiPo or Li-Ion battery packs rated at 12S or 14S voltage levels must guarantee a minimum of 20 minutes endurance under fully loaded conditions.

- Propellers: Integrate foldable propellers optimized specifically for heavy-lift efficiency, minimizing noise and maximizing flight endurance.

### 3.4 Electrical Systems

- Electrical Layout: Wiring harnesses shall be as short as possible and clearly labeled for ease of maintenance and fault isolation. All wiring must be heat-resistant and abrasion-resistant to withstand harsh operational environments.

- Power Distribution: Install dedicated relays and fuses to protect critical flight electronics and payload circuits from potential short circuits or electrical surges.

### 3.5 Payload Handling and Camera

- Gimbal System: Implement a 3-axis stabilized gimbal, providing precise control of camera orientation to deliver steady footage even in turbulent flight conditions.

- Camera Capabilities: Equip PT2 with a camera capable of delivering at least 1080p resolution at 30fps, streaming live footage directly to the ground control system with minimal latency.

- Payload Attachment Interface: Establish a quick-release payload rail system with adjustable balance points, enabling secure payload attachment and easy in-field interchangeability.

### 3.6 Flight Control and Telemetry

- Communication Systems: Employ telemetry links capable of maintaining reliable communication over distances of at least 2 km, utilizing 900 MHz or 2.4 GHz bands.

- Ground Control Station (GCS): Real-time telemetry data, including flight parameters, payload conditions, and battery health, must be continuously transmitted to the operator’s interface.

### 3.7 Environmental and Operational Specifications

- Operating Temperature: The drone shall reliably operate in a temperature range from -10°C to +45°C, enabling effective use in diverse environmental conditions.

- Wind and Moisture Resistance: Prototype must maintain stable flight control in wind speeds up to 25 km/h and include basic splash-resistant protection for electrical and propulsion systems, protecting against incidental moisture exposure.

### 3.8 Maintenance, Assembly, and Documentation

- Assembly Instructions: BOMs and detailed assembly instructions should be created and provided.

- Assembly Efficiency: Assembly of the UAV, including installation of payloads and batteries, shall be achievable within 60 minutes by trained personnel from packaged state.

- Maintenance Schedule: A clear and concise maintenance manual detailing procedures and inspection intervals must be provided.

### 3.9 Flight Testing and Validation

- Initial Flight Tests: Conduct controlled test flights covering hover stability, maneuverability, payload management, and endurance under realistic operational scenarios. All results and incidents should be carefully documented.

- Documentation: Provide comprehensive documentation, including flight logs, inspection reports, photographic and video evidence of successful testing outcomes, ensuring traceability of performance improvements for future iterations.

## Mission Performance

The following mission performance analysis is the same as in the Quiver PT1 engineering report since the key components and weights are pretty similar.

Below is a mission performance analysis of maximum possible flight time for two missions: Surveillance and Waypoint Missions both under a Tattu 3.5 14S LiHV 30 Ah battery.

Key assumptions:

- **Usable Battery**: 21.6 Ah (after 2C derating to \~27 Ah, then a 20% reserve).
- **Propulsion**: 4 Hobbywing X6 Plus motors.
- **Mission Legs**: short, fixed‐time take‐off, climb, descent, landing; the remaining time is the main mission leg.
- **Real-World Effects**: Climb rates, aerodynamic efficiency, battery health, and environmental conditions do not affect the performance..

## 4.1 Surveillance Mission (20 kg MTOW)

Table 1: Surveillance Current Requirements

| Flight Condition        | Current (A) |
| ----------------------- | ----------- |
| Hover (100%)            | 40.9        |
| Take-Off / Climb (110%) | 48.6        |
| Descent (90%)           | 35.5        |
| Landing (100%)          | 40.9        |

Table 2: Surveillance Mission Leg Times and Capacities

| Flight Segment | Current (A) | Duration (min) | Duration (hr) | Capacity (Ah) |
| -------------- | ----------- | -------------- | ------------- | ------------- |
| Take-Off       | 48.6        | 0.5            | 0.0083        | 0.40          |
| Climb          | 48.6        | 1.5            | 0.0250        | 1.22          |
| Descent        | 35.5        | 1.0            | 0.0167        | 0.59          |
| Landing        | 40.9        | 1.0            | 0.0167        | 0.68          |
| Hover (max)    | 40.9        | 27.4           | 0.4570        | 18.71         |
| **Totals**     | —           | **31.4**       | —             | **21.6**      |

- **Sum of non-hover segments:** 2.89 Ah
- **Remaining battery for hover:** 18.71 Ah
- **Maximum hover duration:** \~27.4 min
- **Total Surveillance Flight Time:**
  - Non-hover segments: 4.0 min
  - Hover: 27.4 min
  - **Overall: \~31.4 min**

---

## 4.2 Waypoint Mission (25 kg MTOW)

Table 3: Waypoint Current Requirements

| Flight Condition        | Current (A) |
| ----------------------- | ----------- |
| Hover (100%)            | 57.5        |
| Forward Flight (120%)   | 69.0        |
| Take-Off / Climb (110%) | 66.5        |
| Descent (90%)           | 49.9        |
| Landing (100%)          | 57.5        |

Table 4: Waypoint Mission Leg Times and Capacities

| Flight Segment       | Current (A) | Duration (min) | Duration (hr) | Capacity (Ah) |
| -------------------- | ----------- | -------------- | ------------- | ------------- |
| Take-Off             | 66.5        | 1.0            | 0.0167        | 1.11          |
| Climb                | 66.5        | 2.0            | 0.0333        | 2.22          |
| Descent              | 49.9        | 1.0            | 0.0167        | 0.83          |
| Landing              | 57.5        | 1.0            | 0.0167        | 0.96          |
| Forward Flight (max) | 69.0        | 14.3           | 0.2390        | 16.48         |
| **Totals**           | —           | **19.3**       | —             | **21.6**      |

- **Sum of non-forward-flight segments:** 5.12 Ah
- **Remaining battery for forward flight:** 16.48 Ah
- **Maximum forward-flight duration:** \~14.3 min
- **Total Waypoint Flight Time:**
  - Non-forward-flight segments: 5.0 min
  - Forward flight: 14.3 min
  - **Overall: \~19.3 min**

## Flight Mechanics

A light mechanics analysis has not been conducted yet. The first flights were successful and showed stable flight behavior. Interested parties can view an analysis for PT1 in the PT1 engineering report under point 5 "Flight Mechanics". The two prototypes are very similar in terms of dimensions and weight.

## Propulsion System

Based on the QUIVER project specifications, alternative manufacturers for electric motors, compatible propellers, and ESCs were evaluated.

Table 5: Drone Propulsion System Comparison for 25 kg MTOW

| Feature                         | System 1                       | System 2                       | System 3                       | System 4                       | System 5                       | System 6                                     |
| ------------------------------- | ------------------------------ | ------------------------------ | ------------------------------ | ------------------------------ | ------------------------------ | -------------------------------------------- |
| **Motor**                       | MAD 6215 IPE                   | T-Motor P80Ⅲ P                 | T-Motor P60                    | MAD M6C12 EEE                  | Freerchobby FRC Heavy          | Hobbywing XRotor X6 Plus (integrated system) |
| **Max Thrust**                  | 11.5 kg                        | 16 kg                          | 8.5 kg                         | 9.4 kg                         | 11.5 kg                        | 11.822 kg                                    |
| **Voltage (V)**                 | 44.4V (12S)                    | 44.4V (12-14S)                 | 44.4V (12-14S)                 | 44.4V (12-14S)                 | 48V (6S-12S)                   | 44.4V (12-14S)                               |
| **Max Current (A)**             | 60A                            | 70A                            | 38A                            | 36.2A                          | 59.7A                          | 51.8A                                        |
| **Price (USD)**                 | $98                            | $199.9                         | $107.9                         | $129                           | $62                            | $97                                          |
| **Weight (g)**                  | 370 g                          | 649 g                          | 225 g                          | 257 g                          | 370 g                          | 710 g (integrated)                           |
| **Recommended Propeller**       | 21-22"                         | 30-32"                         | 22"                            | 21-24"                         | 22"                            | 24"                                          |
| **Propeller Cost Estimation**   | $28                            | $45                            | $28                            | $28                            | $28                            | Included                                     |
| **Propeller Weight Estimation** | 0.065 kg                       | 0.170 kg                       | 0.065 kg                       | 0.065 kg                       | 0.065 kg                       | Included                                     |
| **ESC**                         | MAD AMPX 80A (5-14S) Drone ESC | MAD AMPX 80A (5-14S) Drone ESC | MAD AMPX 80A (5-14S) Drone ESC | MAD AMPX 80A (5-14S) Drone ESC | MAD AMPX 80A (5-14S) Drone ESC | Included                                     |
| **ESC Cost**                    | $60                            | $60                            | $60                            | $60                            | $60                            | Included                                     |
| **ESC Weight**                  | 0.19 kg                        | 0.19 kg                        | 0.19 kg                        | 0.19 kg                        | 0.19 kg                        | Included                                     |
| **System Thrust**               | 46 kg                          | 64 kg                          | 34 kg                          | 37.6 kg                        | 46 kg                          | 47.288 kg                                    |
| **System Weight**               | 2.5 kg                         | 4.035 kg                       | 1.92 kg                        | 2.048 kg                       | 2.5 kg                         | 2.84 kg                                      |
| **System Cost**                 | $744                           | $1,219.6                       | $783.6                         | $868                           | $600                           | $388                                         |

The **Hobbywing XRotor X6 Plus integrated propulsion system** is selected as the best match for QUIVER propulsion requirements in terms of thrust, weight, and cost. Integrated propulsion systems combine a motor, ESC, and propeller into one optimized unit. This system offers the lowest cost compared to other evaluated options, with comparable weight. It includes power cables which can be trimmed to the necessary length. Advantages of an integrated system include optimized performance due to matched components, reduced electrical losses from shorter wiring, improved aerodynamics, and waterproof casing, significantly reducing installation workload.

## Selected Battery

The **Tattu 14S HV 30000mAh Smart Battery** is chosen for its integrated battery management system (BMS) and efficient mechanical integration. The battery connects to the drone through a specialized Molex connector, secured by a safety latch.

Table 6: Tattu battery data

| Specification                        | Details                                     |
| ------------------------------------ | ------------------------------------------- |
| **Configuration**                    | 14S1P (14 series, 1 parallel)               |
| **Nominal Capacity**                 | 30,000 mAh (0.2C, 4.3-3.0V)                 |
| **Minimum Shipping Voltage**         | 52.5 \~ 54.6V (3.75-3.9V per cell)          |
| **Nominal Voltage**                  | 53.2V (3.8V per cell)                       |
| **Internal Resistance**              | 9 ± 3.5 mΩ (1 kHz AC method)                |
| **Dimensions (H×W×L)**               | MOLEX: 103 × 251 × 333 mm                   |
| **Battery Weight**                   | 11,200 ± 300 g                              |
| **Charging Mode**                    | CC-CV (Constant Current – Constant Voltage) |
| **Maximum Charging Voltage**         | 60.9V                                       |
| **Standard Charging Current**        | 6A (0.2C, \~450 min charge time)            |
| **Fast Charging Current**            | 150A (5C, \~18 min charge time)             |
| **Discharge Cut-off Voltage**        | 3.0V/cell @ 0.2C, 3.3V/cell @ ≥0.5C         |
| **Standard Discharge Current**       | 6A (0.2C, \~270 min discharge time)         |
| **Max Continuous Discharge Current** | 180A (\~9 min discharge time)               |
| **Peak Discharge Current**           | 220A (≤ 3s)                                 |

Table 7: Quiver PT2 Propulsion System Configuration

| #   | PART DESCRIPTION                                      | EQ DESIGNATION     | WEIGHT (g) |
| --- | ----------------------------------------------------- | ------------------ | ---------- |
| 1   | Hobbywing XRotor X6 Plus integrated propulsion system | MOTOR,PROP,ESC, LF | 710        |
| 2   | Hobbywing XRotor X6 Plus integrated propulsion system | MOTOR,PROP,ESC, RF | 710        |
| 3   | Hobbywing XRotor X6 Plus integrated propulsion system | MOTOR,PROP,ESC, LR | 710        |
| 4   | Hobbywing XRotor X6 Plus integrated propulsion system | MOTOR,PROP,ESC, RR | 710        |
| 5   | TATTU 14S HV 30000mAh Smart Battery                   | BATTERY, MAIN      | 11250      |

## Propulsion System Mechanical Interfaces

The Hobbywing XRotor X6 Plus integrated propulsion system must be mounted on a 30 mm diameter tube, with cables routed internally. The system is secured using four included screws.

The battery connects via a specialized Molex connector, featuring a safety latch for secure, simplified installation.

## Installation Requirements

Follow manufacturer guidelines for secure mechanical mounting, correct internal cable routing, and proper electrical connections to ensure optimal system performance and safety.

## Electrical System

This section provides a comprehensive overview of the electrical design and integration work carried out for Quiver PT2. It details the planning, layout, and execution of the power and signal systems essential for the second iteration of Project Quiver, which is engineered to deploy a brush bullet payload. The report outlines power and signal layouts,  wiring schematics, along with an in-depth review of the selected components—from battery systems and power distribution boards to flight controllers and ESCs. Finally, it covers critical considerations such as wiring methods, connector selection, and the integration of control signals via the flight controller.

### 7.1 System Design and Layout

Image 2: Main PCB layout with system overview

![](https://holocron.so/uploads/ea2e17c4-quiver-pt2-main-pcb-overview.png)

The electrical power layout is dedicated to providing power from the battery to the ESCs via the main PCB. An additional SSR and fuse are used to protected the power system and to offer emergency shut off options. The main PCB additionally provides power to all of the outgoing connections and all internal components.

All signals are routed through the main PCB. Some components are attached with a wire connector to the PCB, some are directly connected via a pin header. Following devices are connected to the canbus: Flight controller, altimeter, GNSS, RPI, ESCs. Following devices are connected via UART: Flight controller, telemetry module, RPI. An additional signal that is being used is a GPIO signal coming from the flight controller to enable the main power via the SSR.

Image 3: Front compartment overview

![](https://holocron.so/uploads/f2c1ef94-quiver-pt2-front-compartment.png)

Image 4: Front compartment with main PCB and wiring skeleton

![](https://holocron.so/uploads/6fe6d90c-quiver-pt2-wiring-sceleton.png)

### 7.2 Hardware Selection

#### Main PCB

Summary of capabilities:

- Pre-charge circuit
- SSR control
- 12V power regulation, fused output
- 5V power regulation fused output
- Communication protocols: CAN, UART, and Aux signals (PWM, GPIO, etc.)
- Several EURO connectors for easy maintenance
- XT60 output connectors for the motors
- Screw terminals for battery power connection
- Onboard computer with canbus connection (RPI)
- Onboard GNSS module
- Onboard telemetry module

Image 5: Front and back of the main PCB

![](https://holocron.so/uploads/49c77002-quiver-pt2-main-pcb-front-back.png)

##### Pre-charge and SSR control

The SSR in the front compartment activates full battery power to the ESCs and all other devices that run on the battery voltage. It is controlled by the user via a toggle switch on their RC that instructs the flight controller to set one of the GPIOs in high state (3.3V). The SSR is then activated. It allows the user to safely disconnect the power to the ESCs and motor in the case of an emergency or at the end of operation.\
The precharge is already activated as soon as the main toggle switch on the aircraft is activated. Do note that it will not supply enough current to spin the motors. The pre-charge allows the capacitors on the ESCs to be partially filled and prevents a large in rush current once the SSR is closed. This is important to mitigate any electrical arcing and damaging the ESCs.

Image 6: Main PCB schematic

![](https://holocron.so/uploads/d2bf10b8-quiver-pt2-main-pcb-schematics-seite-1.png)

##### Main PCB Design Files

Click here for KiCAD project files including CAD and manufacturing files.

Table 8: Main PCB BOM

| Reference                               | Value                     | Footprint                                                 | Qty | MPN                       | Checked | Ordered from   | Date     |
| --------------------------------------- | ------------------------- | --------------------------------------------------------- | --- | ------------------------- | ------- | -------------- | -------- |
| C1,C2                                   | 8pF                       | Capacitor_SMD:C_0603_1608Metric_Pad1.08x0.95mm_HandSolder | 2   | CC0603JRNPO9BN8R0         | True    | Mouser         | 1/8/2025 |
| C3,C4,C5                                | 100nF                     | Capacitor_SMD:C_0805_2012Metric_Pad1.18x1.45mm_HandSolder | 3   | CC0805KRX7R9BB104         | True    | Mouser         | 1/8/2025 |
| D1,D2                                   | PESD0603-240              | Samacsys:DIONC1608X55N                                    | 2   | PESD0603-240              | True    | Mouser         | 1/8/2025 |
| IC1                                     | CPC1002NTR                | Samacsys:SOP254P610X216-4N                                | 1   | CPC1002NTR                | True    | Mouser         | 1/8/2025 |
| J1                                      | mRX-TX_SSQ-104            | Samacsys:mRX-TX_SSQ-104                                   | 1   | SSQ-104-01-L-D            | True    | Mouser         | 1/8/2025 |
| J1 mating part                          | mRX-TX_TSW-104            | -                                                         | 1   | TSW-104-07-G-D            | True    | Mouser         | 1/8/2025 |
| J2                                      | RPI_5_WITH_SSQ-120-01-F-D | Samacsys:RPI_5_WITH_SSQ-120-XX-YYY-D                      | 1   | SSQ-120-01-F-D            | True    | Mouser         | 1/8/2025 |
| J4                                      | FCPDB_HC_PINS             | Snapeda:FCPDB                                             | 12  | H2182-05                  | True    | Mouser         | 1/8/2025 |
| J5,J6,J7,J8                             | XT60PW-M                  | Snapeda:XT60PW-M_AMASS_XT60PW-M                           | 4   | XT60PW-M                  | True    | TME            | 1/8/2025 |
| J5,J6,J7,J8 mating part                 | XT60H-F                   | nan                                                       | 4   | XT60H-F                   | True    | TME            | 1/8/2025 |
| J9,J10,J19                              | Screw Terminal 7461096    | Samacsys:7461096                                          | 3   | 7461096                   | True    | Mouser         | 1/8/2025 |
| J11                                     | 39512-1005_M1             | Samacsys:395121005                                        | 1   | 39512-1005                | True    | Mouser         | 1/8/2025 |
| J12                                     | 39512-1005_M2             | Samacsys:395121005                                        | 1   | 39512-1005                | True    | Mouser         | 1/8/2025 |
| J13                                     | 39512-1005_M3             | Samacsys:395121005                                        | 1   | 39512-1005                | True    | Mouser         | 1/8/2025 |
| J14                                     | 39512-1005_M4             | Samacsys:395121005                                        | 1   | 39512-1005                | True    | Mouser         | 1/8/2025 |
| J11, J12, J13, J14 mating part          | 39510-0005                | nan                                                       | 4   | 39510-0005                | True    | Mouser         | 1/8/2025 |
| J15                                     | 39512-1007                | Samacsys:395121007                                        | 1   | 39512-1007                | True    | Mouser         | 1/8/2025 |
| J15 mating part                         | 39510-0007                | nan                                                       | 1   | 39510-0007                | True    | Mouser         | 1/8/2025 |
| J16,J17,J18,J24,J25,J26,J27             | 39512-1004                | Samacsys:395121004                                        | 7   | 39512-1004                | True    | Mouser         | 1/8/2025 |
| J16,J17,J18,J24,J25,J26,J27 mating part | 39510-0004                | nan                                                       | 7   | 39510-0004                | True    | Mouser         | 1/8/2025 |
| J20,J21                                 | 39512-1002                | Samacsys:SHDRRA2W80P0X381_1X2_901X920X730P                | 2   | 39512-1002                | True    | Mouser         | 1/8/2025 |
| J20,J21 mating part                     | 39510-0002                | nan                                                       | 2   | 39510-0002                | True    | Mouser         | 1/8/2025 |
| J22,J23                                 | 203556-1207               | Samacsys:2035561207                                       | 2   | 203556-1207               | True    | Mouser         | 1/8/2025 |
| J22,J23 mating part 1                   | Wire Housing 501330-1200  | -                                                         | 2   | 501330-1200               | True    | Mouser         | 1/8/2025 |
| J22,J23 mating part 2                   | Crimps                    | -                                                         | 100 | 538-501334-0000-CT        | True    | Mouser         | 1/8/2025 |
| J28                                     | USB3075-30-A              | Samacsys:USB307530A                                       | 1   | USB3075-30-A              | True    | Mouser         | 1/8/2025 |
| R1,R6                                   | R not specified yet       | Resistor_SMD:R_0805_2012Metric_Pad1.20x1.40mm_HandSolder  | 2   | -- value not specified -- | True    | In house stock | 1/8/2025 |
| R2                                      | PRE_3                     | Samacsys:PWR163S2550R0F                                   | 1   | PWR163S-25-50R0F          | True    | Mouser         | 1/8/2025 |
| R3                                      | PRE_2                     | Samacsys:PWR163S2550R0F                                   | 1   | PWR163S-25-50R0F          | True    | Mouser         | 1/8/2025 |
| R4                                      | PRE_1                     | Samacsys:PWR163S2550R0F                                   | 1   | PWR163S-25-50R0F          | True    | Mouser         | 1/8/2025 |
| R5,R7,R9,R10,R11                        | 10K                       | Resistor_SMD:R_0805_2012Metric_Pad1.20x1.40mm_HandSolder  | 5   | RC0805FR-7W10KL           | True    | Mouser         | 1/8/2025 |
| R8                                      | 0R                        | Resistor_SMD:R_0805_2012Metric_Pad1.20x1.40mm_HandSolder  | 1   | RC0805FR-070RL            | True    | Mouser         | 1/8/2025 |
| R12                                     | 120                       | Resistor_SMD:R_0805_2012Metric_Pad1.20x1.40mm_HandSolder  | 1   | RC0805FR-07120RL          | True    | Mouser         | 1/8/2025 |
| S1                                      | SLW-913535-2A-SMT         | Samacsys:SLW9135352ASMT                                   | 1   | SLW-913535-2A-SMT         | True    | Mouser         | 1/8/2025 |
| U1,U2,U3                                | 178.6165.0002             | Samacsys:17861650002                                      | 3   | 178.6165.0002             | True    | Mouser         | 1/8/2025 |
| U4                                      | PRE_F                     | Samacsys:17861650002                                      | 1   | 178.6165.0002             | True    | Mouser         | 1/8/2025 |
| U5                                      | MCP2515-I/SO              | Samacsys:SOIC127P1030X265-18N                             | 1   | MCP2515-I/SO              | True    | Mouser         | 1/8/2025 |
| U6                                      | TJA1049T/3J               | Samacsys:SOIC127P600X175-8N                               | 1   | TJA1049T/3J               | True    | Mouser         | 1/8/2025 |
| X1                                      | 16MHz                     | Samacsys:NX3225GD-STD-CRA-3                               | 1   | NX3225GB-16M-STD-CRA-2    | True    | Mouser         | 1/8/2025 |

#### Flight Controller

Model: Flight Controller H743-SLIM V3

- 7x UART (1,2,3,4,6,7,8) with built-in inversion.

- 13x PWM outputs(including “LED” pad)

- 2x I2C

- 1x CAN

- 6x ADC (VBAT, Current, RSSI, Analog AirSpeed, Vbat2, Cur2)

- 3x LEDs for FC STATUS (Blue, Red) and 3.3V indicator(Red)

- 1x SPI3 breakout

- USB Type-C(USB2.0)

- 1x JST-SH1.0_8pin connector (Vbat/G/Curr/Rx8/S1/S2/S3/S4)

- 1x JST-GH1.25_4pin connector (5V/CAN-H/CAN-L/G)

- Dual Camera Inputs switch

- 5V/Vbat filtered power ON/OFF switch

Image 7: Flight Controller

![](https://holocron.so/uploads/92ab6aa0-quiver-pt2-fc.png)

#### PDB with power supply

Model: Mateksys XCLASS PDB FCHUB-12S

Image 8: PDB with power supply

![](https://holocron.so/uploads/9c089f31-quiver-pt2-pdb.png)

#### GNSS

For the GPS a Mateksys AP DroneCAN M10Q-3100 GNSS module is used. This module is no longer produced. Instead the Mateksys AP DroneCAN GNSS M9N-G4-3100 can be used.

Image 9: GNSS

![](https://holocron.so/uploads/b1a79290-quiver-pt2-gnss.png)

#### telemetry transmitter and receiver

The receiver in this setup is the Mateksys mLRS mR24-30 (MAVLink 2.4GHz) receiver. The transmitter is the Mateksys mR24-30-TX mLRS MAVLink 2.4GHz TX Module KIT. The mLRS project offers an open source 2.4 GHz & 915/868 MHz & 433 MHz/70 cm LoRa-based high-performance long-range radio link, which provides bidirectional serial connection combined with full remote control.

The main positive aspects of the mLRS system are:

- relatively cheap
- 2.4 GHz, 915/868 MHz, 433 MHz/70 cm
- LoRa
- full-duplex serial link with sufficient data rate
- plenty full-size RC channels
- open source
- rich features and outstanding performance for MAVLink systems

Image 10: telemetry receiver and transmitter

![](https://holocron.so/uploads/0e93eb25-quiver-pt2-telemetrie.png)

#### Onboard computer

The onboard computer is an Raspberry Pi 5 8GB with an active cooling fan. Older versions of the RPI can also be used, since the pin header is mostly the same.

Image 11: Onboard computer

![](https://holocron.so/uploads/344e8515-quiver-pt2-computer.png)

#### Tattu 3.5 14S - 53.2V 30000 mAh

Image 12: Battery

![](https://holocron.so/uploads/35d9609a-tattu-3.5-14s-53.2v-30000-mah.png)

- Capable of CAN communication. Current battery used is on firmware xx.xx and was not compatible with Ardupilot.
- Battery side connector: Molex EXTreme 46562-9206 manually latching with 46562-9306 = 46562-2657 (a non-official part number)
- Mates to: Molex EXTreme 46437-9206 manually latching with 46437-9306
- See Propulsion System for detailed specs

#### Battery Adapter

[Link to the part](https://store.effort-tech.com/products/1005980019-brand-new-battery-plug-molex-1pcs-for-eft-drone-frame-spare-parts-from-professional-chinese-manufacurer)

Link to the shop: [https://store.effort-tech.com/](https://store.effort-tech.com/)

Image 13: Battery adapter

![](https://holocron.so/uploads/cb85047c-battery-adapter.png)

#### Solid state relay

Model: 70V 140/280A

Table 9: Different variations of the SSR

| Specification             | 34V 60/120A             | 34V 60/120A (Multicopters) | 70V 60/120A             | 70V 100/200A            | 70V 140/280A            | 60V 60/120A     | 60V 120/240A   | XL 180/360A          |
| ------------------------- | ----------------------- | -------------------------- | ----------------------- | ----------------------- | ----------------------- | --------------- | -------------- | -------------------- |
| Suitable batteries (LiPo) | 2S ... 8S               | 2S ... 8S                  | 6S ... 16S              | 6S ... 16S              | 6S ... 16S              | 6S ... 14S      | 6S ... 14S     | 3S ... 16S           |
| Voltage range             | 6V ... 34V              | 6V ... 34V                 | 18V ... 70V             | 18V ... 70V             | 18V ... 70V             | 18V ... 60V     | 18V ... 60V    | 12V ... 70V          |
| Current consumption (off) | max. 0.5mA, typ. 0.25mA | Info coming soon           | max. 0.5mA, typ. 0.25mA | max. 0.5mA, typ. 0.25mA | max. 0.5mA, typ. 0.25mA | ---             | ---            | ---                  |
| Permanent current\*       | 60A                     | 100A                       | 60A                     | 100A                    | 140A                    | 60A             | 120A           | 180A                 |
| Maximum peak current\*\*  | 120A                    | 200A                       | 120A                    | 200A                    | 280A                    | 120A            | 240A           | 360A                 |
| Power dissipation @ 50A   | approx. 5W              | Info coming soon           | approx. 2.25W           | approx. 7.3W            | approx. 9.6W            | ---             | ---            | ---                  |
| Dimensions                | 65 x 30 x 9.3mm         | 65 x 30 x 9.3mm            | 65 x 30 x 9.3mm         | 65 x 30 x 16mm          | 65 x 30 x 20mm          | 65 x 30 x 9.3mm | 65 x 30 x 16mm | 82.4 x 62.4 x 26.5mm |
| Weight                    | 45g                     | 45g                        | 45g                     | 71g                     | 105g                    | 45g             | 71g            | 195g                 |

Image 14: Solid state relay

![](https://holocron.so/uploads/083a7a4b-solid-state-relay.png)

Manual: [https://www.hacker-motor.com/daten/anleitungen/emcotec/sps-safetypowerswitch_quick-reference-guide_DE-EN.pdf](https://www.hacker-motor.com/daten/anleitungen/emcotec/sps-safetypowerswitch_quick-reference-guide_DE-EN.pdf)

#### Main Fuse

Model: SIBA 9005805.200

Rating: 200A, 80VDC

Image 15: Main fuse

![](https://holocron.so/uploads/7653be2a-quiver-pt2-fuse.png)

#### Altimeter

Model: Benewake TF03-100 in canbus configuration.

Note: Canbus and UART can not be used at the same time.

The Benewake TF03-100 is a highly accurate LiDAR distance sensor designed for UAV altitude measurement and obstacle avoidance, offering stable performance in challenging conditions. It provides precise measurements at ranges up to 100 meters, enhancing UAV navigation reliability and safety.

Image 16: Altimeter

![](https://holocron.so/uploads/6af69e46-quiver-pt2-altimeter.png)

#### Gimbal Camera

Model: SIYI A8 gimbal camera

In this prototype the SIYI camera is connected to he power connectors on the main PCB and the signal is shared over ethernet with the RPI. The ethernet cable is going from the SIYI camera directly into the ethernet port of the RPI.

Image 17: Gimbal camera

![](https://holocron.so/uploads/e70216ce-siyi-a8.png)

#### Brush Bullet Dispenser

[Brush Bullet Applicator Pod](https://brush-bullet.myshopify.com/products/applicator-pod) Variant

Image 18: Brush bullet dispenser

![](https://holocron.so/uploads/e19737c6-brush-bullet-dispenser.png)

[Onshape Model](https://cad.onshape.com/documents/9d9eb91af3f6540b56a5ea5a/w/635a8ab526b8b9d145aa4388/e/e4f46004af7e190882276375)

#### Attachment Interface

Image 19: Attachment interface

![](https://holocron.so/uploads/9c76b7b4-quick-release-mount.png)

### 7.3 Wiring

- All components (except the front compartment assembly of SSR, Fuse and battery connector) have a direct connection to the main PCB. The pinouts are clearly labeled on the the PCB. Please follow the specific device manual to identify which cable color is for which pin function.
- The EURO plug connectors offer an easy way to attach the cables to the PCB. Make sure the cable ends are stripped from the insulation and enough copper goes into the connector. Tighten the screws with a appropriate amount of torque.

## Geometry & Structure

The design of this aircraft centers on incorporating the battery below all the main electric systems and the integration of a main PCB that is handling all of the electrical connections. The location of the main PCB on top of the drone structure is reserving straightforward access to all key components. The system can be quickly reconfigured or expanded to integrate novel sensors, payloads, or propulsion elements. Structural integrity is achieved through robust aluminum structure that is riveted and glued together with connections that distribute loads uniformly. This approach enables the prototype to withstand potentially harsh landings, while finite element analysis (FEA) helps validate each subsystem’s load-bearing capacity. Furthermore, by minimizing mass through efficient structural layouts and selective material use, the aircraft maintains better flight performance, high agility, and reduced power consumption to extend operational times.

---

## 8.1. Overall Geometry

The overall geometry is largely symmetrical. The main components are responsible for the general dimensions of the prototype. The battery is intentionally placed in the bottom part of the structure, shifting the center of gravity (CG) downwards to enable a stable flight.

Below is a summary of the aircraft’s key dimensional parameters:

Table 10: Dimensional parameters

| **Parameter**                             | **Measurement** |
| ----------------------------------------- | --------------- |
| Folded Width                              | 60 cm           |
| Folded Length                             | 60 cm           |
| Unfolded Width (propellers still folded)  | 93 cm           |
| Unfolded Length (propellers still folded) | 93 cm           |
| Overall Height                            | 64 cm           |
| Max Attachment Height                     | 40 cm           |
| Max Attachment Diameter                   | 30 cm           |

These dimensions ensure balanced weight distribution in both folded and unfolded states while providing adequate space for payloads and accessories.

### Subsystem Weight Breakdown

Below are several weight breakdowns for the major subsystems. The last table shows the overall subsystem weight breakdown. These figures are meant to serve as general estimates. Some weights were measured, some were taken from the CAD, some were taken from the slicer of the 3D printer, some were taken from documentation and some are simple estimates.

Table 11: Breakdown of the weight of the structure

| Structure Part                       | Weight (g) | Quantity | Total Weight (g) |
| ------------------------------------ | ---------- | -------- | ---------------- |
| Top plate 2mm aluminum               | 410        | 1        | 410              |
| Bottom plate 2mm aluminum            | 419        | 1        | 419              |
| Small square tube 40x40x2 aluminum   | 102        | 2        | 204              |
| Small square tube 40x40x2 aluminum   | 237        | 1        | 237              |
| Sides rectangle 30x100x2 aluminum    | 271        | 2        | 542              |
| Attachment plate 4mm aluminum        | 587        | 1        | 587              |
| Folding arm adapter                  | 149        | 4        | 596              |
| CF motor beam                        | 47         | 4        | 188              |
| CF landing leg beam                  | 52         | 4        | 208              |
| CF landing leg bottom beam           | 65         | 2        | 130              |
| Landing leg adapter top (aluminum)   | 47         | 4        | 188              |
| Landing leg adapter bottom (printed) | 46.5       | 4        | 186              |
| Rivets/Screws/Paint                  | 100        | 1        | 100              |
| **Total**                            |            |          | 3995             |

Table 12: Breakdown of the weight of the main PCB assembly

| PCB Part                                            | Weight (g) | Quantity | Total Weight (g) |
| --------------------------------------------------- | ---------- | -------- | ---------------- |
| Bare PCB                                            | 107        | 1        | 107              |
| Matek flight controller                             | 13         | 1        | 13               |
| Matek PDB                                           | 28         | 1        | 28               |
| Matek GNSS module                                   | 15         | 1        | 15               |
| Matek telemetry module                              | 10         | 1        | 10               |
| Raspberry Pi 5 with active cooler                   | 54         | 1        | 54               |
| Copper                                              | 100        | 1        | 100              |
| C1,C2, CC0603JRNPO9BN8R0                            | 0.02       | 2        | 0.04             |
| C3,C4,C5, CC0805KRX7R9BB104                         | 0.03       | 3        | 0.09             |
| D1,D2, PESD0603-240                                 | 0.02       | 2        | 0.04             |
| IC1, CPC1002NTR                                     | 0.15       | 1        | 0.15             |
| J1, SSQ-104-01-L-D                                  | 0.5        | 1        | 0.5              |
| J1 mating part, TSW-104-07-G-D                      | 0.5        | 1        | 0.5              |
| J2, SSQ-120-01-F-D                                  | 1.2        | 1        | 1.2              |
| J4, H2182-05                                        | 0.8        | 12       | 9.6              |
| J5,J6,J7,J8, XT60PW-M                               | 7.5        | 4        | 30               |
| J5,J6,J7,J8 mating part, XT60H-F                    | 6.5        | 4        | 26               |
| J9,J10,J19, 7461096                                 | 2          | 3        | 6                |
| J11,J12,J13,J14, 39512-1005                         | 1          | 4        | 4                |
| J11,J12,J13,J14 mating part, 39510-0005             | 0.8        | 4        | 3.2              |
| J15, 39512-1007                                     | 1.2        | 1        | 1.2              |
| J15 mating part, 39510-0007                         | 1          | 1        | 1                |
| J16,J17,J18,J24,J25,J26,J27, 39512-1004             | 0.8        | 7        | 5.6              |
| J16,J17,J18,J24,J25,J26,J27 mating part, 39510-0004 | 0.6        | 7        | 4.2              |
| J20,J21, 39512-1002                                 | 0.5        | 2        | 1                |
| J20,J21 mating part, 39510-0002                     | 0.4        | 2        | 0.8              |
| J22,J23, 203556-1207                                | 1.5        | 2        | 3                |
| J22,J23 mating part 1, 501330-1200                  | 0.8        | 2        | 1.6              |
| J22,J23 mating part 2, 538-501334-0000-CT           | 0.02       | 100      | 2                |
| J28, USB3075-30-A                                   | 2          | 1        | 2                |
| R1,R6, -- value not specified --                    | 0.03       | 2        | 0.06             |
| R2,R3,R4, PWR163S-25-50R0F                          | 1          | 3        | 3                |
| R5,R7,R9,R10,R11, RC0805FR-7W10KL                   | 0.03       | 5        | 0.15             |
| R8, RC0805FR-070RL                                  | 0.03       | 1        | 0.03             |
| R12, RC0805FR-07120RL                               | 0.03       | 1        | 0.03             |
| S1, SLW-913535-2A-SMT                               | 1.5        | 1        | 1.5              |
| U1,U2,U3, 178.6165.0002                             | 0.8        | 3        | 2.4              |
| U4, 178.6165.0002                                   | 0.8        | 1        | 0.8              |
| U5, MCP2515-I/SO                                    | 0.25       | 1        | 0.25             |
| U6, TJA1049T/3J                                     | 0.2        | 1        | 0.2              |
| X1, NX3225GB-16M-STD-CRA-2                          | 0.1        | 1        | 0.1              |
| **Total**                                           |            |          | 439.24           |

Table 13: Breakdown of the weight of the front compartment

| PCB Part                       | Weight (g) | Quantity | Total Weight (g) |
| ------------------------------ | ---------- | -------- | ---------------- |
| Front compartment part         | Weight (g) | Quantity | Total Weight (g) |
| SafetyPowerSwitch 70V 140/280A | 105        | 1        | 105              |
| Fuse                           | 16.42      | 1        | 16.42            |
| Battery adapter                | 130        | 1        | 130              |
| Cables                         | 200        | 1        | 200              |
| Cable lug                      | 10         | 6        | 60               |
| 3D print front compartment 1   | 82.64      | 1        | 82.64            |
| 3D print front compartment 2   | 59.94      | 1        | 59.94            |
| **Total**                      |            |          | 654              |

Table 14: Weight of the main assembly

| Main Assembly                    | Weight (g) | Quantity | Total Weight (g) |
| -------------------------------- | ---------- | -------- | ---------------- |
| Structure                        | 3995       | 1        | 3995             |
| PCB assembly                     | 439.24     | 1        | 439.24           |
| Front compartment                | 654        | 1        | 654              |
| Motor+Propeller+ESC+Cable        | 710        | 4        | 2840             |
| 3D printed main PCB adapter      | 68.2       | 1        | 68.2             |
| Battery                          | 11250      | 1        | 11250            |
| 3d printed battery slider        | 32.61      | 2        | 65.22            |
| Lidar with adapter               | 77         | 1        | 77               |
| SIYI gimbal camera               | 109        | 1        | 109              |
| 3D printed lid                   | 215        | 1        | 215              |
| 3d printed lid clip              | 2          | 2        | 4                |
| Clear PC window for lid          | 50         | 1        | 50               |
| Hinge for lid                    | 25         | 2        | 50               |
| Landing gear foam                | 8          | 4        | 32               |
| 3D printed main switch housing   | 24.8       | 1        | 24.8             |
| Main switch                      | 10         | 1        | 10               |
| Quick release attachment adapter | 66         | 1        | 66               |
| Screws                           | 20         | 1        | 20               |
| **Total without battery**         |            |          | 8719.46          |
| **Total with battery**           |            |          | 19969.46         |

### Remaining Payload Capacity: 5,030 kg

Please note that these weights are not definitive values and should be verified after prototype assembly and testing.

---

## 8.2. Detailed Zones

### Main Chassis

Three parallel aluminum plates, two rectangular aluminum tubes and two square tubes form the central chassis of the aircraft. These parts are riveted together. Additional adhesive is used between the faces to to dampen vibrations and make the structure even stiffer. The two upper plates are connected by the motor mounts on the corners and the two square tubes in the center. The two rectangular tubes connect the top section and the attachment plate that sits in the bottom of the main structure.

---

### Motors

Each motor is situated at the end of a 360mm-long, 30 mm-diameter carbon fiber arm that extends radially from the central chassis. These arms are attached to the plates using hinged, foldable connectors made out of aluminum. The hinging mechanism typically includes a locking pin, which secures the arms in flight position and allows rapid folding for compact transport. The motor mounts are supplied by the motor manufacturer, embedded around the motor.

---

### Landing Gear

The landing gear system employs 30 mm-diameter carbon fiber tubes attached with off-the-shelf aluminum housing under the central chassis. Two vertical tubes are connected to one horizontal tube on the bottom with 3D printed tube connectors. The tubes position the aircraft at a large ground clearance, giving enough height for any attachments.

---

### Battery Space

The battery sits in the middle of the aluminum structure. The structure is designed in a way, that the battery can slide between the two rectangular aluminum tubes. 3D printed sliders are used to slide the battery into the structure with ease. Because of the location of the battery inside the aluminum structure, it is well protected in case of a crash.

---

### Electrical Compartment

The electrical compartment consolidates the high and low power distribution as well as the all the signal distribution into one space. The battery connector is located in the front of the compartment next to the fuse and main SSR. Wires are attaching to the main PCB which integrates most of the functions of the drone (in detail description see chapter #7). By integrating most functions into one PCB a lot of space is saved and the cabling work is significantly reduced. All components are easily accessible for any troubleshooting or replacement.

---

### Belly Equipment

The underside of the aircraft provides dedicated screw holes for the attachment of the altimeter , the gimbal camera  and the payload adapter. The attachment is connected to the payload adapter utilizing a quick release mechanism. The gimbal camera and the altimeter are located on a 3D-printed adapter.

8.3 FEA analysis

The FEM demonstrate how the structure will behave under the following forces:

- 12.5 Kg of force acting at the end of each motor beam (full throttle).

- 50 kg of counterforce acting on the attachment plate.

- The materials in this study are:

  - Aluminum 6060 for all the foldable motor arm connectors, upper landing gear adapters, aluminum plates, rectangle aluminum tubes.
  - Carbon fiber for the motor arms and landing gear legs.

**Note:** The structure is constrained at the bottom landing legs. They will not feel any force, as the forces in flight only act in the cockpit, and this has been taken into account in this simulation (force and counterforce).

### Safety

Image 20: FEA safety

![](https://holocron.so/uploads/6f008d11-image.png)

### Displacement

Image 21: FEA displacement

![](https://holocron.so/uploads/c8a84756-image.png)

### Stress

Image 22: FEA stress

![](https://holocron.so/uploads/859d38cb-image.png)

Image 23: FEA stress 2

![](https://holocron.so/uploads/9ec4db9b-image.png)

Stress detail:

Image 24: FEA stress detail

![](https://holocron.so/uploads/937426df-image.png)

### Results Summary

- The aluminum structure has very low stress values indicating a high possibility of weight savings through the removal of material and the reduction of component thickness.

- The results yielded a 2.318 safety factor at the motor arm adapter. The required safety factor of 2.5 was not quite achieved, but this is no cause for concern as this condition only occurs in extreme cases. Under normal conditions, the safety factor is around 4.0. Furthermore, the adapter was tested under maximum thrust and no permanent deformations were detected. A dynamic simulation was not carried out.

- The max displacement of one of the motor beams reached 2.31 mm.

- The max stress occurred at the motor beam to foldable motor arm connector with a value of 159.175 Mpa.

**Recommendation:**

- Observation of the motor arm adapter.
- Dynamic simulation in the future.
- Weight reduction of the aluminum structure.

## Appendix

\-
