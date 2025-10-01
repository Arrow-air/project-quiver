# PT 3 Flight Controller PCB

# Status

`Valid`

`Revision History: V1`

`Replacement Log: None`

`Reference: Updates to PT 3 Flight Controller PCB Information Note`

# Project Description

## PCB Update

The FC PCB was updated to include various changes that were noticed during the build and testing process. Few changes were made to the components or operation of the PCB. Majority of the changes involved changing the size of the screw holes, component placement and routing, and correcting the orientation of the flight controller. This information note will give a detailed breakdown of the updates. 

# Methodology

Updates were collected via the manufacturing, assembly, and testing process of Quiver PT3.

# Results and Deliverables

## Updated Schematics and CAD files

![image.png](attachment:d8df6b62-205a-4a2b-9ecc-9e15bcd1fee3:image.png)

<sub>***Previous Schematic with Highlighted changes***</sub>

![image.png](attachment:e47ae7e0-659b-4982-bf1a-ca2e5aebbfe0:image.png)

<sub>Updated ***Schematic with Highlighted changes***</sub>

## PCB Updates

- J2 & J3 replaced header with socket (AXK6S00547YG)
- JP1 & F3
    - shorting VDD5V_BRICK1 & VDD_5V_PERIPH with fuse to prevent boot loop on startup
    - This is optional and added just in case it is needed. This can be removed in a future update.
- Board Updates
    - Pix32 rotated by 180°
    - Pix32 position adjustment to fit screw holes
    - Pix32 screw hole diameter increased for better tolerance
    - Bigger offset around mounting holes to better space components and traces from edges

![image.png](attachment:bd131c59-e723-4c2c-9788-3099bb19e461:image.png)

![image.png](attachment:1b825b90-d37e-4e87-bedc-6b2f19838cca:image.png)

![image.png](attachment:d6c11e60-42b2-4503-ade2-314005f6876d:image.png)

![image.png](attachment:dba98b9a-ea19-46a6-abcb-1d9add5fdca1:image.png)

![image.png](attachment:60949b9c-5833-4755-8e14-3c5db7709e04:image.png)

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

# Remarks

- Design updated was conducted by Julius.
- Schematic and CAD files can be found in the Quiver PT3 task and bounties directory
- information note prepared by Erick.
