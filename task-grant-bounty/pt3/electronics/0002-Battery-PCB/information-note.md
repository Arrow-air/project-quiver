# PT 3 Battery PCB

# Status

`Valid`

`Revision History: None`

`Replacement Log: None`

`Reference: PT3 PCB Spec information note`

# Project Description
## PCB Overview

The Battery PCB is one of the four custom PCBs that are being designed for PT3. This PCB will be responsible for safely controlling, protecting, and monitoring the main power out from the Tattu Smart battery to the Main PCB. These features are achieved through the use of on board voltage regulators, a variety of MOSFETs, SSRs, resistors, TVS diodes, fuses, LEDs, temperature sensors, and FC control signals. The PCB will also transmit battery telemetry over CAN, temperature data over I<sup>2</sup>C, and notifying the user of various power status through the use of LEDs. 

# Methodology
Reviewed and studied the PT3 Battery PCB design files from Julius. Discussed and developed understanding over various direct messages and calls. 
Designed was based on the information provided in the [PT3 PCB Spec information note](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/pt3/electronics/0001-PCB-Spec/information-note.md).

# Results and Deliverables

## Schematics and CAD files

![image](https://github.com/user-attachments/assets/d2069ed5-11fc-4284-acd2-e70262ae9e71)
<sub>***PCB Schematic***</sub>

![image](https://github.com/user-attachments/assets/0464dc3f-7fb1-43d6-8e26-aa0a17950f73)
<sub>***PCB All layers***</sub>

![image](https://github.com/user-attachments/assets/6c28e00b-952d-481f-b907-5e7decf42872)
<sub>***PCB Traces***</sub>

![image](https://github.com/user-attachments/assets/0715c92d-a0e8-44c0-acad-2efea78f4180)
<sub>***PCB Ground Plane***</sub>

![image](https://github.com/user-attachments/assets/7d8148c0-d913-441b-97cd-1790c3cd3c88)
<sub>***PCB Front***</sub>

![image](https://github.com/user-attachments/assets/37097078-6148-4a15-b0f8-a76b30861fce)
<sub>***PCB Back***</sub>

![image](https://github.com/user-attachments/assets/d1d315af-214b-41d8-b83c-806cd963b508)
<sub>***PCB CAD front***</sub>

![image](https://github.com/user-attachments/assets/1718bb4e-d316-4642-ba28-5423d2784b7d)
<sub>***PCB CAD back***</sub>

### PCB Spec

Dimensions: 172.2 x 101.85 mm

Layers: 4 

PCB Thickness: 1.6 mm

Trace width: XX mm

## Layout Description

- J1
    - connector for pre-charge push button with LED
        - LED powered by PS1
- J2 (5 pin Eurostyle)
    - FC_2 - pre-charge termination signal from FC
    - I<sup>2</sup>C SDA & SCL - temperature data
    - CAN H & L - battery telemetry
- J3 (4 pin Eurostyle)
    - SSR_S - Enable signal for SSR U3
    - 12V and 5V input from Main PCB
    - Ground
- J5
    - Jumper for CAN connection
    - Optional if battery telemetry is not being used
- J6
    - jumper for optional pre-charge termination control
- J7 & J8
    - Press fit pins for 200A fuse
- Main input (J9 & J10)
    - custom manufactured Molex connector
        - Contact pins: 2x of Molex EXTreme 46437-9206
        - Guiding pins: 1x of Molex 464379-301
            
            ![image](https://github.com/user-attachments/assets/25b01ce6-ce58-47d5-9ec5-f6734b6db862) <sub>***Custom Molex Connector***</sub>

            
    - J9
        - P1 - P5 main negative outputs
            - 200A fuse at J7 & J8
            - will act as ground for entire circuit
        - P6 is the battery CAN_L
    - J10
        - P2 - P6 main positive output
        - P1 CAN_H
- J11 - Main output
    - AMASS power connector
    - 6 or 8 AWG cable
- Temperature Sensors (IC1 & IC2)
    - Powered by PS2 with 3.3V
    - Placed on top layer of PCB and measures temperature of pre-charge resistors and SSR MOSFETS (PCB bottom)
    - Address determined by soldering 1 jumper pad circled in red
        - Solder +3V3 (JP3) for IC1 and GND(JP6) for IC2
        
        ![image](https://github.com/user-attachments/assets/05ec57e4-b48f-41dd-9d74-34ce5bb7f4d3) <sub>***Temp Sensor Address Assignment***</sub>

        
- Main MOSFETs (Q2 - Q7) operation
    - Source connected to fused BAT -
    - Gate voltage controlled by small SSR (U3) that passes through a Vreg (U2)
        - SSR controlled by FC (make clear that this is for main power out)
    - Protections
        - 10 ohm R in series with gate input
        - 220k ohm R from gate to ground
        - TVS diode form gate to ground
    - Similar operation and protections apply to pre-charge MOSFET (Q1)
- Test points
    - TP1 - voltage divider for PS1 remote operation
        - Powered off reading: ~10-15V
        - Powered on reading: Battery voltage
    - TP2 - 5V input to PS2 (Temperature sensor voltage regulator)
    - TP3 - 3.3V PS2 output
    - TP4 - Gate voltage for Q1 MOSFET (pre-charge )
        - 12V after push button pressed
    - TP5 - Gate voltage for MOSFETs Q2-Q7
        - 12V after SSR_S triggered
    - TP6 - Battery voltage out of SSR U3
        - Battery voltage after SSR_S triggered
- The remainder of the circuit can be explained in the Circuit Operation section

## Circuit Operation

- Battery is plugged in
    - PS1 is energized but is not outputting 12V without pushbutton (J1) activation
    - Main output (J11)
        - + terminal is live
        - - terminal is open circuit with MOSFETS Q1 - Q7
    - Depending on J5 jumper placement, Battery telemetry will be on CAN bus
- User presses push button (J1)
    - LED on pushbutton will light up
    - 12V output from PS1 to Q1 MOSFET gate
    - Pre-charge will begin allowing current to pass through 200A fuse (J7 & J8), xA automotive fuse (U1), MOSFET (Q1), NC SSR (K1), pre-charge resistors (R15 - R17), and then the main negative output
    - This will allow limited power output from the Battery PCB to the Main PCB
        - pre-charge ESC capacitors
        - Power on Main PCB 12V and 5V regulators
        - Power to FC and aux components
    - This will also bring in 5V and 12V from the Main PCB
        - 5V will power the 3.3V regulator (PS2)
            - temperature sensors will be powered on(3.3V) and transmit data over I<sup>2</sup>C back to Main PCB
    - After pre-charge is complete the following LEDs will be visible on the Battery PCB exterior
        - LED5 - 3.3V (from internal voltage regulator)
        - LED6 - 5V (coming from Main PCB, J3)
        - LED6 - 12V (coming from Main PCB, J3)
- User completes pre-arm checklist
- Users sends signal to fully activate main power out from FC (SSR_S, J3) and end pre-charge signal (FC_2, J2) (Depending on JP9 and JP10 selection)
    - Two things can happen here depending on J6 jumper placement
        - With jumper
            - SSR_S or FC_2 will open the NC SSR (K1) effectively terminating the pre-charge
            - Simultaneously, SSR_S will trigger the NO SSR (U3) allowing another 12V regulator (U2) to be powered on
                - this will apply 12V to the gate of the MOSFETs (Q2 - Q7)
                - current will pass through the MOSFETs to main negative output (J3)
            - circuit will have full power output capabilities
        - without jumper
            - pre-charge will remain on
            - FC_2 will be an open circuit
            - SSR_S will trigger the NO SSR (U3) allowing another 12V regulator (U2) to be powered on
                - this will apply 12V to the gate of the MOSFETs (Q2 - Q7)
                - current will pass through the MOSFETs to main negative output (J3)
            - circuit will have full power output capabilities
    - LED5 - SSR Signal will be visible on the Battery PCB exterior
 
# Remarks
- Design work was conducted by Julius.
- Schematic and CAD files can be find in the Quiver PT3 task and bounties directory
- information note prepared by Erick.
- Final update will come after design freeze. 
