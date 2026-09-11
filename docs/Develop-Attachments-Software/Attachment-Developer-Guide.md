---
title: Attachment Developer Guide
sidebar_label: Attachment Developer Guide
sidebar_position: 1
description: Physical, electrical, and software contract for building a Quiver attachment on the V1.4 interface.
---

# Attachment Developer Guide

**Interface revision:** QuiverAttachPCB **V1.4** (as built on Dev-Kit / current Main PCB)  
**Companion software guide:** [Quiver SDK Developer Guide](./Quiver-SDK-Developer-Guide.md)

> [!WARNING]
>
> This guide documents the **V1.4 attachment interface as shipped**. Power delivery redesign ([#234](https://github.com/Arrow-air/project-quiver/issues/234)), the adapter-board reference design ([#233](https://github.com/Arrow-air/project-quiver/issues/233)), and a future interface replacement are open engineering threads. Do not treat those open threads as requirements for an attachment that must fly on today's aircraft.

---

## 1. What a Quiver attachment is

A Quiver attachment is mission equipment that mounts on one of three quick-release ports, draws power and signals through the Attachment Interface PCB, and optionally talks to the flight controller and companion computer.

### The three ports

| Port | Role | Main PCB power/signal | Main PCB Ethernet | Harness |
| --- | --- | --- | --- | --- |
| Bottom (C1) | Belly payload | **J31** | **J39** | HAR-0014 |
| Side 1 / Right (C2) | Right side | **J29** | **J37** | HAR-0012 |
| Side 2 / Left (C3) | Left side | **J30** | **J38** | HAR-0013 |

Sources: Main PCB copper nets (`src/pcb/main_pcb/Quiver_PT3_Main_PCB.kicad_pcb`), [Harness Manufacturing Guide](../Manufacturing/Harness-Manufacturing-Guide.mdx), Dev-Kit Engineering Report.

### Hot-swap concept

The Attachment Interface PCB is designed so payloads can be connected or removed without opening the avionics stack ([PT3 Engineering Report](../Engineering-Reports/PT3-Engineering-Report.md), [Dev-Kit Engineering Report](../Engineering-Reports/Dev-Kit-Engineering-Report.md)).

> [!NOTE]
>
> **Open — hot-swap operating rules.** Design intent is hot-swap of the mechanical/electrical interface. Whether attachments may be mated or removed with rails live, and how `+12V_PL`, `12VSW`, and switched HV behave across arm, disarm, and kill, is not yet written as a procedure. Confirm with electrical (Erick) at the bench before publishing a hard rule. Until then: treat live hot-mate of high-voltage paths as unsafe, and prefer powering payload rails off (Mission Planner relays / SSR hierarchy) before connecting or removing attachments.

### What exists today

- Three V1.4 Attachment Interface PCBs on the aircraft (spring-loaded pogo array, Molex aircraft cable).
- Shared switched 12 V payload rail (`+12V_PL`) sized for logic-class loads ([#234](https://github.com/Arrow-air/project-quiver/issues/234)).
- Bottom-only switched aux 12 V (`12VSW`).
- Separate switched HV accessory connector **J26** on the Main PCB (not on the pogo array) for high-power attachments ([#233](https://github.com/Arrow-air/project-quiver/issues/233)).
- Companion computer + Quiver Hub software path — see the [SDK Developer Guide](./Quiver-SDK-Developer-Guide.md).
- Demand-side attachment categories (community vote): cargo, LiDAR, machine vision, camera, stabilized carrier, floodlight — see [§1.1](#11-attachments-people-want-to-build).
- Worked examples from the August meetup and Javelina dispenser work — see [§9](#9-lessons-learned).

### 1.1 Attachments people want to build

Priority requirement documents under `task-grant-bounty/equipment/attachment/0002-detailed_attachment_requirement_for_bounty/`:

| Document | Intent |
| --- | --- |
| [001 Universal Cargo Container](../../task-grant-bounty/equipment/attachment/0002-detailed_attachment_requirement_for_bounty/001-Universal_Cargo_Container_comprehensive_requirement.md) | Belly cargo box, actuators, optional release |
| [002 Aerial LiDAR](../../task-grant-bounty/equipment/attachment/0002-detailed_attachment_requirement_for_bounty/002-General_Aerial_LiDAR_Scanning_Device_comprehensive_requirement.md) | Scanning LiDAR with Ethernet control |
| [003 Machine Vision](../../task-grant-bounty/equipment/attachment/0002-detailed_attachment_requirement_for_bounty/003-Ground_Target_Machine_Vision_System_Comprehensive_Requirement.md) | Onboard vision / AI from camera feeds |
| [004 Magnification Camera](../../task-grant-bounty/equipment/attachment/0002-detailed_attachment_requirement_for_bounty/004-Standard_Magnification_Camera_comprehensive_requirement.md) | Dual fixed-focus imaging module |
| [005 Stabilized Sensor Carrier](../../task-grant-bounty/equipment/attachment/0002-detailed_attachment_requirement_for_bounty/005-General_Stabilized_Sensor_Device_Carrier_comprehensive_requirement.md) | 3-axis gimbal-style carrier |
| [006 High Capacity Flood Light](../../task-grant-bounty/equipment/attachment/0002-detailed_attachment_requirement_for_bounty/006-High_Capacity_Flood_Light_comprehensive_requirement.md) | High-lumen flood; expects more than the shared 12 V rail |

Broader brainstorm list: [0001 possible attachment list](../../task-grant-bounty/equipment/attachment/0001-possible_attachment_list/information-note.md).

---

## 2. Mechanical interface

### 2.1 Quick-release plate

Aircraft parts **2112 / 2122 / 2132** are identical quick-release interface plates ([Manufacturing Guide](../Manufacturing/Manufacturing-Guide.md), [BOM](../Manufacturing/BOM.md)). Order the COTS plate **without** PCB board; the Quiver Attachment Interface PCB mounts into the plate stack.

| Item | Value | Source |
| --- | --- | --- |
| Part numbers | 2112 (bottom), 2122 / 2132 (sides) | Manufacturing Guide / BOM |
| CAD | `src/quiver/supporting_structure/attachment_interface/steps/2112_attach_plate.step` | BOM |
| Clearance adapter | ~3 cm extension adapter from body (PT3 airframe change) | [PT3 Engineering Report](../Engineering-Reports/PT3-Engineering-Report.md) |

> [!NOTE]
>
> **Open — structural load ratings.** Side versus bottom port allowable payload mass / moment is not published. Use the aircraft MTOW and empty-weight budget below as the mass ceiling, keep CG and lever arm conservative, and treat FEA or a documented limit from structures (Alperen) as pending. Do not invent a side-port rating.

### 2.2 Attachment Interface PCB V1.4 geometry

Traceability: `src/pcb/attach_pcb/` (live KiCad), production outputs under `src/pcb/attach_pcb/production/`, history and BOM under [`task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB/`](../../task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB/), V1.4 note [`2026-Update/information-note.md`](../../task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB/2026-Update/information-note.md).

| Item | Value | Source |
| --- | --- | --- |
| Board outline | 23.5 mm × 15.8 mm | Edge.Cuts / README |
| Thickness | 1.2 mm (thinner than standard 1.6 mm) | PCB + README |
| Mounting | 4× M2 | README |
| Contacts | BWCD spring contacts `C2826546-BWCD-L4.5W2.0H2.3` (U1–U10); mating pads U11–U20 | V1.4 BOM / positions |
| Layout | 5 × 2 grid, **2.54 mm** pitch | `production/positions.csv` |
| Span | 10.16 mm × 2.54 mm | Derived from positions |
| Orientation | Silkscreen notch on V1.4 | 2026-Update note |
| Aircraft cable | Molex **2077601281** (12-pin) on board; mating housing **204523-1201** | Attach README / harness guide |

#### Pogo pad coordinates (relative to U1)

Extracted from `src/pcb/attach_pcb/production/positions.csv` (Mid X/Y). Origin = U1. Units mm. Net names are as labeled on the **attach PCB** (see [§3](#3-electrical-contract) for vehicle-side corrections).

| Ref | Net (attach PCB) | X | Y |
| --- | --- | ---: | ---: |
| U1 | ETH_RX+ | 0.00 | 0.00 |
| U2 | 12VSW | 0.00 | 2.54 |
| U3 | ETH_RX− | 2.54 | 0.00 |
| U4 | GND | 2.54 | 2.54 |
| U5 | ETH_TX+ | 5.08 | 0.00 |
| U6 | +12V | 5.08 | 2.54 |
| U7 | ETH_TX− | 7.62 | 0.00 |
| U8 | FMU_CH1 | 7.62 | 2.54 |
| U9 | CAN1_P | 10.16 | 0.00 |
| U10 | CAN1_N | 10.16 | 2.54 |

Absolute Mid coordinates in the KiCad project (for adapter-board work matching [#233](https://github.com/Arrow-air/project-quiver/issues/233)): U1 = (105.18, −130.50) mm through U10 = (115.34, −127.96) mm.

### 2.3 Mass guidance

Empty weight and battery mass are published in the [Dev-Kit Engineering Report — Weight & Payload Summary](../Engineering-Reports/Dev-Kit-Engineering-Report.md#weight--payload-summary) (closes the weigh-in request from [#209](https://github.com/Arrow-air/project-quiver/issues/209)):

| Configuration | Battery | Battery mass | Empty weight | AUW | Payload capacity |
| --- | --- | ---: | ---: | ---: | ---: |
| Standard | 20 Ah LiPo (14S) | 7.90 kg | 9.65 kg | 17.55 kg | **7.45 kg** |
| Long endurance | 30 Ah LiPo (14S) | 11.40 kg | 9.65 kg | 21.40 kg | **3.95 kg** |
| MTOW limit | — | — | — | **25.00 kg** | — |

Empty weight excludes the battery and includes the shipped Dev-Kit sensor set. Payload capacity = MTOW − empty − battery. Keep attachment mass inside the selected configuration's capacity and leave margin for CG and structural unknowns ([§2.1](#21-quick-release-plate)).

### 2.4 Mounting and orientation

- Align the V1.4 orientation notch with the quick-release plate.
- Route the harness so the side-facing cable exit on PT3 plates is not pinched ([PT3 Engineering Report](../Engineering-Reports/PT3-Engineering-Report.md)).
- Bottom port is the usual home for high-mass or spinner/dispenser equipment; sides for sensors and cameras with smaller envelopes.
- Do not block propeller arcs, landing gear, or SIYI antenna clearances.

---

## 3. Electrical contract

> [!WARNING]
>
> **Version banner — V1.4 as built.** Pin tables and power limits below are traced to the manufactured Main PCB copper, Attach PCB V1.4, harness maps, and cited issues. When the interface is redesigned, update **this chapter** and leave the rest of the guide intact where possible.

### 3.1 Authority order when documents disagree

1. Main PCB copper nets (`Quiver_PT3_Main_PCB.kicad_pcb`)
2. Attach PCB V1.4 IPC / positions (`src/pcb/attach_pcb/production/`)
3. Main PCB Updates information note (CAN2 reassignment, J38 Ethernet)
4. Harness Manufacturing Guide (cable assembly)
5. Older information notes, silkscreen, and stale `.net` exports

Silkscreen on every Attach PCB labels the aux pin `FMU_CH1` and the CAN pair `CAN1_*`. That is **board artwork**, not the per-port vehicle net. Use the tables below.

### 3.2 Developer-facing Molex pinout (all ports)

Aircraft-side Molex **204523-1201** / board J1 **2077601281** (same signal set on the pogo array). Mapping from Attach README + harness guides, with vehicle corrections applied:

| Molex pin | Attach PCB net name | Vehicle meaning |
| ---: | --- | --- |
| 1 | ETH_RX+ | 100BASE-TX pair B+ (RX on payload) |
| 2 | 12VSW | Switched 12 V — **driven on bottom only**; NC on side port Main PCB pin 6 |
| 3 | ETH_RX− | Pair B− |
| 4 | 12VSW | Doubled with pin 2 |
| 5 | ETH_TX+ | 100BASE-TX pair A+ (TX on payload) |
| 6 | GND | Ground |
| 7 | ETH_TX− | Pair A− |
| 8 | GND | Ground (doubled) |
| 9 | CAN1_N | Vehicle **CAN2_L** |
| 10 | +12V / 12V_PL | Shared switched payload rail `+12V_PL` |
| 11 | CAN1_P | Vehicle **CAN2_H** |
| 12 | FMU_CH1 | Port-specific FMU aux — see [§3.3](#33-per-port-main-pcb-nets) |

Ethernet is **100BASE-TX, pairs A and B only** (four wires). There is **no GPS timepulse** line to any bay; use the aux FMU channel when you need a timing or trigger path ([#252](https://github.com/Arrow-air/project-quiver/issues/252) brief, confirmed by signal set on V1.4).

### 3.3 Per-port Main PCB nets

Verified from pad nets on `src/pcb/main_pcb/Quiver_PT3_Main_PCB.kicad_pcb` (authoritative). Aux → ArduPilot servo mapping from Pix32 / Pixhawk FMU convention and field confirmation in [#233](https://github.com/Arrow-air/project-quiver/issues/233) (`FMU_CH1` = AUX1 = **SERVO9**).

| Port | Power/signal | Pin 1 | Pin 2 | Pin 3 | Pin 4 | Pin 5 | Pin 6 | Aux servo | CAN bus |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Bottom C1 | J31 | GND | `+12V_PL` | `CAN2_L` | `CAN2_H` | `FMU_CH1` | `12VSW` | **SERVO9** | **CAN2** |
| Side 1 C2 | J29 | GND | `+12V_PL` | `CAN2_L` | `CAN2_H` | `FMU_CH7` | NC | **SERVO15** | **CAN2** |
| Side 2 C3 | J30 | GND | `+12V_PL` | `CAN2_L` | `CAN2_H` | `FMU_CH8` | NC | **SERVO16** | **CAN2** |

| Port | Ethernet connector | PCB nets (pairs) |
| --- | --- | --- |
| Bottom C1 | J39 | `ETH1_2B±`, `ETH1_2A±` |
| Side 1 C2 | J37 | `ETH1_3B±`, `ETH1_3A±` |
| Side 2 C3 | J38 | `ETH2_1B±`, `ETH2_1A±` |

#### Corrections vs common wrong sources

| Claim you may see | As-built fact | Prefer |
| --- | --- | --- |
| Attach silk: every port is `FMU_CH1` | Bottom `FMU_CH1`; Side 1 `FMU_CH7`; Side 2 `FMU_CH8` | Main PCB pads |
| HAR-0014 lists Molex 12 = `FMU_CH7` | Bottom Molex 12 = `FMU_CH1` | Main PCB J31 |
| Older Main info note / stale `.net`: J29/J31 on CAN1 | All three ports on **CAN2** | PCB pads + [Updates note](../../task-grant-bounty/pt3/electronics/0007-Main-PCB/Updates/information_note.md) (“all payloads will operate on CAN2”) |
| [#252](https://github.com/Arrow-air/project-quiver/issues/252) brief: J29+J31 on CAN1, only J30 on CAN2 | Superseded by as-built copper | PCB |
| Dev-Kit report: Ethernet on C1 and C2 only | J38 is wired on current Main PCB | PCB + Updates (“J38 wired to ethernet port 4”) |

> [!NOTE]
>
> **Open — Ethernet continuity.** Engineering Report text still says Ethernet on C1/C2 only while copper and Updates wire C3. Treat “all three ports carry Ethernet” as the design intent of the current Main PCB; confirm with a continuity check at the bench if your attachment depends on side-2 Ethernet.

### 3.4 CAN buses (safety)

| Bus | Typical use on Quiver | Bitrate (configured) |
| --- | --- | --- |
| **CAN1** | Flight-critical DroneCAN: ESCs, GNSS, Remote ID | 1 Mbit/s |
| **CAN2** | Payload ports (all three) + NanoRadar / obstacle sensors (RadarCAN) | Often 500 kbit/s for NanoRadar coexistence |

Attachment CAN pins land on **CAN2**, not CAN1. That keeps payload nodes off the ESC/GNSS bus — the important safety property. Still:

- Match bitrate and protocol to whatever already shares CAN2 on that aircraft (NanoRadar often needs 500 kbit; DroneCAN payload nodes must agree).
- Do not retie a payload onto CAN1 without an explicit aircraft redesign.
- Attach PCB labels `CAN1_P` / `CAN1_N` are historical names for the **vehicle CAN2** pair.

Sources: Main PCB Updates note; FC setup / firmware docs (CAN1 = ESCs + GNSS); Obstacle Avoidance notes (NanoRadar on CAN2); [#233](https://github.com/Arrow-air/project-quiver/issues/233) field notes (payloads on CAN2).

### 3.5 Power tree and limits

Traced in [#234](https://github.com/Arrow-air/project-quiver/issues/234) from Main PCB + Attach V1.4 (matches BOM part numbers):

```text
HV battery
  └─ PS2 RECOM REC30K-4812SZ  (HV → 12 V, 30 W / 2.5 A total aircraft 12 V)
        └─ F4 (5 A) → +12V   (also feeds SIYI air unit / other avionics)
              ├─ F8 1812L110 PTC (~1.1 A hold / ~2.2 A trip)
              │     └─ F7 (2 A) → U5 CPC1907B SSR → +12V_PL
              │           └─ shared by J29, J30, J31 pin 2
              │
              └─ K1 CPC1019N → F1 (2 A) → 12VSW → J31 pin 6 only

HV switched accessory (NOT on pogo array):
  HV+ → U4 CPC1907B → F2 (5 A) → J26
```

| Rail | Where | Limit (schematic / #234) | Notes |
| --- | --- | --- | --- |
| Aircraft `+12V` | Shared avionics | 30 W / 2.5 A from PS2 | SIYI and others already draw from this |
| Payload `+12V_PL` | All three ports | ~**13 W shared** (~1.1 A PTC hold) | One floodlight-class load can starve neighbors and the video link |
| `12VSW` | Bottom J31 only | 2 A fuse after SSR | FC-switched aux; still fed from the same 30 W converter upstream |
| J26 switched HV | Separate Main PCB connector | 5 A fuse; SSR ~3.5 A class continuous (verify datasheet); 14S up to 58.8 V | High-power path; CPC1907B blocks 60 V |

> [!NOTE]
>
> **Open — measured 12 V rail load test.** [#234](https://github.com/Arrow-air/project-quiver/issues/234) numbers are schematic traces; PTC thermal derating at temperature is unmeasured. Until a bench load test is recorded, publish these schematic limits and mark measured headroom as open.

### 3.6 What trips and what browns out

- **PTC F8 / fuse F7** trip or fold back when payload current on `+12V_PL` is too high — shared across ports, so one attachment can take down others.
- Saturating **PS2 (30 W)** browns out shared avionics. Field failure mode observed with dispenser work: SIYI video-link degradation when the 12 V domain is overloaded ([#233](https://github.com/Arrow-air/project-quiver/issues/233) / [#234](https://github.com/Arrow-air/project-quiver/issues/234)), not necessarily a clean fuse open.
- **`12VSW`** can be killed from the FC independently of `+12V_PL` (relay `P1 12V`).
- **J26 HV** can be killed via relay `Add HV` independently of PWM — use this for motors that must hard-stop.

High-power attachments (≥ ~13 W continuous, or any motor load that risks the shared rail) must use the **J26 HV path with local regulation**, not the pogo `+12V_PL` rail. See [#233](https://github.com/Arrow-air/project-quiver/issues/233) adapter pattern and [#234](https://github.com/Arrow-air/project-quiver/issues/234) options A–C (out of scope to resolve here).

---

## 4. Power budgeting

Budget every attachment against [§3.5](#35-power-tree-and-limits). Work the continuous current first, then inrush and shared-rail neighbors.

### 4.1 Logic payload (camera trigger, small MCU, DroneCAN node)

| Item | Budget |
| --- | --- |
| Path | `+12V_PL` via pogo (and/or local 5 V buck on the attachment) |
| Example draw | Matek CAN-L431 class node ~100 mA on 12 V ([#233](https://github.com/Arrow-air/project-quiver/issues/233)) |
| Fit | Comfortably inside ~1.1 A shared hold if neighbors are quiet |
| Control | Optional `12V Pay` relay for rail enable; CAN or Ethernet for data |

### 4.2 25 W floodlight

| Item | Budget |
| --- | --- |
| Path | **Cannot** run from `+12V_PL` (~13 W shared). Use **J26 switched HV** + onboard regulator, or wait for a future dedicated payload rail ([#234](https://github.com/Arrow-air/project-quiver/issues/234)) |
| Requirement context | [006 High Capacity Flood Light](../../task-grant-bounty/equipment/attachment/0002-detailed_attachment_requirement_for_bounty/006-High_Capacity_Flood_Light_comprehensive_requirement.md) already anticipates 12 V 2 A **or** 60 V external |
| Control | `Add HV` relay for power kill; CAN/analog for dimming per the requirement doc |

### 4.3 Granular dispenser (JMRRC FS2516 field path)

| Item | Budget |
| --- | --- |
| Spinner | Needs real current and, at 14S native, overheated the stock ESC — team ran **12 V** operation ([#233](https://github.com/Arrow-air/project-quiver/issues/233)) |
| Early path | `12VSW` on bottom J31 (FC kill retained); unloaded disc under 0.5 A @ 12 V |
| Shared-rail risk | Loading `+12V` / `12VSW` enough to stress PS2 → SIYI brownout risk; [#234](https://github.com/Arrow-air/project-quiver/issues/234) exists because this class of attachment outgrew the interface |
| Preferred high-power pattern | J26 HV → attachment-side buck → motor rail; logic/CAN node on `+12V_PL` |
| Signals | Speed PWM on bottom `FMU_CH1` / SERVO9; second actuator needed a spare AUX (J24 used in v1) because the interface exposes **one** aux per port |

---

## 5. Control and data paths

Pick the lightest path that meets the job.

| Path | When it is right | Port resources |
| --- | --- | --- |
| **PWM / GPIO aux** | One trigger, latch, ESC, or servo | One FMU channel per port ([§3.3](#33-per-port-main-pcb-nets)); default params often leave these as GPIO — see below |
| **DroneCAN node** | Multiple PWM/GPIO, telemetry, standard AP_Periph pattern | CAN2 pair on every port; [#233](https://github.com/Arrow-air/project-quiver/issues/233) Matek L431 reference |
| **Ethernet** | Cameras, LiDAR, Hub apps, high-rate data | 100BASE-TX on the pogo pairs; static IP in `.100`–`.199` |

### 5.1 PWM on the aux channel

Stock `SERVO_GPIO_MASK` in `docs/Operations/firmware/parameters/standard-params.param` is **65520**, which marks SERVO5–SERVO16 as GPIO. Mission Planner can show healthy `SERVOn` values while the pin stays flat 0 V — field bug found on the dispenser ([#233](https://github.com/Arrow-air/project-quiver/issues/233)).

To emit PWM on an attachment aux:

1. Identify the servo number for the port (9 / 15 / 16).
2. Clear that bit in `SERVO_GPIO_MASK` (and any other channels you need as PWM).
3. Set `SERVOn_FUNCTION` for the feature (or RC pass-through / script).
4. **Reboot** the flight controller.
5. Confirm with a scope or servo tester on the **pogo pin**, not only GCS feedback.

Example from dispenser bring-up: `SERVO_GPIO_MASK = 61168` cleared SERVO9 and SERVO13 while leaving the `12VSW` GPIO control intact ([#233](https://github.com/Arrow-air/project-quiver/issues/233)). Latch V1 at the August meetup used the same “clear the port’s GPIO bit” step ([#257](https://github.com/Arrow-air/project-quiver/issues/257) / T-11).

Narrative detail for SSR hierarchy and commissioning order lives in the Initial Configuration Guide (T-02 / [#249](https://github.com/Arrow-air/project-quiver/issues/249), §11 / §11.6) — not yet merged on `main` at the time of this guide. Until it lands, use this section plus the Pilot Handbook relay table.

### 5.2 DroneCAN

- Enumerate on **CAN2** at the aircraft’s CAN2 bitrate.
- Power the node from `+12V_PL` so it can come up before arming when that rail is enabled.
- Prefer AP_Periph (or equivalent) when you need multiple PWM outputs behind one connector — the interface only brings out one FMU wire ([#233](https://github.com/Arrow-air/project-quiver/issues/233)).

### 5.3 Ethernet and Hub

- Assign a static address in `192.168.144.100`–`192.168.144.199`.
- Recommended defaults: bottom `.100`, side 1 `.101`, side 2 `.102`. Side-port IPs should be configurable if the attachment can mount on either side ([Dev-Kit Engineering Report](../Engineering-Reports/Dev-Kit-Engineering-Report.md)).
- Path: payload pogo → Attach PCB → Molex harness → Main PCB Ethernet connector (J39/J37/J38) → GigaBlox Nano switches → companion computer / FC CubeNode.

Software APIs, widgets, and Hub pipelines: [SDK Developer Guide §9](./Quiver-SDK-Developer-Guide.md) — do not duplicate here.

---

## 6. Flight controller integration

### 6.1 Relay functions (Pilot Handbook §2.8.5)

Set Mission Planner relay labels before flight ([Pilot Handbook](../Operations/Pilot-Handbook.md)):

| Relay | Label | Attachment relevance |
| ---: | --- | --- |
| 1 | `SSR` | Main HV / motor power MOSFETs — auto-engage after boot |
| 2 | `Bypass` | Legacy; leave off on current Dev-Kit |
| 3 | `Add HV` | Enables **J26** additional HV output |
| 4 | `P1 Sig` | Bottom payload GPIO / signal path |
| 5 | `P1 12V` | Bottom **`12VSW`** enable |
| 6 | `12V Pay` | General **`+12V_PL`** enable to attachment interfaces |

Labels are operator aids; they do not rewire the aircraft.

### 6.2 SSR / power timing (hierarchy)

Conceptual order for attachment power (aligns with Pilot Handbook power-up and the configuration guide §11 SSR discussion once merged):

1. Aircraft avionics power and FC boot.
2. Main `SSR` (Relay 1) closes — propulsion HV domain ready.
3. Enable `12V Pay` when the attachment needs `+12V_PL`.
4. Enable `P1 12V` only if the bottom attachment needs `12VSW`.
5. Enable `Add HV` only if using J26.
6. Arm motors only after payload rails and failsafes are understood.

Do not open the main SSR under load as a routine payload control — see Pilot Handbook cautions around SSR state and companion/attachment draw through pre-charge paths.

### 6.3 Servo outputs and arming

| Port aux | Servo | Typical use |
| --- | ---: | --- |
| Bottom `FMU_CH1` | 9 | Trigger, latch, spinner, camera shutter |
| Side 1 `FMU_CH7` | 15 | Side attachment PWM |
| Side 2 `FMU_CH8` | 16 | Side attachment PWM |

Related Main PCB controls (not on the pogo, but part of attachment power):

| Net | Role |
| --- | --- |
| `FMU_CH4` → U5 | `+12V_PL` SSR |
| `FMU_CH2` → K1 | `12VSW` SSR |
| `IO_CH7` → U4 | J26 HV SSR |

Arming interactions are attachment-specific (example: ArduPilot Sprayer left spinner PWM unset until first sprayer-on, so a JMRRC ESC never armed mid-mission — [#233](https://github.com/Arrow-air/project-quiver/issues/233)). Document your arming/failsafe behavior in the attachment note; do not assume PWM is live merely because the aircraft is armed.

---

## 7. Software handoff

This page stops where the Hub and companion stack start. Read, in order:

1. **This guide** — mechanical + electrical contract, FC parameters for the port.
2. **[Quiver SDK Developer Guide](./Quiver-SDK-Developer-Guide.md)** — network, companion services, Hub REST/Socket.IO, custom payload apps (§9).
3. **Org repositories** (Arrow-air):
   - [`quiver-sdk`](https://github.com/Arrow-air/quiver-sdk) — Python SDK
   - [`quiver-payload-template`](https://github.com/Arrow-air/quiver-payload-template) — starting point for a payload app
   - [`payload-systems`](https://github.com/Arrow-air/payload-systems) — open payload designs

### Network addresses for payload developers

| Role | Address | Notes |
| --- | --- | --- |
| Payload range | `192.168.144.100`–`.199` | Developer-assigned static |
| Bottom port default | `.100` | Fixed recommendation |
| Side defaults | `.101` / `.102` | Make configurable if dual-side |
| Flight controller | `.51` | |
| Companion Pi | `.49` | Corrected target per [#252](https://github.com/Arrow-air/project-quiver/issues/252) |
| CubeNode ETH | `.50` | Corrected target per [#252](https://github.com/Arrow-air/project-quiver/issues/252) |

> [!NOTE]
>
> **Address table sync.** Published SDK guide and Dev-Kit Engineering Report on `main` still list CubeNode `.10` and Pi `.50`. [#252](https://github.com/Arrow-air/project-quiver/issues/252) directs attachment authors to use CubeNode `.50`, Pi `.49`, FC `.51` once the repo sync lands. Prefer the corrected values above for new attachments; avoid SIYI-reserved addresses (`.11`, `.12`, `.20`, `.25`, `.60`). Cite the sync PR in this note when it merges.

---

## 8. Validation

### 8.1 Bench checklist (standalone)

Use this list alone before first flight. Aircraft powered per Pilot Handbook avionics sequence; motors disarmed; props removed or secured.

**Identity**

- [ ] Port selected (bottom / side 1 / side 2) recorded.
- [ ] Mechanical fit: orientation notch, latch closed, cable strain relieved.

**Power**

- [ ] Expected rail documented: `+12V_PL`, `12VSW`, and/or J26 HV.
- [ ] Continuous current estimate ≤ schematic limit ([§3.5](#35-power-tree-and-limits)); shared-rail neighbors considered.
- [ ] With rail enabled, measure attachment current (clamp or series meter).
- [ ] Measure rail voltage at the attachment under load — no sag into brownout territory for SIYI / other avionics.
- [ ] Kill path works: `12V Pay` / `P1 12V` / `Add HV` as applicable removes power.

**Aux / PWM**

- [ ] `SERVO_GPIO_MASK` bit cleared for the port’s servo; FC rebooted.
- [ ] Scope or tester on the **pogo aux pin** shows the expected pulse train (not only GCS `SERVOn`).
- [ ] Endpoints calibrated after any intermediary PCB bypass.

**CAN**

- [ ] Node appears on **CAN2** at the configured bitrate.
- [ ] No unexpected bus errors; NanoRadar / other CAN2 devices still healthy if installed.

**Ethernet**

- [ ] Link light / `ping` to the assigned `.100`–`.199` address from the companion network.
- [ ] Hub or local service receives the intended stream (if applicable).

**Regression**

- [ ] SIYI video/telemetry still healthy under attachment load.
- [ ] FC has no new pre-arm errors introduced by the attachment params.

### 8.2 Flight rules

- Complete [§8.1](#81-bench-checklist-standalone) before armed flight with the attachment.
- Stay inside MTOW and the selected battery configuration’s payload capacity ([§2.3](#23-mass-guidance)).
- Brief the pilot on which relays arm payload power and how to hard-kill the attachment.
- Log the flight; note any link drop, rail sag, or actuator fault for the attachment information note.
- High-voltage pigtails (J26) are not hot-swap casual — connect before enabling `Add HV`.

---

## 9. Lessons learned

Sources: August meetup scope in [#257](https://github.com/Arrow-air/project-quiver/issues/257) / [#253](https://github.com/Arrow-air/project-quiver/issues/253) / [#254](https://github.com/Arrow-air/project-quiver/issues/254); dispenser field thread [#233](https://github.com/Arrow-air/project-quiver/issues/233); power truth [#234](https://github.com/Arrow-air/project-quiver/issues/234). Formal latch and multispectral information notes are T-11 ([#257](https://github.com/Arrow-air/project-quiver/issues/257)) — until those merge, treat the bullets below as the authoritative short form.

### 9.1 Servo latch (August meetup V1)

- Aux pins had to move from GPIO to PWM (`SERVO_GPIO_MASK` bit for the port).
- Regulate **12 V → 6 V** on the payload side for the servo.
- Housing by Alperen; exercised with cans and a first-aid kit.
- A late open/close fault traced to a twisted pin linkage on the PWM tester (straightened); dust also suspected.
- V2 tracking: [#254](https://github.com/Arrow-air/project-quiver/issues/254) (opens from the V1 note).

### 9.2 Multispectral camera (August meetup V1)

- Clean power on the interface plus a **native PWM trigger** on the port aux.
- USB power configuration on Alperen’s mount.
- Ground tested, then flown on Gray’s Quiver at the meetup — field usable, components exposed.
- V2 tracking: [#253](https://github.com/Arrow-air/project-quiver/issues/253).

### 9.3 Starlink Mini

- High-voltage feed through a regulator ([#252](https://github.com/Arrow-air/project-quiver/issues/252) brief).
- Unresolved link-drop behavior — **do not copy as a finished pattern**; document measurements if you repeat the experiment.
- No merged information note yet beyond this one-line record.

### 9.4 JMRRC FS2516 dispenser (field)

| Lesson | Takeaway |
| --- | --- |
| Stock door-channel PCB corrupted/blocked clean 3.3 V PWM | Bypass intermediary electronics; wire actuators direct; recalibrate endpoints |
| Shared / switched 12 V domain is easy to overload | Move motor power to **J26 HV + local regulation**; keep logic on `+12V_PL` |
| `SERVO_GPIO_MASK` hides PWM failures | Always verify on the pin |
| Sprayer/ESC arming handshake | Pulse timing matters; ground-cycle actuators before takeoff if the device needs an arm dwell |
| 14S into the stock ESC | Thermal shutdown under spin; 12 V operation was the interim choice |
| Adapter pattern | Matek L431 AP_Periph on CAN2, dual PWM + GPIO, single sealed connector — [#233](https://github.com/Arrow-air/project-quiver/issues/233) |

Long-term path discussed in-thread: open-source Arrow dispenser with zero JMRRC electronics content.

---

## Appendix A — Open engineering questions

| Topic | State | Owner / source |
| --- | --- | --- |
| Measured `+12V_PL` load / PTC derating | Schematic ~13 W only | Bench test requested with [#252](https://github.com/Arrow-air/project-quiver/issues/252) |
| Hot-swap live-mate rules | Design intent only | Erick / bench |
| Side vs bottom structural ratings | Unpublished | Alperen / FEA |
| Ethernet on C3 continuity | Copper yes; some docs say no | Bench continuity |
| Network address sync (Pi `.49`, CubeNode `.50`) | Directed by [#252](https://github.com/Arrow-air/project-quiver/issues/252); docs on `main` still older | Sync PR when merged |
| Interface power redesign | Options in [#234](https://github.com/Arrow-air/project-quiver/issues/234) | Out of scope for this guide |
| Adapter board hardware | [#233](https://github.com/Arrow-air/project-quiver/issues/233) | Out of scope for this guide |
| Latch / multispectral full notes | T-11 [#257](https://github.com/Arrow-air/project-quiver/issues/257) | Erick |

Open items are **not** requirements.

## Appendix B — Source index

| Source | Role |
| --- | --- |
| `src/pcb/attach_pcb/` V1.4 | Pogo geometry, Molex nets, BOM |
| `src/pcb/main_pcb/Quiver_PT3_Main_PCB.kicad_pcb` | Per-port nets (authoritative) |
| [`0003-Attachment-Interface-PCB`](../../task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB/) | History, README pin tables, V1.4 note |
| [`0007-Main-PCB/Updates`](../../task-grant-bounty/pt3/electronics/0007-Main-PCB/Updates/information_note.md) | CAN2 for all payloads, J38 Ethernet |
| [Harness Manufacturing Guide](../Manufacturing/Harness-Manufacturing-Guide.mdx) | HAR-0012/13/14 |
| [#233](https://github.com/Arrow-air/project-quiver/issues/233) | Adapter pattern, dispenser lessons, SERVO9 / GPIO mask |
| [#234](https://github.com/Arrow-air/project-quiver/issues/234) | Power tree numbers |
| [Pilot Handbook §2.8.5](../Operations/Pilot-Handbook.md) | Relay labels |
| [Dev-Kit Engineering Report](../Engineering-Reports/Dev-Kit-Engineering-Report.md) | Weights, network, attach PCB summary |
| [SDK Developer Guide](./Quiver-SDK-Developer-Guide.md) | Software |
| [`0002-*` attachment requirements](../../task-grant-bounty/equipment/attachment/0002-detailed_attachment_requirement_for_bounty/) | Demand-side context |
