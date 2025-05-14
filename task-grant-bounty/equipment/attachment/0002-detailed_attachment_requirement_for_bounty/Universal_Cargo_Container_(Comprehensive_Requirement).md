# Comprehensive Requirement of Universal Cargo Container:

Version: 05.14.25-1 (MM.DD.YY-V) 
Initial version

## General Objective Description:
A multipurpose container that can be rigidly mounted onto belly attachment interface, to statically carry and transport objects except un-packaged fluid or gas. 
Cargo inside may be dropped or released through the control from users or program. And the container may support optional cargo management interfaces.

## Optional Functions:
  - OF-1: May include a GUI or control interface, and reserve certain space for cargo content control.
  - OF-2: May include a controllable cargo release mechanism.

## Architecture & Boundary:
  - AB-1: Any electrical functions shall accept 12~60V DC power supply.
  - AB-2: Any actuator (e.g. cargo release, servo) shall be controllable by companion computer or flight controller via CAN or analog signal.
  - AB-3: Any non-real-time modules (e.g. GUI or interface) shall be controllable by companion computer via CAN or Ethernet.

## Performance:
  - P-1: Maximum static carrying weight shall be determined and right under the aircraft's maximum payload limit.
  - P-2: Shall have optimized aerodynamic shape to reduce the shape drag.
  - P-3: Shall maximize the use of redundant spaces in any dimensions.
  - P-4: Shall have tool-less ergonomics for most ground users whether wearing personal protection equipment.
  - P-5: Shall have non-destructive design for maintenance personnel.
  - P-6: May manually transportable and stackable while detached from aircraft.
  - P-7: May tolerate oversized cargo with a small amount.

## Manufacturing & Maintenece Process Technology
  - M-1: May be manufacturable using a variety of conventional and composite processes.

## Safety:
  - S-1: Must have either (1) A full weight rated safety rope, or (2) At least 2 rigid structure connections for structral fail safe.
  - S-2: Must not generate harmful vibration, inertia or center of gravity shifting.
  - S-3: Must have carge placement guide or marker to ensure the center of gravity is adjustable and controllable.
  - S-4: Must not perform any permanent structral deformation or deformation causing malfunctions within the rated load.
