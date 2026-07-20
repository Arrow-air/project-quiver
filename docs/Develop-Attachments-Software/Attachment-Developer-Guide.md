---
title: Quiver Attachment Developer Guide
sidebar_label: Attachment Developer Guide
sidebar_position: 1
description: Mechanical, electrical, networking, software, and verification guidance for Quiver payload attachments.
---

# Quiver Attachment Developer Guide

**Document status:** Draft — pending attachment electrical and mounting-interface redesign validation

**Target platforms:** PT3 and Dev-Kit aircraft revisions equipped with the three C1/C2/C3 attachment interfaces

**Source baseline:** project-quiver commit `ef316bc9f4e9e001dd5421f8070e54f3180f1600`

**Last reviewed:** July 2026

:::warning Revision-dependent interface
Maintainer feedback indicates that the attachment PCB and mounting interface are being revised. Confirm mechanical dimensions, current limits, CAN configuration, and the position-specific auxiliary-signal characteristics against the target aircraft revision before manufacturing or flight use.
:::

## Quick start

1. Identify the exact Quiver aircraft and attachment-interface revision.
2. Select Bottom/J31, Side 1/J29, or Side 2/J30.
3. Obtain maintainer confirmation for mass, CG, current, and interface limits.
4. Choose the data path:
   - Ethernet for cameras, LiDAR, and high-rate sensors;
   - DroneCAN for deterministic low-bandwidth devices;
   - the auxiliary flight-controller signal only after its position-specific channel and electrical behavior are confirmed.
5. Design and independently review the mechanical and electrical interface.
6. Complete bench testing before installation on an aircraft.
7. Submit the evidence package described in [Section 9](#9-contribution-package).

## Audience and prerequisites

This guide is intended for developers integrating sensors, cameras, actuators, and companion-computer payloads with Quiver.

Before starting, the developer should have:

- access to the target aircraft revision and current repository sources;
- basic mechanical CAD and electrical integration experience;
- appropriate bench power, continuity, and network test equipment;
- familiarity with Linux networking for Ethernet payloads;
- familiarity with DroneCAN tooling for CAN payloads;
- access to an Arrow maintainer for revision-dependent approvals.

### What this guide does not provide

This guide is not:

- a released interface-control drawing;
- a substitute for the current KiCad, CAD, and harness sources;
- a certification or flight-approval document;
- authorization to manufacture or fly an attachment with unconfirmed limits;
- a specification for attachment-specific performance or airworthiness.

This guide provides a staged path from attachment concept through bench validation and flight-readiness review. It covers the mechanical interface, electrical power, Ethernet, CAN, the flight-controller signal, payload software, and the evidence expected in a contribution.

> **Safety boundary**
>
> The [Dev-Kit Engineering Report](../Engineering-Reports/Dev-Kit-Engineering-Report.md) describes the interface as designed for hot-swap operation, but the repository does not provide a released live-mating procedure or electrical qualification envelope. Treat that statement as design intent, not permission to connect or remove a powered attachment. Unless a specific aircraft revision has a validated live-mating procedure, disarm the aircraft, isolate propulsive power, switch payload rails off, and verify zero voltage before mating or removing an attachment.

## 1. Start with the correct source revision

Quiver evolves quickly, and some archived documents retain older connector or CAN-bus names. Before designing hardware:

1. Record the aircraft hardware revision and the commit or release used for the design.
2. Use the current [`src/pcb/attach_pcb`](https://github.com/Arrow-air/project-quiver/tree/ef316bc9f4e9e001dd5421f8070e54f3180f1600/src/pcb/attach_pcb) and [`src/pcb/main_pcb`](https://github.com/Arrow-air/project-quiver/tree/ef316bc9f4e9e001dd5421f8070e54f3180f1600/src/pcb/main_pcb) design files as the electrical source of truth.
3. Use the [V1.4 Attachment Interface PCB update note](https://github.com/Arrow-air/project-quiver/blob/ef316bc9f4e9e001dd5421f8070e54f3180f1600/task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB/2026-Update/information-note.md) for the current spring-contact construction and orientation mark.
4. Use the [Manufacturing Guide](../Manufacturing/Manufacturing-Guide.md) for aircraft-side interface orientation and harness routing.
5. Ask the Arrow engineering team to confirm the available power budget and payload mass/CG envelope for the specific aircraft before ordering hardware.

V1.4 is the current repository design baseline for the attachment PCB, but operational use remains subject to electrical, mechanical-fit, and manufacturability validation.

### 1.1 Source and confidence matrix

| Topic | Source to check | Revision/status | Appropriate use |
| --- | --- | --- | --- |
| Attachment PCB geometry | [`src/pcb/attach_pcb`](https://github.com/Arrow-air/project-quiver/tree/ef316bc9f4e9e001dd5421f8070e54f3180f1600/src/pcb/attach_pcb) | V1.4 repository baseline; validation pending | Candidate PCB and mechanical geometry |
| Attachment functions | [Current KiCad schematic](https://github.com/Arrow-air/project-quiver/blob/ef316bc9f4e9e001dd5421f8070e54f3180f1600/src/pcb/attach_pcb/QuiverAttachPCB.kicad_sch), [production netlist](https://github.com/Arrow-air/project-quiver/blob/ef316bc9f4e9e001dd5421f8070e54f3180f1600/src/pcb/attach_pcb/production/netlist.ipc), and [legacy pin-map README](https://github.com/Arrow-air/project-quiver/blob/ef316bc9f4e9e001dd5421f8070e54f3180f1600/task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB/README.md) | Commit-specific | Logical connectivity, not a released connector-control drawing |
| Aircraft-side payload ports | [Main PCB schematic](https://github.com/Arrow-air/project-quiver/blob/ef316bc9f4e9e001dd5421f8070e54f3180f1600/src/pcb/main_pcb/Quiver_PT3_Main_PCB.kicad_sch), [netlist](https://github.com/Arrow-air/project-quiver/blob/ef316bc9f4e9e001dd5421f8070e54f3180f1600/src/pcb/main_pcb/Quiver_PT3_Main_PCB.net), and [design note](https://github.com/Arrow-air/project-quiver/blob/ef316bc9f4e9e001dd5421f8070e54f3180f1600/task-grant-bounty/pt3/electronics/0007-Main-PCB/information_note.md) | Target-aircraft revision | Aircraft-side routing and connector designations |
| V1.4 design changes | [2026 update information note](https://github.com/Arrow-air/project-quiver/blob/ef316bc9f4e9e001dd5421f8070e54f3180f1600/task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB/2026-Update/information-note.md) | Marked valid; electrical, fit, and manufacturability tests remain | Change rationale and known validation work |
| Mechanical mounting | [Manufacturing Guide](../Manufacturing/Manufacturing-Guide.md) and released CAD | Revision-specific | Position, orientation, assembly, and released geometry |
| System-level Dev-Kit context | [Dev-Kit Engineering Report](../Engineering-Reports/Dev-Kit-Engineering-Report.md) | System summary with revision-dependent implementation details | Validated system context and known design intent, not pin-level authority |
| Payload networking and Hub integration | [Quiver SDK Developer Guide](./Quiver-SDK-Developer-Guide.md) | April 2026 guide; implementation status is revision-dependent | Static addressing, companion services, and Hub data paths |

The [legacy attachment PCB documentation](https://github.com/Arrow-air/project-quiver/blob/ef316bc9f4e9e001dd5421f8070e54f3180f1600/task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB/README.md) calls the differential CAN pair `CAN1_P`/`CAN1_N`. The [PT3 Main PCB update note](https://github.com/Arrow-air/project-quiver/blob/ef316bc9f4e9e001dd5421f8070e54f3180f1600/task-grant-bounty/pt3/electronics/0007-Main-PCB/Updates/information_note.md) moves payload operation to `CAN2_H`/`CAN2_L`. Treat these as revision-dependent names for the attachment CAN pair and confirm continuity against the current schematics before wiring.

### 1.2 Requirement language

- **Required** means an explicit repository requirement, maintainer decision, or formal acceptance item.
- **Recommended baseline** means engineering guidance to use unless Arrow approves an alternative.
- **Revision-dependent** means the value or behavior must be verified for the target aircraft.

Unless a checklist item is explicitly identified as Arrow-required, the verification gates in this guide are recommended engineering baselines rather than a published Arrow qualification standard.

### 1.3 Logical system context

This is a data-flow overview, not a wiring diagram or permission to use an unverified interface:

```text
Attachment sensor or actuator
   |-- verified +12V / 12VSW power path
   |-- Ethernet --> Main PCB switch --> Raspberry Pi --> Quiver Hub
   |-- CAN pair --> revision-confirmed aircraft CAN / DroneCAN network
   `-- auxiliary signal --> protected, position- and revision-confirmed interface
```

## 2. Choose an interface position

The targeted PT3 and Dev-Kit revisions provide three aircraft-side quick-release positions. Verify the connector and harness designations on the target revision:

| Position | Main PCB connector | Recommended payload IP | Orientation example |
| --- | --- | --- | --- |
| Bottom | [`J31`](https://github.com/Arrow-air/project-quiver/blob/ef316bc9f4e9e001dd5421f8070e54f3180f1600/task-grant-bounty/pt3/electronics/0007-Main-PCB/information_note.md) | `192.168.144.100` | Nadir-facing payloads such as mapping sensors, subject to mass/CG approval |
| Side 1 | [`J29`](https://github.com/Arrow-air/project-quiver/blob/ef316bc9f4e9e001dd5421f8070e54f3180f1600/task-grant-bounty/pt3/electronics/0007-Main-PCB/information_note.md) | `192.168.144.101` | Lateral-facing sensors, subject to clearance and asymmetry approval |
| Side 2 | [`J30`](https://github.com/Arrow-air/project-quiver/blob/ef316bc9f4e9e001dd5421f8070e54f3180f1600/task-grant-bounty/pt3/electronics/0007-Main-PCB/information_note.md) | `192.168.144.102` | Lateral-facing sensors, subject to clearance and asymmetry approval |

The IPs are conventions, not DHCP leases. Any unused address in `192.168.144.100`–`192.168.144.199` may be assigned after checking for conflicts. Do not use the reserved addresses listed in the [Quiver SDK Developer Guide](./Quiver-SDK-Developer-Guide.md#3-network-configuration).

Validate the power, CAN, auxiliary-signal, and Ethernet harness for `J29`, `J30`, and `J31` independently. Do not validate one position and assume the other two have identical routing or population.

Select a position by considering:

- payload mass, center of gravity, drag, and propeller clearance;
- sensor field of view and electromagnetic interference;
- cable bend radius and strain relief;
- rain path, dust exposure, and drainage;
- access to the release mechanism and fasteners;
- whether an asymmetric side payload requires a counterweight or flight-control validation.

Do not infer an allowable payload mass from the aircraft's total 5–8 kg payload capacity stated in the [platform overview](../index.md). That figure is an aircraft-level capability, not a per-interface structural rating.

## 3. Mechanical integration

### 3.1 Reuse the released geometry

Build against the released CAD rather than measuring a printed part or marketplace listing. Relevant sources are:

- attachment spacers `2111`/`2121` (left/right) and `2131` (bottom) in the [Manufacturing Guide](../Manufacturing/Manufacturing-Guide.md);
- quick-release parts `2112`/`2122`/`2132` in the [Manufacturing Guide](../Manufacturing/Manufacturing-Guide.md);
- the current attachment PCB STEP model in [`src/pcb/attach_pcb`](https://github.com/Arrow-air/project-quiver/tree/ef316bc9f4e9e001dd5421f8070e54f3180f1600/src/pcb/attach_pcb).

The following repository images are orientation aids from [Manufacturing Guide step 15](../Manufacturing/Manufacturing-Guide.md#step-15-install-attachment-interfaces), not dimensioned interface-control drawings. Replace or re-annotate them when the redesigned mounting interface is released.

| Side-interface notch orientation | Bottom-interface notch and forward orientation |
| --- | --- |
| <img src="../Manufacturing/Assembly-Guides/assets/images/structural/step15_3.png" alt="Side attachment interface notch facing upward" width="420" /> | <img src="../Manufacturing/Assembly-Guides/assets/images/structural/step15_4.png" alt="Bottom attachment interface notch and cable tray facing forward" width="420" /> |

The current V1.4 attachment PCB render comes from the [2026 Attachment Interface PCB update note](https://github.com/Arrow-air/project-quiver/blob/ef316bc9f4e9e001dd5421f8070e54f3180f1600/task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB/2026-Update/information-note.md) and shows the spring-contact layout and silkscreen orientation cue. Use the KiCad and STEP sources, not this raster image, for geometry or contact numbering.

<img src="https://raw.githubusercontent.com/Arrow-air/project-quiver/ef316bc9f4e9e001dd5421f8070e54f3180f1600/task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB/2026-Update/images/QuiverAttachPCB_new1.jpg" alt="V1.4 attachment PCB repository render" width="600" />

The aircraft-side interface PCB is mounted with the spring-contact side facing outward. The PCB orientation mark must align with the quick-release notch. On the side interfaces the notch faces upward; on the bottom interface the notch faces forward, toward the sensor mount.

### 3.2 Attachment-side design checklist

- Model the mating quick-release plate, keep-out volume, PCB contact area, and release travel.
- Provide a hard mechanical load path; do not transfer payload loads through the electrical PCB or spring contacts.
- Retain the attachment against vibration and verify that the release cannot be operated by a snagged cable.
- Add strain relief before every connector and keep wiring clear of the latch.
- Keep conductive hardware away from exposed contacts and PCB test points.
- Preserve the notch and orientation cue so the payload cannot be installed rotated.
- Use locking fasteners appropriate for vibration and document their torque or installation method.
- Verify propeller, landing, sensor, and ground clearances through the full expected aircraft attitude range.

Record the final mass, mounting position, center of gravity relative to the interface, frontal area, and any protruding dimensions in the attachment README.

## 4. Electrical interface

The attachment PCB carries one four-wire Ethernet link, a differential CAN pair, regulated 12 V rails, ground, and one flight-controller auxiliary signal. The V1.4 board replaces the legacy header arrangement with individual spring contacts and enlarged mating pads while retaining the original functions.

### 4.1 Provisional logical pin map

The [attachment PCB BOM](https://github.com/Arrow-air/project-quiver/blob/ef316bc9f4e9e001dd5421f8070e54f3180f1600/task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB/BOM/QuiverAttachPCB_BOM.csv) identifies the 12-circuit locking connector as Molex [`207760-1281`](https://www.molex.com/en-us/products/series-chart/207760) and the cable-side mating housing as Molex [`204523-1201`](https://www.molex.com/en-us/products/part-detail/2045231201). The [current schematic](https://github.com/Arrow-air/project-quiver/blob/ef316bc9f4e9e001dd5421f8070e54f3180f1600/src/pcb/attach_pcb/QuiverAttachPCB.kicad_sch), [production netlist](https://github.com/Arrow-air/project-quiver/blob/ef316bc9f4e9e001dd5421f8070e54f3180f1600/src/pcb/attach_pcb/production/netlist.ipc), and connector manufacturer drawings remain authoritative for physical orientation and pin numbering.

:::caution Not a released connector-control drawing
This table records logical connectivity from the current repository sources. Before manufacturing a cable or mating PCB, validate every contact against the target attachment PCB, aircraft Main PCB, harness continuity, and the connector manufacturer's pin-1 view.
:::

| Pin | Net/function | Integration rule |
| --- | --- | --- |
| 1 | `ETH_RX+` | Keep paired with pin 3; route as a controlled differential pair |
| 2 | `12VSW` | Switched 12 V rail; duplicated with pin 4 |
| 3 | `ETH_RX-` | Keep paired with pin 1 |
| 4 | `12VSW` | Switched 12 V rail; duplicated with pin 2 |
| 5 | `ETH_TX+` | Keep paired with pin 7; route as a controlled differential pair |
| 6 | `GND` | Power and signal reference |
| 7 | `ETH_TX-` | Keep paired with pin 5 |
| 8 | `GND` | Power and signal reference |
| 9 | Legacy `CAN1_N` | CAN2-low candidate; verify continuity and polarity on the target position |
| 10 | `+12V` | Main regulated 12 V payload supply |
| 11 | Legacy `CAN1_P` | CAN2-high candidate; verify continuity and polarity on the target position |
| 12 | Attachment-board label `FMU_CH1` | Flight-controller auxiliary signal; identify the aircraft-side channel and define direction and voltage before use |

The table is transcribed from the [legacy pinout section](https://github.com/Arrow-air/project-quiver/blob/ef316bc9f4e9e001dd5421f8070e54f3180f1600/task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB/README.md#pinout). Do not infer permanent CAN high/low polarity from the legacy `P`/`N` names alone. Verify the current KiCad sources and harness continuity for `J29`, `J30`, and `J31`; never determine pin 1 from a rendered image alone.

### 4.2 Power budget and protection

Before connecting a payload, obtain written confirmation of:

- the continuous and peak current available on `+12V` and `12VSW`;
- whether the quoted limit is per port or shared across all attachment ports;
- fuse rating and population on the exact Main PCB revision;
- allowed inrush current and rail rise/fall behavior;
- whether the payload must remain off until commanded by an operator.

The [PT3 Main PCB update note](https://github.com/Arrow-air/project-quiver/blob/ef316bc9f4e9e001dd5421f8070e54f3180f1600/task-grant-bounty/pt3/electronics/0007-Main-PCB/Updates/information_note.md) mentions a 2 A fuse upgrade for a switched 12 V output, but that is not a universal payload allowance. Cable gauge, connector contacts, regulator thermal limits, other active payloads, and aircraft configuration may impose a lower limit.

Unless the maintainer approves an alternative protection strategy, the recommended baseline is to include:

- input fuse or resettable protection sized below the verified port limit;
- reverse-polarity protection where practical;
- transient suppression appropriate for the payload electronics;
- inrush limiting or staged power-up for large capacitive loads;
- local regulation and decoupling;
- a defined safe state if `12VSW`, CAN, Ethernet, or the auxiliary signal is absent;
- a common ground reference without using the airframe as the return path.

High-power loads that exceed the confirmed interface budget need a separately approved power path. Do not parallel `+12V` and `12VSW`, and do not back-feed either rail.

### 4.3 Power sequencing

For first power-up:

1. Remove propellers or use an Arrow-approved restrained bench configuration.
2. Leave the attachment mechanically disconnected and verify its input resistance and polarity.
3. Use a current-limited bench supply at the attachment's intended input; validate startup and brownout behavior.
4. Power the aircraft without mating the payload and measure the interface rails.
5. Power down and verify zero voltage.
6. Mate the attachment, apply aircraft power with the payload rail disabled, and watch for unexpected current.
7. Enable only the required rail. Confirm steady-state current, inrush, voltage droop, regulator temperature, and safe shutdown.

The Pilot Handbook identifies `P1 12V` for the separate bottom-port supply and `12V Pay` for the general payload rail. Operators should label and verify these relays before test; see [Pilot Handbook — Mission Planner Servo/Relay Page](../Operations/Pilot-Handbook.md#285-mission-planner-servorelay-page).

## 5. Data interfaces

### 5.1 Ethernet

Use Ethernet for cameras, LiDAR, companion computers, and other high-rate payloads.

Ethernet population is revision-dependent. The [Dev-Kit Engineering Report](../Engineering-Reports/Dev-Kit-Engineering-Report.md) says in its Attachment Interface section that Ethernet is present on C1 and C2, while its Ethernet Integration section says the switches provide connectivity to C1, C2, and C3. Verify link continuity and switch-port population on each target position rather than resolving this source conflict by assumption.

- Configure a static IPv4 address in `192.168.144.100`–`192.168.144.199` with prefix `/24`.
- Check the [reserved address table](./Quiver-SDK-Developer-Guide.md#reserved-addresses-do-not-use) before assignment.
- Do not run a DHCP server on the aircraft network.
- Keep TX and RX differential pairs twisted through the harness and length-matched on the PCB.
- Avoid untwisting pairs near spring contacts and connectors more than necessary.
- Document every listening port, protocol, expected data rate, and authentication method.

Minimum smoke test from the companion computer:

```bash
ip address show
ping -c 3 192.168.144.100
ip neigh show
curl --fail --max-time 2 http://192.168.144.100:<port>/health
```

Replace the address and health endpoint with the attachment configuration. A payload without HTTP should provide an equivalent deterministic health check.

### 5.2 CAN / DroneCAN

Use CAN for deterministic low-bandwidth sensors and actuators. The source baseline contains an unresolved transition: the [Main PCB netlist](https://github.com/Arrow-air/project-quiver/blob/ef316bc9f4e9e001dd5421f8070e54f3180f1600/src/pcb/main_pcb/Quiver_PT3_Main_PCB.net) connects `J29` and `J31` to CAN1 and `J30` to CAN2, while the later [Main PCB update note](https://github.com/Arrow-air/project-quiver/blob/ef316bc9f4e9e001dd5421f8070e54f3180f1600/task-grant-bounty/pt3/electronics/0007-Main-PCB/Updates/information_note.md) says `J31` was reassigned and all payloads will operate on CAN2. The attachment PCB also retains legacy `CAN1_P`/`CAN1_N` net names. Verify the populated Main PCB, harness continuity, configured flight-controller bus, and termination before connecting or enabling a node.

- Confirm bus bitrate and protocol with the aircraft configuration before enabling a node.
- Assign a unique DroneCAN node ID; do not copy the ID from another installed device.
- Do not add termination until the complete bus topology has been checked. A CAN bus should have termination only at its two physical ends.
- Keep CAN high and low as a twisted pair and provide a common reference.
- Ensure an actuator remains safe during bus-off, duplicate-ID, timeout, and malformed-command conditions.

Example Linux bring-up after confirming the bitrate:

```bash
sudo ip link set can0 down 2>/dev/null || true
sudo ip link set can0 up type can bitrate 1000000 restart-ms 100
ip -details -statistics link show can0
candump can0
```

Do not copy the example 1 Mbit/s value without checking the aircraft configuration.

### 5.3 Position-specific flight-controller auxiliary signal

The attachment PCB labels pin 12 `FMU_CH1`, but that label does not mean every aircraft position reaches flight-controller channel 1. In the source-baseline [Main PCB netlist](https://github.com/Arrow-air/project-quiver/blob/ef316bc9f4e9e001dd5421f8070e54f3180f1600/src/pcb/main_pcb/Quiver_PT3_Main_PCB.net), the position mapping is:

| Position | Main PCB connector | Aircraft-side auxiliary net |
| --- | --- | --- |
| Bottom | `J31` | `FMU_CH1` |
| Side 1 | `J29` | `FMU_CH7` |
| Side 2 | `J30` | `FMU_CH8` |

These are auxiliary flight-controller signals, not general-purpose power pins. Before using one, document:

- signal direction;
- logic voltage and tolerance;
- configured ArduPilot output/function;
- boot, disarmed, failsafe, and lost-link states;
- electrical isolation or buffering;
- the payload's safe behavior if the signal is floating or stale.

Do not connect an inductive load, motor, solenoid, or relay coil directly to an auxiliary signal. Use a protected driver stage and an independently approved power source.

## 6. Payload software integration

Keep flight-critical control on the flight controller. The Raspberry Pi companion may handle perception, logging, data conversion, and non-critical mission logic, but a companion crash must not create an unsafe attachment state.

Choose the simplest data path that meets the requirement:

| Requirement | Recommended path |
| --- | --- |
| High-rate local sensor data | Ethernet payload to companion service |
| Deterministic sensor/actuator messages | DroneCAN on the attachment CAN pair |
| Operator visualization in Quiver Hub | Companion service to a custom payload endpoint |
| Existing telemetry combined into a dashboard | Quiver Hub stream subscription |
| Prototype with clean JSON | Quiver Hub passthrough app |

The [Quiver SDK Developer Guide](./Quiver-SDK-Developer-Guide.md) describes network addresses, companion services, Hub endpoints, custom apps, and service deployment. The [Dev-Kit Engineering Report](../Engineering-Reports/Dev-Kit-Engineering-Report.md) distinguishes the validated terrain-mapping pipeline and existing companion scripts from the planned formal `quiver-sdk` packages, which it says are not yet implemented. Verify each package and endpoint in the target software release rather than treating the SDK architecture as proof of deployment.

The recommended production baseline for an attachment service is to:

- run under `systemd` with bounded restart behavior;
- use an environment file for configuration and secrets;
- expose a local health signal;
- use timeouts and bounded queues;
- rate-limit data sent over the cellular/cloud link;
- log connection state and counters without logging API keys;
- reject commands when the aircraft or payload is not in an allowed state;
- recover cleanly after attachment power cycling.

### 6.1 End-to-end example: Ethernet environmental sensor

This minimal executable reference validates networking and software without depending on unreleased mechanical or power limits. It is an integration example, not production sensor code or a complete attachment package.

1. Select the physical position and its revision-specific harness. This example uses Bottom/J31 and its conventional address `192.168.144.100`; Side 1/J29 conventionally uses `.101`, and Side 2/J30 uses `.102`.
2. Configure the payload with a static `/24` address and no DHCP server. Check the [reserved-address table](./Quiver-SDK-Developer-Guide.md#reserved-addresses-do-not-use) before assignment.
3. Expose deterministic local `/health` and `/data` resources. The following standard-library service returns representative data; replace `read_sample()` with the real, bounded-time sensor driver:

```python
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


def read_sample():
    return {"temperature_c": 23.4, "humidity_percent": 51.2}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body, status = {"status": "ok"}, 200
        elif self.path == "/data":
            body, status = read_sample(), 200
        else:
            body, status = {"error": "not found"}, 404
        encoded = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
```

4. For Linux payloads, a recommended `systemd` template is:

```ini
[Unit]
Description=Quiver environmental sensor
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=quiver-payload
Group=quiver-payload
ExecStart=/usr/bin/python3 /opt/quiver-sensor/sensor_payload.py
Restart=on-failure
RestartSec=2
NoNewPrivileges=true
PrivateTmp=true
ProtectHome=true
ProtectSystem=strict

[Install]
WantedBy=multi-user.target
```

Save the Python block as `sensor_payload.py` and the unit block as `quiver-environment-sensor.service`. On a Debian-family payload computer with `systemd`, install them with:

```bash
getent passwd quiver-payload >/dev/null || \
  sudo useradd --system --user-group --no-create-home --shell /usr/sbin/nologin quiver-payload
sudo install -d -m 0755 -o root -g root /opt/quiver-sensor
sudo install -m 0644 -o root -g root sensor_payload.py \
  /opt/quiver-sensor/sensor_payload.py
sudo install -m 0644 quiver-environment-sensor.service \
  /etc/systemd/system/quiver-environment-sensor.service

sudo systemd-analyze verify /etc/systemd/system/quiver-environment-sensor.service
sudo systemctl daemon-reload
sudo systemctl enable --now quiver-environment-sensor.service
sudo systemctl status --no-pager quiver-environment-sensor.service
```

Inspect logs or stop and remove the example service with:

```bash
sudo journalctl -u quiver-environment-sensor.service -f
sudo systemctl disable --now quiver-environment-sensor.service
```

5. From the Raspberry Pi companion, verify local behavior:

```bash
ping -c 3 192.168.144.100
curl --fail --max-time 2 http://192.168.144.100:8000/health
curl --fail --max-time 2 http://192.168.144.100:8000/data
```

Expected responses are JSON objects such as `{"status": "ok"}` and `{"temperature_c": 23.4, "humidity_percent": 51.2}`. Confirm that unplugging Ethernet, cycling attachment power, restarting the service, and returning malformed sensor data all produce bounded failures and automatic recovery without an unsafe output.

6. To display the data in Quiver Hub, follow [SDK Guide section 9.2](./Quiver-SDK-Developer-Guide.md): create a custom payload endpoint, have a companion-side forwarder read `/data`, and POST the JSON to `/api/rest/payload/{appId}/ingest`. Keep the Hub API key only on the companion, use timeouts and rate limits, and verify the App Builder connection indicator and parsed values.

## 7. Verification gates

### Gate A — Design review

- [ ] Aircraft revision and source commit recorded
- [ ] Position, mass, CG, drag, and clearance reviewed
- [ ] CAD interference and latch travel checked
- [ ] Connector orientation and complete pin map independently reviewed
- [ ] Power/current/inrush budget approved for the target aircraft
- [ ] CAN node ID, bitrate, termination, and failure behavior documented
- [ ] Ethernet address and ports checked for conflicts
- [ ] Software and hardware safe states defined

### Gate B — Unpowered and bench testing

- [ ] Continuity and isolation checked on every contact
- [ ] No short from either 12 V rail to ground or data pairs
- [ ] Attachment starts on a current-limited bench supply
- [ ] Inrush, steady current, and brownout behavior recorded
- [ ] Recommended initial Ethernet or CAN soak test passes for at least 30 minutes; replace this duration if Arrow publishes a formal qualification value
- [ ] Power cycling does not require manual recovery
- [ ] Loss of Ethernet, CAN, and companion process is safe
- [ ] Thermal test completed at representative load

### Gate C — Installed ground test

- [ ] Aircraft is restrained under an approved test procedure
- [ ] Mechanical latch and secondary retention verified
- [ ] Harness has strain relief and cannot enter propeller or latch paths
- [ ] Interface voltage and payload current match bench results
- [ ] No CAN errors, duplicate IDs, or Ethernet address conflicts
- [ ] Flight controller can arm/disarm without payload faults
- [ ] Payload remains safe through relay changes and emergency shutdown

### Gate D — Flight-readiness review

- [ ] Arrow maintainer accepts the test evidence
- [ ] Pilot Handbook and aircraft configuration updated if operator actions changed
- [ ] Initial flight envelope, abort conditions, and observer roles documented
- [ ] First flight uses the minimum-risk site and profile approved by the operator
- [ ] Post-flight fastener, contact, log, and thermal inspection planned

## 8. Troubleshooting

| Symptom | Checks |
| --- | --- |
| Payload is unpowered | Confirm operator relay state, `+12V`/`12VSW` selection, fuse continuity, connector orientation, and ground return |
| Voltage collapses at startup | Disconnect immediately; check polarity, short circuit, inrush, cable drop, fuse, and shared power budget |
| Ethernet link is down | Check static IP, subnet, duplicate address, pair continuity/order, switch link, and payload boot time |
| CAN has no frames | Confirm the target CAN bus, bitrate, node power, high/low polarity, common reference, and termination |
| CAN errors increase | Check duplicate node IDs, extra termination, long stubs, pair untwist, grounding, and EMI sources |
| Auxiliary output is inactive | Verify the position-specific ArduPilot output assignment, disarmed behavior, signal voltage, and that the auxiliary signal is not being treated as power |
| Intermittent operation in vibration | Inspect latch retention, spring-contact contamination/tension, strain relief, and connector alignment |
| Companion service loops or stalls | Check `systemctl status`, `journalctl`, device health, network timeout handling, and bounded restart policy |

## 9. Contribution package

Submit one PR with a reproducible package:

- attachment README with purpose, supported aircraft revision, mass, CG, position, and limitations;
- source CAD and neutral STEP export;
- schematic, PCB source, pin map, and released fabrication files when electronics are included;
- BOM with manufacturer part numbers and approved substitutes;
- software source, dependency lock/version information, install script, and `systemd` unit;
- configuration template with no credentials;
- bench and installed test procedure;
- test results covering power, communications, failures, and thermal behavior;
- photos showing interface orientation, strain relief, and installed clearances;
- operator steps, safe-state description, and rollback/removal procedure.

Link claims to repository sources or manufacturer datasheets. Mark assumptions and unvalidated limits explicitly instead of presenting them as released specifications.

## 10. Guide validation

- [x] Repository-relative links resolve locally
- [ ] Heading anchors verified in the rendered documentation site
- [ ] Documentation website build completed in the publishing repository
- [x] Pin-map entries trace to repository design sources and are labeled provisional
- [x] Mechanical claims link to CAD or manufacturing documentation
- [x] No unconfirmed numeric value is presented as a released interface limit
- [x] Referenced connector part numbers checked against current Molex product information
- [x] Python reference block syntax-checked
- [ ] `systemd` unit copied and verified with `systemd-analyze` on the target Linux distribution
- [ ] Page rendering reviewed on desktop and mobile
- [ ] Maintainer questions tracked to resolution

This repository provides Markdown link and spelling checks but does not contain the complete documentation-site build configuration. Complete the rendering checks in the publishing environment before release.

## 11. Maintainer questions before final release

The following values must be confirmed per aircraft revision and should be promoted into this guide once released:

1. continuous and peak current limits for `+12V` and `12VSW`, per port and in aggregate;
2. maximum mass, bending moment, and CG offset for each interface;
3. released payload CAN bus, bitrate, node-ID allocation policy, and termination topology;
4. electrical levels and standard ArduPilot output assignments for each position's auxiliary signal;
5. approved environmental and vibration qualification levels;
6. whether any attachment revision is explicitly rated for live mating.

## 12. Change impact for pending revisions

| New source | Sections to update |
| --- | --- |
| Released quick-release CAD | 2, 3, source images, and mechanical verification items |
| New Attachment PCB | 1, 3, 4, and the provisional pin map |
| New Main PCB or harness | 1, 2, 4, and 5 |
| Released current limits | 4.2, 7, and 11 |
| Released CAN configuration | 4.1, 5.2, 7, and 11 |
| Released auxiliary-signal specifications | 4.1, 5.3, 7, and 11 |

## 13. Revision history

| Guide version | Hardware baseline | Changes | Status |
| --- | --- | --- | --- |
| 0.1 | Main branch at `ef316bc9f4e9e001dd5421f8070e54f3180f1600`, July 2026 | Initial complete draft and source-to-claim review | Under review |
| 0.1.1 | Same source baseline | Add quick start, scope boundaries, reproducible service setup, precise source links, and change-impact routing | Under review |
| 0.2 | New attachment electrical and mounting-interface revision | Update released geometry, connector views, power limits, CAN, and auxiliary-signal data | Planned |
