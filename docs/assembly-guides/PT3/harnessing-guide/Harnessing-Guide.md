# Main PCB & Battery Control PCB Wiring Harness Manufacturing Guide

## Purpose

This guide explains how to manufacture and assemble the wiring harnesses for both:

- The **Main PCB**, which handles core avionics and power distribution.
- The **Battery Control PCB (BC_PCB)**, which interfaces with the Main PCB and pushbutton systems.

Use the following wiring table for all of the connections TO/FROM for all of PT3’s systems: https://docs.google.com/spreadsheets/d/1INDpDhqC1wYGbbJhMCmYZ-2Rzxx5Ob4zoG5JTc_2Sps/edit?gid=2139598833#gid=2139598833

---

## Wire Harnessing Scope

| PCB Section | Description |
| --- | --- |
| **Main PCB** | Routes power, data, and control signals to all subsystems |
| **BC_PCB** | Routes battery HV signals, pushbutton I/O, CAN/I2C |

---

## Materials Required

- **Wires:**
    - 26 AWG silicon
    - 20 AWG silicon
    - 6 AWG silicone (HV power)
- **Crimp Tools**
    - Engineer PA-09
        - JST-GH and Molex Micro-Lock compatible
    - Hex die pneumatic crimper
        - Amass connector crimp compatible
- Wire Stripper
- Wire Cutter

---

## Main PCB Connectors & Housing

Eurostyle Plug

| Connector | Mating Housing | Crimp Required |
| --- | --- | --- |
| `39511-1004` | `39510-0004` | No |
| `39511-1005` | `39510-0005` | No |

### JST Connectors & Housings (1.25mm GH Series)

| Connector | Mating Housing | Crimp Required | Crimp Type |
| --- | --- | --- | --- |
| `SM03B-GHS-TB(LF)(SN)` | `GHR-03V-S` | Yes | `SSHL-002T-P0.2` |
| `SM04B-GHS-TB(LF)(SN)` | `GHR-04V-S` | Yes | `SSHL-002T-P0.2` |
| `SM05B-GHS-TB(LF)(SN)` | `GHR-05V-S` | Yes | `SSHL-002T-P0.2` |
| `SM06B-GHS-TB(LF)(SN)` | `GHR-06V-S` | Yes | `SSHL-002T-P0.2` |
| `SM09B-GHS-TB` | `GHR-09V-S` | Yes | `SSHL-002T-P0.2` |

### Molex Connector

| Connector | Mating Housing | Crimp Required | Crimp Type |
| --- | --- | --- | --- |
| `207760-1281` | `204523-1201` | Yes | `2145291000` |

### Phoenix Contact Terminal Blocks

| Connector | Mating Connector | Position |
| --- | --- | --- |
| `1814922` | `1704854` | 3 |
| `1814935` | `1704857` | 4 |
| `1839211` | `1704857` | 4 (vertical) |
| `1814948` | `1704858` | 5 |
| `1814951` | `1704859` | 6 |
| `1778735` | `1704859` | 6 (vertical) |
| `1814964` | `1704860` | 7 |

### Power Connectors

| Female | Male | Crimp Required | Crimp Type |
| --- | --- | --- | --- |
| `XT60PW-F` | `XT60-M` | No | N/A |
| `XT30PW-F` | `XT30-M` | No | N/A |
| `LCB60PB-M` | `LCB60-F` | Yes | 91021-F.S |

### Other Parts

- Pushbutton: `PVHC4F23SS344`
- Compression Lug: `7461097` (M6, 180A)

---

## Manufacturing Instructions

### 1. Wire Cutting

- Cut wires to specified lengths (in cm) from the wiring table.
- No strain relief required since the lengths do not take the connectors into account and some lengths were rounded up.

### 2. Crimping

- Strip approximately 2 mm of insulation for 20 - 26 AWG cables
- Strip approximately 9 mm of insulation for 6 AWG cables
    - Do not double crimp and apply heat shrink if necessary
- Use appropriate crimp tool for terminals
- Verify both conductor and insulation are captured securely.

### 3. Connector Assembly

- Insert crimped wires into JST, Molex, or Phoenix housings per the wiring diagram.
- Match **pin numbers** at both ends of the cable using the table.
- Ensure proper keying and orientation

### 4. Continuity Testing

- Perform multimeter continuity checks for each wire.
- Verify no shorts or open wires exist.

### 5. Harness Bundling

- Use mesh sleeving, zip ties, and cable clips.
- Route for minimal EMI, avoiding parallel runs of HV and signal cables.

---

## Wire Color Coding Reference

| Signal Type | Examples | Color |
| --- | --- | --- |
| Ground | `GND`, `HV-` | Black |
| 5V Power | `VDD_5V_*`, `5V` | Gray |
| 12V Power | `12V`, `12V_PL`, `12VSW` | Red |
| CAN High | `CAN1_H`, `CAN2_H` | Green |
| CAN Low | `CAN1_L`, `CAN2_L` | Gray |
| UART TX | `UART*_TX_*` | White |
| UART RX | `UART*_RX_*` | Pink |
| Ethernet RX+/- | `ETH_RX+`, `ETH_RX-` | White / Orange |
| Ethernet TX+/- | `ETH_TX+`, `ETH_TX-` | Grey / Green |
| Digital IO | `IO_*`, `FMU_CH*` | Blue |
| HV Battery + | `HV+` | Red |
| HV Battery - | `HV-` | Black |

---

## Final Checklist (Main + BC_PCB)

- [ ]  All wires cut to correct length
- [ ]  Crimps tight and in correct connector housing
- [ ]  Pinout and polarity verified on both PCBs
- [ ]  Continuity testing passed for all connections
- [ ]  HV wires securely lugged and insulated
- [ ]  Harnesses neatly bundled and strain-relieved
