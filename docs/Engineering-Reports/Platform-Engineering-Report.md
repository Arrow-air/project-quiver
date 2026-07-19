---
title: Platform Engineering Report
sidebar_position: 5
description: Source-traceable engineering reference for the current Project Quiver Dev-Kit platform
---

# Project Quiver Platform Engineering Report

| Field | Value |
|---|---|
| Platform | Project Quiver Dev-Kit |
| Report type | Whole-platform engineering reference |
| Evidence cut | 19 July 2026 |
| Repository baseline | `Arrow-air/project-quiver` `main` |
| Intended readers | Designers, builders, maintainers, operators, and payload developers |

## Executive Summary

Project Quiver is an open-source, modular, heavy-lift quadcopter platform with an intended maximum takeoff weight (MTOW) of 25 kg. The current Dev-Kit configuration combines a folding aluminum and carbon-fiber airframe, four Hobbywing XRotor X6 Plus G2 propulsion units, a Tattu 4.0 14S 30 Ah battery, a Pix32 v6 flight controller, four custom PCB types, three quick-release payload interfaces, a Raspberry Pi 5 companion computer, and CAN, serial, and Ethernet communications.

The repository contains substantially more than a concept design: generated CAD, PCB source and production files, a structured bill of materials (BOM), assembly and harnessing instructions, a custom ArduCopter firmware build, parameter layers, operating and maintenance guidance, and payload-integration documentation. Earlier prototype reports also preserve the design rationale from PT1 through PT3, while the [Dev-Kit Engineering Report](./Dev-Kit-Engineering-Report.md) records the changes made for the current developer release.

The available evidence does **not**, however, support treating every published capability as production- or flight-validated. The most recent project status report records a propellers-off ground run on 29 June 2026, not a first flight. Remote ID, backup GNSS acquisition, in-flight LiDAR continuity, DroneCAN ESC reliability, and onboard logging were still open flight-readiness items. Endurance and payload figures remain calculations or uncompleted test objectives rather than a closed flight-test envelope.

This report therefore serves two purposes:

1. provide one traceable description of the platform as a system; and
2. make the boundary between design intent, checked-in configuration, reported testing, and unresolved evidence explicit.

This report is not a type certificate, declaration of compliance, flight authorization, or substitute for the [Pilot Handbook](../Operations/Pilot-Handbook.md). Where engineering and operating documents differ, the more restrictive operating instruction governs until the project records a verified resolution.

## 1. Scope and Evidence Method

### 1.1 Scope

The report covers:

- evolution from PT1 through the Dev-Kit;
- mechanical, propulsion, power, avionics, communications, payload, and software architecture;
- manufacturing, configuration, operation, and maintenance interfaces;
- current verification status and unresolved blockers;
- contradictions between current repository artifacts; and
- evidence gates required before stronger readiness or performance claims.

It does not duplicate detailed assembly steps, parameter tables, maintenance procedures, or API endpoint references. Those remain in their dedicated guides and are linked from the traceability matrix.

### 1.2 Evidence labels

Every maturity statement in this report uses one of four evidence classes:

| Label | Meaning |
|---|---|
| **Repository-backed** | A design, configuration, or instruction exists in the current repository. This proves documented intent, not physical behavior. |
| **Reported test** | A dated engineering or progress report records an observed result. Raw logs may still be needed for independent reproduction. |
| **Planned** | A design, feature, or test is described but not recorded as completed. |
| **Blocked / conflicting** | Current evidence records an unresolved fault, or authoritative sources disagree materially. |

### 1.3 Source precedence

When sources disagree, this report applies the following order for describing the current platform:

1. dated build and flight evidence, especially the [June 2026 progress report](https://dao.arrowair.com/t/project-quiver-june-2026-progress-report/172);
2. current safety and operating limits in the [Pilot Handbook](../Operations/Pilot-Handbook.md);
3. checked-in BOM, CAD, PCB, firmware, and parameter artifacts;
4. the current [Dev-Kit Engineering Report](./Dev-Kit-Engineering-Report.md); and
5. PT1, PT2, and PT3 reports as historical design evidence.

This order does not automatically resolve a safety-relevant conflict. It identifies which claim should govern operations while the underlying artifacts are reconciled.

## 2. Platform Evolution

The prototype sequence is evolutionary rather than a set of independent aircraft. Each stage retained the basic quadcopter concept while changing the power distribution, electronics, payload capacity, and developer interfaces.

| Stage | Platform contribution | Evidence boundary |
|---|---|---|
| [PT1](./PT1-Engineering-Report.md) | Established the folding quadcopter layout, 25 kg MTOW design target, single quick-release payload interface, 14S power concept, CAN-connected propulsion, exposed flight controller, and contactor/pre-charge power architecture. | The PT1 report also records a calculated structural safety factor of 1.53 at full throttle and recommends bench validation; its performance analysis is not the current Dev-Kit envelope. |
| [PT2](./PT2-Engineering-Report.md) | Moved to a custom Main PCB, solid-state relay (SSR) and pre-charge switching, a Mateksys H743 flight controller, improved enclosure and service access, and LiDAR altitude sensing. The report records successful initial flights and stable behavior. | PT2 hardware and flight results are historical; they do not validate later PT3 or Dev-Kit changes. |
| [PT3](./PT3-Engineering-Report.md) | Introduced the Pix32 v6, a distributed four-PCB architecture, three payload interfaces, dual navigation and altitude-sensor concepts, Ethernet, companion-computer integration, and improved enclosure and serviceability. | The report describes intended performance improvements but does not provide a closed Dev-Kit flight-test data set. |
| [Dev-Kit](./Dev-Kit-Engineering-Report.md) | Revised PCB protection and connectors, integrated the Raspberry Pi and Ethernet switches, added PCB vibration isolation and copper bus bars, modified the enclosure, selected production landing gear, added 360-degree and forward obstacle sensors, and documented Quiver Hub and payload workflows. | The report is a delta from PT3. Its April 2026 results must be read with the later June 2026 regression and readiness status. |

### 2.1 Current configuration identity

The repository uses both “PT3” and “Dev-Kit” for the current aircraft. The physical architecture is best understood as a Dev-Kit revision of PT3:

- PT3 supplies the underlying distributed electronics and three-interface architecture.
- The Dev-Kit report specifies later structural, PCB, enclosure, networking, and software changes.
- The generated BOM contains additional current substitutions and notes not reflected in every report.

Until a versioned configuration record is published, “current Dev-Kit” should mean the exact BOM revision, CAD revision, PCB production package, firmware image, parameter set, and deviation list used for a named serial-numbered aircraft—not an undifferentiated PT3 label.

## 3. Current Reference Architecture

### 3.1 Airframe and packaging

The platform is a folding quadcopter built primarily from laser-cut aluminum plates and beams, carbon-fiber motor-arm and landing-gear tubes, and printed enclosure or adapter parts. The current source assembly is generated from Python modules under [`src/quiver`](../../src/quiver/), with manufacturing source data under [`bom`](../../bom/) and human-readable outputs under [Manufacturing](../Manufacturing/).

The main structural groups are:

- three stacked rack plates and cockpit support beams;
- battery walls and sliders forming the central battery bay;
- four foldable motor-arm connectors and carbon-fiber arms;
- detachable 30 mm carbon-fiber landing gear;
- top, side, and bottom equipment mounts;
- a sealed cockpit enclosure and removable cap; and
- one bottom and two side attachment-interface structures.

The Dev-Kit report records a successful 7 kg payload flight test only in the context of discovering that thinning the lower structure was unsafe. It says the accepted configuration kept the lower plate at 4 mm while thinning upper structure. The current BOM instead specifies part 1113, the lower plate, as 1 mm. This is a release-blocking configuration conflict; see Section 8.

The current BOM specifies a Nanuk 976 transport case. The Dev-Kit report instead documents a used Pelican 1640 with custom foam. Either may be workable, but the packed configuration and foam design must be tied to the case actually procured.

### 3.2 Mass and payload budget

The Dev-Kit report publishes the following calculated mass budget:

| Configuration | Empty aircraft | Battery | Calculated takeoff mass | Calculated payload to 25 kg MTOW |
|---|---:|---:|---:|---:|
| 20 Ah, 14S | 9.65 kg | 7.90 kg | 17.55 kg | 7.45 kg |
| 30 Ah, 14S | 9.65 kg | 11.40 kg | 21.40 kg | 3.95 kg |

These values are useful configuration calculations, not a flight-validated payload envelope. The current BOM lists only the Tattu 4.0 14S 30 Ah battery, while the documentation landing page summarizes a broader “5–8 kg” payload range. A released payload limit therefore requires measured as-built empty weight, the installed battery mass, center-of-gravity limits, structural configuration, propulsion margin, and flight-test results for that exact aircraft.

### 3.3 Propulsion and primary power

The checked-in BOM specifies:

- four Hobbywing XRotor X6 Plus G2 motor/ESC units;
- two clockwise and two counterclockwise Hobbywing MFP 24 × 8.0 propellers; and
- one Tattu 4.0 14S 30,000 mAh smart battery with CAN telemetry.

The Battery Connector PCB controls and protects the high-voltage path. The Dev-Kit revision adds copper bus bars, upgraded power MOSFETs, high-current fusing, transient protection, pre-charge control, temperature monitoring, a heat-sink path into the chassis, and status or probe points. The flight controller is intended to close the main SSR automatically through a Lua script after the low-voltage system boots. The Pilot Handbook requires confirmation that the SSR is closed and prohibits flight if that state is uncertain.

The propulsion command path is DroneCAN. The base parameters set the ESC bitmask for motors 1–4, while the June report records a remaining reliability investigation for Hobbywing X6 Plus G2 ESCs on DroneCAN. Repository presence of the parameter does not close that hardware-integration item.

### 3.4 Distributed electronics

The Dev-Kit retains four PCB types:

| Board | Installed quantity | Platform responsibility |
|---|---:|---|
| Battery Connector PCB | 1 | High-voltage switching, pre-charge, protection, battery monitoring, and power handoff. |
| Main PCB | 1 | Central low-voltage power and signal distribution; CAN, serial, Ethernet, telemetry, payload, Raspberry Pi, and switch integration. |
| Flight Controller PCB | 1 | Pix32 v6 adapter and breakouts for power, PWM/GPIO, GNSS, CAN, serial, and I2C interfaces. |
| Attachment Interface PCB | 3 | Spring-contact handoff of regulated payload power and data to the three quick-release interfaces. |

KiCad source and production packages are checked in under [`src/pcb`](../../src/pcb/). That is repository evidence that the boards are manufacturable artifacts. Build-specific inspection, electrical test results, and configuration control remain necessary for each assembled board.

The Main PCB hosts or connects the Raspberry Pi 5, two BotBlox GigaBlox Nano Ethernet switches, Pix32 v6 stack, telemetry hardware, primary and backup GNSS, altitude and obstacle sensors, camera, and payload interfaces. The current BOM notes that several installed items are not represented as separate CAD parts, so CAD completeness should not be used as the sole as-built inventory.

### 3.5 Flight control, navigation, and sensing

The current baseline flight controller is a Holybro Pix32 v6 running a custom ArduCopter build for the Pixhawk 6C target. The custom build and parameter layers document:

- DroneCAN motor control;
- optional PPP networking through the Raspberry Pi;
- RPLidar S2 support on SERIAL5 / TELEM3;
- optional object-avoidance parameters;
- temperature-sensor support; and
- optional OpenDroneID support for the DroneBeacon db201.

The configured sensor set is:

| Function | Current BOM item | Integration status |
|---|---|---|
| Primary GNSS | Here4 or Holybro H-RTK F9P (DroneCAN) | Repository-backed alternatives. Outdoor 3D fix and compass calibration were reported in June. |
| Backup GNSS | Mateksys M9N-G4-3100 | Repository-backed; unreliable acquisition remained open in June. |
| Downward altitude | Nanoradar NRA15 | Reported together with the other obstacle sensors after CAN ID correction; Pilot Handbook treats radar and LiDAR as test-only. |
| Forward obstacle sensing | Nanoradar MR82 | Reported after CAN ID and filter correction; field validation remains incomplete. |
| 360-degree obstacle sensing | RPLidar S2L | Ground integration and browser pipeline reported; in-flight dropout remains unresolved. |
| Remote ID | DroneBeacon db201 | April integration test reported successful; June hardware/CAN regression blocks arming. |
| Gimbal camera | SIYI A8 Mini | Video and control integration reported. |

The Pilot Handbook is authoritative for operational use: radar and LiDAR are experimental and must not be relied upon during critical flight phases. Sensor presence and telemetry do not prove avoidance performance.

### 3.6 Communications and onboard network

The platform combines several communication paths:

- DroneCAN for ESCs, GNSS, Remote ID, and other supported peripherals;
- serial links for telemetry and selected sensors;
- Ethernet between the Raspberry Pi, flight controller adapter, SIYI system, and payload devices;
- SIYI HM30 for command, telemetry, and video; and
- HTTPS and WebSocket connections from the companion computer to Quiver Hub.

The documented onboard subnet is `192.168.144.0/24`, with no DHCP service because of SIYI firmware conflicts.

| Address or range | Assignment |
|---|---|
| `192.168.144.10` | CubeNode ETH adapter |
| `192.168.144.11`, `.12`, `.20`, `.25`, `.60` | SIYI-reserved equipment addresses |
| `192.168.144.50` | Raspberry Pi companion computer |
| `192.168.144.51` | Flight controller |
| `192.168.144.100`, `.101`, `.102` | Default payload addresses for C1, C2, and C3 |
| `192.168.144.100–199` | Developer-assigned payload range |
| `192.168.144.200–254` | Ground station or development machines |

The June build report says a flight-controller/SIYI address conflict was corrected and the HM30–MK32 link was restored by installing a matched firmware set. The MK32 was then the control station, with Mission Planner used as a telemetry view and a Tailscale subnet route through the Raspberry Pi for remote engineering access.

### 3.7 Payload interface

The aircraft provides bottom, left-side, and right-side quick-release payload positions, conventionally C1, C2, and C3. Each has a mechanical mounting plate and an Attachment Interface PCB using spring-loaded contacts.

The Dev-Kit report documents regulated 12 V and CAN on all three interfaces, but says Ethernet is present on C1 and C2 in one section and all three interfaces in another. The physical pinout and PCB netlist must be treated as the deciding source before designing a C3 Ethernet payload. Hot-swap language in the reports describes the mechanical and electrical design objective; a payload developer should not infer that live connection is safe without an approved power-state procedure and inrush analysis.

### 3.8 Companion computer, Quiver Hub, and SDK boundary

The [Quiver SDK Developer Guide](../Develop-Attachments-Software/Quiver-SDK-Developer-Guide.md) describes a cloud-connected architecture in which Raspberry Pi services bridge local hardware to Quiver Hub. It documents five data paths:

1. MAVLink and DroneCAN telemetry;
2. RPLidar point clouds;
3. SIYI camera video and gimbal control;
4. flight-controller logs, diagnostics, and over-the-air firmware workflows; and
5. custom payload applications.

The guide names companion services for job polling, telemetry forwarding, log/firmware operations, camera streaming, and SIYI control, together with REST and Socket.IO interfaces. These are interface-level documentation in this repository; the corresponding Hub and companion application source is not present here and must be versioned and validated in its owning repository.

The Dev-Kit report makes a further important distinction: the existing telemetry and job-runner scripts predate the formal `quiver-sdk` / `quiver-hub` package design, and the formal SDK packages were still planned rather than implemented. The working sensor-to-browser path is reported evidence for one integration, not proof that every SDK module described in the architecture exists or has passed hardware testing.

Flight-critical control remains on the Pix32 v6. The Raspberry Pi and Hub should be treated as non-flight-critical integration layers unless a future safety assessment and verified architecture explicitly changes that boundary.

## 4. Manufacturing and Configuration Flow

### 4.1 Source-to-aircraft chain

The repository supports the following controlled build chain:

1. [`bom/*.yaml`](../../bom/) defines sourced parts, quantities, notes, and design references.
2. [`src/quiver`](../../src/quiver/) composes the mechanical assembly and generated outputs.
3. [`src/pcb`](../../src/pcb/) contains KiCad sources and production files for each PCB type.
4. The [BOM](../Manufacturing/BOM.md) provides a human-readable procurement view.
5. The [Manufacturing Guide](../Manufacturing/Manufacturing-Guide.md) covers part preparation and 22 structural/equipment assembly stages.
6. PCB and harness guides define board assembly and aircraft wiring.
7. [Firmware & Parameters](../Operations/firmware/index.md) provides the flight-controller image and layered parameter sets.
8. The [Pilot Handbook](../Operations/Pilot-Handbook.md) requires the manufacturer to load firmware, apply the approved baseline, and perform airframe-specific calibration before delivery.

The chain is usable, but it is not yet a complete configuration-management record. A released aircraft still needs an as-built manifest tying component substitutions, CAD and PCB revisions, firmware hash, parameter export, calibration record, and known deviations to its serial number.

### 4.2 Firmware and parameter layering

The documented load order is:

1. `standard-params.param` for the base vehicle;
2. `params-ethernet.param` when PPP networking is required;
3. `params-object-avoidance.param` when the RPLidar avoidance configuration is enabled; and
4. `params-remoteid.param` when the external Remote ID module is enabled.

Calibration parameters are airframe-specific and intentionally excluded from the base set. The repository therefore cannot prove a particular aircraft is flight-ready from the standard parameter file alone.

The checked-in parameter file is stronger evidence than the explanatory table when the two disagree, but a mismatch still blocks release because maintainers and operators may follow the prose. Current discrepancies are listed in Section 8.

### 4.3 First-time setup boundary

The Pilot Handbook defines first-time setup as **verification**, not initial configuration by the operator. The manufacturer is expected to deliver the declared firmware, baseline parameters, sensor calibrations, motor mapping, failsafes, and logging configuration. The operator verifies the baseline, geofence, return-to-launch altitude, battery failsafes, kill switch, SSR state, and logging before flight.

The June report says the Houston bring-up produced an extensive Initial Configuration Guide, but that guide is not present in the current `docs` tree. Migrating the reviewed manufacturer procedure into the repository is therefore a documentation release gate.

## 5. Operations and Maintenance Boundary

### 5.1 Current operating limits

The Pilot Handbook currently specifies:

- VLOS operation;
- EU Open Category A3 or applicable Specific Category authorization;
- US operations under Part 107 and Remote ID requirements;
- maximum sustained wind of 15 knots and gusts of 18 knots;
- ambient temperature from -10 °C to +35 °C;
- maximum battery core temperature of 56 °C;
- no flight in rain, snow, or hail;
- a geofence for every flight;
- active onboard logging; and
- no reliance on radar or LiDAR during critical flight phases.

These are operating instructions, not proof of certification or a validated edge-of-envelope test campaign. Legal applicability still depends on aircraft configuration, operator, location, and mission.

### 5.2 Maintenance model

The [Maintenance Guide](../Operations/Maintenance-Guide.md) organizes checks by subsystem and by pre/post-flight, 8-hour, 24-hour, and 50-hour intervals. It covers the airframe, propulsion, attachment structures, landing gear, enclosures, electrical equipment, and unscheduled inspection after abnormal behavior or impact.

The guide is useful as a framework but retains placeholder content and markup that requires editorial and field verification. Maintenance intervals should therefore be treated as the current documented program, not as statistically validated life limits.

## 6. Verification Status

### 6.1 Platform status matrix

| Capability or item | Status | Evidence and interpretation |
|---|---|---|
| Mechanical and PCB source packages | **Repository-backed** | CAD/STEP assemblies, KiCad sources, and PCB production packages are checked in. This does not prove every built unit matches them. |
| BOM and assembly process | **Repository-backed** | Structured YAML, generated BOM, PCB/harness guidance, and a 22-step manufacturing guide exist. Several substitutions and conflicts remain. |
| Four-PCB architecture | **Repository-backed / reported test** | Source packages exist and Dev-Kit integration is reported. Unit-level electrical acceptance records are not included. |
| Props-off Houston ground run | **Reported test** | Completed 29 June 2026; log review reportedly found no major motor output/input issue beyond Remote ID. |
| Current Dev-Kit first flight | **Planned / blocked** | The June status moved first flight to July behind Remote ID, GNSS, travel, and related readiness work. No later first-flight evidence is included here. |
| HM30–MK32 control and A8 video | **Reported test** | Matched firmware resolved binding; command/telemetry and video were reported working. |
| Primary GNSS and compass | **Reported test** | Outdoor 3D fix and compass calibration were completed on the Houston build. |
| Backup M9N GNSS | **Blocked** | Satellite acquisition remained unreliable and required a cold-start recovery. |
| Three obstacle sensors reporting | **Reported test** | CAN IDs and filters were corrected so RPLidar S2, NRA15, and MR82 could report together. |
| LiDAR obstacle avoidance in flight | **Blocked** | An in-flight RPLidar dropout remains open. The Pilot Handbook restricts use to controlled testing. |
| DroneCAN ESC reliability | **Blocked** | June goals include converter and termination checks for X6 Plus G2 reliability. |
| Remote ID | **Blocked after earlier test** | April BLE/DroneCAN integration was reported successful; the module later disappeared from CAN and blocks arming on the Houston unit. |
| Onboard flight logging | **Blocked / unverified** | SD-card write verification remained a first-flight gate in June. |
| Weather sealing | **Reported test with operational restriction** | A garden-hose test is reported as IP53 validation; the Pilot Handbook nevertheless prohibits precipitation flight. |
| Sensor-to-Hub point-cloud path | **Reported test** | RPLidar data was reported at 10 Hz through Raspberry Pi, HTTP, Hub, WebSocket, and browser rendering. |
| Formal Quiver SDK packages | **Planned** | Architecture and interface documentation exists, but the Dev-Kit report says formal packages were not yet implemented. |
| 25–31 minute endurance | **Planned / unverified** | The landing page publishes the figure while the Dev-Kit report marks endurance results pending. |
| 3.95–7.45 kg payload capacity | **Calculated** | Derived from 25 kg MTOW and published mass estimates; not a released flight-tested payload envelope. |
| EASA C3 certification | **Not achieved / deferred** | The Dev-Kit report says the certification path was deferred. |
| FAA Declaration of Compliance | **Not achieved** | The June goal reconciliation says the filing was not done. |
| Attachment-interface supply | **Blocked** | The prior supplier became unavailable and PCB inventory was reported low, with no replacement path started. |

### 6.2 What the current evidence supports

The evidence supports describing Quiver as a detailed, buildable, integrated Dev-Kit platform undergoing flight-readiness closure. It supports hardware procurement and assembly work, controlled bench integration, manufacturer configuration, payload development against verified pinouts, and structured test planning.

It does not yet support an unconditional claim that the current configuration is flight-proven, shipment-ready, certified, precipitation-capable, or validated to the published endurance and payload numbers.

## 7. Traceability Matrix

| Topic | Primary current source | Supporting source | What it establishes |
|---|---|---|---|
| Platform purpose and public overview | [Project Quiver introduction](../index.md) | [Dev-Kit report](./Dev-Kit-Engineering-Report.md) | Intended product and capability summary; some maturity claims require reconciliation. |
| Prototype rationale | [PT1](./PT1-Engineering-Report.md), [PT2](./PT2-Engineering-Report.md), [PT3](./PT3-Engineering-Report.md) | [Dev-Kit report](./Dev-Kit-Engineering-Report.md) | Design evolution and prototype-specific decisions. |
| Current procurement configuration | [Generated BOM](../Manufacturing/BOM.md) | [`bom` source](../../bom/) | Part identities, quantities, design references, cost snapshot, and substitution notes. |
| Mechanical source | [`src/quiver`](../../src/quiver/) | [Manufacturing Guide](../Manufacturing/Manufacturing-Guide.md) | Source assembly and human build sequence. |
| PCB source and production data | [`src/pcb`](../../src/pcb/) | [Dev-Kit electronics sections](./Dev-Kit-Engineering-Report.md) | Four-board source packages and functional rationale. |
| Flight-controller baseline | [Firmware & Parameters](../Operations/firmware/index.md) | [`standard-params.param`](../Operations/firmware/parameters/standard-params.param) and overlays | Firmware artifact, parameter load order, and checked-in values. |
| Payload and network interfaces | [SDK Developer Guide](../Develop-Attachments-Software/Quiver-SDK-Developer-Guide.md) | [Dev-Kit networking and attachment sections](./Dev-Kit-Engineering-Report.md) | Logical network, services, addresses, and payload interface description. |
| Operating limits and preflight | [Pilot Handbook](../Operations/Pilot-Handbook.md) | [Firmware & Parameters](../Operations/firmware/index.md) | Current operational restrictions and verification responsibilities. |
| Maintenance | [Maintenance Guide](../Operations/Maintenance-Guide.md) | [Manufacturing Guide](../Manufacturing/Manufacturing-Guide.md) | Inspection framework, intervals, and assembly context. |
| Latest build and readiness state | [June 2026 progress report](https://dao.arrowair.com/t/project-quiver-june-2026-progress-report/172) | Current GitHub issues and pull requests | Most recent dated integration results and blockers available at this evidence cut. |

## 8. Configuration Conflicts and Documentation Debt

The following items should be tracked to closure. Safety-relevant discrepancies are release blockers, not editorial preferences.

| ID | Conflict | Current evidence | Required disposition |
|---|---|---|---|
| CFG-01 | Lower plate thickness | Dev-Kit flight-test narrative says part 1103/1113 remained 4 mm after unsafe payload oscillation with a thinned lower frame; current BOM and YAML specify 1 mm. | Identify the released part number and thickness from the flown safe configuration, update CAD/BOM/guide together, and document the superseded unsafe variant. |
| CFG-02 | Battery documentation | Current hardware is 14S and `standard-params.param` sets `BATT_ARM_VOLT=47.5`, but the firmware page documents 12S calculations and `BATT_ARM_VOLT=42`. | Regenerate the parameter table from the checked-in file or correct it manually, then validate thresholds against the approved 14S battery and flight-test plan. |
| CFG-03 | RPLidar serial port | Firmware text correctly says SERIAL5, and the parameter file uses SERIAL5, but the later table still says SERIAL3. | Remove the contradictory SERIAL3 table entries and retain the physical connector mapping validated on the Houston build. |
| CFG-04 | Remote ID readiness | April report says validated and “last hardware blocker” cleared; June report records a CAN disappearance and arming block. `DID_OPTIONS=1` is described as suppressing a missing-ID pre-arm block. | Treat June as current, reproduce behavior by firmware version, record CAN evidence, and document exactly which arming checks `DID_OPTIONS` affects. |
| CFG-05 | Current product identity | The introduction calls PT3 the current finalized production design; the same page calls the Dev-Kit current, while June records no first flight for the Houston build. | Publish a versioned Dev-Kit configuration baseline and replace broad “finalized/stable” language with evidence-scoped status. |
| CFG-06 | Endurance and payload claims | Introduction claims 25–31 minutes and 5–8 kg; Dev-Kit report says endurance tests are pending and calculates 3.95 kg with the current 30 Ah battery. | Mark figures as targets or calculations until dated flight logs close the matrix for each battery/payload configuration. |
| CFG-07 | Environmental claim | Dev-Kit report says IP53 garden-hose validation and light-rain feasibility; Pilot Handbook prohibits rain, snow, or hail. | Keep the prohibition until a controlled environmental qualification and operating-risk review approve a revised limit. |
| CFG-08 | Transport case | Dev-Kit report specifies Pelican 1640; current BOM specifies Nanuk 976 and points to older foam data. | Choose the current case, verify packed fit and protection, and version the matching foam profiles. |
| CFG-09 | Primary GNSS CAD | BOM allows Here4 or H-RTK F9P but notes the CAD still shows a retired Wren Mini. | Update the vendor STEP and verify mount, connector, mass, and antenna clearance for each allowed alternative. |
| CFG-10 | Payload Ethernet | Dev-Kit report says Ethernet is on C1/C2 in one section and all C1/C2/C3 ports in another. | Publish one connector/pinout table derived from the released PCB netlist and verify each interface electrically. |
| CFG-11 | Software maturity | SDK guide presents complete services and endpoints; Dev-Kit report says formal SDK packages are planned and existing scripts predate the specification. | Link each documented function to its owning repository, release/tag, implementation status, and hardware test. Separate current services from future package APIs. |
| CFG-12 | Missing manufacturer guide | June report says an Initial Configuration Guide was produced, but it is absent from the current documentation tree. | Merge the reviewed guide or link its authoritative location, then reconcile it with the Pilot Handbook and parameter page. |
| CFG-13 | Stale links and placeholders | Pilot Handbook links a historical `vector/firmware-docs-clean` branch and retains a contact placeholder; Maintenance Guide retains `[toc]`, directive-like markup, and placeholder rows. | Replace stale links, assign a support route, normalize site markup, and field-review maintenance content. |
| CFG-14 | Attachment supply | The BOM describes the interface, while June records an unavailable off-the-shelf source and low PCB inventory. | Qualify a replacement source or redesign, update purchasing data, and validate interchangeability before promising kit availability. |

## 9. Recommended Release Evidence Gates

### Gate A — Configuration authority

- Resolve CFG-01 through CFG-04 before further flight release.
- Assign a platform revision and serial-numbered as-built configuration.
- Record hashes or revisions for CAD, all PCB production packages, firmware image, parameter export, and Lua scripts.
- Record installed component substitutions, calibration files, CAN node IDs, and network addresses.
- Verify BOM, manufacturing guide, and the physical Houston build agree.

### Gate B — Ground readiness

- Close Remote ID CAN and arming behavior with dated evidence.
- Demonstrate reliable M9N cold start or remove it from the released redundancy claim.
- Complete the DroneCAN ESC converter/termination investigation.
- Verify SD-card logging and retrieve a complete ground-run log.
- Demonstrate SSR auto-engage, pre-charge behavior, failsafes, motor order/direction, geofence, RC loss behavior, and kill switch with propellers removed.
- Repeat the integrated sensor test after every CAN ID and firmware change.

### Gate C — First-flight sequence

- Approve a written first-flight sequence and abort criteria.
- Perform the planned propellers-on restrained or protected ground run only under an approved procedure.
- Fly a low-risk initial hover within the Pilot Handbook limits and preserve raw logs, configuration export, weather, mass, center of gravity, pilot, and anomaly record.
- Review vibration, control margin, GNSS health, battery/ESC telemetry, temperature, and communications before expanding the envelope.

### Gate D — Performance envelope

- Test representative aircraft at the released empty mass and structural configuration.
- Publish endurance curves for each supported battery, payload mass, and environmental condition.
- Validate thrust and control margin at the intended MTOW and center-of-gravity limits.
- Close the in-flight LiDAR dropout before enabling obstacle avoidance outside controlled test conditions.
- Separate radar/LiDAR detection performance from flight-control avoidance performance.
- Preserve raw flight logs and calculation scripts with each published result.

### Gate E — Developer release

- Publish the attachment electrical pinout, power budget, inrush limit, mechanical envelope, center-of-gravity rules, and C3 Ethernet disposition.
- Qualify the attachment-interface supply path.
- Version the companion services and formal SDK separately, with an implementation matrix against the Developer Guide.
- Test onboarding from a clean Raspberry Pi and a newly assembled payload.
- Reconcile the Pilot, Maintenance, Manufacturing, Firmware, and SDK guides against the released configuration.

### Gate F — Compliance and shipment claims

- Keep EASA C3 certification and FAA Declaration of Compliance claims explicitly marked as not achieved until the respective evidence exists.
- Configure Remote ID for the actual aircraft and operator before regulated operation.
- Supply region-specific operating limitations without presenting general guidance as legal authorization.
- Complete the as-built, acceptance, calibration, maintenance-baseline, and known-deviation records for every shipped or loaned unit.

## 10. Conclusion

Project Quiver has a strong open-source engineering foundation: a coherent heavy-lift architecture, mechanical and PCB sources available for inspection, a detailed procurement model, a repeatable assembly path, layered flight-controller configuration, and a credible companion/payload integration design. The Dev-Kit has also produced useful reported integration evidence, including network and ground-control recovery, multi-sensor reporting, a propellers-off ground run, and an end-to-end point-cloud path.

Its current engineering status is nevertheless best described as **integrated and approaching first-flight readiness**, not fully validated or production-final. The decisive next work is evidence closure: establish one controlled hardware baseline, resolve the safety-relevant source contradictions, clear the current Remote ID/GNSS/ESC/logging/LiDAR blockers, and publish flight logs before repeating performance or readiness claims.

Maintaining that distinction protects both the project and its developers. It lets contributors build against real interfaces today while giving operators and future customers a precise view of what has—and has not—been demonstrated.
