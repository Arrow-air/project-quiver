# Quiver Attachment Developer Guide — Chapters 1–3 (M1 draft)
*Versioned to QuiverAttachPCB V1.4 as built. Draft for T-05 M1 review.*

> **Trace convention:** every electrical claim in this draft carries a source tag:
> `[NET]` = main-PCB production netlist ([src/pcb/main_pcb/production/netlist.ipc](../../src/pcb/main_pcb/production/netlist.ipc)),
> `[ISSUE-233]` = [the adapter-board issue](https://github.com/Arrow-air/project-quiver/issues/233),
> `[ISSUE-234]` = [the power-delivery issue](https://github.com/Arrow-air/project-quiver/issues/234),
> `[ICD]` = the payload-systems interface control document ([ICD.md](https://github.com/Arrow-air/payload-systems/blob/main/interface/ICD.md)),
> `[PH-2.8.5]` = Pilot Handbook §2.8.5 (docs/Operations/Pilot-Handbook.md).

## Chapter 1 — What a Quiver attachment is

A Quiver attachment is a self-contained payload module that mates to the aircraft through
one of three identical contact groups (bottom port J31, side port 1 J29, side port 2 J30).
All three groups are electrically identical [NET: identical pin nets, differing only in the
aux PWM signal — see Chapter 3] and mechanically mirrored (J29/J30 are mirrored placements
of the same pad layout [NET: mirrored pad coordinates]).

The attachment interface provides per port: +12 V payload power, an aux PWM signal, a CAN
bus pair, and (on the bottom port only) a switched 12 V auxiliary rail. High-power payloads
are served by the HV battery taps on the main PCB (Chapter 3), not by the attachment ports.

Hot swap: the interface is designed for attachment change without reboot; the SSR-controlled
rails engage after mating (the Quiver SSR auto-engage Lua script [PH-2.8.5]).

## Chapter 2 — Mechanical interface

### 2.1 Contact array geometry (extracted from QuiverAttachPCB V1.4 KiCad, this repository)

The interface array is ten spring contacts (C2826546-BWCD, Mill-Max-style pogo springs) in
two rows of five, on a 2.54 mm grid — the "two mirrored 2×5 contact groups, 2.54 mm pitch"
of the V1.4 interface [ISSUE-233].

Board coordinates (mm, KiCad Y-down, footprint centres; source: QuiverAttachPCB.kicad_pcb,
this repository, V1.4 as built):

| Contact | Row 1 (y = 127.96) | Row 2 (y = 130.50) |
|---|---|---|
| Column 1 | U2 (105.18) | U1 (105.18) |
| Column 2 | U4 (107.72) | U3 (107.72) |
| Column 3 | U6 (110.26) | U5 (110.26) |
| Column 4 | U8 (112.80) | U7 (112.80) |
| Column 5 | U10 (115.34) | U9 (115.34) |

- X pitch: 2.54 mm exactly (column centres). Y pitch between rows: 2.54 mm.
- All contacts are mounted at −90° rotation.
- Each spring contact carries four signal pads (doubled per signal, at ±0.5525 mm X and
  ±0.55 mm Y off the contact centre) plus a 0.6 mm centre pad and a 0.2×0.1 mm offset pad
  — the "doubled per signal" redundancy noted in #234.
- Payload-side landing plates: ten 2×2 mm pads (U11–U20) at y = 135.50 / 138.04, x-pitch
  2.54 mm, mirrored below the contact rows — these are the plates a payload's own PCB
  presents to the spring tips.

Coordinates above are the absolute board placement from the V1.4 KiCad source in this
repository — no second-hand extraction is involved.

### 2.2 Envelope, mounting, and orientation
- The interface area is centered at x ≈ 110.26 mm; the array spans 105.18–115.34 mm
  (10.16 mm wide) and 127.96–130.50 mm (2.54 mm deep), with the landing plates 5.0–5.5 mm
  further along −Y.
- Orientation is agnostic by design: J29 and J30 are mirrored placements of the same pad
  layout, so the payload lands either way [ISSUE-233].
- Mass guidance: no published payload mass limit exists yet (T-05 gap table — "no ratings
  anywhere"); marked pending bench/FEA analysis. Handle conservatively until a number is
  published.
- Mass guidance: no published payload mass limit exists yet (T-05 gap table — "No ratings
  anywhere"). Marked pending bench/FEA analysis; conservative handling until a number is
  published.

## Chapter 3 — Electrical contract

### Per-port pin table (from the production netlist, J-pins as built)

| Port | Pin 1 | Pin 2 | Pin 3 | Pin 4 | Pin 5 | Pin 6 |
|---|---|---|---|---|---|---|
| J31 (bottom) | GND | +12V_PL | CAN2_L | CAN2_H | FMU_CH1 | /12VSW |
| J29 (side 1) | GND | +12V_PL | CAN2_L | CAN2_H | FMU_CH7 | (TED pad 6) |
| J30 (side 2) | GND | +12V_PL | CAN2_L | CAN2_H | FMU_CH8 | (TED pad 6) |

[NET: netlist records `327... J31 -1..-6`, `327... J29 -1..-6`, `327... J30 -1..-6` —
see netlist_port_pins.txt for the full records with pad coordinates.]

**Correction against the T-05 brief:** the brief states "the bottom and side 1 ports sit on
CAN1, the flight critical bus, and only side 2 is on CAN2." The production netlist shows
**all three ports on CAN2_L/CAN2_H**. No attachment port carries CAN1. This correction is
the single most consequential claim in M1: a payload node on CAN2 does not share the bus
with the ESCs, GNSS, or RemoteID; the CAN1 flight-critical bus is not exposed to payloads
at the attachment interface. (CAN1_H/CAN1_L exist in the netlist as internal nets only.)

**Second source — the payload-systems ICD** (Arrow-air/payload-systems,
`interface/ICD.md`, main branch): the capability table reads
"**CAN2 (DroneCAN)** — ✓ (bottom J31) — ✓ (side 1 J29) — ✓ (side 2 J30)" and the pin
table carries the note "**CAN2_H (labelled CAN1_P on board)** / **CAN2_L (labelled
CAN1_N on board)**" — the board silkscreen mislabels the CAN2 pair as CAN1, which is the
root cause of the brief's error. Two independent sources (production netlist + ICD) agree:
**all three attachment ports are CAN2 / DroneCAN**.

**Design consequence:** a DroneCAN payload node (e.g. the #233 Matek CAN-L431 running
AP_Periph) can be enrolled on any of the three ports without touching the flight-critical
CAN1 bus. The network plan is: attachment node on CAN2 at 500 kbit/s alongside the two
NanoRadar sensors; static IP or DroneCAN for network payloads per the ICD's network section.

### Aux PWM per port
- Bottom J31: FMU_CH1 — ArduPilot servo output 9 [NET: `327/FMU_CH1 J31 -5`]
- Side 1 J29: FMU_CH7 — ArduPilot servo output 15 [NET: `327/FMU_CH7 J29 -5`]
- Side 2 J30: FMU_CH8 — ArduPilot servo output 16 [NET: `327/FMU_CH8 J30 -5`]
[ISSUE-233/T-05 brief: "the aux signal is FMU_CH1 on the bottom port but FMU_CH7 and
FMU_CH8 on the side ports (servo outputs 9, 15, 16)"] ✓ netlist-confirmed.

### Power rails per port
- `+12V_PL`: shared across all three ports [NET: +12V_PL on J31-2, J29-2, J30-2].
  Source chain: PS2 RECOM REC30K-4812SZ (HV→12 V, 30 W / 2.5 A) → F4 (5 A) → +12V →
  F8 (PTC 1812L110, ~1.1 A hold / ~2.2 A trip) → F7 (2 A fuse) → U5 (CPC1907B SSR) →
  +12V_PL [ISSUE-234: full trace]. Effective shared attachment power ≈ 13 W across
  three ports [ISSUE-234].
- `12VSW` (switched aux, CPC1019N + 2 A fuse): bottom port J31 pin 6 only [NET:
  `327/12VSW J31 -6`] [PH-2.8.5: relay `P1 12V` "Enables the separate 12 V supply for
  the bottom payload port"].
- High-power attachments: use the main-PCB HV battery taps (XT60, HV+/HV− at
  J25/J28/J34/J42 [ISSUE-234]) through the attachment-side regulator pattern of the
  #233 adapter design. The attachment pogo contacts themselves carry only the low-power
  rails; the HV path is a separate connector/pigtail, not through the pogo array
  [ISSUE-233: "Power path: XT60 pigtail from an HV tap"].

### Trips and brown-outs (what trips and what browns out)
- The shared PTC (1812L110) trips at ~2.2 A on the +12V_PL rail; a >1 A 12 V attachment
  can nuisance-trip it and brown out neighbors on the shared rail [ISSUE-234].
- The 30 W PS2 source saturates if the SIYI air unit plus attachments exceed its budget
  [ISSUE-234].
- High-power attachments on the HV tap must regulate locally; the JMRRC dispenser
  browned out on the switched 12 V line and moved to HV [T-05 field lessons].

### Hot-swap and SSR power timing
- Relay `SSR` (relay 1) auto-engages after boot via the Quiver SSR auto-engage Lua
  script [PH-2.8.5].
- Relay `12V Pay` (relay 6) gates the general 12 V payload supply to the attachment
  interfaces [PH-2.8.5].
- Relay `P1 Sig` (relay 4) drives the bottom-port GPIO/payload logic signal [PH-2.8.5].
- Open question (needs Erick/bench): whether attachments may be connected or removed
  powered, and what the rails do across arm/disarm/kill — the T-05 gap table marks this
  "design intent from Erick, confirmed at the bench."
