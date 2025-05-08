# PT3 PCB Needs

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
        
        ![image.png](attachment:ca98b681-b15e-4261-9326-bbbe3bb14625:image.png)
        
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

![image.png](attachment:f4cf35b1-ba57-4643-8039-3a8b4b79dbce:image.png)

![image.png](attachment:98845ebb-1ea2-4fe2-be1b-3515eef59755:image.png)

![image.png](attachment:ac0ec72a-6e4b-492f-8731-79b19ed840d3:image.png)

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
    - Vreg (internal)
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
    - Vreg
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
    
    ![PIX32](attachment:cbe8a08f-e82e-4f80-95a8-e2ef6e1170f0:image.png)
    
    PIX32
    
    ![Cube](attachment:a398cd0b-2ccf-4538-aa29-aae156dbdca9:image.png)
    
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
