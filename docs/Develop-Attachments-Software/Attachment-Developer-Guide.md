# Attachment Developer Guide

If you are designing or building a hardware attachment for Quiver, this guide covers everything you need: how the attachment mounts to the airframe, what off-the-shelf parts to order, how the electrical connectors mate, and how to safely wire power, CAN, PWM, and Ethernet.

This guide covers the mechanical and electrical attachment interface, plus the payload software handoff.

---

## Quick Start: The Mental Model

Use the board routing and CAD geometry below as design references. Verify fit, electrical levels, protocol compatibility, and load limits on the aircraft before flight:

- the attachment uses the BOM 2112 quick-release interface plate and its associated spacers,
- each bay uses the same pogo-pin contact interface, but the aux line is different per bay,
- all three bays share the same CAN2 bus, and all three share the same switched 12V payload rail,
- the bottom bay has an extra dedicated `12VSW` motor line,
- the high-power path is the switched HV line on the Main PCB, not the shared 12V payload rail.

The electrical design described here is for Main PCB V1.2 and Attachment Interface PCB V1.4. Design files describe intended routing and geometry; they do not certify a completed aircraft-level test.

### Builder-First Summary

A payload developer should be able to determine:

- the payload bay layout and where the three ports sit on the aircraft,
- the PCB dimensions present in the current KiCad layout and the attachment CAD assembly placement,
- what the payload-side board looks like and how the pogo-pin / landing-pad pairing works,
- the bay-by-bay electrical contract for power, CAN, PWM, and Ethernet,
- which interface details are fixed by the board design and which require aircraft-level verification.

![Figure 1: Quiver multirotor drone](./Images/fig01_quiver_photo.jpg)
*Figure 1: Project Quiver multirotor drone.*

### The Drone

Project Quiver is an **open-source, modular quadcopter platform for developers and operators**. It is a 25 kg MTOW drone with 5-8 kg payload capacity and three quick-release attachment interfaces: bottom, left, and right. The aircraft is built around a central motherboard called the Main PCB.
- **Bottom Bay:** Facing straight down under the fuselage.
- **Side 1 Bay (Right / Starboard):** Facing outward to the right.
- **Side 2 Bay (Left / Port):** Facing outward to the left.

Each bay uses the same mechanical interface and contact layout; auxiliary signals differ by bay, and the bottom bay alone has the additional `12VSW` rail.

### How an Attachment Mates

Connecting an attachment to Quiver involves two parts: a mechanical clamp and an Attachment Interface PCB.

1. **Mechanical Interface:** The aircraft uses BOM 2112 quick-release interface plates. Confirm the payload-side mating dimensions and fasteners against the hardware you will install; this guide does not specify a clamp load rating.
2. **Pogo-Pin Contact Interface:** The Attachment Interface PCB has spring-loaded contact positions (`U1` to `U10`) and corresponding pad positions (`U11` to `U20`). The aircraft side uses pins; the payload side uses pads.
3. **Internal Wiring:** **You do not solder or wire to the pogo pins or landing pads.** On the back face of the provided payload PCB is a 12-pin locking Molex connector (**J1**). All of your internal sensors, servos, cameras, and microcontrollers plug into this Molex connector via a simple wire harness.

```
[ AIRCRAFT AIRFRAME ]
         │
         ▼
[ PETG Spacer ]                (side spacers; wiring notch on bottom spacer)
         │
         ▼
[ Quick-Release Interface ]    (BOM 2112; aircraft-side CAD model)
         │
 [ Aircraft PCB ]              (Populated with male Pogo Pins U1 to U10)
═════════╪══════════════════════════════════════════════════════════════════ POGO-PIN / PAD CONTACT INTERFACE
 [ Payload PCB ]               (Provided to you; populated with flat pads U11 to U20)
         │
         ▼
[ Payload Mounting Plate ]     (mating hardware dimensions per current supplier drawing)
         │
 [ Molex J1 Header ]           (12-pin locking header on rear of Payload PCB)
         │
         ▼
[ Your Payload Wire Harness ]  (Mates with Molex 2045231201 plug)
         │
         ▼
[ YOUR PAYLOAD HARDWARE ]
```

### Key Terms

> [!IMPORTANT]
> Board routing and nominal geometry below describe Main PCB V1.2 and Attachment Interface PCB V1.4. Verify operating behavior, mating fit, and electrical limits on the specific aircraft.

| Term | What It Means |
|---|---|
| **Attachment Interface PCB** | The compact 23.5 x 15.8 mm board ([`QuiverAttachPCB`](../../src/pcb/attach_pcb/QuiverAttachPCB.kicad_pcb)) that sits inside the quick-release plate. |
| **Pogo Pins (`U1` to `U10`)** | Spring-loaded brass pins on the **drone-side** board. |
| **Landing Pads (`U11` to `U20`)** | Flat circular copper pads on the **payload-side** board that contact the drone pogo pins. |
| **Molex J1** | The 12-pin locking connector (Molex part 2077601281) on the back of the payload board. This is where your harness plugs in. |
| **CAN2** | All three payload bays are routed to CAN2. Configure the bus rate and protocol for the attached devices; the PCB does not set them. |
| **DroneCAN** | A supported CAN protocol. Do not assume DroneCAN can share the bus with a NanoRadar MR82; test protocol compatibility on the complete aircraft before use. |
| **FMU** | Flight Management Unit (the ArduPilot flight controller). Each bay has a routed FMU signal net; waveform and output configuration require aircraft-specific verification. |
| **Switched 12V (`+12V_PL`)** | The shared 12V payload power rail (pin 10 on Molex J1), switched by SSR K2 (CPC1019N) driving MOSFET Q2, controlled via `FMU_CH4`. The F8 hold rating implies about 13W at nominal 12V; this is an estimate, not a measured system budget. |
| **Motor 12V (`12VSW`)** | A secondary 12V line on the **bottom bay only** (pins 2 and 4 on Molex J1). SSR K1 controls MOSFET Q1, which switches regulated `+12V` onto this line; K1 is controlled via `FMU_CH2`. Dedicated to the brush bullet DC motor payload. |
| **Switched HV (`J26`)** | Switched flight-battery power from a dedicated 2-pin connector on the Main PCB, controlled by `IO_CH7` through K3/Q3. Select the power path using measured payload demand and aircraft limits; the board files do not establish a 13 W crossover. |

---

## 1. What is a Quiver Attachment?

A Quiver attachment is a hardware module mounted at one of the three bay locations on the drone:

| Bay Location | Physical Position | Facing Direction | Typical Payloads |
|---|---|---|---|
| **Bottom** | Underside of lower chassis plate | Facing straight down (-Z) | Gimbal cameras, LiDAR scanners, drop mechanisms, brush bullet actuators |
| **Side 1 (Right)** | Starboard battery wall | Facing outward right (+X) | Inspection cameras, atmospheric sensors, radio links, spotlight pods |
| **Side 2 (Left)** | Port battery wall | Facing outward left (-X) | Starlink Mini terminals, radar units, environmental air samplers |

### Where the Bays Sit on the Aircraft

The three bays are integrated into the fuselage structure:

| Rear View (Bay Locations) | Side View (Port Offsets) |
|:---:|:---:|
| ![Figure 2: Payload bays rear cross-section](./Images/fig02_ports_rear_view.png) | ![Figure 3: Payload bays side view](./Images/fig03_ports_side_view.png) |
| *Figure 2: Payload bays viewed from the rear. Origin is at the airframe centre; image right is aircraft right (+X). Orange denotes attachment interface hardware.* | *Figure 3: Payload bays viewed from the side.* |

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

### 2.3 The Quick-Release Clamp Plate (BOM 2112)

Part 2112 is the aluminum quick-release interface plate used at all three bays. The dimensions, fasteners, and load rating of the mating plate pair are not specified here; measure the hardware you will use.

![Figure 6: Quick Release Clamp Plate Assembly](../../docs/Manufacturing/Assembly-Guides/assets/images/structural/2112_2122_2132.png)

*Figure 6: Quick-release clamp plate assembly (BOM 2112).*

Determine payload-side mating geometry, fasteners, thickness, and load limits from the actual hardware before designing the attachment.

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
- **Orientation:** The board outline has chamfered corners and a silkscreen orientation notch. Confirm the payload board orientation against the aircraft-side board before mating.

![Figure 8: PCB Rear View Showing J1 Connector](./Images/fig09_pcb_back_j1.png)
*Figure 8: Rear face of the payload board showing the 12-pin Molex J1 connector.*

### 2.5 How the Boards Mate vs. How You Wire

![Figure 9: Mechanical and Electrical Mating Cross-Section](./Images/fig10_mating_section.png)
*Figure 9: Cross-section showing drone pogo pins contacting payload pads, and your harness connecting to Molex J1.*

A single board design serves both sides of the interface by populating different parts:

| Drone-Side Board | Payload-Side Board (Provided to You) |
|---|---|
| Populated with 10 male spring-loaded pogo pins (`U1` to `U10`, LCSC part `C2826546` / `BWCD-L4.5W2.0H2.3`). | Populated with 10 flat circular copper landing pads (`U11` to `U20`, 2.0 mm diameter). |
| The pogo pins face outward toward the docking bay. | The landing pads face inward toward the aircraft. |
| Rear Molex J1 connects to the aircraft internal avionics harness. | Rear Molex J1 connects to your payload internal electronics. |

In reality, The PCB is the same for both sides. The payload is however mirrored in placement but not in fabrication. 

| Physical PCB: Mating Face | Physical PCB: Rear Connector Face |
|:---:|:---:|
| ![Physical Hardware Mating Face](../../task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB/2026-Update/images/QuiverAttachPCB_new1.jpg) | ![Physical Hardware Rear Face](../../task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB/2026-Update/images/QuiverAttachPCB_new2.jpg) |

> [!WARNING]
> **Wiring rule:** The aircraft-side board uses spring-loaded pins U1–U10; the payload-side board uses copper pads U11–U20. Connect payload wiring through Molex J1, not directly to the contacts.

---

## 3. Electrical Contract

This section summarizes routing in the current board designs and separates it from firmware configuration and system behavior that require separate validation.

The current design references are the board layouts and schematics for the Main PCB and Attachment Interface PCB:
- Main PCB: [`Quiver_PT3_Main_PCB-rounded.kicad_pcb`](../../src/pcb/main_pcb/Quiver_PT3_Main_PCB-rounded.kicad_pcb) and [`Quiver_PT3_Main_PCB-rounded.kicad_sch`](../../src/pcb/main_pcb/Quiver_PT3_Main_PCB-rounded.kicad_sch)
- Attachment Interface PCB: [`QuiverAttachPCB.kicad_pcb`](../../src/pcb/attach_pcb/QuiverAttachPCB.kicad_pcb) and [`QuiverAttachPCB.kicad_sch`](../../src/pcb/attach_pcb/QuiverAttachPCB.kicad_sch)

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
| **Recommended payload IP** | `192.168.144.100` | `192.168.144.101` | `192.168.144.102` | Static address; match the installed bay |

### 3.2 Main PCB Payload Headers (J29, J30, J31) and Ethernet Connectors (J37, J38, J39)

On the aircraft's Main PCB, each payload bay connects to a 6-pin Phoenix Contact PTSM connector for power, CAN, and FMU signals, and to a separate 4-pin Phoenix Contact PTSM Ethernet header routed to an onboard switch:

| Bay | Avionics Header (power + CAN + FMU) | Ethernet Header |
|---|---|---|
| **Bottom** | `J31` (PTSM `1814951`, 6-pin) | `J39` (Phoenix PTSM `1814935`, 4-pin) |
| **Side 1 (Right)** | `J29` (PTSM `1778735`, 6-pin) | `J37` (PTSM `1778719`, 4-pin) |
| **Side 2 (Left)** | `J30` (PTSM `1778735`, 6-pin) | `J38` (PTSM `1778719`, 4-pin) |

The avionics (J29/J30/J31) and Ethernet (J37/J38/J39) headers are internal to the aircraft harness; your attachment only sees the signals arriving at Molex J1 on the Attachment Interface PCB. The PCB files establish pair routing, not a negotiated Ethernet link speed.

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

The **12-pin Molex connector (J1)** on the back of your payload board is where your attachment wiring connects:
- **Board Header (J1):** Molex part `2077601281` (12-circuit, 1.25 mm pitch, vertical locking connector).
- **Mating Cable Plug:** Molex housing `2045231201` with gold-plated crimp terminals `2045250001`.

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
| **10** | `+12V` | Power | +12V DC, ~1.1A hold | Main switched payload rail `+12V_PL` (K2 controls Q2; `12V Pay`) |
| **11** | `CAN_H` | I/O | CAN high | Aircraft **CAN2_H**. *(Board silkscreen says `CAN1_P`)* |
| **12** | `FMU_AUX` | I/O | FMU signal; verify voltage and waveform on aircraft | Bay auxiliary net: **Bottom:** `FMU_CH1`, **Side 1:** `FMU_CH7`, **Side 2:** `FMU_CH8` |

*(Molex J1 signal and pin mapping.)*

### 3.4 Pogo Pin and Landing Pad Map

When you check electrical continuity with a multimeter, here is how the 10 contact pads across the mating plane match up:

| Signal Name | Drone Pogo Pin (`U1` to `U10`) | Payload Landing Pad (`U11` to `U20`) | Mated Signal Function |
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

If your payload uses Ethernet, its differential pairs route through the onboard switch modules. Verify the negotiated link speed with the attached equipment:
- **Switch Hardware:** Two BotBlox GigaBlox Nano modules are installed on the Main PCB. Their board-mount connectors are internal module mounts, not user-facing payload connectors.
- **Port Assignment:**
  - Switch 1 serves the Bottom and Side 1 bay Ethernet headers.
  - Switch 2 serves the Side 2 bay Ethernet header.
- **Wiring to the Bay:** The harness carries the `ETH_TX` and `ETH_RX` pairs to pins 1, 3, 5, and 7 on Molex J1.

### 3.6 CAN Bus Architecture

The Main PCB design uses two CAN nets; the payload connectors are routed to CAN2:

1. **CAN1:** The Main PCB keeps the payload connector nets off CAN1.
2. **CAN2:** Bottom J31, Side 1 J29, and Side 2 J30 route to `/CAN2_H` and `/CAN2_L`.
  - The NanoRadar MR82 uses CAN at 500 kbit/s with a non-DroneCAN protocol. The RPLidar S2L connects over serial.
  - Keep the NanoRadar separate from DroneCAN nodes unless the combination has been tested successfully. Before flight, verify the bitrate, protocol, wiring, and termination of all devices on the bus.

> [!NOTE]
> **CAN label mapping:** The attachment-board labels are `CAN1_P` and `CAN1_N`; at all three aircraft payload ports these conductors connect to Main PCB `CAN2_H` and `CAN2_L`.

- **Bus Termination:** The Main PCB layout includes a 120 ohm resistor (R14) that slide switch S2 can connect across CAN2_H and CAN2_L. Enable it only when the Main PCB is an endpoint in the CAN bus topology. Do not add another terminator inside an attachment by default; account for the complete bus and its two endpoints.

### 3.7 Power Delivery and Switching Rules

Quiver does not provide an always-on, unswitched battery feed on the attachment connectors. Every power rail is controlled by an electronic switch.

```
[14S LiPo, ~50–58.8V] ──/HV+,/HV-── (unfused at both converters' VIN)
   │
   ├─> PS2 (REC30K-4812SZ, 30W/2.5A) ─VOUT─> F4 (5A) ─> +12V
   │                                                       │
   │        ┌───────────────────── K1 (CPC1019N) ─LOAD_1─> F1 (2A) ─> /12VSW ─> J31 pin 6 only
   │        │    ctrl: R1 <─ /FMU_CH2
   │        │
   │        └───────────────────── F8 (PTC ~1.1A hold) ─> F7 (2A) ─> U5 (CPC1907B) ─D1─> +12V_PL ─> J29/J30/J31 pin 6/16
   │                                                              ctrl: R15 <─ /FMU_CH4 ("12V Pay")
   │
   ├─> PS1 (REC20K-4805SZ, 20W) ─VOUT─> F3 (5A) ─> +5V ─> companion computer (J1, Raspberry Pi 5 header), CAN transceiver U1, misc headers
   │
   └─> U4 (CPC1907B) ─D1─(from /HV+ directly)─D2─> F2 (5A) ─> J26 pin 1, switched HV
                    ctrl: R23 <─ /IO_CH7 ("Add HV")
```

#### A. Main 12V Payload Rail (`+12V_PL`)
- **Available on:** All three bays (Molex J1 pin 10; Pogo pin U6/U16).
- **Electronic Switch:** SSR **K2 (CPC1019N)** drives MOSFET **Q2 (SIRA99DP-T1-GE3)** on the Main PCB.
- **Control Signal:** Flight controller channel **`FMU_CH4`**, labeled **`12V Pay`** in ground control software.
- **Protection:** Protected by fast fuse **F7** (2A) and self-resetting PTC **F8** (Littelfuse `1812L110`, 1.10A hold-current part).
- **Conservative Design Estimate:** The F8 hold rating corresponds to about **13W at nominal 12V** across all three bays. This is not a measured system-level payload budget, and exceeding 1.1A is not the PTC trip specification.
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
  - Provides full 14S LiPo battery voltage (~50.0V to 58.8V DC).
  - Switched by SSR **K3 (CPC1019N)** driving MOSFET **Q3 (SIR570DP-T1-RE3)**, controlled by `IO_CH7`, and protected by a **5A fuse (F2)**.
- **Never Tap the ESC Connectors:**
  - Connectors **J25, J28, J34, and J42** (yellow XT60PW-F sockets) on the Main PCB are **strictly for motor ESCs**. Never tap or connect payloads to these ports.
- **Local Voltage Step-Down:** High-power attachments must bring their own onboard DC-DC converter to step down the 50V battery rail to whatever local voltages their electronics need.

---

## 4. Power Budgeting and Worked Examples

This chapter explains the rail routing and the current-derived estimate from the installed protection components. The continuous payload budget for a complete aircraft has not been measured here.

The aircraft power system is shared. Treat the component ratings below as constraints, not as a measured system payload budget:

- `+12V_PL` is a shared 12V rail across all three bays. F8 is a 1.10A hold-current PTC, equivalent to about **13W at nominal 12V**; treat this as a conservative design estimate, not a measured system-level payload budget.
- The 12V rail is protected by PTC F8 and fuse F7. The PTC hold rating is not its trip threshold.
- `12VSW` exists only on the bottom bay and is a dedicated 2A motor path.
- High-power payloads should use the switched HV path at J26 and regulate it locally.

### 4.1 Logic Payload Example

A compact sensor or compute payload that runs a small SBC, a camera, and one or two sensors is generally a **logic payload**. It can often run from the shared 12V payload rail, as long as it stays under the overall budget and has local regulation.

A typical example is a small payload board that draws:

- 5V SBC: 4W to 8W
- Camera module: 1W to 3W
- Sensor bus and LEDs: 0.5W to 2W

This may fit the approximate current-derived estimate if the combined load across all bays is low; measure the actual system before relying on that estimate.

### 4.2 Floodlight Example

A 25W floodlight or similar high-drain payload exceeds the approximately 13W conservative estimate derived from the F8 hold rating. The `+12V_PL` rail has not been validated by a system-level load test.

The correct architecture is:

- connect the payload to the switched HV rail on J26,
- place the payload's own buck or DC-DC converter on the attachment,
- regulate to 12V, 5V, or 24V locally,
- keep the aircraft supply limited to the dedicated HV path and never draw a high-power lamp directly from `+12V_PL`.

This is the design pattern recommended for high-power floodlights, spray pumps, and other actuator-heavy payloads.

### 4.3 Payload Load Validation

Measure the combined `+12V_PL` draw on the aircraft and compare it with the component ratings and approved operating limits. Do not treat the 13W arithmetic estimate as a validated budget.

---

## 5. Control and Data Paths

Choose a signal path based on the payload's control and data needs. Verify electrical levels and protocol compatibility on the aircraft before flight.

Quiver gives each payload a specific job based on what it needs to do. In practice, the rule is simple:

- use the auxiliary PWM/GPIO line for an actuator or trigger signal,
- use CAN2 for bus devices and low-bandwidth telemetry,
- use Ethernet for high-bandwidth payload data or networked devices.

### 5.1 When to Use Each Path

| Need | Correct Path | Typical Use | Notes |
|---|---|---|---|
| Trigger or actuator control | Bay FMU signal net | Payload-specific control input | Electrical levels and ArduPilot output setup require system verification |
| CAN device | CAN2 pair at the payload port | Protocol-compatible CAN device | Do not assume simultaneous DroneCAN and NanoRadar compatibility |
| Networked device | Ethernet pairs at the payload port | Payload Ethernet interface | Link speed depends on the attached equipment and must be verified |

### 5.2 Aux Signal Mapping and PWM Rules

The Main PCB routes a different FMU net to each bay:

| Bay | FMU signal net |
|---|---|
| Bottom | `FMU_CH1` |
| Side 1 | `FMU_CH7` |
| Side 2 | `FMU_CH8` |

The bay nets are `FMU_CH1`, `FMU_CH7`, and `FMU_CH8`. Their waveform, voltage level, and ArduPilot output assignment depend on aircraft configuration. Configure and measure the selected output at the payload connector before attaching an actuator.

### 5.3 CAN2 Rules

The Main PCB routes all three payload connectors to the shared vehicle bus **CAN2**:

- bitrate: set the bus rate required by attached devices; the NanoRadar MR82 uses **500 kbit/s**
- bus: the three payload bays share the physical CAN2 pair
- protocol compatibility: NanoRadar MR82 uses a non-DroneCAN protocol. Keep it separate from DroneCAN nodes unless the combination has been tested successfully
- termination: Main PCB R14 is selectable with S2; enable it only when the Main PCB is a bus endpoint. The complete bus should be terminated at its two physical endpoints; do not add another terminator inside an attachment by default.

Validate the configured bitrate, termination, and compatibility of all attached CAN nodes before flight.

### 5.4 Ethernet Paths and Network Conventions

If your attachment uses Ethernet, its pairs route through the onboard switches. Assign a static address on the aircraft subnet. The payload range and recommended defaults are:

- `192.168.144.100` to `192.168.144.199`
- bottom bay default is `192.168.144.100`
- side 1 default is `192.168.144.101`
- side 2 default is `192.168.144.102`

Use these onboard device addresses when configuring payload networking:

| Device | Address |
|---|---|
| Raspberry Pi (companion computer) | `192.168.144.50` |
| CubeNode ETH adapter | `192.168.144.10` |
| Flight controller | `192.168.144.51` |

Confirm the active aircraft network configuration before assigning an address; avoid duplicating any address already in use.

### 5.5 The Standard Payload Network Table

| Function | Address | Notes |
|---|---|---|
| Companion computer | `192.168.144.50` | Pi on the drone network |
| CubeNode ETH | `192.168.144.10` | Ethernet adapter |
| Flight controller | `192.168.144.51` | ArduPilot MAVLink endpoint |
| Payload bottom | `192.168.144.100` | Default bottom port payload |
| Payload side 1 | `192.168.144.101` | Default right-side payload |
| Payload side 2 | `192.168.144.102` | Default left-side payload |
| Payload reserved range | `192.168.144.100`–`192.168.144.199` | Developer-assigned static range |

Use static addressing within the payload range and do not rely on DHCP. The network is intentionally flat and is shared across the drone's onboard switch fabric.

---

## 6. Flight Controller Integration

This section describes the flight-controller signals exposed at the payload bays and the checks required before connecting an actuator.

The flight controller does not treat the attachment as a generic consumer. It provides power timing, aux signals, and bus routing under a few explicit rules that the developer must respect.

### 6.1 Relay Labels and Power Semantics

The aircraft control labels used for the attachment power paths are:

- `12V Pay` = `FMU_CH4` drives the shared `+12V_PL` rail.
- `Add HV` = the switched high-voltage battery line for power-hungry attachments.

The sequence matters. The switched high-voltage path is the highest-power path and is treated as a deliberate, explicitly enabled device path. The shared 12V payload rail is a lower-power general service path. The bottom bay's `12VSW` motor line is a dedicated motor path and is not a general purpose rail.

### 6.2 SSR Power Hierarchy

The system power hierarchy is:

1. `12V Pay` for the shared low-power payload rail on all bays.
2. `12VSW` for the bottom-bay dedicated motor line.
3. `Add HV` for high-power payloads that need direct flight-battery power.

Use the shared 12V rail only within the measured aircraft power limit; use the switched high-voltage port and local conversion when the payload requires a different power path.

### 6.3 Arming, Disarming, and Hot-Swap Rules

Live attachment or removal is not established as a tested operating procedure here. Keep the aircraft unpowered unless live connection has been tested and approved for the specific aircraft and payload.

Practical rules:

- never hot-plug a payload while the aircraft is armed or the power rails are alive,
- do not rely on the attachment board to absorb inrush current,
- measure the combined payload rail draw before takeoff,
- select the power path based on measured load and the aircraft's approved operating limits.

### 6.4 Direct Flight Controller Wiring for a Servo or Latch

The auxiliary nets connect to flight-controller channels, but their waveform, voltage, and servo-function configuration depend on the aircraft setup. Verify these before connecting an actuator.

The basic pattern is:

- reserve a bay-specific aux output (`FMU_CH1`, `FMU_CH7`, or `FMU_CH8`),
- configure the relevant ArduPilot output for the intended function,
- validate the waveform at the payload connector before flight.

This is the recommended path for a latch, release mechanism, or shutter trigger.

---

## 7. Software Handoff

The attachment application should communicate with its hardware locally and expose only the data and controls required by the aircraft operator.

### 7.1 Payload Application

Implement payload-specific device control in the payload application. Keep it separate from flight-control logic, and define the required inputs, outputs, startup behavior, and failure response before integration.

### 7.2 Recommended Handoff Pattern

1. Build a payload application that opens a local service on the payload device.
2. Expose a controlled API over Ethernet or an onboard serial/CAN service.
3. Let the companion computer forward telemetry or video into the central Quiver Hub flow.
4. Keep the onboard payload logic local and keep the vehicle-level control logic in the flight controller and companion computer.

This allows the payload to remain independent while still integrating with the wider aircraft system.

### 7.3 Hub and Companion Interaction

When the aircraft uses a companion computer, it can relay payload telemetry, logs, and operator commands between the aircraft network and the ground station.

Keep payload device control, vehicle control, and operator-facing services as separate responsibilities:

- flight controller handles flight control,
- companion computer handles payload network and telemetry,
- Hub handles operator visibility and control,
- the payload app handles its own local sensor or actuator function.

---

## 8. Validation Checklist and Flight Rules

This checklist is written so you can use it on a bench or in a hangar without reading the rest of the guide.

### 8.1 Bench Validation Checklist

- [ ] **Connector orientation:** The payload-side attachment board is installed with the copper pads facing the aircraft and the J1 connector on the rear face.
- [ ] **No direct soldering to pogo pins:** All payload wiring is terminated only on Molex J1.
- [ ] **Power check:** Measure `+12V_PL` current on the aircraft and compare it with the conservative 1.10A F8 hold-current rating and the approved system limit.
- [ ] **Fuse and protection check:** The payload does not exceed the fuse and PTC limits for the rail being used.
- [ ] **PWM check:** The aux signal is measured on the actual bay connector and the correct output is confirmed for the bay (`FMU_CH1`, `FMU_CH7`, or `FMU_CH8`).
- [ ] **CAN validation:** Verify bitrate, node protocol compatibility, and termination on the complete bus. Account for Main PCB R14/S2 and keep NanoRadar separate from DroneCAN nodes unless interoperability has been tested.
- [ ] **Ethernet validation:** Confirm the payload link comes up and the Tx/Rx pairs are wired correctly; verify negotiated link speed with the attached equipment.
- [ ] **No rail sag:** The payload does not pull the avionics rail down under normal operation.
- [ ] **Mechanical fit:** The payload clears the bay envelope and does not interfere with propeller clearance, battery motion, or harness routing.

### 8.2 Flight Rules

- never arm a payload that is drawing more than the allowed rail budget,
- never use the shared 12V payload rail for a high-power payload,
- never use the bottom bay's `12VSW` line for a general purpose bus,
- do not attach or remove a powered payload unless that live operation has been validated and is allowed by the aircraft procedure,
- if the payload fails to enumerate on CAN2 or fails to show a stable PWM waveform, do not fly it.

Use the aircraft-specific operating procedure and record test results for the deployed configuration.

---

### 9. Integration Checklist

Before flight, verify mechanical fit, contact alignment, power draw, auxiliary signal levels, CAN bitrate/protocol/termination, and Ethernet connectivity on the aircraft configuration that will be used. Do not treat an untested payload or operating mode as validated.

---

## Quick Reference

### Connectors You Need to Know

| Designator | Component Part Number | Location | What It Does |
|---|---|---|---|
| **J1** | Molex `2077601281` | Payload PCB (rear) | 12-pin locking header. Mates with cable housing Molex `2045231201`. |
| **U1 to U10** | LCSC `C2826546` | Drone PCB (front) | 10 male spring-loaded pogo pins. Mates with U11 to U20. |
| **U11 to U20** | 2.0 mm Copper Pads | Payload PCB (front) | 10 flat circular landing pads. Mates with U1 to U10. |
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
| **`IO_CH7`** | K3 (`CPC1019N`) | Q3 (`SIR570DP`) | `AC_HV−` on J26 | Switched direct battery power (~50V to 58.8V) for high-power payloads. Protected by F2 (5A). |
| **`FMU_CH1`** | Flight-controller channel | — | Auxiliary signal net | Routed to Bottom bay; waveform and output configuration must be verified on the aircraft. |
| **`FMU_CH7`** | Flight-controller channel | — | Auxiliary signal net | Routed to Side 1; waveform and output configuration must be verified on the aircraft. |
| **`FMU_CH8`** | Flight-controller channel | — | Auxiliary signal net | Routed to Side 2; waveform and output configuration must be verified on the aircraft. |

### Official Board and Design Files

| Path | What It Defines |
|---|---|
| [`src/pcb/main_pcb/Quiver_PT3_Main_PCB-rounded.kicad_pcb`](../../src/pcb/main_pcb/Quiver_PT3_Main_PCB-rounded.kicad_pcb) | Main PCB layout. |
| [`src/pcb/main_pcb/Quiver_PT3_Main_PCB-rounded.kicad_sch`](../../src/pcb/main_pcb/Quiver_PT3_Main_PCB-rounded.kicad_sch) | Main PCB schematic. |
| [`src/pcb/attach_pcb/QuiverAttachPCB.kicad_pcb`](../../src/pcb/attach_pcb/QuiverAttachPCB.kicad_pcb) | Attachment Interface PCB layout. |
| [`src/pcb/attach_pcb/QuiverAttachPCB.kicad_sch`](../../src/pcb/attach_pcb/QuiverAttachPCB.kicad_sch) | Attachment Interface PCB schematic and pin mapping. |
