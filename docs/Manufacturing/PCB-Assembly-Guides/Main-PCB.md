---
title: Main_PCB Dev-Kit Assembly
sidebar_label: Main_PCB Dev-Kit Assembly
tags: [pcb]
---

# Project Quiver Dev-Kit Main PCB Assembly Manual

This manual will help with the Project Quiver Main PCB assembly process.

:::warning
This is not a final version of this document. The given instructions will give a general guide on the assembly process. Assembly should only be carried out by an experienced worker with experience in SMD soldering and the appropriate equipment. If you need this PCB fully assembled please contact the Project Quiver team.
:::

This PCB can be ordered fully assembled from the respective PCB manufacturer (e.g. JLCPCB). There are several parts that are normally not in stock at the PCB manufacturer and need to be sourced from one of the large electronic component distributors by the PCB manufacturer. This means that the production time for a finished PCB is around 3 weeks.

The manual soldering of the circuit board can be done with the help of this interactive BOM which is stored in the respective GitHub folder of this PCB (it is not recommended):

## Interactive BOM

Open the interactive BOM: [Quiver_PT3_Main_PCB_V0.1_ibom.html](pathname:///docs/project-quiver/Archive/PT3-Assembly-Guides/PCB-assembly/assets/Quiver_PT3_Main_PCB_V0.1_ibom.html)

![alt text](../Assembly-Guides/assets/images/PCBs/Main1.png)


This is an HTML file that opens in the browser. On the left side is the parts list and on the right side are the views for the front and back of the circuit board. It will help to put the components in the right place.

It is essential to use a PCB stencil to place the solder paste in the right places. A reflow oven or a hot air blower (temperature and airflow controllable) should be used for the soldering process.

### View on the top side of this PCB:

![alt text](../Assembly-Guides/assets/images/PCBs/Main2.jpg)


### View on the bottom side of this PCB:

![alt text](../Assembly-Guides/assets/images/PCBs/Main3.jpg)


## Additional Steps

The Main PCB has designated mounting positions for additional devices apart from the flight controller:

- Raspberry Pi
- GNSS
- 2X 4 port ethernet switch

These additional devices are not necessary to ensure the basic function of the board.
