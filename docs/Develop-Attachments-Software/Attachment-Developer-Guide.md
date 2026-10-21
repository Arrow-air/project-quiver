# Attachment Developer Guide

If you are designing or building a hardware attachment for Quiver, this guide explains what an attachment is, how it mounts to the airframe, and what the electrical interface provides at each of the three bays.


The interface contract itself is the payload-systems [Interface Control Document (ICD)](https://github.com/Arrow-air/payload-systems/blob/main/interface/ICD.md); this guide links it and adds the pin tables and power rules a builder needs. Software is covered in the [SDK Developer Guide](./Quiver-SDK-Developer-Guide.md). Flight-controller parameters and the network layout come from the [Initial Configuration Guide](https://github.com/Arrow-air/project-quiver/blob/errrks-init-config-1/docs/Operations/Initial-Configuration-Guide.md); relay labels come from the [Pilot Handbook](../Operations/Pilot-Handbook.md) §2.8.5.

---

## Quick Start: The Mental Model

Use the board routing and CAD geometry below as design references. Verify fit, electrical levels, protocol compatibility, and load limits on the aircraft before flight:

- the attachment uses the JMRRC quick-release clamp (BOM 2112) and its associated spacers,
- each bay uses the same pogo-pin contact interface, but the aux line is different per bay,
- all three bays share the same CAN2 bus, and all three share the same switched 12V payload rail,
- the bottom bay has an extra dedicated `12VSW` motor line,
- the high-power path is the switched HV line on the Main PCB, not the shared 12V payload rail.

The electrical design described here is for Main PCB V1.2 and Attachment Interface PCB V1.4. Design files describe intended routing and geometry; they do not certify a completed aircraft-level test.

### Builder-First Summary

A payload developer should be able to determine:

- the payload bay layout and where the three ports sit on the aircraft,
- the PCB dimensions present in the current KiCad layout and the attachment CAD assembly placement,
- what the Attachment Interface PCB looks like and how the pogo-pin / landing-pad pairing works,
- the bay-by-bay electrical contract for power, CAN, PWM, and Ethernet,
- which interface details are fixed by the board design and which require aircraft-level verification.

![Figure 1: Quiver multirotor drone](./Images/fig01_quiver_photo.jpg)
*Figure 1: Project Quiver multirotor drone.*

### The Drone

The [docs overview](../index.md) describes Quiver as an **open-source, modular quadcopter platform for developers and operators**. It has a 25 kg MTOW and three quick-release attachment interfaces: bottom, left, and right, and the overview advertises 5-8 kg of payload capacity. The Weight & Payload Summary in the [Dev-Kit Engineering Report](../Engineering-Reports/Dev-Kit-Engineering-Report.md) lists a 9.65 kg empty weight, a 7.90 kg 20 Ah pack (7.45 kg of payload capacity) and an 11.40 kg 30 Ah pack (3.95 kg). Those capacities are MTOW minus empty weight minus battery, not a weigh-in: several subsystem masses in the report are still TBD, and it calls the packs LiPo where the Pilot Handbook specifies LiHV. A rated per-port payload mass is not documented (see issue #209).
- **Bottom Bay:** Facing straight down under the fuselage.
- **Side 1 Bay (Right / Starboard):** Facing outward to the right.
- **Side 2 Bay (Left / Port):** Facing outward to the left.

Each bay uses the same mechanical interface and contact layout; auxiliary signals differ by bay, and the bottom bay alone has the additional `12VSW` rail.

### How an Attachment Mates

Connecting an attachment to Quiver involves two parts: a mechanical clamp and an Attachment Interface PCB.

1. **Mechanical Interface:** The aircraft uses BOM 2112 quick-release interface plates. Confirm the payload-side mating dimensions and fasteners against the hardware you will install; this guide does not specify a clamp load rating.
2. **Pogo-Pin Contact Interface:** The Attachment Interface PCB is one design used on both the aircraft and the payload. Every board has spring-loaded pogo pins in positions `U1` to `U10` and flat landing pads in positions `U11` to `U20`. The placement is mirrored, so the pogo pins on one board land on the pads of the board it mates with.
3. **Internal Wiring:** **Do not solder or wire to the pogo pins or landing pads.** Every PCB has a 12-pin locking Molex connector (**J1**) on its back face. On the aircraft, J1 connects to the aircraft harness. On your attachment, connect sensors, servos, cameras, and controllers through J1 using a wire harness.

```
        AIRCRAFT SIDE                                  PAYLOAD SIDE

[ AIRCRAFT AIRFRAME ]                          [ YOUR PAYLOAD HARDWARE ]
         |                                                  ^
[ PETG Spacer ]                                [ Your Payload Wire Harness ]
(side spacers; wiring notch                    (mates with the Molex plug)
 on bottom spacer)                                          ^
         |                                      [ Molex J1 Header ]
[ Quick-Release Interface ]                     (12-pin, rear of PCB)
(BOM 2112)                                                  |
         |                                      [ Attachment Interface PCB ]
[ Molex J1 Header ]                             (same board: pogo pins U1 to U10,
(12-pin, rear of PCB)                            pads U11 to U20)
         |                                                  |
[ Attachment Interface PCB ]                    [ Payload Mounting Plate ]
(same board: pogo pins U1 to U10,               (mating hardware dimensions per
 pads U11 to U20)                                current supplier drawing)
         |                                                  |
         +=========== POGO-PIN / PAD CONTACT INTERFACE =====+
                   (mirrored placement, pins land on pads)
```

### Key Terms

> [!IMPORTANT]
> Board routing and nominal geometry below describe Main PCB V1.2 and Attachment Interface PCB V1.4. Verify operating behavior, mating fit, and electrical limits on the specific aircraft.

| Term | What It Means |
|---|---|
| **Attachment Interface PCB** | The compact 23.5 x 15.8 mm board ([`QuiverAttachPCB`](../../src/pcb/attach_pcb/QuiverAttachPCB.kicad_pcb)) that sits inside the quick-release plate. |
| **Pogo Pins (`U1` to `U10`)** | Spring-loaded pins (part `C2826546`) populated on every Attachment Interface PCB, aircraft and payload alike. |
| **Landing Pads (`U11` to `U20`)** | Flat circular copper pads on every Attachment Interface PCB, mirrored in placement so they meet the pogo pins of the mating board. |
| **Molex J1** | The 12-pin locking connector (Molex part 2077601281) on the back of every Attachment Interface PCB. On the payload board this is where your harness plugs in. |
| **CAN2** | All three payload bays are routed to CAN2, the 500 kbit/s radar bus shared with the two NanoRadar sensors. Attachments do not share a bus with the ESCs, GNSS, or Remote ID. The bitrate and protocols are set in the flight controller configuration (`CAN_P2`), not by the PCB. |
| **FMU** | Flight Management Unit (the ArduPilot flight controller). Each bay has a routed FMU signal net; waveform and output configuration require aircraft-specific verification. |
| **Switched 12V (`+12V_PL`)** | The shared 12V payload power rail (pin 10 on Molex J1), switched by SSR K2 (CPC1019N) driving MOSFET Q2, controlled via `FMU_CH4`. The F8 hold rating implies about 13W at nominal 12V; this is an estimate, not a measured system budget. |
| **Motor 12V (`12VSW`)** | A secondary 12V line on the **bottom bay only** (pins 2 and 4 on Molex J1). SSR K1 controls MOSFET Q1, which switches regulated `+12V` onto this line; K1 is controlled via `FMU_CH2`. Dedicated to the brush bullet DC motor payload. |
| **Switched HV (`J26`)** | Switched flight-battery power from a dedicated 2-pin connector on the Main PCB, controlled by `IO_CH7` through K3/Q3. Select the power path using measured payload demand and aircraft limits; the board files do not establish a 13 W crossover. |

---

## 1. What is a Quiver Attachment?

A Quiver attachment is a hardware module mounted at one of the three bay locations on the drone:

| Bay Location | Physical Position | Facing Direction | Port-Specific Features |
|---|---|---|---|
| **Bottom** | Underside of lower chassis plate | Facing straight down (-Z) | Aux signal `FMU_CH1` (servo output 9); the only bay with the `12VSW` line |
| **Side 1 (Right)** | Starboard battery wall | Facing outward right (+X) | Aux signal `FMU_CH7` (servo output 15) |
| **Side 2 (Left)** | Port battery wall | Facing outward left (-X) | Aux signal `FMU_CH8` (servo output 16) |

The bays are otherwise electrically identical, so choose a bay by the aux channel and the `12VSW` line you need, not by payload type.

**Existing builds.** The August meetup produced a servo latch, a multispectral camera, and a Starlink Mini; the built payloads and planned concepts are catalogued in [payload-systems](https://github.com/Arrow-air/payload-systems). Six additional payload concepts have requirement documents: cargo, lidar, machine vision, camera, stabilized carrier, and floodlight (see the [attachment requirements](../../task-grant-bounty/equipment/attachment/0002-detailed_attachment_requirement_for_bounty/information-note.md)).

### Where the Bays Sit on the Aircraft

The three bays are integrated into the fuselage structure:

| Rear View (Bay Locations) | Side View (Port Offsets) |
|:---:|:---:|
| ![Figure 2: Payload bays rear cross-section](./Images/fig02_ports_rear_view.png) | ![Figure 3: Payload bays side view](./Images/fig03_ports_side_view.png) |
| *Figure 2: Payload bays viewed from the rear. Origin is at the airframe centre; image right is aircraft right (+X). Orange denotes attachment interface hardware.* | *Figure 3: Payload bays viewed from the side.* |

Figure 3's green region and dimensions are CAD-derived illustrations, not a validated payload clearance envelope. Check the current aircraft assembly and installed hardware before setting payload dimensions.

![Figure 4: Payload bays oblique overview](./Images/fig04_ports_oblique.png)
*Figure 4: Oblique view from below and rear-left. Orange indicates the quick-release plate and spacer; the green Attachment Interface PCB is visible at the left bay. The right-side bay is hidden behind a leg.*

### Practical Rules Before You Build

- **Live Connection:** Live attachment or removal is not established as a tested operating procedure here. Keep the aircraft unpowered unless live connection has been specifically tested and approved for that aircraft and payload.
- **Example Integration Patterns:** An actuator may use a bay aux signal and its own local regulation; a data payload may use the routed CAN or Ethernet pairs. Confirm protocol compatibility, signal levels, power draw, and physical fit on the actual assembly before flight.

---

## 2. Mechanical Interface

This chapter describes the attachment plate, bay locations, spacers, and mating PCB dimensions. Values that require aircraft-level measurement are marked for verification.

### 2.1 Coordinate Frame and Bay Locations

The coordinates below are the placement points used for the three attachment-plate CAD models. They are model placement coordinates, not mounting-hole centers or validated clearance limits.

Quiver uses standard aircraft coordinates with the origin `(0, 0, 0)` at the center of the fuselage interior:
- **+X:** To the right (Starboard)
- **+Y:** Forward toward the nose
- **+Z:** Upward toward the top lid

```
                        +Z (Up)
                           ▲
                           │
       Side 2 (Left)       │       Side 1 (Right)
       [-X bay]            │            [+X bay]
      [===]──────────[ FUSELAGE ]──────────[===]
                           │
                           │
                           ▼ -Z (Down)
                         [===]
                      Bottom bay
```

| Bay | Plate Model Center-of-Mass Placement (X, Y, Z) | Facing Direction in Assembly | Mounting Hardware on Aircraft |
|---|---|---|---|
| **Bottom** | `(0.00, 0.00, -160.70) mm` | Down (-Z) | Assembly includes spacer `2131` and interface plate `2112` |
| **Side 1 (Right)** | `(+185.65, -0.02, -71.00) mm` | Right (+X) | Assembly includes spacer `2111` and interface plate `2112` |
| **Side 2 (Left)** | `(-185.65, +0.02, -71.00) mm` | Left (-X) | Assembly includes spacer `2111` and interface plate `2112` |

An approximate overview datum also places interfaces at X = ±150 mm and Z = -125 mm; its relationship to the model placement points above is unspecified. Use the aircraft CAD assembly to establish the datum before designing clearances.

### 2.2 Drone-Side Hardware and Spacers

The aircraft uses three quick-release interface plates (2112), two side spacers (2111), and one bottom spacer (2131). Payload mass rating and clearance envelope are not specified here; verify both for the installed aircraft.

The builder should be able to answer these questions from this section alone:
- what the payload side and drone side mating hardware look like,
- which spacer is used at each bay,
- what the thickness and envelope are,
- whether the bottom or side bays have a different wiring exit requirement.

The assembly uses PETG spacers at the attachment locations:

| Bottom Interface Assembly | Side Interface Exploded View |
|:---:|:---:|
| ![Figure 5a: Bottom payload interface](./Images/fig05a_bottom_interface_cad.jpg) | ![Figure 5b: Side payload interface exploded](./Images/fig05b_side_interface_exploded_cad.jpg) |
| *Figure 5a: Bottom interface assembly showing the wire notch.* | *Figure 5b: Side interface exploded view showing the 30 mm spacer.* |

- **Side Ports (Right and Left):** Each side bay uses spacer `2111` ([`2111_attach_spacer.step`](../../src/quiver/supporting_structure/attachment_interface/steps/2111_attach_spacer.step)). Confirm the assembled standoff against the aircraft before setting the payload envelope.
- **Bottom Port:** The bottom bay uses spacer `2131` ([`2131_attach_spacer_bottom.step`](../../src/quiver/supporting_structure/attachment_interface/steps/2131_attach_spacer_bottom.step)), which has a wiring notch.

| Side Spacer (`2111_attach_spacer`) | Bottom Spacer with Notch (`2131_attach_spacer_bottom`) |
|:---:|:---:|
| ![Side Spacer](../../docs/Manufacturing/Assembly-Guides/assets/images/structural/2111_2121.png) | ![Bottom Spacer](../../docs/Manufacturing/Assembly-Guides/assets/images/structural/2131.png) |

### 2.3 JMRRC Quick-Release Clamp (BOM 2112)

Part 2112 (listed in the [BOM](../Manufacturing/BOM.md) as the Quick-Release Interface Plate) is the aluminum clip-plate pair used at all three bays; the payload READMEs name the payload half as a JMRRC clip plate. The payload-systems [mechanical README](https://github.com/Arrow-air/payload-systems/blob/main/interface/mechanical/README.md) identifies the payload-side clip plate as a 50 x 50 mm footprint, 10.5 mm thick, ordered without a PCB, and places its mounting plane near Z = -171 mm. Confirm dimensions and datum against the hardware and aircraft assembly you will use. No load rating is specified.

![Figure 6: Quick Release Clamp Plate Assembly](../../docs/Manufacturing/Assembly-Guides/assets/images/structural/2112_2122_2132.png)

*Figure 6: JMRRC quick-release clamp assembly (BOM 2112).*

Determine payload-side mating geometry, fasteners, thickness, and load limits from the actual hardware before designing the attachment. The mechanical-only [RAM-ball C design](https://github.com/Arrow-air/payload-systems/blob/main/payloads/ram-ball-c/README.md) specifies four Ø3 mm holes on a 38 x 38 mm square pattern (centers at X/Y = +/-19 mm) and a 16 x 24 mm shaft. Check those dimensions against the selected hardware revision.

### 2.4 Attachment Interface PCB Dimensions

This section describes the current V1.4 Attachment Interface PCB layout. Confirm the supplied payload-side assembly and mechanical fit before manufacturing an attachment.

The electrical connection is made by the **Quiver Attachment Interface PCB** ([`src/pcb/attach_pcb/QuiverAttachPCB.kicad_pcb`](../../src/pcb/attach_pcb/QuiverAttachPCB.kicad_pcb)); verify its installed position using the current mechanical assembly:

![Figure 7: PCB Dimensions and Layout Drawing](./Images/fig08_pcb_front_dimensions.png)
*Figure 7: PCB layout dimensions and edge-cut hole pattern. Right-side labels show the 2.54 mm pin-row pitch and 5.00 mm offset between aircraft pins and payload pads.*

- **Outer Dimensions:** 23.50 mm wide x 15.80 mm high.
- **Board Thickness:** **1.20 mm FR4**, as specified by the current KiCad layout. Confirm receiving-pocket clearance against the current mechanical assembly.
- **Edge-Cut Holes:** 4 circular cut-outs arranged in a rectangle:
  - Horizontal spacing (X axis): **20.00 mm** center-to-center.
  - Vertical spacing (Y axis): **8.00 mm** center-to-center.
  - KiCad board coordinates: `(100.0, 129.0)`, `(120.0, 129.0)`, `(100.0, 137.0)`, `(120.0, 137.0)`.
  - The KiCad outline defines the holes as 2.00 mm diameter; it does not specify threaded holes or fasteners.
- **Orientation:** The board outline has chamfered corners and a silkscreen orientation notch. Confirm the board orientation against the mating board before mating.

![Figure 8: PCB Rear View Showing J1 Connector](./Images/fig09_pcb_back_j1.png)
*Figure 8: Rear face of the Attachment Interface PCB showing the 12-pin Molex J1 connector. The same board is used on the aircraft and the payload.*

### 2.5 How the Boards Mate vs. How You Wire

![Figure 9: Mechanical and Electrical Mating Cross-Section](./Images/fig10_mating_section.png)
*Figure 9: Cross-section showing the pogo pins of one board contacting the pads of the mating board, and the harness connecting to Molex J1.*

One board design serves both sides of the interface, and every board is populated the same way:

- 10 spring-loaded pogo pins (`U1` to `U10`, part `C2826546`),
- 10 flat circular copper landing pads (`U11` to `U20`, 2.0 mm diameter),
- a rear 12-pin Molex J1 connector, which connects to the aircraft harness on the aircraft board and to your payload electronics on the payload board.

Placement is mirrored: in the V1.4 KiCad layout the pad positions `U11` to `U20` sit opposite the pogo positions `U1` to `U10` about the board center line, and each pad carries the same net as its opposite pogo pin. Two boards face to face therefore connect signal to signal.

| Physical PCB: Mating Face | Physical PCB: Rear Connector Face |
|:---:|:---:|
| ![Physical Hardware Mating Face](../../task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB/2026-Update/images/QuiverAttachPCB_new1.jpg) | ![Physical Hardware Rear Face](../../task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB/2026-Update/images/QuiverAttachPCB_new2.jpg) |

> [!WARNING]
> **Wiring rule:** Every board carries pogo pins U1 to U10 and pads U11 to U20. Connect payload wiring through Molex J1, not directly to the contacts.

### 2.6 Open Mechanical Items

These values are not documented anywhere yet. They are marked open here rather than estimated:

- **Empty weight, battery weight, and maximum payload mass:** requested in issue #209; pending a bench weigh-in.
- **Structural load limits per port (side versus bottom):** no rating exists; pending CAD or FEA analysis. Do not assume a limit.
- **Pogo pad coordinates and a mechanical drawing:** defined only in the V1.4 KiCad project today; this guide does not reproduce them.

For the mating mechanics, the ICD (§6) and the STEP files and mounting coordinates under [`interface/mechanical/`](https://github.com/Arrow-air/payload-systems/tree/main/interface/mechanical) in payload-systems are the reference.

---

## 3. Electrical Contract

This section summarizes routing in the current board designs and separates it from firmware configuration and system behavior that require separate validation. The interface contract is the payload-systems [ICD](https://github.com/Arrow-air/payload-systems/blob/main/interface/ICD.md) (§2 to §5); where this guide differs from the ICD, it says so.

The current design references are the board layouts and schematics for the Main PCB and Attachment Interface PCB:
- Main PCB: [`Quiver_PT3_Main_PCB-rounded.kicad_pcb`](../../src/pcb/main_pcb/Quiver_PT3_Main_PCB-rounded.kicad_pcb) and [`Quiver_PT3_Main_PCB-rounded.kicad_sch`](../../src/pcb/main_pcb/Quiver_PT3_Main_PCB-rounded.kicad_sch)
- Attachment Interface PCB: [`QuiverAttachPCB.kicad_pcb`](../../src/pcb/attach_pcb/QuiverAttachPCB.kicad_pcb) and [`QuiverAttachPCB.kicad_sch`](../../src/pcb/attach_pcb/QuiverAttachPCB.kicad_sch)

The ICD is the interface overview, but several details in its current draft conflict with the board and configuration sources. It names U5 as the `+12V_PL` switch (on V1.2, U5 is the lidar connector), calls K1 a mechanical relay, budgets about 25 W per port, says the rail is enabled by default, and calls the V1.4 spring-pin mate validated. Main PCB V1.2 instead switches `+12V_PL` with K2 (CPC1019N) driving Q2 and `12VSW` with K1 (CPC1019N) driving Q1, both solid-state; F8's 1.10 A hold rating corresponds to about 13 W nominal across the whole shared rail, not per port. The [configuration baseline](https://github.com/Arrow-air/project-quiver/blob/errrks-init-config-1/docs/Operations/Initial-Configuration-Guide.md) does not configure the relay outputs, and the [V1.4 update note](../../task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB/2026-Update/information-note.md) lists electrical validation as an open action. Use the board files for routing and the parameters read back from the aircraft for runtime behavior.

### 3.1 Port Capability Matrix

The three bays share power and CAN, but have different auxiliary lines:

| Capability | Bottom Bay | Side 1 / Right Bay | Side 2 / Left Bay | Details |
|---|---|---|---|---|
| **Main 12V Rail (`+12V_PL`)** | **Switched** (K2→Q2) | **Switched** (K2→Q2) | **Switched** (K2→Q2) | Main PCB layout and schematic |
| **Motor 12V Rail (`12VSW`)** | **Switched** (+12V via Q1; K1 controlled by `FMU_CH2`) | **No Connect (NC)** | **No Connect (NC)** | Main PCB layout and schematic |
| **CAN pair routing** | **CAN2** | **CAN2** | **CAN2** | Main PCB layout; verify bitrate and protocol against aircraft configuration |
| **Ethernet pairs** | Routed via J39 to onboard switch | Routed via J37 to onboard switch | Routed via J38 to onboard switch | Main PCB layout and schematic |
| **FMU Aux signal net** | `FMU_CH1` | `FMU_CH7` | `FMU_CH8` | Main PCB layout and schematic |
| **Avionics Header** | `J31` (PTSM 1814951) | `J29` (PTSM 1778735) | `J30` (PTSM 1778735) | [`Quiver_PT3_Main_PCB-rounded.kicad_pcb`](../../src/pcb/main_pcb/Quiver_PT3_Main_PCB-rounded.kicad_pcb) |
| **Ethernet Header** | `J39` (PTSM 1814935) | `J37` (PTSM 1778719) | `J38` (PTSM 1778719) | Main PCB layout and schematic |

### 3.2 Main PCB Payload Headers (J29, J30, J31) and Ethernet Connectors (J37, J38, J39)

On the aircraft's Main PCB, each payload bay connects to a 6-pin Phoenix Contact PTSM connector for power, CAN, and FMU signals, and to a separate 4-pin Phoenix Contact PTSM Ethernet header routed to an onboard switch:

| Bay | Avionics Header (power + CAN + FMU) | Ethernet Header |
|---|---|---|
| **Bottom** | `J31` (PTSM `1814951`, 6-pin) | `J39` (Phoenix PTSM `1814935`, 4-pin) |
| **Side 1 (Right)** | `J29` (PTSM `1778735`, 6-pin) | `J37` (PTSM `1778719`, 4-pin) |
| **Side 2 (Left)** | `J30` (PTSM `1778735`, 6-pin) | `J38` (PTSM `1778719`, 4-pin) |

The avionics (J29/J30/J31) and Ethernet (J37/J38/J39) headers are internal to the aircraft harness; your attachment only sees the signals arriving at Molex J1 on the Attachment Interface PCB. Payload Ethernet is 100BASE-TX over pairs A and B only (the two pairs on Molex J1 pins 1, 3, 5, and 7), so gigabit operation is not available at the payload ports.

**Avionics headers pinout (J29, J30, J31):**

| Pin | Bottom Bay (`J31`) Net | Side 1 Bay (`J29`) Net | Side 2 Bay (`J30`) Net | Function |
|:---:|---|---|---|---|
| **1** | `GND` | `GND` | `GND` | Ground reference |
| **2** | `+12V_PL` | `+12V_PL` | `+12V_PL` | Shared switched 12V payload rail (K2 controls Q2) |
| **3** | `/CAN2_L` | `/CAN2_L` | `/CAN2_L` | CAN2 Low; verify bitrate and protocol on aircraft |
| **4** | `/CAN2_H` | `/CAN2_H` | `/CAN2_H` | CAN2 High; verify bitrate and protocol on aircraft |
| **5** | `/FMU_CH1` | `/FMU_CH7` | `/FMU_CH8` | FMU signal net; verify output function and electrical levels |
| **6** | `/12VSW` | *No Connect* | *No Connect* | Switched regulated 12V motor line (**Bottom bay only**; Q1 controlled by K1) |

The current Main PCB layout defines these pins on J31, J29, and J30. Signal names are shown without KiCad-internal net numbers, which can change between revisions.

### 3.3 Payload Harness Connector: Molex J1 Pinout

The **12-pin Molex connector (J1)** on the back of the payload-side board is where your attachment wiring connects:
- **Board Header (J1):** Molex part [`207760-1281`](https://www.molex.com/en-us/products/part-detail/2077601281) (Micro-Lock Plus, 12-circuit, dual-row, 1.25 mm pitch, vertical surface-mount locking header; rated 2.0 A per contact and 50 V maximum by Molex).
- **Mating Cable Plug:** Molex housing `204523-1201`; the [harness manufacturing guide](../../task-grant-bounty/pt3/electronics/0009-Harnessing-Guide/Harnessing-Guide.md) lists terminal `2145291000` and pre-crimped lead `79758-1149`. Check the ratings for the selected terminal and wire as well as the header: the lowest-rated part sets the limit.

| Pin | Signal Name | Type | Electrical Rating | Description |
|:---:|---|---|---|---|
| **1** | `ETH_RX+` | Input | Ethernet pair | Ethernet Receive positive (from the onboard Ethernet switch) |
| **2** | `12VSW` | Power | +12V DC, 2A fused | **Bottom bay only:** Q1-switched regulated 12V line for the brush bullet motor. K1 controls Q1; F1 protects the line. Unconnected on Side 1 and Side 2. |
| **3** | `ETH_RX-` | Input | Ethernet pair | Ethernet Receive negative (from the onboard Ethernet switch) |
| **4** | `12VSW` | Power | +12V DC, 2A fused | Paralleled with pin 2 for extra current handling (Bottom bay only). |
| **5** | `ETH_TX+` | Output | Ethernet pair | Ethernet Transmit positive (to the onboard Ethernet switch) |
| **6** | `GND` | Ground | 0V Reference | Power and signal ground return |
| **7** | `ETH_TX-` | Output | Ethernet pair | Ethernet Transmit negative (to the onboard Ethernet switch) |
| **8** | `GND` | Ground | 0V Reference | Power ground return (doubled pin for current capacity) |
| **9** | `CAN_L` | I/O | CAN low | Aircraft **CAN2_L**. *(Board silkscreen says `CAN1_N`)* |
| **10** | `+12V` | Power | +12V DC; F8 1.10A hold | Main switched payload rail `+12V_PL` (K2 controls Q2; `12V Pay`) |
| **11** | `CAN_H` | I/O | CAN high | Aircraft **CAN2_H**. *(Board silkscreen says `CAN1_P`)* |
| **12** | `FMU_AUX` | I/O | FMU signal; verify voltage and waveform on aircraft | Bay auxiliary net: **Bottom:** `FMU_CH1`, **Side 1:** `FMU_CH7`, **Side 2:** `FMU_CH8` |

*(Molex J1 signal and pin mapping.)*

> [!NOTE]
> **Doubled pins are doubled on J1 only.** Each board has one pogo pin and one pad for `12VSW` (`U2`, `U12`) and for `GND` (`U4`, `U14`), so the paralleled J1 pins (2 and 4, 6 and 8) do not add current capacity across the interface. Whether both the pin and the pad of a mirrored pair conduct when two boards mate has not been confirmed on assembled hardware, so do not count on it for current. This guide does not specify the pogo-pin current rating; check the `C2826546` datasheet before loading those contacts. The J1 50 V rating is below full battery voltage; the HV tap is on Main PCB J26, not on this interface.

### 3.4 Pogo Pin and Landing Pad Map

When you check electrical continuity with a multimeter, here is how the pogo pins and their mirrored pads on a board line up. Every board has the same layout, and each pogo pin lands on the pad of the same signal on the mating board. Source: `QuiverAttachPCB.kicad_pcb` (V1.4), where `U1` to `U10` are the pogo footprints and `U11` to `U20` the pad-only footprints.

| Signal Name | Pogo Pin (`U1` to `U10`) | Mirrored Landing Pad (`U11` to `U20`) | Mated Signal Function |
|---|:---:|:---:|---|
| `ETH_RX+` | `U1` | `U11` | Ethernet RX+ differential line |
| `12VSW` | `U2` | `U12` | Switched DC motor rail (Bottom bay only; NC on sides) |
| `ETH_RX-` | `U3` | `U13` | Ethernet RX- differential line |
| `GND` | `U4` | `U14` | System ground reference |
| `ETH_TX+` | `U5` | `U15` | Ethernet TX+ differential line |
| `+12V` | `U6` | `U16` | Main switched 12V payload rail (`+12V_PL`) |
| `ETH_TX-` | `U7` | `U17` | Ethernet TX- differential line |
| `FMU_AUX` | `U8` | `U18` | Auxiliary PWM/GPIO (`FMU_CH1` / `FMU_CH7` / `FMU_CH8`) |
| `CAN_H` | `U9` | `U19` | Vehicle CAN2 high pair |
| `CAN_L` | `U10` | `U20` | Vehicle CAN2 low pair |

*(Contact designators and corresponding signals.)*

### 3.5 Network and Ethernet Routing

![Figure 10: Quiver Payload Network Architecture](./Images/Quiver%20Payload%20Network.png)
*Figure 10: Quiver network routing showing Ethernet switches and CAN separation.*

The Main PCB design routes the payload's Ethernet pairs through two switch modules. The payload port is 100BASE-TX over pairs A and B only, so its design limit is 100 Mbit/s:
- **Designed routing:** Bottom J39 and Side 1 J37 connect to switch module J47; Side 2 J38 connects to J51.
- **Aircraft status:** The first aircraft's GigaBlox switches were removed on 2026-08-24 after a static bench test tied them to loss of the M9N GNSS receiver; confirmation in flight was still pending in the Initial Configuration Guide. Payload Ethernet is therefore unavailable on that aircraft unless the switches are restored and GNSS coexistence is validated.
- **Wiring to the Bay:** The harness carries the `ETH_TX` and `ETH_RX` pairs to pins 1, 3, 5, and 7 on Molex J1.

### 3.6 CAN Bus Architecture

The Main PCB design uses two CAN nets; the payload connectors are routed to CAN2:

1. **CAN1:** The payload connector nets are not on CAN1, so an attachment never shares a bus with the ESCs, GNSS, or Remote ID.
2. **CAN2:** Bottom J31, Side 1 J29, and Side 2 J30 route to `/CAN2_H` and `/CAN2_L`. CAN2 is the 500 kbit/s radar bus and is shared with the two NanoRadar sensors.
  - Protocols on CAN2: DroneCAN in driver slot 1 (`CAN_D2_PROTOCOL = 1`) and RadarCAN in slot 2 (`CAN_D2_PROTOCOL2 = 14`), as set in Initial Configuration Guide §9. The radars use raw CAN IDs 1 (NRA15) and 2 (MR82), which are not DroneCAN node IDs.

> [!NOTE]
> **CAN label mapping:** The attachment-board labels are `CAN1_P` and `CAN1_N`; at all three aircraft payload ports these conductors connect to Main PCB `CAN2_H` and `CAN2_L`.

- **Bus Termination:** CAN2 is terminated on the Main PCB by a 120 ohm resistor (R14) that slide switch S2 connects across CAN2_H and CAN2_L. Do not add termination inside an attachment.

### 3.7 Power Delivery and Switching Rules

There is no always-on, direct battery feed on the attachment connectors. Every power rail is controlled by an electronic switch.

```
[14S LiHV, 53.2V nominal, 60.9V full charge] --/HV+,/HV-- (no fuse ahead of either converter input)
   |
   +-> PS2 (REC30K-4812SZ, 30W/2.5A) output -> F4 (5A) -> +12V
   |      |
   |      +-- K1 (CPC1019N) -> Q1 -> F1 (2A) -> /12VSW -> J31 pin 6 only
   |      |      ctrl: /FMU_CH2
   |      |
   |      +-- K2 (CPC1019N) -> Q2 -> F8 (PTC ~1.1A hold) -> F7 (2A) -> +12V_PL -> J29/J30/J31 pin 2
   |             ctrl: /FMU_CH4 ("12V Pay")
   |
   +-> PS1 (REC20K-4805SZ, 20W) output -> F3 (5A) -> +5V -> companion computer (J1, Raspberry Pi 5 header), misc headers
   |
   +-> J26 switched HV: HV+ -> F2 (5A) -> J26 pin 2
                        HV- -> Q3 (low-side switch) -> J26 pin 1 (AC_HV-)
                        ctrl: K3 (CPC1019N) <- /IO_CH7 ("Add HV")
```

#### A. Main 12V Payload Rail (`+12V_PL`)
- **Available on:** All three bays (Molex J1 pin 10; Pogo pin U6/U16).
- **Electronic Switch:** SSR **K2 (CPC1019N)** drives MOSFET **Q2 (SIRA99DP-T1-GE3)** on the Main PCB.
- **Control Signal:** Flight controller channel **`FMU_CH4`**, labeled **`12V Pay`** in ground control software.
- **Protection:** Protected by fuse **F7** (2A) and self-resetting PTC **F8** (Littelfuse `1812L110`, 1.10A hold-current part).
- **Conservative Design Estimate:** The F8 hold rating corresponds to about **13W at nominal 12V** across all three bays. This is not a measured system-level payload budget. Issue [#234](https://github.com/Arrow-air/project-quiver/issues/234) gives an approximate trip-current figure; do not treat it as a guaranteed threshold. Trip behavior depends on the exact installed part, temperature, and duration.
- **Upstream Converter:** The Main PCB power-supply schematic specifies a 30W RECOM isolated converter (`REC30K-4812SZ`, approximately 2.5A at 12V). Other aircraft loads also use the 12V supply, so this rating is not an available payload budget.

#### B. Switched 12V Motor Rail (`12VSW`) for Brush Bullet Payloads
- **Available on:** **Bottom bay only** (Molex J1 pins 2 and 4; Pogo pin U2/U12). On Side 1 (`J29`) and Side 2 (`J30`), this pin is not connected.
- **Purpose:** Specifically wired to drive the **brush bullet attachment** (payload DC drive motor).
- **Electronic Switch:** SSR **K1 (CPC1019N)** controls the gate of P-channel MOSFET **Q1**. Q1 switches the regulated `+12V` supply onto `12VSW`; K1 is in the control path, not the battery or motor-current path.
- **Control Signal:** Flight controller channel **`FMU_CH2`**, labeled `"12V switch for payload DC motor"`.
- **Protection:** Fast fuse **F1** (2A rating).

#### C. High-Power Attachments
The approximate 13W estimate is derived from the F8 hold-current rating, not from a system load test. Do not treat it as a measured capability or a guaranteed trip threshold for `+12V_PL`; validate payload loads on the actual aircraft. The switched HV port J26 is a separate power path that requires payload-side voltage conversion as needed.

- **Dedicated Switched HV Port (J26):**
  - High-power attachments tap direct flight battery power from **J26** on the Main PCB (Phoenix Contact PTSM 2-pin connector, part `1814919`).
  - Provides full 14S LiHV battery voltage: 14 x 3.8 V = 53.2 V nominal and 14 x 4.35 V = 60.9 V fully charged. The [Pilot Handbook](../Operations/Pilot-Handbook.md) §1.3.2 specifies 14S LiHV packs; the per-cell figures are generic LiHV values, so confirm them on the pack datasheet. A converter rated for 60 V has no margin at 60.9 V.
  - Switched by SSR **K3 (CPC1019N)** driving MOSFET **Q3 (SIR570DP-T1-RE3)**, controlled by `IO_CH7`, and protected by a **5A fuse (F2)**.
- **Never Tap the ESC Connectors:**
  - Connectors **J25, J28, J34, and J42** (yellow XT60PW-F sockets) on the Main PCB are **strictly for motor ESCs**. Never tap or connect payloads to these ports.
- **Local Voltage Step-Down:** High-power attachments must bring their own onboard DC-DC converter to step down the 50V battery rail to whatever local voltages their electronics need.

---

## Quick Reference

### Connectors You Need to Know

| Designator | Component Part Number | Location | What It Does |
|---|---|---|---|
| **J1** | Molex `2077601281` | Every Attachment Interface PCB (rear) | 12-pin locking header. Mates with cable housing Molex `2045231201`. |
| **U1 to U10** | Part `C2826546` | Every Attachment Interface PCB (front) | 10 spring-loaded pogo pins. Land on the pads of the mating board. |
| **U11 to U20** | 2.0 mm Copper Pads | Every Attachment Interface PCB (front) | 10 flat circular landing pads. Meet the pogo pins of the mating board. |
| **J31** | Phoenix PTSM `1814951` | Main PCB | Bottom bay avionics header (6-pin SMT). |
| **J29** | Phoenix PTSM `1778735` | Main PCB | Side 1 (Right) bay avionics header (6-pin SMT). |
| **J30** | Phoenix PTSM `1778735` | Main PCB | Side 2 (Left) bay avionics header (6-pin SMT). |
| **J39** | Phoenix PTSM `1814935` | Main PCB | Bottom bay Ethernet header routed to an onboard switch. |
| **J37** | Phoenix PTSM `1778719` | Main PCB | Side 1 (Right) bay Ethernet header routed to an onboard switch. |
| **J38** | Phoenix PTSM `1778719` | Main PCB | Side 2 (Left) bay Ethernet header routed to an onboard switch. |
| **J26** | Phoenix PTSM `1814919` | Main PCB | Switched High-Voltage (HV) payload port (2-pin SMT, 5A fused). |
| **J25, 28, 34, 42** | Amass XT60PW-F | Main PCB | **Exclusively for Motor ESC power.** Do not connect attachments here. |

### Relays and Control Channels

| Control Signal | SSR (Gate Driver) | MOSFET | Rail Controlled | Function |
|---|---|---|---|---|
| **`FMU_CH4`** (`12V Pay`) | K2 (`CPC1019N`) | Q2 (`SIRA99DP`) | `+12V_PL` | Main 12V payload rail across all 3 bays. Protected by F7 (2A) and PTC F8 (1.1A hold). |
| **`FMU_CH2`** | K1 (`CPC1019N`) | Q1 (`SIRA99DP`) | `12VSW` | K1 controls Q1, which switches regulated 12V motor power for the **brush bullet payload** (Bottom bay J31 only). Protected by F1 (2A). |
| **`IO_CH7`** | K3 (`CPC1019N`) | Q3 (`SIR570DP`) | `AC_HV−` on J26 | Switched 14S LiHV power (53.2 V nominal, 60.9 V maximum charge) for high-power payloads. Protected by F2 (5 A). |
| **`FMU_CH1`** | Flight-controller channel | n/a | Auxiliary signal net | Routed to Bottom bay; waveform and output configuration must be verified on the aircraft. |
| **`FMU_CH7`** | Flight-controller channel | n/a | Auxiliary signal net | Routed to Side 1; waveform and output configuration must be verified on the aircraft. |
| **`FMU_CH8`** | Flight-controller channel | n/a | Auxiliary signal net | Routed to Side 2; waveform and output configuration must be verified on the aircraft. |

### Official Board and Design Files

| Path | What It Defines |
|---|---|
| [`src/pcb/main_pcb/Quiver_PT3_Main_PCB-rounded.kicad_pcb`](../../src/pcb/main_pcb/Quiver_PT3_Main_PCB-rounded.kicad_pcb) | Main PCB layout. |
| [`src/pcb/main_pcb/Quiver_PT3_Main_PCB-rounded.kicad_sch`](../../src/pcb/main_pcb/Quiver_PT3_Main_PCB-rounded.kicad_sch) | Main PCB schematic. |
| [`src/pcb/attach_pcb/QuiverAttachPCB.kicad_pcb`](../../src/pcb/attach_pcb/QuiverAttachPCB.kicad_pcb) | Attachment Interface PCB layout. |
| [`src/pcb/attach_pcb/QuiverAttachPCB.kicad_sch`](../../src/pcb/attach_pcb/QuiverAttachPCB.kicad_sch) | Attachment Interface PCB schematic and pin mapping. |