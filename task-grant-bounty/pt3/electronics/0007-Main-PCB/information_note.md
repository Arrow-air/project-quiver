# PT 3 Main PCB

# Status

`Valid`

`Revision History: V1`

`Replacement Log: None`

`Reference: PT3 PCB Spec information note`

# Project Description
## PCB Overview

The Main PCB is the central hub for routing power and signals between the flight controller and all major PT3 subsystems. It interfaces with power regulation circuits, payload modules, sensors, telemetry units, and CAN networks. The schematic is divided into functional blocks, each described below along with its associated connectors.

# Methodology
Reviewed and studied the PT3 Main PCB design files from Julius. Discussed and developed understanding over various direct messages and calls. 
Designed was based on the information provided in the [PT3 PCB Spec information note](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/pt3/electronics/0001-PCB-Spec/information-note.md).

# Results and Deliverables

## Schematics and CAD files

![Main PCB - schematic](https://github.com/user-attachments/assets/cdca0d3a-3f9e-4b80-b690-58a7413e7d91)
<sub>***Main PCB Schematic***</sub>

![Main PCB - CAN schematic](https://github.com/user-attachments/assets/5a3148b8-4fea-48e8-b371-b3727f36a93b)
<sub>***CAN Circuitry***</sub>

![Main PCB - ethernet schematic](https://github.com/user-attachments/assets/31249b51-76ca-41fe-9101-679290774d19)
<sub>***Ethernet Circuitry***</sub>

![Main PCB - PCB Editor](https://github.com/user-attachments/assets/ac3eb0e7-0494-4800-b68c-9f3920d7bfe9)
<br />
<sub>***PCB All Layers***</sub>

![Main PCB - front](https://github.com/user-attachments/assets/8f7f4ab5-2762-4478-817b-1aa845a69d3a)
<sub>***PCB CAD front***</sub>

![Main PCB - back](https://github.com/user-attachments/assets/c0cec140-f43a-43b1-8c7e-8d69ce2ac8b5)
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

### **Power Input**

- Main Inputs
    - J44 - Positive
        - 16 Pin Screw Terminal, Power Tap M6 Through Hole
    - J45 - Negative
        - 16 Pin Screw Terminal, Power Tap M6 Through Hole
- Pre-charge bypass (J49, F5, F6, U3)
    - J49 - Additional HV- to bypass pre-charge resistor
        - Connector 2 Position Header, Male Pins Board to Cable/Wire 0.098" (2.50mm)
        - 1 pin will be connected via 16 AWG cable to the fuse on the Battery PCB (BC_PCB - J7)
        - runs through a 5A automotive fuse (F5)  and a 2A resettable fuse (F6), which protect the SSR (U3) and downstream electronics.
            - 5A fuse - Provides permanent, reliable protection against severe short circuits. Protects the resettable fuse, SSR, and the rest of the electronics from catastrophic failures.
            - 2A fuse - Rated for 2A continuous current, tripping at ~4A. This provides reversible protection. If a slight overload occurs (between 2A to 4A), it temporarily opens and resets after the overload clears.
        - U3 - SSR controlling bypass output
            - SSR RELAY SPST-NO 6A 0-60V
            - controlled by IO_CH6 (FC, J4  -Pin 95)
    - Pre-charge pushbutton on the Battery PCB (BC_PCB - J1) must first be pressed so that the Main PCB 5V and 12V regulator are active. This will power up the FC and a script can be executed that sends signal IO_CH6 from J4 (pin 95) to U3 (pin 2)
        - This will allow current to flow through this architecture instead of the pre-charge resistors on the Battery PCB
- **Note: Mounting Pads (MP) are connected to GND to increase solder surface and durability of connectors**

### Signal Connectors to BC_PCB

These connectors relay telemetry, control signals, and regulated power between the Main PCB and the Battery Connector PCB.

- J43 - connects to BC_PCB J2
    - Connector 5 Position Header, Male Pins Board to Cable/Wire 0.098" (2.50mm)
    - CAN data
    - Temperature data over I²C bus 2
    - FMU_CH3 (FC_2 on BC_PCB) is an optional signal to terminate the pre-charge operation
- J46 - connects to BC_PCB J3
    - Connector 4 Position Header, Male Pins Board to Cable/Wire 0.098" (2.50mm)
    - 5V and 12V output
    - IO_CH5 (SSR_S on BC_PCB) is the signal that enables the main power out on BC_PCB

### 12V and 5V Power Supply

- PS1 - 20W, 5V DC DC Converter
    - 5A fused (F3) output
    - LED 1 will indicate operation
- PS2 - 30W, 12V DC DC Converter
    - 5A fused (F4) output
    - LED 2 will indicate operation
- U5 - SSR to control payload voltage
    - Solid State SPST-NO
    - Resettable fuse (F8) and fuse (F7)
    - controlled by FMU_CH4 (FC, J4 - Pin 75)
    - This SSR will give the user explicit control of the payload voltage

### Safety Switch Connector

- J50 - Software Safety switch on Pixhawk
    - 4 Position Terminal Block Header, Male Pins, Shrouded (4 Side) 0.098" (2.50mm) Vertical
    - Unsure what this connector is being used for

### Ethernet

- J35, J36, and J41 are connectors for a PPP to Ethernet adapter
    - supports CAN (on CAN2 Bus), UART, and ethernet
    - J35 - JST GH Connector Header Surface Mount, Right Angle 4 position 0.049" (1.25mm)
        - VDD_5V_TEL2
        - CAN2_L & H
    - J36 - JST GH Connector Header Surface Mount, Right Angle 5 position 0.049" (1.25mm)
        - ETH_TX0+ / TX0−, ETH_RX0+ / RX0−
    - J41 - JST GH Connector Header Surface Mount, Right Angle 6 position 0.049" (1.25mm)
        - VDD_5V_TEL2
        - UART5_RX_TEL2 & UART5_RX_TEL2
        - UART5_CTS_TEL2 & UART5_RTS_TEL2
- **ETHERNET.kicad_sch**
    - J47 is a 40 pin Board to Board & Mezzanine Connector
        - connects to drop in ethernet module with 4 switches
        - breakouts included
            - 4 ethernet ports (4 pins each)
            - 12V and GND
            - +3V3_ETH and GND
            - SDA_ETH & SCK_ETH
    - J48 is a 4 pin connector for an additional ethernet hub if desired
        - 3V3_ETH and GND
        - SDA_ETH & SCK_ETH

### USB Connector to FC

- J33 is a USB3.2 GEN1, TYPE C, drop in module
- Will be used for initial FC parameter settings

### Temperature sensors for Main PCB

- select between JP1 and JP2 for I²C address assignment of IC1
- select between JP3 and JP4 for I²C address assignment of IC2

### 12V switch for Payload DC Motor

- K1 relay controlled by FC FMU_CH2
    - manual trigger for brush bullet dispenser
    - SPST NO
- 12V switch output fused (F1) with 1A (SMD fuse)
    - outputs to pin 6 on J31 (bottom payload)

### Buzzer

- LS1 is a surface mounted magnetic buzzer
    - capable of preset sounds from the FC
    - controlled by pins 91 & 93 on J3 (FC breakout)

### H-RTK NEO-F9P DroneCAN Version

- J7 and J8 are identical ports compatible with a NEO-F9P
    - both of these devices will be mounted on the lid or elsewhere
    - Connector 4 Position Header, Male Pins Board to Cable/Wire 0.098" (2.50mm)

### Mateksys GNSS M9N-G4-3100

- J9 - M9N-G4 or WrenMini connector
    - 4 Position Terminal Block Header, Male Pins, Shrouded (4 Side) 0.098" (2.50mm) Vertical
- J11 allows for the component to be mounted on the Main PCB

### Mateksys mLRS TX RX 2.4 GHZ

- additional telemetry unit
- Connects to Main PCB with header pins

### RPI ethernet connector

- J2 is a 4-pin Ethernet connector used to communicate with the SIYI A8 camera gimbal when the HM30 telemetry unit is not installed.
    - Connector 4 Position Header, Male Pins Board to Cable/Wire 0.098" (2.50mm)
        - J2 (1) - ETH_RX1+
        - J2 (2) - ETH_RX1-
        - J2 (3) - ETH_TX1+
        - J2 (4) - ETH_TX1-

### RPI

- J1 - partial pin‐out of the Raspberry Pi 5 (40-pin header)
    - mainly used for Serial Peripheral Interface (SPI) pins
        - **SPI_SCLK** – Serial Clock (Pi pin 23)
        - **SPI_MISO** – Master-In Slave-Out (Pi pin 21)
        - **SPI_MOSI** – Master-Out Slave-In (Pi pin 19)
        - **SPI_CE0** – Chip-Enable 0 (Pi pin 24)
    - **GPIO_26_CS** on Pi pin 37 is a GPIO that can function as a “software” chip-select for additional SPI devices beyond CE0/CE1.
    - 5V
    - 3.3V out for CAN controller and driver
- J6 - spare connector for 12V, 5V, 3.3V, and GND
    - 4 Position Terminal Block Header, Male Pins, Shrouded (4 Side) 0.098" (2.50mm) Vertical
- J10 - spare connector for GPIO 14, 15, 23, & 24
    - 4 Position Terminal Block Header, Male Pins, Shrouded (4 Side) 0.098" (2.50mm) Vertical

**CAN circuit.kicad_sch**

- These additional components are required because the RPI does not have a built in CAN controller or CAN driver. A standalone controller (MCP2515) to frame CAN data, plus a transceiver (TJA1049T) to drive/receive the differential signals on CANH/CANL
- CAN Controller (U2) - MCP2515
    - Interfaces to the Raspberry Pi 5 over SPI and handles CAN packets
        - SCK (pin 13) ← SPI_SCLK (RPI pin 23)
        - SI (pin 14) ← SPI_MOSI (RPI pin 19)
        - SO (pin 15) → SPI_MISO (RPI pin 21)
        - CS (pin 16) ← SPI_CE0 (RPI pin 24)
            - Pulled high by R19 (10 kΩ) to +3.3 V so it will remain idle until CE0 goes low.
    - Clock (Crystal) Circuit
        - OSC1 (pin 8) & OSC2 (pin 7) connected to a 16 MHz crystal oscillator (X1), each side decoupled to GND via C6/C7 (8 pF).
        - Provides the timing reference for CAN-bit timing and internal oscillator
    - TXCAN (pin 1) → U1 (TJA1049T) TX (pin 1)
        - Drives a 0 V/3.3 V “dominant/recessive” bit-stream to the transceiver, so that U1 can convert those logic levels into the correct differential voltages on CANH/CANL
    - RXCAN (pin 2) ← U1 (TJA1049T) RX (pin 4)
        - Receives the decoded bus-level bits (0/3.3 V) from the transceiver, so that U2 can reconstruct incoming CAN frames from the differential bus signals
    - Various decoupling capacitors for clean voltage
- CAN Transceiver (U1) - TJA1049T/3J
    - High-speed CAN bus transceiver that interfaces between the CAN controller (MCP2515) and the physical CAN wires
        - Converts the MCP2515's (U2) TX/RX signals into differential CANH/CANL pairs
        - Provides driver strength and protective features
    - **STB (pin 8)** selects active or low-power mode.
        - Pulled **high** to +3.3 V via **R17 (10 kΩ)** → transceiver stays in **normal (active)** mode.
        - If R17 is replaced by **R16 (0 Ω)** to GND, STB is driven low → transceiver enters **standby** (low-power) mode.
    - Various decoupling capacitors for clean voltage
- S1 - physical switch to enable 120 ohm termination resistor for the CAN network
    - TVS diodes (D1 & D2) clamps CANH to GND on any positive surge, and D2 clamps CANL on any negative surge

### SIYI A8 without HM30 unit

These are connections required to control the SIYI A8 camera gimbal if the SIYI HM30 Air Unit is not being used.

- J12 - Gimbal UART
    - 4 Position Terminal Block Header, Male Pins, Shrouded (4 Side) 0.098" (2.50mm) Vertical
    - UART8_TX_GPS2 & UART8_RX_GPS2 to FC (J3)
- J13 - Gimbal Power
    - 4 Position Terminal Block Header, Male Pins, Shrouded (4 Side) 0.098" (2.50mm) Vertical

### Additional Outside Connectors

- J14 - SIYI Power
    - XT30PW-F connector
    - 12V power to Siyi HM30 Air Unit
- J15 - SIYI UART
    - 4 Position Header, Male Pins Board to Cable/Wire 0.098" (2.50mm)
    - UART and GND connections to HM30
    - Note: TX from Main J15 must connect to RX on HM30, and vice versa.
        - UART7_TX_TEL1 & UART7_RX_TEL1 to FC (J3)
- J16 - Additional **CAN1** Connector
    - 4 Position Terminal Block Header, Male Pins, Shrouded (4 Side) 0.098" (2.50mm) Vertical
- J17 - SIYI SBUS
    - 3 Position Header, Male Pins Board to Cable/Wire 0.098" (2.50mm)
    - SBUS and GND connection to HM30
- J18 - Benewake Lidar Altimeter
    - Connector 7 Position Header, Male Pins Board to Cable/Wire 0.098" (2.50mm)
    - 12V, GND
    - CAN1_L & CAN1_H
    - UART (not connected to FC)
- J19 - Additional **CAN2** connector
    - 4 Position Terminal Block Header, Male Pins, Shrouded (4 Side) 0.098" (2.50mm) Vertical
- J20 - Optional UART connector
    - 4 Position Terminal Block Header, Male Pins, Shrouded (4 Side) 0.098" (2.50mm) Vertical
    - USART1_TX_GPS1 & USART1_RX_GPS1 to FC (J3)
- J21 - Additional UART Connector
    - 4 Position Terminal Block Header, Male Pins, Shrouded (4 Side) 0.098" (2.50mm) Vertical
- J22 - US-D1 Radar Altimeter
    - Connector 4 Position Header, Male Pins Board to Cable/Wire 0.098" (2.50mm)
    - 12V, GND
    - CAN1_L & CAN1_H
- J24 - Additional IO connector
    - 4 Position Terminal Block Header, Male Pins, Shrouded (4 Side) 0.098" (2.50mm) Vertical
    - FMU_CH5

**Additional HV connector with SSR**

This is an additional HV connector for an undefined accessory or component requiring 60V or less. 

- J26 - additional high voltage connector
    - Connector 2 Position Header, Male Pins Board to Cable/Wire 0.098" (2.50mm)
    - HV -
    - HV +
        - Fused output (F2)  connects to pin 7 & 8 of U4, a SSR
- U4 - SSR
    - SSR RELAY SPST-NO 6A 0-60V
    - controlled by IO_CH7 (FC, J4 - Pin 97)

**Attachment Interface Payload Connector (bottom payload)**

- J31
    - Connector 6 Position Header, Male Pins Board to Cable/Wire 0.098" (2.50mm)
    - 12V_PL controlled by SSR U5 (power to payload) and GND
    - CAN1_L & H
    - FMU_CH1 aux signal (FC, J4 - Pin 68)
    - 12VSW controlled by SSR K1
- J39
    - Connector 4 Position Header, Male Pins Board to Cable/Wire 0.098" (2.50mm)
    - ETH_RX2 & TX2 (+,-)

**Payload Side_1 (Right, PCB Bottom)**

- J29
    - Connector 6 Position Header, Male Pins Board to Cable/Wire 0.098" (2.50mm) Vertical
    - 12V_PL controlled by SSR U5 (power to payload) and GND
    - CAN1_L & H
    - FMU_CH7 aux signal (FC, J4 - Pin 81)
- J37
    - 4 Position Terminal Block Header, Male Pins, Shrouded (4 Side) 0.098" (2.50mm) Vertical
    - ETH_RX3 & TX3 (+,-)

**Payload Side_2 (Left, PCB Bottom)**

- J30
    - Connector 6 Position Header, Male Pins Board to Cable/Wire 0.098" (2.50mm) Vertical
    - 12V_PL controlled by SSR U5 (power to payload) and GND
    - CAN2_L & H
    - FMU_CH8 aux signal (FC, J4 - Pin 83)
- J38
    - 4 Position Terminal Block Header, Male Pins, Shrouded (4 Side) 0.098" (2.50mm) Vertical
    - Ethernet not included on this side due to limited available ports

### Motor Connectors

- J25, J28, J34, & J42
    - XT60PW-F, Main power outputs to ESCs
- J23, J27, J32, J40
    - Connector 5 Position Header, Male Pins Board to Cable/Wire 0.098" (2.50mm)
    - GND
    - CAN1_H & L
    - IO_CH1-4 (FC, J4)

### FC Connection

J3 and J4 connect to the FC PCB through two 100-position vertical connectors that route UART, GPIO, PWM, and other signal lines between the flight controller and Main PCB.

Connector used: Panasonic AXK5S00347YG Board to Board & Mezzanine Connectors CONN SOCKET BRD/BRD 100 POS 0.5mm
 
# Remarks
- Design work was conducted by Julius.
- Schematic and CAD files can be found in the Quiver PT3 task and bounties directory
- information note prepared by Erick.
- Manufacturing instructions can be found in the assembly guide. 
