
# PT 3 PCB Spec

# Status

`Valid`

`Revision History: None`

`Replacement Log: None`

`Reference: PT2 Engineering Report & Recording Notes`

# Project Description

This information note will cover the design choices, requirements, and spec for the PT3 PCBs.

# Methodology

Discussions around PT3 baseline designs were started on May5th, 2025 and documented via [recording](https://drive.google.com/file/d/1gKChez0KID_fH9h32p80YMG8lpvG8C8I/view?usp=drive_link) and [FigJam Board](https://www.figma.com/board/SU1d7bKC6t5i6ATU0lYqLt/PT3-Baseline-Design-Discussion?node-id=1-1034&t=OotsqhjERJzCrPtP-0). This review revealed the need for a deeper discussion around PT3's PCB design and electrical architecture. 

This information note will cover the design choices made  over the course of two calls on May 6-7, 2025. For a detail review of the conversations, listen to the recordings.

[Day 1](https://drive.google.com/file/d/1PiIob_eGq5ElMCwGZTUeyg_mtlkL63G9/view?usp=drive_link) - Reviewing relevant Quiver requirements and PT 1.5 & PT 2 PCBs.

[Day 2](https://drive.google.com/file/d/1p_hfNhdg6mo9MM4S5YFZBDAfLjT9-_I8/view?usp=drive_link) - Deciding on components and upgrades

[Notes]()

# Results and Deliverables

### Design Constraints

- PCB Size
- Component placement
- Enclosure dimensions
- Layers
- Section for manufacturing constraints
  - PCB Trace width
  - Distance between traces 

### Overview of Changes

PT3 introduces significant changes to Quiver's electrical architecture by dividing the system into two distinct PCBs: the Battery PCB and the Main PCB. The Battery PCB neatly arranges components necessary for safely controlling and distributing high-voltage power to the Main PCB. The Main PCB houses the flight controller components, peripherals, and power regulation circuitry. Both PCBs include various I/O connections, status LEDs, and testing probes. A detailed log of changes for each PCB is provided below.

**Battery PCB**
- Replacing the third party SSR with a power MOSFET (will continue to refer to as SSR)
- 150A - 200A Fuse
- Custom Molex connector to interface with the Tattu Battery
  - Molex EXTreme 46437-9206 manually latching with 46437-9306
- Pre-charge circuitry with automotive fuse
- Various status LEDs
  - MOSFET input (internal LED)
  - MOSFET status (external LED)
  - Precharge (external)
    - Request to make this a pushbutton with an LED similar to Feather PT2
- Temperature sensors for SSR and pre-charge 
- I/O
  - Inputs
    - CAN
    - Pre-charge switch
    - MOSFET control
  - Outputs
    - 2 CAN Ports
    - HV power out
    - Pre-charge out

 **Main PCB**
  - Pix32 V6 with carrier board
    - Connects to PCB with cable
  - GNSS or RTK TBD
  - 12V and 5V regulator
  - Connections for lidar or radar altimeter
  - telemetry
    - provisions similar to PT2
    - additional ports for SIYI telemetry unit
  - ESC power and CAN connections
  - Probe points
    - CAN
    - 12V & 5V
    - TBD during design
  - Status LEDs
    - TBD during design
  - additional HV output
  - 10 pin payload connector
  - ethernet switch
    - additional board required to add ethernet functionality to Pix32 V6 via telemetry
  - temperature sensor 


# Remarks
- 5V and 12V regulation was originally meant for the Battery PCB but was switch to the main PCB on May 9, 2025
- PCB design will be led by Julius
- Additional specs to the PCB will be added during the design 

