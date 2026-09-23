# Attachment Developer Guide

This guide documents the **V1.4 Attachment Interface** as built, flown, and currently in dev-kit service. Interface and power-delivery changes under discussion in [#234](https://github.com/Arrow-air/project-quiver/issues/234) will get their own revision once settled.

This is the one document a third party needs to build a Quiver attachment: how to get a payload connected physically, connected electrically without browning out the aircraft, and talking to the flight controller and the Hub software.

For the software side (SDK, payload app template, the Hub), see the [Quiver SDK Developer Guide](./Quiver-SDK-Developer-Guide.md). This document covers hardware and the electrical/data contract only.

**How to use this guide.** Read in order: mechanical interface first (what you're physically building to), then the electrical contract (what will and won't damage the aircraft), then the control/data and validation chapters . Don't skip to the pinout table and start wiring. The "Before you build" section near the end lists what's still unconfirmed. Check it before you commit to a design.

---

## New here? Read this first

If you have never seen a Quiver before, this section gives you the mental model the rest of the guide assumes. Skim it, then read Chapters 1 to 3 in order.

**The aircraft in one paragraph.** Quiver is a multirotor drone built around a main avionics board (the Main PCB). It has three exposed payload bays: one on the bottom of the fuselage and one on each side. Each bay presents the same connector to the outside world, twenty spring-loaded pogo pins that carry 12V power, ground, a CAN bus, one PWM/GPIO signal, and an Ethernet pair. Your attachment lands on those pins and bolts on through a quick-release clip mechanism. Power and signals come from the aircraft; anything your payload needs beyond ~13W must be sourced differently (Chapter 3 explains how).

**Terms used throughout:**

| Term | Plain meaning |
|---|---|
| **Pogo pin** | Spring-loaded contact on the drone side of the blind-mate connector. The payload side has matching flat pads, not more pogo pins, see Chapter 2 for why there are two pin ranges. |
| **CAN bus** | A two-wire vehicle network (CAN_H / CAN_L). Quiver has two: CAN1 runs the flight-critical avionics (ESCs, GNSS, Remote ID) at 1 Mbit. CAN2 ("RadarCAN", 500 kbit) serves the radar sensors. Which port sits on which bus is not what you'd guess, see Chapter 3. |
| **DroneCAN** | The protocol spoken on the CAN bus by payload nodes. If your payload has a microcontroller, it typically joins as a DroneCAN node. |
| **FMU** | The flight-management unit, i.e. the flight controller (an ArduPilot-class computer). FMU_CHn are its auxiliary output channels. |
| **PWM** | A single control wire carrying a timed pulse, the simplest way to trigger or drive something (servo, camera shutter). |
| **12V payload rail (`+12V_PL`)** | The shared, switched 12V supply available at all three bays. ~13W total, all ports combined, still unmeasured (see "Before you build"). |
| **12VSW** | A second switched 12V line, available on the bottom port only. |
| **HV** | Direct battery voltage, 14S, roughly 50 to 58.8V. The high-power path. |
| **SSR / relay** | A solid-state switch the flight controller toggles. Relay names like `12V Pay` control attachment power timing. |
| **PTC** | A self-resetting overcurrent fuse. Heats and trips at roughly 1.1A hold, 2.2A trip, on the payload rail. |
| **Brown-out** | A rail sagging under load so far that other avionics reset or lose radio link. The thing this guide is written to prevent. |
| **ICD** | The Interface Control Document in the `payload-systems` repository, the formal interface contract this guide summarizes and cites. |

---

## 1. What is a Quiver attachment?

A Quiver attachment is a payload module that connects to one of three physical ports on the airframe: **bottom**, **side 1**, or **side 2**. Each port presents the same physical interface (power, a CAN bus, one PWM/GPIO auxiliary channel, and an Ethernet pair) through a pogo-pin interface between the airframe's Attachment Interface PCB ([`src/pcb/attach_pcb/QuiverAttachPCB.kicad_pcb`](../../src/pcb/attach_pcb/QuiverAttachPCB.kicad_pcb)) and a matching landing connector on the attachment itself.

**Hot swap.** Whether attachments may be connected or disconnected while the aircraft is powered is not yet formally documented. Design intent needs confirming with Erick and validating at the bench before this guide can state a rule. Treat attachments as **connect-only-when-unpowered** until that is resolved.

**What exists today.** Three attachments have been built and flown as of the August 2026 meetup:
1. **Actuated payload latch.** Servo-driven via native PWM output, stepping down the 12V rail to 6V on the payload side.
2. **Multispectral/NIR camera.** Native PWM trigger with clean isolated power.
3. **Starlink Mini unit.** Powers up and establishes network connectivity, but drops its link when a camera stream opens on the same aircraft. Power delivery and rail sag under load are suspected causes, still unresolved.

---

## 2. Mechanical interface


This chapter follows the [payload-systems ICD](https://github.com/Arrow-air/payload-systems/blob/main/interface/ICD.md) §6, with the vendored STEP files in [`payload-systems/interface/mechanical/`](https://github.com/Arrow-air/payload-systems/tree/main/interface/mechanical). Where the ICD is silent, that's called out below rather than filled in.

### The quick-release mechanism

Quiver mounts payloads on three hot-swappable quick-release points: bottom, side 1 (right), side 2 (left). Each is a COTS aluminum clip-plate pair (BOM 2112, ordered without PCB). The aircraft carries the fixed half (spring press-pins) at each port. **Your payload carries the mating clip half of the same product.** Buy the same part, don't design your own mate, or you won't be mechanically compatible with the flying aircraft. No tools are required to install or remove a payload once the clip plate is bolted on.

STEP files (vendored copies, originals in project-quiver are source of truth):

| File | Part | You need this for |
|---|---|---|
| `2112_attach_plate_payload_side.step` | Payload-side clip plate ("Replaceable Base") | Your payload's mounting pattern. 50 x 50 mm footprint, 10.5 mm thick. |
| `2112_attach_plate.step` | Drone-side fixed plate | Reference only, you don't build this. |
| `2111_attach_spacer.step` | Side-port PETG spacer | Reference for side-port clearance. |
| `2131_attach_spacer_bottom.step` | Bottom-port PETG spacer, has a wiring notch | Reference for bottom-port clearance. |

### Mounting-point positions

Drone coordinate frame: origin at airframe center, +Z up, +Y forward.

| Port | Plate position (x, y, z) mm | Mechanism faces |
|---|---|---|
| Bottom | (0, 0, -160.7) | -Z (down) |
| Side 1 / Right | (+185.65, -0.02, -71.0) | +X (outboard) |
| Side 2 / Left | (-185.65, +0.02, -71.0) | -X (outboard) |

A bottom payload's top mounting plane sits at roughly Z = -171 mm (the drone-side plate hardware adds ~10 mm). Side ports carry a 3 cm extension adapter for body clearance. Cable ports on both spacers face sideways, not down, to avoid abrasion and water ingress.

To check your design against the full airframe: the parametric example at [`src/quiver/attachments/designs/example_plate/`](https://github.com/Arrow-air/project-quiver/tree/main/src/quiver/attachments/designs/example_plate) in project-quiver builds a placeholder plate on the bottom interface and can render your design in place (`python -m quiver.attachments.designs.example_plate.assembly --show`).

### The electrical connector (attachment PCB)

Separate from the mechanical clip plate, and mounted behind it, is the blind-mate electrical connector. This is the actual PCB, extracted directly from the V1.4 KiCad sources (`src/pcb/attach_pcb/QuiverAttachPCB.kicad_pcb`, `.kicad_sch`):

- **Board:** 23.5 x 15.8 mm, 1.2 mm FR4 (thinner than the standard 1.6 mm), corners chamfered at 45 degrees.
- **Mounting:** four M2 holes on a 20 x 8 mm rectangular pattern, at `(100,129)`, `(120,129)`, `(100,137)`, `(120,137)` in board-local coordinates.
- **Orientation:** board-local +X runs across the long axis of the array (from the mounting-hole column at x=100 toward x=120), +Y toward the wider edge (y=129 to y=137). The chamfers are asymmetric and only mate one way. Confirm orientation against the STEP assembly before cutting anything, don't rely on this coordinate description alone.
- **One board design, two populations.** The same layout serves both sides of the blind-mate. Confirmed by both the ICD and the [Attachment Interface PCB README](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB/README.md): header **J2** (male pogo pins, pads `U1` to `U10`) is populated on the **drone side**. Header **J3** (female flat landing pads, `U11` to `U20`) is populated on the **payload side**. They carry the same 10 signals. They are not a redundant pair, they're the two halves of one connector, so wire your payload's pads to J3's population, not both ranges.

### What the ICD doesn't cover yet

- **Formal keep-out or envelope volumes.** Not published. Practical limits for now: propeller disk clearance for wide payloads, landing-gear ground clearance for bottom payloads, battery-slider travel for side payloads. If in doubt, load your STEP against the full drone assembly using the example above.
- **Per-port structural mass limits.** Not formally specified anywhere. The platform-level budget (25 kg MTOW, 5 to 8 kg total payload capacity across all ports) governs. The ICD itself flags anything over 3 kg on a single port as needing review against the airframe before flight.
- **Empty weight, battery weight.** Not documented anywhere, including the ICD. Asked for in this issue (#209).

---

## 3. Electrical contract

This chapter follows the [payload-systems ICD](https://github.com/Arrow-air/payload-systems/blob/main/interface/ICD.md) §2 to §5. The per-port table and every net name are re-verified here against the Main PCB netlist (`src/pcb/main_pcb/Quiver_PT3_Main_PCB.net`) and the attachment PCB sources, not copied from the ICD text. Where the two disagree, that's flagged, not silently resolved.


### Port capability matrix (ICD §2)

The three ports are not identical. Design against the port you target:

| Capability | Bottom (J31) | Side 1 / Right (J29) | Side 2 / Left (J30) |
|---|---|---|---|
| 12V_PL (main 12V payload rail) | Yes | Yes | Yes |
| 12VSW (relay-switched 12V, 2A fused) | Yes | No | No |
| CAN bus | CAN1 (flight-critical) | CAN1 (flight-critical) | CAN2 (RadarCAN, isolated) |
| Ethernet 100BASE-T | Yes (switch 1) | Yes (switch 1) | Yes (switch 2) |
| PWM aux channel | FMU_CH1 | FMU_CH7 | FMU_CH8 |
| Suggested static IP | 192.168.144.100 | 192.168.144.101 | 192.168.144.102 |

### Per-port routing, verified against the netlist

| Port | Connector | CAN bus | Aux/FMU channel | 12VSW (pin 6) |
|---|---|---|---|---|
| **Bottom** | J31 | **CAN1** (H: net 15, L: net 16), flight-critical bus, shared with ESCs, GNSS, Remote ID | FMU_CH1 (net 54, servo output 9) | Connected (`/12VSW`, net 6, via K1 CPC1019N + 2A fuse F1) |
| **Side 1** | J29 | **CAN1** (H: net 15, L: net 16), flight-critical bus | FMU_CH7 (net 60, servo output 15) | No connect (NC) |
| **Side 2** | J30 | **CAN2** (H: net 17, L: net 18), RadarCAN, 500 kbit, shared with two NanoRadar sensors | FMU_CH8 (net 61, servo output 16) | No connect (NC) |

**Flight Safety Critical: CAN bus routing, ICD discrepancy**
The payload-systems ICD (1.0-draft, 2026-08-06) describes a single shared "CAN2" bus present identically on all three ports. **The netlist does not support that**, and the ICD's own preamble says the project-quiver sources win in a disagreement. Re-verified against the netlist on 2026-09-22.

- Bottom (J31) and Side 1 (J29) sit on the net named **CAN1_H / CAN1_L**, the same bus the ESCs use. The PT1 Engineering Report states directly: "The ESCs will connect to the flight controller's CAN 1 and use the DroneCAN protocol." Two independent sources (netlist, PT1 report) agree this is the flight-critical bus.
- Side 2 (J30) sits on a physically separate net, **CAN2_H / CAN2_L**, at 500 kbit, shared with the two NanoRadar sensors, not with the ESCs.

**Treat the netlist values in the table above as authoritative.** This is flagged here pending an ICD revision, not silently resolved, because a developer following the ICD's capability matrix alone would not know that a bottom or side-1 payload shares a bus with the ESCs, or that side 2 runs at a different bitrate than the other two. A malformed packet storm or a flooding DroneCAN node on bottom or side 1 can degrade flight-critical avionics traffic. Third-party CAN payloads on those two ports must be tested for bus-utilization limits and fault behavior before flight.


Also from the ICD (§4): a 120 ohm termination resistor (R14) is switchable on the Main PCB via switch S2. **Payloads must not add their own bus termination** without coordinating with the airframe configuration, regardless of which port they're on.

### Pogo pin signal map (attachment PCB)

Same 10 signals on both halves of the blind-mate connector (see Chapter 2 for why there are two pin ranges):

| Signal | Pin (drone side, J2) | Pin (payload side, J3) | Function / Notes |
|---|---|---|---|
| **ETH_RX+** | U1 | U11 | 100BASE-TX Ethernet Receive + |
| **12VSW** | U2 | U12 | Switched 12V, 2A fused. Bottom port only, NC on Side 1/2. |
| **ETH_RX-** | U3 | U13 | 100BASE-TX Ethernet Receive - |
| **GND** | U4 | U14 | System Ground |
| **ETH_TX+** | U5 | U15 | 100BASE-TX Ethernet Transmit + |
| **+12V (12V_PL)** | U6 | U16 | Main 12V payload rail. SSR-switched, see below, not a hard-wired always-on tap. |
| **ETH_TX-** | U7 | U17 | 100BASE-TX Ethernet Transmit - |
| **FMU_AUX** | U8 | U18 | Auxiliary PWM/GPIO. Port-dependent channel: FMU_CH1 / CH7 / CH8. |
| **CAN_H** | U9 | U19 | CAN High. Port-dependent bus, see the discrepancy callout above. |
| **CAN_L** | U10 | U20 | CAN Low. Same caveat. |

No 5V or 3.3V logic rail is provided at this connector. No UART either. If your payload needs a logic rail, bring your own DC-DC (the ICD suggests something in the Mean Well SD-25B-05 class for 5V).

#### Which port for switched 12V

If your payload needs relay-switched power, it has to be the **bottom port**. On the Main PCB, pin 6 (`12VSW`) connects to `/12VSW` only on J31 (bottom), through solid-state relay K1 (CPC1019N) and a 2A fuse (F1). Side 1 (J29) and Side 2 (J30) leave that pin unconnected.

#### 12V_PL is not always-on

The ICD (§3) states the main 12V payload rail (`+12V_PL`, pin 6/16 above) is switched through solid-state relay **U5 (CPC1907B)**, controlled by flight-controller channel **FMU_CH4**, labeled `12V Pay` in the ground-station relay list. In the standard configuration this defaults to on, so it behaves as always-on in normal operation, but it is not hard-wired. The flight controller can drop and restore it, including to hard power-cycle a hung payload. **Payloads must tolerate power appearing late, being removed at any time, and repeated cycling.**

#### Relay semantics (Pilot Handbook §2.8.5)

The relays your attachment's power timing depends on, as labeled in the ground-station software:

| Relay label | Meaning |
|---|---|
| `Add HV` | Adds HV battery power to the switched-HV path (J26) |
| `P1 Sig` | Signal path for port 1 |
| `P1 12V` | 12V enable for port 1 |
| `12V Pay` | The `+12V_PL` payload rail switch (U5, CPC1907B, FMU_CH4) |

`12V Pay` is the one that gates your main 12V rail. Attachment rails are sequenced after avionics power-up per the SSR hierarchy (Initial Configuration Guide §11). Exact timing across arm, disarm, and kill is an open question, see "Before you build".

#### Ethernet harness path

The pogo connector carries a full 100BASE-TX pair (TX+/TX-/RX+/RX-) through the Attachment Interface PCB to a 12-pin Molex locking connector (J1, part 2077601281). J1's pinout doubles the power and ground pins relative to the 10-pin J2/J3 headers, for extra current capacity, see the [Attachment Interface PCB README](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB/README.md) for the full 12-pin table. From J1, the run continues to the Main PCB's Ethernet switch (bottom and side 1 on switch 1, side 2 on switch 2, per the ICD; GigaBlox J47 ports P0A/P0B in the netlist). The physical harness between the two ends still needs a bench continuity check. This guide confirms both endpoints exist in the design, not that the run between them is intact on a given airframe.

### Power delivery limits

Two sources give different numbers for the same rail, and neither is a bench measurement:

- **Schematic-derived (this guide, from `src/pcb/main_pcb/`):** `+12V_PL` is protected by F8, a 1812L110 PTC resettable fuse (~1.1A hold / ~2.2A trip), plus a 2A fast fuse F7, shared across all three ports. That implies roughly **13W total, shared**, before F8 trips.
- **ICD (§3) design guidance:** budget **~25W per port**, and "verify total draw against Main PCB limits before exceeding."

These don't reconcile cleanly. 25W per port across three ports is far more than a ~13W shared trip point would allow. Until someone runs the bench load test (requested in this issue), treat the schematic-derived ~13W shared figure as the conservative ceiling, and flag the ICD's 25W/port guidance as unverified against it.

Also on the 12V supply chain: the aircraft's main 12V rail comes from a RECOM REC30K-4812SZ isolated converter (30W / 2.5A total, protected by a 5A fuse F4), which also feeds the companion computer, the SIYI air unit/camera, and essential avionics, not just attachments. Saturated draw on this converter (>2.5A) risks browning out the SIYI video/telemetry link, separately from the attachment-specific F8/F7 limits above.

### High-voltage / high-power attachments

Given the payload-rail limits above, high-power attachments (the JMRRC granular dispenser, high-output floodlights) must not draw from `+12V_PL`. The standard architecture instead:

1. **Power path.** Direct battery voltage (14S, ~50 to 58.8V) via the Main PCB's XT60 high-voltage taps (`HV+`/`HV-` on J25/J28/J34/J42) or the switched HV port J26 (relay U4, CPC1907B, 5A fuse).
2. **Local regulation.** The attachment brings its own payload-side DC-DC step-down, sized for its own load.
3. **Logic isolation.** CAN, PWM, and Ethernet still route through the pogo pads; high-current power bypasses them entirely.

---

## Before you build

These are open questions in the sources this guide is built from. None of them are guesses, they're gaps. Check the linked issue for current status before you finalize a design around them.

- **CAN bus naming, ICD vs. netlist.** The ICD describes one shared "CAN2" bus across all three ports. The netlist and the PT1 report agree bottom/side 1 share the ESC bus (netlist name CAN1) while side 2 is an isolated, different-bitrate bus (netlist name CAN2, shared with radar). This is a real contradiction between two authoritative-looking sources, not a guess on either side. Needs Erick to confirm which is correct before it's safe to treat as settled.
- **12V payload rail budget, ICD vs. schematic.** The ICD's design guidance says ~25W per port. The schematic's fuse/PTC chain implies ~13W total, shared across all three ports. These don't reconcile. A bench load test (requested in this issue) would settle it.
- **Rail behavior across arm, disarm, kill.** When exactly `12V Pay` and the per-port relays energize and de-energize has not been written down. Design intent from Erick, then bench validation, is needed before this guide can state a rule.
- **Hot swap rules.** Not documented anywhere, including the ICD. Assume connect-only-when-unpowered (Chapter 1) until Erick confirms otherwise.
- **Empty weight, battery weight, max payload mass.** Not documented anywhere, including the ICD. Tracked in #209, asked for again in this issue.
- **Formal keep-out/envelope volumes and per-port structural mass limits.** The ICD explicitly leaves both open (§6 TODO). The 25 kg MTOW / 5 to 8 kg total payload budget governs until per-port numbers exist. Anything over 3kg on one port needs review against the airframe.
- **Ethernet harness continuity.** The netlist and the ICD agree Ethernet reaches the pogo pads at both ends (attachment connector and Main PCB switch), but the physical harness run between them hasn't been bench-tested.

If you're building against this guide and hit one of these in practice, that's useful information for whoever picks up M2. Post it in the issue rather than working around it silently.

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
| U5 | CPC1907B | Solid-state relay, `+12V_PL` switching (`12V Pay`, FMU_CH4) |
| K1 | CPC1019N | Solid-state relay, bottom-port `/12VSW` |
| F1 | 2A fuse | `/12VSW` protection |
| F7 | 2A fuse | `+12V_PL` protection |
| F8 | 1812L110 PTC | `+12V_PL` resettable overcurrent (~1.1A hold) |
| N/A | RECOM REC30K-4812SZ | Main 12V supply, 30W / 2.5A |

### Source files referenced in this guide

| File | What it defines |
|---|---|
| `src/pcb/attach_pcb/QuiverAttachPCB.kicad_pcb` | Attachment-side pogo pad layout and PCB envelope |
| `src/pcb/attach_pcb/QuiverAttachPCB.kicad_sch` | Attachment-side schematic |
| `src/pcb/main_pcb/Quiver_PT3_Main_PCB.net` | Main PCB netlist, per-port CAN/FMU/12VSW routing |
| [payload-systems `interface/ICD.md`](https://github.com/Arrow-air/payload-systems/blob/main/interface/ICD.md) | Interface Control Document, mechanical + electrical + software integration overview |
| [payload-systems `interface/mechanical/`](https://github.com/Arrow-air/payload-systems/tree/main/interface/mechanical) | STEP files for the quick-release clip-plate mechanism |
| [Attachment Interface PCB README](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB/README.md) | J2/J3/J1 connector pinouts |
| Pilot Handbook §2.8.5 | Relay labels (`Add HV`, `P1 Sig`, `P1 12V`, `12V Pay`) |
| Initial Configuration Guide §0, §11, §11.6 | Network topology, SSR power hierarchy, PWM aux parameters |

### Related issues

| Issue | Topic |
|---|---|
| [#209](https://github.com/Arrow-air/project-quiver/issues/209) | Weigh-in (empty weight, battery weight, max payload mass) |
| [#233](https://github.com/Arrow-air/project-quiver/issues/233) | Adapter board reference design (JMRRC dispenser) |
| [#234](https://github.com/Arrow-air/project-quiver/issues/234) | 12V payload rail power delivery analysis, also the ~25W/port vs ~13W shared discrepancy |

---
