# PT3 PCB Needs
[Day 1 Recording](https://drive.google.com/file/d/1PiIob_eGq5ElMCwGZTUeyg_mtlkL63G9/view?usp=drive_link)

[Day 2 Recording](https://drive.google.com/file/d/1p_hfNhdg6mo9MM4S5YFZBDAfLjT9-_I8/view?usp=drive_link)
## From Requirements:

- 14S Input
- Pixhawk
- HV and LV switch
- 12V & 5V
- CAN capabilities

## PT 1.5/2 Improvements:

- Internal HV traces for individual ESC output
- Dedicated Voltage regulating PDB with current and voltage data
- LV Kill switch
- SSR introduced
- Prototype friendly connectors
- removed the need for cable splitters and additional voltage regulators
- Neatly packaged battery interface, fuse, and SSR as an output to PCB (2)
- Connection for additional peripherals (2)
- Space for Raspberry Pi (2)
- integrated telemetry module (2)
- Easily integrated FC on PCB (2)
    - Not Pixhawk
- CAN components:
    - FC
    - Altimeter
    - GNSS
    - RPI
    - ESCs
- UART:
    - FC
    - Telemetry
    - RPI

## Requested improvements for PT3:

- Reduced cabling
    - largely reduced in PT2
- Connector for main power bus
    - don’t think this is necessary since battery is designed to be swapped
- Separation of signals from HV board
    - a lot of request for a modular board approach
    - Board can also be segregated
        
        ![image](https://github.com/user-attachments/assets/4c9e4065-2821-49d8-a310-6fbcee60730d)

        
    - additional practices for EMI reduction: https://drive.google.com/file/d/1zd6G54uSHPU9XQ0gly3Un4Vb1Vb5CWO8/view?usp=drive_link
    - combination of improved segregation and modularity with cables to connect the two
- Use RPI for battery CAN
- Adapter PCB for FC connected via wires to main PCB
- Disconnect switch for FC instead of Precharge
    - triggered pre-charge from RPI via CAN?
        - Why not trigger SSR via CAN at that point too?
- Protection circuits on boards
    - Protection relays
        - under and over voltage
    - reverse-voltage
        - which components would we apply this to?
    - How much of this already covered by voltage regulator (?)
- LED status indicators
- Probing points
- Hybrid footprint
    - SMD and through hole components

## Design Constraints

- PCB size
- component placement
    - RPI size
        - compute module can be an option
    - Pixhawk size
- enclosure dimensions

## Baseline Design to Improve

![image](https://github.com/user-attachments/assets/646977cd-678c-40a0-a6d3-0fedcb1fd33a)
![image](https://github.com/user-attachments/assets/ad3a4f65-79cc-4101-8836-8745cdd79fd8)
![image](https://github.com/user-attachments/assets/fe0922c6-6156-43fb-98dc-68d8a7d996c5)





## Battery PCB

- Note: PT2 25kg MTOW hover at 72A
- SSR
    - MOSFETs
- Fuse
    - similar to PT 1.5
    - 200A
    - similar mounting to PT2 Main power input
- Battery interface
    - solder Molex connectors directly to PCB
        - check battery forum for part numbers
- Pre-charge
    - same as PT2
        - fuse may change depending on space constraints
- Status LEDs
    - Voltage regulator (internal)
    - MOSFET input (internal)
    - MOSFET status (external)
    - Precharge (external)
    - suggestion for Pushbutton with LEDs
- Probing points
    - 5V
    - 12V
- Output
    - CAN
        - 2 ports
    - HV
        - Main power out
        - pre charge
    - Voltage regulators
        - 12V
        - 5V
            - 2 ports
        - Pre packaged IC
- Input
    - CAN
    - Pre-charge
        - Physical switch
        - Passive for now
        - Future implementation of MOSFET
            - spec required for operation
    - MOSFET signal
        - AUX output from FC

## Main PCB

- FC
    - Pending FC selection
    - carrier board for cube
    - https://arkelectron.com/product/ark-pixhawk-autopilot-bus-carrier/
    - custom carrier that drops into main PCB and attached with cables
    
    ![image](https://github.com/user-attachments/assets/2110752f-0df8-4e22-a7d1-b6cb5c6de43f)

    
    PIX32
    
    ![image](https://github.com/user-attachments/assets/73253042-6875-4d25-8042-3820b3701adc)

    
    Cube
    
    - Plan to use locking connectors for PCB interface
- GNSS
    - could be RTK
        - comparison study required
    - TBD
- RPI & necessary CAN components
- ESCs
- 12V & 5V Vreg
    - maybe
- Lidar/Altimeter
- SIYI camera connections
- Telemetry unit (depends on SIYI decision)
    - will have existing PT2 telemetry provisions on board
    - Additional ports for SIYI telemetry unit
- ESC connections
    - CAN
    - HV power
- Upgrades from PT2
    - Probe Points
        - CAN
        - 12V
        - 5V
        - will add more during design
    - Status LEDs
    - additional connector for 60V
    - adjustment to payload connector
        - change to 10 pin
    - ethernet connection/switch
        - https://ardupilot.org/copter/docs/common-ethernet-vehicle.html
        - https://irlock.com/products/cubelan-8-port-switch?variant=42816064847923&country=US&currency=USD&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&utm_campaign=gs-2018-09-19&utm_source=google&utm_medium=smart_campaign&gad_source=1&gad_campaignid=17509105140&gbraid=0AAAAADivTnrgs_xK9FAiUgKPagSsbcjqK&gclid=EAIaIQobChMIzrOygeyRjQMVkp8DAB2uYRj6EAsYASABEgLEovD_BwE
