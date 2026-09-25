# Quiver Attachment Developer Guide

*Version: 1.0 – September 2026*  
*Target audience: Third‑party hardware developers building payloads that plug into a Quiver aircraft.*

---

## Table of Contents

1. [Overview](#overview)  
2. [Mechanical Interface](#mechanical-interface)  
3. [Electrical Interface](#electrical-interface)  
   - 3.1 [Power Rails & Limits](#power-rails--limits)  
   - 3.2 [Signal Set](#signal-set)  
   - 3.3 [Connector Pin‑out](#connector-pin-out)  
4. [Software Integration](#software-integration)  
   - 4.1 [DroneCAN / UAVCAN](#dronecan--uavcan)  
   - 4.2 [Quiver Hub API](#quiver-hub-api)  
   - 4.3 [Payload‑Systems ICD](#payload-systems-icd)  
5. [Testing & Validation](#testing--validation)  
6. [References](#references)  

---

## Overview

A Quiver attachment is a **plug‑in payload module** that connects to the aircraft via a standardized **Pogo‑pin array** and a **Molex 6‑pin power/communication connector**. The attachment must:

* **Physically mount** securely without interfering with the airframe.  
* **Electrically interface** without exceeding the aircraft’s power budget or causing brown‑outs.  
* **Communicate** with the flight controller (FC) and the ground‑station Hub using the Quiver SDK / DroneCAN protocol.

All required specifications are defined in the following sources:

| Source | Description |
|--------|-------------|
| Issue #233 | Pogo array geometry, signal set, HV battery taps, DroneCAN adapter board pattern |
| Issue #234 | Power truth – 12 V payload rail, 12VSW, HV switched path |
| `src/pcb/attach_pcb/` | KiCad V1.4 attachment PCB (gerbers in `production/`) |
| `src/pcb/main_pcb/Quiver_PT3_Main_PCB.net` | Netlist for the main aircraft PCB |
| `docs/Archive/Dev-Kit-Guides/Quiver-SDK-Developer-Guide.md` | SDK usage and message definitions |
| Payload‑Systems ICD (internal) | Logical interface contract (referenced in the SDK guide) |

---

## Mechanical Interface

### 1. Pogo‑Pin Array

* **Location** – Bottom side of the attachment port (see the schematic in `src/pcb/main_pcb/Quiver_PT3_Main_PCB.net`).  
* **Pitch** – 2.54 mm (0.1 in) grid, 8 pins total.  
* **Pin Types** – 4 power pins, 4 signal pins (see the table in **Signal Set**).  
* **Mounting** – The attachment PCB must have a **4‑hole M3 pattern** (Ø 3 mm) that aligns with the aircraft’s mounting bosses. Hole locations are defined in the KiCad file `src/pcb/attach_pcb/attach_pcb.kicad_mod`.

### 2. Power/Comm Connector

* **Connector** – Molex 6‑pin (part # 22‑23‑2061).  
* **Orientation** – Keyed; the notch faces the forward direction of the aircraft.  
* **Cable** – Use the supplied **shielded twisted‑pair** for CAN and a **2‑wire 12 V** pair for power.  

> **Tip:** Verify the connector keying by inserting a test board before final assembly.

---

## Electrical Interface

### Power Rails & Limits

| Rail | Nominal Voltage | Max Current | Notes |
|------|-----------------|-------------|-------|
| **12V Payload** | 12 V (typ. 13 V under load) | **13 W total** across *all three* attachment ports | Shared bus – each port may draw up to **1 A** (≈12 W) but the sum of all ports must stay ≤ 13 W. |
| **12VSW** | 12 V (switched) | 2 A (bottom port only) | Used for high‑power payloads that need a dedicated switched rail. |
| **HV Battery Tap** | 22 V (raw) | 0.5 A (max) | For payloads that require direct battery voltage (e.g., Li‑Po charger). Must be **isolated** via the on‑board MOSFET (see KiCad). |
| **GND** | Common ground | – | All grounds are tied together on the main PCB. |

> **Important:** Do **not** exceed the 13 W total payload budget. Over‑current will trigger the aircraft’s protection circuit and cause a brown‑out.

### Signal Set

| Pin | Function | Protocol | Default State |
|-----|----------|----------|---------------|
| **P1** | CAN‑H | DroneCAN (UAVCAN) | High‑Z |
| **P2** | CAN‑L | DroneCAN (UAVCAN) | High‑Z |
| **P3** | UART_TX | Optional debug UART | High‑Z |
| **P4** | UART_RX | Optional debug UART | High‑Z |
| **P5** | PWM_OUT | PWM control (e.g., servo) | 0 V |
| **P6** | GPIO_IN | General‑purpose input | Pull‑down |

The **CAN bus** is the primary communication channel. All payloads must implement the **DroneCAN node** defined in the Quiver SDK (see the SDK guide). UART and PWM are optional but must be left un‑driven if not used.

### Connector Pin‑out

