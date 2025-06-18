# PT 3 Flight Controller PCB

# Status

`Valid`

`Revision History: V1`

`Replacement Log: None`

`Reference: PT3 PCB Spec information note`

# Project Description
## PCB Overview

The FC PCB is an adapter board for the Pix 32 V6 flight controller. It includes breakouts for the various PWM, GPIO, GPS, I²C, CAN, S.BUS, and power pins on the flight controller. Various components were included based on the documentation provided by Holybro for the Pix32 V6 Schematic.

# Methodology
Reviewed and studied the PT3 FC PCB design files from Julius. Discussed and developed understanding over various direct messages and calls. 
Designed was based on the information provided in the [PT3 PCB Spec information note](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/pt3/electronics/0001-PCB-Spec/information-note.md).

# Results and Deliverables

## Schematics and CAD files

![FCPCB](https://github.com/user-attachments/assets/45920029-1f06-4030-a8d5-ef6df8b8cb7f)
<sub>***FC PCB Schematic***</sub>

![editor1](https://github.com/user-attachments/assets/bd965d1a-349f-4028-9fef-d120dd88fc03)
<br />
<sub>***PCB All Layers***</sub>

![editor - top](https://github.com/user-attachments/assets/7bccf4f6-7c60-4aed-9787-55d23e133e93)
<br />
<sub>***PCB Top Traces***</sub>

![editor - bottom](https://github.com/user-attachments/assets/c3a10c2f-dd78-4a84-8c81-65bfab8d7038)
<br />
<sub>***PCB Bottom Traces***</sub>

![FCPCB top](https://github.com/user-attachments/assets/1a479517-a6a7-4d9a-a4a2-57c13f6a1748)
<sub>***PCB CAD front***</sub>

![FCPCB bottom](https://github.com/user-attachments/assets/22b2bbae-5e97-4ace-9c1c-36cd5be77680)
<sub>***PCB CAD back***</sub>

### PCB Build Specifications

- Base material: FR-4
- Dimensions: XXXX mm x XXXX mm
- Layers: 4
- PCB thickness: 1.6 mm
- PCB Color: Blue
- Silkscreen: White
- Material Type: FR-4 TG155
- Via Covering: Plugged
- Min via hole size/diameter: 0.3mm/(0.4/0.45mm)
- Surface finish: ENIG
- Gold Thickness: 2U”
- Outer/Inner Copper Weight: 2 oz each
- Board Outline Tolerance: ±0.2mm(Regular)

## Layout Description

### Inputs/Outputs

**J1 - Main Input** 

- Panasonic AXK5S00347YG
- .35A resettable fuse added on pin 98 output
- Pull-up resistors (R1-R4) on the I²C lines on pins 86, 84, 82, and 80
- Decoupling capacitors added for pins 96, 74, 70, 64, 16, and 2

**J2 & J3 - Main Output**

- Panasonic AXK5S00347YG
    - breaks out the 100 pins from J1 into two separate connectors

**LED1 - LED8** 

- status indicators for various power rails

### **Power Line Filtering and Protection**

The power outputs on the FC PCB are conditioned using a combination of EMI filters (NFM21PC104R1E3D), decoupling capacitors, and TVS diodes to ensure clean and protected power delivery to downstream systems. The inclusion of these components was based off of Holybro’s documentation (Sheet: UART-I²C-CAN). 

- **NFM21PC104R1E3D (FL1–FL8)**:
    
    3-terminal EMI suppression filters that attenuate high-frequency noise while allowing low-impedance DC power flow. Work as filters that block high frequency EMI
    
- **Decoupling Capacitors (C1–C8)**:
    
    Placed immediately after the EMI filters, these ceramic capacitors provide local energy storage and further filter high-frequency ripple, ensuring stable voltage levels.
    
- **TVS Diodes (D1 and D2)**:
    
    Transient Voltage Suppression diodes protect the power rails from electrostatic discharge (ESD), inductive kickback, and other voltage transients by clamping overvoltage conditions and safely diverting excess energy to ground.
    

### Buzzer Power Protection

Additional circuitry protects the VDD_5V_PERIPH rail from faults at the buzzer output:

- **D3 (DFLS240L-7)** is a Schottky diode that blocks reverse current from the buzzer, preventing backfeed into the 5V rail.
- **F2 (nanoSMD035F-2)** is a polyfuse that limits current in case of a buzzer short or overcurrent condition.

Together, these components isolate the buzzer from the rest of the system, ensuring faults do not affect other peripherals on the same rail.
 
# Remarks
- Design work was conducted by Julius.
- Schematic and CAD files can be found in the Quiver PT3 task and bounties directory
- information note prepared by Erick.
- Manufacturing instructions can be found in the assembly guide. 
