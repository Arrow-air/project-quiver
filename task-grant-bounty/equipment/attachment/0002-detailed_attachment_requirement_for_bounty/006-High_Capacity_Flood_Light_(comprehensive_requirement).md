# Comprehensive Requirement
### 006 - High Capacity Flood Light
Version: 15.05.25-1 Dragon Lady

## General Objective Description:
A high brightness directional lighting lamp that can be used for various purposes, powered directly by the aircraft power supply. With optional color and light effect changing functions.

## Optional Functions:
- OF-1: May support flashing and breathing light effect functions.
- OF-2: May include multi light source design.
- OF-3: May support adjustable brightness function.
- OF-4：May support external color changing filters function for special scenario.

## Architecture & Boundary:
- AB-1: Must accept 48~60V DC power supply and include anti-spark and voltage regulating design.
- AB-2：May be able to pair with 3-axis gimbal via standard 1/4 or non-standard mounting interface, but except power supply wiring.
- AB-3: May be controllable by CAN or analog control signal.
- AB-4: May include a state machine interface for lamp status and control feedback.

## Performance:
- P-1: Shall have 4500 ~ 4800 K of color temperature.
- P-2: Shall have power consumption within 350 W.
- P-3: Shall have total brightness ≥ 20000 lumens.
- P-4: Light spot shall cover a horizontal range of 45 ~ 60 degrees.
- P-5: Light spot shall be rectang shape to ensure lighting efficiency.

## Manufacturing & Maintenance Process Technology:
- M-1: Shall use LED or LED-COB for light source.
- M-2: Use of optical glass and composite materials are encouraged.
- M-3: Structure parts must be designed using materials with a thermal softening point above 130 ℃.
- M-4: Shall use a long endurance thermal paste for heat removal.

## Safety:
- S-1: Must include high capacity heatsink or active heat removal design.
- S-2: Must include over-temprature protection with forced power down grade design, instead of power off.
- S-3: May include an isolated power supply design.
  
## Revision:
- 15.05.25-1 Dragon Lady: Initial public release. WIP
