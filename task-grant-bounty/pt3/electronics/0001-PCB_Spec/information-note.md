
# PT 3 PCB Spec

# Status

`Valid`

`Revision History: None`

`Replacement Log: None`

`Reference: PT2 Engineering Report`

# Project Description

This information note will cover the design choices, requirements, and spec for the PT3 PCBs.

# Methodology

Discussions around PT3 baseline designs were started on May5th, 2025 and documented via [recording](https://drive.google.com/file/d/1gKChez0KID_fH9h32p80YMG8lpvG8C8I/view?usp=drive_link) and [FigJam Board](https://www.figma.com/board/SU1d7bKC6t5i6ATU0lYqLt/PT3-Baseline-Design-Discussion?node-id=1-1034&t=OotsqhjERJzCrPtP-0). This review revealed the need for a deeper discussion around PT3's PCB design and electrical architecture. This information note will cover the design choices made  over the course of two calls on May 6-7, 2025. For a detail review of the conversations, listen to the recordings.
[Day 1](https://drive.google.com/file/d/1PiIob_eGq5ElMCwGZTUeyg_mtlkL63G9/view?usp=drive_link) - Reviewing relevant Quiver requirements and PT 1.5 & PT 2 PCBs.
[Day 2](https://drive.google.com/file/d/1p_hfNhdg6mo9MM4S5YFZBDAfLjT9-_I8/view?usp=drive_link) - Deciding on components and upgrades
[Notes]()

# Results and Deliverables

### Overview of Changes

The following components were removed from the PT1 design:

- Feather PT3 Testbed PDB
- Contactor
- XT-60 Splitter
- Custom designed enclosure
- Pixhawk PM02D Voltage regulator
- KDE UBEC

The following components were added to the design:

- “PT2 PCB”
    - See [information note](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/pt1/electronics/0001-PDB_V1/information-note.md) for detailed review.
    - Handles all voltage regulation and power distribution
    - Introduces various plug size [Molex Eurostyle Terminal blocks](https://github.com/Arrow-air/project-quiver/blob/errrks-patch-1/task-grant-bounty/pt1/electronics/0002-PT1.5_Harnessing_Update/picture/PS-39500-001-001.pdf) 
    - Added physical switch for pre-charge control
    - XT60PW-M for ESC Output
- Solid State Relay (SSR)
- Updated PCB enclosure merged with the attachment interface

The following connectors are being reused:

- compression lugs
- XT30PW-F

An updated To/From table was prepared for all connections in a [CSV format](https://docs.google.com/spreadsheets/d/16EMP2wPfAB1RD0uh3B_RAArtTbWv5ikxNuRASy50kpA/edit?gid=1237259679#gid=1237259679). Refer to this table to get specifics on pins and what connectors are used. This will eventually be used to create a detailed routing CAD diagram. 

### Cables Created

J1 → SIYI

- SIYI cable plugs into J1

J2 → SSR LED

J3 → SSR Control Pins

- 4 position Eurostyle plug to header pins
- 28 AWG

J4 & J5 → Various FC ports

- 6 and 10 position Eurostyle plug to JST connectors on Pixhawk
- 28 AWG
- 75 cm
- Note: J5 pins 8 and 9 will go to flight controller AD&IO port

J6 → Payload (Attachment interface)

- 7 position Eurostyle plug to 8 position Molex

J7 → Battery Interface

- 2 position Eurostyle plug with bare leads
    - solder into slots on battery interface

J8 → Radar Altimeter

- 4 Position Eurostyle plug directly from radar altimeter

J9 → Battery (-)

- 2 position Eurostyle plug
- Pin 1 connects to negative terminal of battery interface with ring terminal

SSR + → J10

- 6 AWG Silicon cable with compression lug

J11 → Precharge Switch 

- 2 position Eurostyle connecting to toggle switch

SSR - → J12

- 6 AWG Silicon cable with compression lug

XT60PW-F are used for power delivery to the ESCs and 5 Position Eurostyle plugs are used for the CAN and PWM connections. 

### Updated Enclosure

The pictures below give a brief description of the internal connections for the updated enclosure. Please see the PT 1.5 cockpit information note for additional details. 

![image](https://github.com/user-attachments/assets/cf45d422-9dad-4e57-b60b-4e9aa96e5479)

![image](https://github.com/user-attachments/assets/556f5af2-7406-41f9-9b71-69f66dac7ceb)


# Remarks

- Cable lengths and colors have not been recorded. This note will be updated when the information is available
- Suggestions received so far for changes to harnessing:
    - shielded, threaded, barrel connectors
    - 3rd party manufactured harnessing
- There is a lot of cabling in this update that could be reduce with a different harnessing approach.
    - We can attempt a single connector for PT3 and have a harness with nodes that branch off to different areas of the drone.
    - This will increase the complexity of the harnessing and would require more information of cable lengths and where to place components.
- Below is a rough drawing of the harnessing for PT 1.5
    - The drawing is incomplete because there was too many harnesses to fit in one screen.
     ![image](https://github.com/user-attachments/assets/63169051-6ce5-4dea-b155-1f239acd61c4)

