# Attachment Developer Guide

This guide documents the **V1.4 Attachment Interface** as built, flown, and currently in dev-kit service. Interface and power-delivery changes under discussion in [#234](https://github.com/Arrow-air/project-quiver/issues/234) will get their own revision once settled.

This is the one document a third party needs to build a Quiver attachment: how to get a payload connected physically, connected electrically without browning out the aircraft, and talking to the flight controller and the Hub software.

For the software side (SDK, payload app template, the Hub), see the [Quiver SDK Developer Guide](./Quiver-SDK-Developer-Guide.md). This document covers hardware and the electrical/data contract only.

**How to use this guide.** Read in order: mechanical interface first (what you're physically building to), then the electrical contract (what will and won't damage the aircraft), then the control/data and validation chapters. Don't skip to the pinout table and start wiring. Section 4 below ("Before you build") lists what's still unconfirmed. Check it before you commit to a design.

---

## New here? Read this first

If you have never seen a Quiver before, this box gives you the mental model the rest of the guide assumes. Skim it, then read Chapters 1–3 in order.

**The aircraft in one paragraph.** Quiver is a multirotor drone built around a main avionics board (the *Main PCB*). It has three exposed payload bays : one on the **bottom** of the fuselage and one on each **side**. Each bay presents the same connector to the outside world: twenty spring-loaded *pogo pins* that carry 12 V power, ground, a CAN bus, one PWM/GPIO signal, and an Ethernet pair. Your attachment lands on those pins and bolts on with four M2 screws. Power and signals come from the aircraft; anything your payload needs beyond ~13 W must be sourced differently (Chapter 3 explains how).

**Terms used throughout:**

| Term | Plain meaning |
|---|---|
| **Pogo pin** | Spring-loaded contact on the aircraft side; your attachment needs matching flat pads. Every electrical signal lands on **two** pins for redundancy — always wire both. |
| **CAN bus** | A two-wire vehicle network (CAN_H / CAN_L). Quiver has two: **CAN1** runs the flight-critical avionics (ESCs, GNSS, Remote ID) at 1 Mbit; **CAN2** ("RadarCAN", 500 kbit) serves the radar sensors. |
| **DroneCAN** | The protocol spoken on the CAN bus by payload nodes. If your payload has a microcontroller, it typically joins as a DroneCAN node. |
| **FMU** | The flight-management unit, i.e. the flight controller (an ArduPilot/PX4-class computer). **FMU_CHn** are its auxiliary output channels. |
| **PWM** | A single control wire carrying a timed pulse; the simplest way to trigger or drive something (servo, camera shutter). |
| **12 V payload rail (`+12V_PL`)** | The shared, switched 12 V supply available at all three bays. **~13 W total, all ports combined.** |
| **12VSW** | A *second* switched 12 V line, available on the **bottom port only**. |
| **HV** | Direct battery voltage, 14S ≈ 50–58.8 V. The high-power path. |
| **SSR / relay** | A solid-state switch the flight controller toggles. Relay names like `12V Pay` control attachment power timing. |
| **PTC** | A self-resetting overcurrent fuse. Heats and trips at ~1.1 A hold / ~2.2 A on the payload rail. |
| **Brown-out** | A rail sagging under load so far that other avionics reset or lose radio link. The thing this guide is written to prevent. |
| **ICD** | The Interface Control Document in the `payload-systems` repository — the formal interface contract this guide summarizes and links, not duplicates. |

---

## 1. What is a Quiver attachment?

A Quiver attachment is a payload module that connects to one of three physical ports on the airframe: **bottom**, **side 1**, or **side 2**. Each port presents the same physical interface (power, a CAN bus, one PWM/GPIO auxiliary channel, and an Ethernet pair) through a pogo-pin interface between the airframe's Attachment Interface PCB [src/pcb/attach_pcb/QuiverAttachPCB.kicad_pcb](../../src/pcb/attach_pcb/QuiverAttachPCB.kicad_pcb) and a matching landing connector on the attachment itself.

**Hot swap:** Whether attachments may be connected or disconnected while the aircraft is powered is not yet formally documented. Design intent needs confirming with Erick and validating at the bench before this guide can state a rule. Treat attachments as **connect-only-when-unpowered** until that is resolved.

**What exists today.** Three attachments have been built and flown as of the August 2026 meetup:
1. **Actuated payload latch:** Servo-driven via native PWM output, stepping down the 12 V rail to 6 V on the payload side.
2. **Multispectral/NIR camera:** Native PWM trigger with clean isolated power.
3. **Starlink Mini unit:** Powers up and establishes network connectivity, but drops its link when a camera stream opens on the same aircraft. Power delivery and rail sag under load are suspected causes, still unresolved.

---

## 2. Mechanical interface

> **Traceability note.** This chapter is a summary. The formal mechanical contract is **ICD §6** and the STEP files and mounting coordinates under `payload-systems/interface/mechanical/`. Build your mechanical model against those files; this chapter only records what the KiCad V1.4 sources show and what the ICD does not cover.

### Envelope

The attachment-side PCB outline (`Edge.Cuts` layer) spans approximately:

- **Width:** ~23.5 mm (X: 98.25 → 121.75)
- **Height:** ~15.8 mm (Y: 125.1 → 140.9)
- Corners are chamfered at 45°, not square.

**Orientation:** board-local coordinates in the sources above have +X running across the long axis of the array (from the mounting-hole column at x=100 toward x=120) and +Y toward the wider edge of the rectangle (y=129 → 137). The two pogo arrays sit between the mounting-hole rows, split across the 5 mm gap along X. Confirm final flight orientation against the STEP assembly before cutting anything — the chamfers are asymmetric and only mate one way.

### Mounting

Four mounting holes, ~2 mm diameter , arranged in a rectangular bolt pattern:
- Coordinates: `(100, 129)`, `(120, 129)`, `(100, 137)`, `(120, 137)` in board-local coordinates
- Pattern: **20 mm × 8 mm** rectangular grid.

### Pogo pad geometry

Twenty pogo pin pads (reference designators `U1`–`U20`), laid out as **two redundant 10-pin arrays**:
- Each array is a 5-column × 2-row grid at 2.54 mm (0.1″) pitch.
- A 5 mm gap separates the two arrays.
- Each signal lands on two separate pins (see pinout table below). This looks like it's for contact reliability under vibration and wear, but that's not confirmed. If you're designing a new attachment connector, wire both pins per signal rather than relying on just one.

---

## 3. Electrical contract

### Per-port routing (Main PCB side)

Verified against the Main PCB netlist (`src/pcb/main_pcb/Quiver_PT3_Main_PCB.net`):

| Port | Connector | CAN bus | Aux/FMU channel | 12VSW (pin 6) |
|---|---|---|---|---|
| **Bottom** | J31 | **CAN1** (H: net 15, L: net 16), flight-critical bus, shared with ESCs, GNSS, Remote ID | FMU_CH1 (net 54, servo output 9) | Connected (`/12VSW`, net 6 via K1 CPC1019N + 2A fuse F1) |
| **Side 1** | J29 | **CAN1** (H: net 15, L: net 16), flight-critical bus | FMU_CH7 (net 60, servo output 15) | *No connect (NC)* |
| **Side 2** | J30 | **CAN2** (H: net 17, L: net 18), RadarCAN, 500 kbps, shared with two NanoRadar sensors | FMU_CH8 (net 61, servo output 16) | *No connect (NC)* |

> **ICD discrepancy — flagged for ICD revision.** ICD 1.0-draft (2026-08-06, `payload-systems`) states CAN2 on **all three** ports. The Main PCB netlist says otherwise: J31 (bottom) and J29 (side 1) sit on **CAN1**, the flight-critical bus, and only J30 (side 2) is on CAN2. Re-verified 2026-09-22. **The netlist values in the table above are authoritative.** This discrepancy is recorded here pending an ICD revision; see the ICD discrepancy entry in `payload-systems`.

### Flight Safety Critical: CAN1 Routing
A payload attached to the **bottom** (J31) or **side 1** (J29) port shares **CAN1**, the same bus as the ESCs, GNSS, and Remote ID. A malformed packet storm or a flooding DroneCAN node on either port can degrade flight-critical avionics traffic.
- Only **side 2** (J30) is isolated on **CAN2** with the radar sensors.
- Third-party CAN payloads on CAN1 must be thoroughly tested for bus-utilization limits and fault behavior before flight.


### Pogo pin signal map (Attachment-side PCB)

Extracted from `QuiverAttachPCB.kicad_pcb` and `QuiverAttachPCB.kicad_sch` net assignments. This connector presents the generic per-port signal set:

| Signal | Pin (Array A) | Pin (Array B, redundant) | Function / Notes |
|---|---|---|---|
| **ETH_RX+** | U1 | U11 | 100BASE-TX Ethernet Receive + |
| **12VSW** | U2 | U12 | Switched 12 V (Driven on Bottom port only; NC on Side 1 / Side 2) |
| **ETH_RX−** | U3 | U13 | 100BASE-TX Ethernet Receive − |
| **GND** | U4 | U14 | System Ground |
| **ETH_TX+** | U5 | U15 | 100BASE-TX Ethernet Transmit + |
| **+12V** | U6 | U16 | Unswitched 12 V payload rail (always-on avionics tap) |
| **ETH_TX−** | U7 | U17 | 100BASE-TX Ethernet Transmit − |
| **FMU_AUX** | U8 | U18 | Auxiliary PWM / GPIO (Port-dependent: FMU_CH1 / CH7 / CH8) |
| **CAN_H** | U9 | U19 | CAN High (Port-dependent: CAN1 on Bottom/Side 1; CAN2 on Side 2) |
| **CAN_L** | U10 | U20 | CAN Low (Port-dependent: CAN1 on Bottom/Side 1; CAN2 on Side 2) |

#### Which port for switched 12V

The attachment PCB has `12VSW` pads on every port (U2/U12), routed to pin 6 of the harness connector (Molex SlimStack J1). If you're picking a port for a payload that needs switched power, check this first. On the Main PCB:
- **Bottom port (J31)** connects pin 6 to `/12VSW` (net 6), powered via solid-state relay K1 (CPC1019N) and 2 A fuse F1.
- **Side 1 (J29)** and **Side 2 (J30)** have pin 6 left unconnected (`no_connect` / NC).
So a payload that needs switched 12V through the attachment interface has to go on the **bottom port**.

#### Relay semantics (Pilot Handbook §2.8.5)

The relays your attachment's power timing depends on, as labeled in the ground-station software:

| Relay label | Meaning |
|---|---|
| `Add HV` | Adds HV battery power to the switched-HV path (J26) |
| `P1 Sig` | Signals path for port 1 |
| `P1 12V` | 12 V enable for port 1 |
| `12V Pay` | The `+12V_PL` payload rail switch (U5, CPC1907B) |

`12V Pay` is the one that gates your 12 V rail; plan for the SSR hierarchy (configuration guide §11) meaning attachment rails are sequenced after avionics power-up and may drop on disarm or kill. Exact timing across arm/disarm/kill is an open question (see "Before you build").

#### Ethernet Harness Path

The pogo connector carries a full 100BASE-TX pair (TX+/TX−/RX+/RX−) through the Attachment Interface PCB to J1 (`Molex 2077601281`), which links to the Main PCB's Ethernet switch (GigaBlox J47, ports P0A/P0B). The physical harness between these two ends still needs a bench continuity check.

### Power delivery limits

Traced from PT3 Main PCB schematics and power-delivery analysis (#234):

- **Aircraft 12V Supply:** RECOM REC30K-4812SZ isolated converter (HV in → 12 V, **30 W / 2.5 A total**), protected by 5 A fuse F4. This rail also powers the companion computer, SIYI air unit/camera, and essential avionics.
- **Attachment 12V Payload Rail (`+12V_PL`):** Sourced from the primary 12 V rail through:
  - F8: 1812L110 PTC resettable fuse (**~1.1 A hold / ~2.2 A trip**)
  - F7: 2 A fast fuse
  - U5: CPC1907B solid-state relay (controlled via flight controller, relay `12V Pay`)
  - Output: `+12V_PL` bus shared across **all three attachment ports** (J29, J30, J31).
- **Available Attachment Power:** **~13 W total shared across all three ports**, derating further at elevated operational temperatures.
- **Risk of Overcurrent:** Any attachment drawing >1.1 A will heat and trip PTC F8, browning out all three attachment bays. Saturated converter draw (>2.5 A) risks browning out the SIYI video/telemetry link.

### High-voltage / high-power attachments

Due to the ~13 W limit on `+12V_PL`, high-power attachments (such as the JMRRC granular dispenser or high-output floodlights) **must not** draw from the 12 V payload rail.

Instead, the standard attachment architecture uses:
1. **Power Path:** Direct battery voltage (14S / ~50–58.8 V) via the Main PCB XT60 high-voltage taps (`HV+`/`HV-` on J25/J28/J34/J42) or switched HV port J26 (U4 CPC1907B + 5 A fuse).
2. **Local Regulation:** High-power attachments must incorporate onboard payload-side DC-DC step-down converters sized for their specific loads.
3. **Logic Isolation:** Signals (CAN, PWM, Ethernet) route through the attachment pogo pads, while high-current power bypasses the pogo contacts.

---

## Before you build

These are open questions in the sources this guide is built from. None of them are guesses, they're gaps. Check the linked issue for current status before you finalize a design around them.

- **Hot swap rules.** Not documented. Assume connect-only-when-unpowered (Chapter 1) until Erick confirms otherwise.
- **Empty weight, battery weight, max payload mass.** Not documented anywhere. Tracked in #209, asked for again in this issue.
- **Structural load limits per port.** No ratings exist for side vs. bottom ports. Needs CAD/FEA from Alperen before you design anything load-bearing.
- **12V payload rail limits.** The ~13 W shared budget and the PTC F8 trip point are traced from the schematic, not measured. A bench load test is requested in this issue; until it lands, treat the schematic numbers as conservative, not final.
- **Pogo pin redundancy.** Each electrical signal lands on two physical pins. Whether that's deliberate design intent or coincidental isn't confirmed. Wire both pins anyway.
- **Ethernet harness continuity.** The netlist confirms Ethernet reaches the pogo pads at both ends (attachment connector and Main PCB switch), but the physical harness run between them hasn't been bench-tested.
- **Rail behavior across arm / disarm / kill.** When exactly `12V Pay` and the per-port relays energize and de-energize has not been written down. Design intent from Erick, then bench validation, is needed before this guide can state a rule.


---

## Quick Reference

### Key connectors

| Ref | Part | Location |
|---|---|---|
| J29 | Side 1 payload port | Main PCB |
| J30 | Side 2 payload port | Main PCB |
| J31 | Bottom payload port | Main PCB |
| J47 | GigaBlox Ethernet switch | Main PCB |
| J1 | Molex 2077601281, harness to pogo array | Attachment PCB |

### Key components (12V payload rail)

| Ref | Part | Role |
|---|---|---|
| U5 | CPC1907B | Solid-state relay, `+12V_PL` switching (`12V Pay`) |
| K1 | CPC1019N | Solid-state relay, bottom-port `/12VSW` |
| F1 | 2 A fuse | `/12VSW` protection |
| F7 | 2 A fuse | `+12V_PL` protection |
| F8 | 1812L110 PTC | `+12V_PL` resettable overcurrent (~1.1 A hold) |
| N/A | RECOM REC30K-4812SZ | Main 12V supply, 30 W / 2.5 A |

### Source files referenced in this guide

| File | What it defines |
|---|---|
| `src/pcb/attach_pcb/QuiverAttachPCB.kicad_pcb` | Attachment-side pogo pad layout and envelope |
| `src/pcb/attach_pcb/QuiverAttachPCB.kicad_sch` | Attachment-side schematic |
| `src/pcb/main_pcb/Quiver_PT3_Main_PCB.net` | Main PCB netlist, per-port CAN/FMU/12VSW routing |
| `payload-systems` ICD §6 + `interface/mechanical/` STEP files | Formal mechanical interface contract |
| Pilot Handbook §2.8.5 | Relay labels (`Add HV`, `P1 Sig`, `P1 12V`, `12V Pay`) |
| Initial Configuration Guide §0, §11, §11.6 | Network topology, SSR power hierarchy, PWM aux parameters |

### Related issues

| Issue | Topic |
|---|---|
| [#209](https://github.com/Arrow-air/project-quiver/issues/209) | Weigh-in (empty weight, battery weight, max payload mass) |
| [#233](https://github.com/Arrow-air/project-quiver/issues/233) | Adapter board reference design (JMRRC dispenser) |
| [#234](https://github.com/Arrow-air/project-quiver/issues/234) | 12V payload rail power delivery analysis |
