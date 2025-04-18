# **Project Quiver PT2 electronics assembly guide**

## Preparation

- You need the following tools:
  - Allen key set
  - Wrench set
  - Screwdriver set
  - Solder iron
  - Solder
  - Hot glue gun
  - Cable ties in various sizes
  - Loctite
  - Cleaning agent (Isopropyl alcohol)

## PCB assembly steps

Familiarize yourself with the PCB layout. The following picture shows the components and connectors.

![](https://holocron.so/uploads/ea934f07-00.png)

### Step 1: Prepare the bare PCB

- Parts you need in this step: Bare PCB

  ![](https://holocron.so/uploads/ad1cb7b8-01.png)

- Clean the PCB with the cleaning agent

### Step 2: Press fit the screw terminals

- Parts you need in this step: 3x Screw terminal
- Press fit the screw terminals. If they are too loose, also solder them

  ![](https://holocron.so/uploads/e239911d-02.png)


### Step 3: Fix the distance adapter

- Parts you need in this step: 1x Distance adapter PDB
- Glue the PDB spacer to the PCB so that the holes are concentric with each other

  ![](https://holocron.so/uploads/a6a05975-03.png)


### Step 4: Solder the high power pins for the Matek PDB

- Parts you need in this step: 12x PDB power pin
- Solder the PDB high-current pins

  ![](https://holocron.so/uploads/b896eac4-04.png)


### Step 5: Solder the two pin headers to the PCB

- Parts you need in this step: 2x pin headers (8 pins)
- Solder the two 8 pin pin headers for the PDB 

  ![](https://holocron.so/uploads/204841cf-05.png)


### Step 6: Matek PDB soldering

- Parts you need in this step: Mateksys FCHUB-12S PDB
- Solder the Mateksys PDB to the PCB (make sure to look at Mateksys manual before you do that, because you should reinforce the solder pads)

  ![](https://holocron.so/uploads/369b2fe9-06.png)

  ![](https://holocron.so/uploads/e8a60699-06-2.png)


### Step 7: Bottom side preparation

- Parts you need in this step: None
- Clean the PCB with the cleaning agent

  ![](https://holocron.so/uploads/c21a8283-07.png)


### Step 8: Solder XT60 and copper rods

- Parts you need in this step: Copper rods and 4x XT60 connector
- Solder the copper rods and the XT60 connectors

  ![](https://holocron.so/uploads/e7e0c652-08.png)

  ![](https://holocron.so/uploads/63398c84-08-2.png)


### Step 9: Bottom side is finished. Turn around the PCB again

### Step 10: Solder the SMD components

- Parts you need in this step: SMD components (see PCB BOM)
- Solder the SMD components

  ![](https://holocron.so/uploads/5a30e1bf-10.png)


### Step 11: Solder the fuse holders

- Parts you need in this step: 4x Fuse holder (see PCB BOM)
- Solder the fuse holders

  ![](https://holocron.so/uploads/7a8d8e28-11.png)


### Step 12: Solder all remaining connectors. After that all components are soldered onto the PCB

- Parts you need in this step: 15x through hole connector (see PCB BOM)
- Solder the connectors

  ![](https://holocron.so/uploads/4867c6ac-12.png)


### Step 13: Push the telemetry module into the connector on the PCB

- Parts you need in this step: 1x Mateksys mLRS telemetry module
- Insert the telemetry module into the slot and fix it with some hot glue

  ![](https://holocron.so/uploads/900646bd-13.png)


### Step 14: Screw the GNSS module onto the PCB and connect it to its designated connector

- Parts you need in this step: Mateksys AP DroneCAN M10Q-3100 GNSS module, 2x plastic screws and nuts
-  Screw the GNSS module onto the PCB and connect it to its designated connector. The arrow on top of the GNSS module should point to the center of the PCB

  ![](https://holocron.so/uploads/53c40f5b-14.png)


### Step 15: Screw the FC on top of the Mateksys PDB and create the FC wiring

- Parts you need in this step: Mateksys H743 Slim V3, 4x M3 distance adapter (10mm), 4x plastic screws and nuts
- Screw the flight controller with the distance adapters on top of the Mateksys PDB. Make sure the soft anti-vibration pads are added to the holes of the FC. Use plastic screws
- To connect the FC to the main PCB, wires are soldered to the upper pads of the FC. These wires attach to the two SMD connectors on the left and right side of the FC. It's not recommended to reproduce this assembly. If you need to do it, please look at the schematics to solder the wires to the corresponding connector pin

  ![](https://holocron.so/uploads/1fd0b1e4-15.png)


### The assembly of the quiver PT2 PCB is finished

If you assembled it right your PCB should look almost like the following picture.

![](https://holocron.so/uploads/8d8aa5bb-rendering-3.png)

## Overall electronics assembly steps

### Step 1: Prepare the PCB adapter print and mount it to the frame

- Parts you need in this step: 1x PCB adapter print
- All thread inserts used in this assembly are M3. Equip the 3D print with the thread inserts
- Screw the pcb adapter onto the frame

  ![](https://holocron.so/uploads/cc953151-2-01.png)


### Step 2: Add the main PCB

- Parts you need in this step: 1x Main PCB
- Screw the main PCB onto the adapter print

  ![](https://holocron.so/uploads/1510d5f7-2-02.png)


### Step 3-1: Front compartment

- Parts you need in this step: 1x Battery connector, 1x Main front compartment print
- All thread inserts in this assembly are M3
- Provide the 3d print with the threaded inserts
- Screw the battery connector onto the front compartment print

  ![](https://holocron.so/uploads/291c423a-2-03-1.png)


### Step 3-2: Front compartment

- Parts you need in this step: 1x SSR
- Place the SSR in the print and secure the SSR with a cable tie. There are extra holes provided for the cable tie. Note the orientation of the output and input

  ![](https://holocron.so/uploads/e91611d9-2-03-2.png)


### Step 3-3: Front compartment

- Parts you need in this step: 1x Fuse print
- Screw the fuse holder over the top of the SSR

  ![](https://holocron.so/uploads/65c46f43-2-03-3.png)


### Step 3-4: Front compartment

- Parts you need in this step: 1x Fuse
- Add the fuse

  ![](https://holocron.so/uploads/2e386291-2-03-4.png)


### Step 3-5: Front compartment

- Parts you need in this step: 4x Cable lug and additional cable
- Fit the cables with the cable lugs and make sure they are the right length.
- Screw down the cable lugs

  ![](https://holocron.so/uploads/3fc4967b-2-03-5.png)


### Step 3-6: Front compartment

- Parts you need in this step: 1x Front print
- Screw the front print onto the main print. The front print contains the tab for the battery holder

  ![](https://holocron.so/uploads/e53ff189-2-03-6.png)


### Step 3-7: Front compartment

- Parts you need in this step: 2x Cable lug
- Later add the cable lugs for the power cables that connect to the main PCB. Make sure the cables are long enough

  ![](https://holocron.so/uploads/31c6a082-2-03-7.png)


### Step 4: Add the front compartment to the assembly

- Parts you need in this step: 1x Assembly of the front compartment
- Add the front compartment to the main assembly and screw it to the frame
- Connect the power cables to the PCB

  ![](https://holocron.so/uploads/cacbaf12-2-04.png)


### Step 5: Add the motors to the assembly

- Parts you need in this step: 4x Motor assembly and motor connectors
- Mount the motor to the motor arms and guide the cables through the tubes
- Connect the motor cables to the main PCB

  ![](https://holocron.so/uploads/3bbd5f3c-2-05.png)


### Step 6: Add the lidar to the assembly

- Parts you need in this step: 1x Benewake TF-03 lidar and 3D printed adapter
- Add the lidar to the back of the frame. It has a 3d printed adapter
- Connect the lidar to the main PCB

  ![](https://holocron.so/uploads/f9db5640-2-06.png)


### Step 7: Add the main switch to the assembly

- Parts you need in this step: 1x Main switch and housing
- Mount the main switch with housing to the front right of the frame
- Connect the main switch to the main PCB

  ![](https://holocron.so/uploads/52606d65-2-07.png)


### The assembly of the quiver PT2 electronics system is finished

If you assembled it right your structure should look almost like the following picture.

![](https://holocron.so/uploads/e8622f79-rendering-2.png)
