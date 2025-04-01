# Status

`Valid`

# Project Description

This project aims to create a custom Quiver PT2 Power Distribution Board (PDB V1) for power distribution, power supply, signal distribution, and additional features. It is intended to replace the testbed PCB used in Quiver PT1. The new PDB will simplify the current testbed PCB and aims to reduce weight, space, and cost. 

The PDB V1, designed for Project Quiver, serves as a cornerstone for future expansions and the addition of further functionalities, leading to a well-integrated and cohesive system.

# Methodology

The design was created using **KiCad**, a free software suite for creating electronic designs. The following workflow was applied to develop this PCB:

1. Capturing the system requirements ([System Requirements Document](https://dao.arrowair.com/t/in-review-by-gbc-project-quiver-pt2-power-pcb-v1/103))
2. Creating the schematic of the electronic circuit
3. Defining the general dimensions of the PCB and orienting components
4. Routing the PCB traces
5. Conducting Design Rule Checks (DRC) and resolving all issues
6. Exporting Gerber files for manufacturing with **JLCPCB**, along with additional required files
7. Checking the Gerber and other files for errors

# Results and Deliverables

## Schematic

The circuit diagram is divided into several clear sections, with extensive comments added for explanation. Each blue rectangle highlights a specific part of the circuit. The key functions covered in the schematic are:

1. Connectors
2. Solid State Relay (SSR) - Safety Switch
3. Matek PDB providing 12V and 5V supply and current measurement
4. Main battery connection
5. Payload switch
6. Motor connections

The schematic is shown in the following image:

![](https://holocron.so/uploads/fdf436b0-image.png)

## Dimensions and Components

The following image shows the 3D-rendered PCB from the top surface. A quick overview of the layout:

- Left and right side connectors: Motors (signal connectors on the top surface, XT60 power connectors on the bottom surface)
- Top side connectors: SSR, payload, battery, and flight controller
- Bottom side connectors: Precharge switch, SSR LED, radar altimeter, and SIYI power connector (XT30)

The Matek PDB is placed in the center of the PCB. Three fuse holders are located at the bottom of the PCB, designated for:

- Precharge fuse
- 12V fuse
- 5V fuse

![](https://holocron.so/uploads/2f0a4dad-image.png)

## Routing

The routing was carried out using the following four net classes:

| Class        | Safety Margin | Track Width | Via Size | Via Hole Size |
| ------------ | -------------- | ----------- | ------- | -------------- |
| Signal       | 0.2 mm         | 0.3 mm      | 0.6 mm  | 0.3 mm         |
| Low Power    | 0.2 mm         | 1 mm        | 1.2 mm  | 0.8 mm         |
| Medium Power | 0.35 mm        | 2.5 mm      | 1.2 mm  | 0.8 mm         |
| High Power   | 0.5 mm         | 5 mm        | 2 mm    | 1.2 mm         |

Additionally, a ground plane was added on the bottom layer of the PCB.

The solder mask was removed on some of the high-power traces (exposing the copper), allowing these traces to be reinforced with additional copper or solder if required.

![](https://holocron.so/uploads/66308e43-image.png)

## Files

All project files can be accessed here:  
[Project Files - Google Drive](https://drive.google.com/drive/folders/16L5hBI6shYaOVsX0JZiCZbpuma5p8X1x)

# Remarks

- As of 05.03.2025, the PCB has not been tested yet.
