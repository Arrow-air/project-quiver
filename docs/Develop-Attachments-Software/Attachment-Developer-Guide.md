# Quiver Attachment Developer Guide

**Version:** July 2026
**Applies to:** Project Quiver PT3 and Quiver Dev-Kit aircraft using the three quick-release attachment interfaces

This guide takes an attachment from concept to a bench-tested, flight-ready integration. It covers the mechanical interface, electrical power, Ethernet, CAN, the flight-controller signal, payload software, and the evidence expected in a contribution.

> **Safety boundary**
>
> The quick-release mechanism is a mechanical feature; it is not permission to connect or remove a powered attachment. Unless a specific aircraft revision has a validated live-mating procedure, disarm the aircraft, isolate propulsive power, switch payload rails off, and verify zero voltage before mating or removing an attachment.

## 1. Start with the correct source revision

Quiver evolves quickly, and some archived documents retain older connector or CAN-bus names. Before designing hardware:

1. Record the aircraft hardware revision and the commit or release used for the design.
2. Use the current [`src/pcb/attach_pcb`](../../src/pcb/attach_pcb/) and [`src/pcb/main_pcb`](../../src/pcb/main_pcb/) design files as the electrical source of truth.
3. Use the [V1.4 Attachment Interface PCB update note](../../task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB/2026-Update/information-note.md) for the current spring-contact construction and orientation mark.
4. Use the [Manufacturing Guide](../Manufacturing/Manufacturing-Guide.md) for aircraft-side interface orientation and harness routing.
5. Ask the Arrow engineering team to confirm the available power budget and payload mass/CG envelope for the specific aircraft before ordering hardware.

The original attachment PCB documentation calls the differential CAN pair `CAN1_P`/`CAN1_N`. Current PT3 Main PCB documentation routes payload ports on `CAN2_H`/`CAN2_L`. Treat these as revision-dependent names for the attachment CAN pair and confirm continuity against the current schematics before wiring.

## 2. Choose an interface position

PT3 provides three aircraft-side quick-release positions:

| Position | Main PCB connector | Recommended payload IP | Typical use |
| --- | --- | --- | --- |
| Bottom | `J31` | `192.168.144.100` | Heavier or nadir-facing payloads, containers, mapping sensors |
| Side 1 | `J29` | `192.168.144.101` | Cameras, compact sensors, light actuators |
| Side 2 | `J30` | `192.168.144.102` | Cameras, compact sensors, light actuators |

The IPs are conventions, not DHCP leases. Any unused address in `192.168.144.100`–`192.168.144.199` may be assigned after checking for conflicts. Do not use the reserved addresses listed in the [Quiver SDK Developer Guide](./Quiver-SDK-Developer-Guide.md#3-network-configuration).

Select a position by considering:

- payload mass, center of gravity, drag, and propeller clearance;
- sensor field of view and electromagnetic interference;
- cable bend radius and strain relief;
- rain path, dust exposure, and drainage;
- access to the release mechanism and fasteners;
- whether an asymmetric side payload requires a counterweight or flight-control validation.

Do not infer an allowable payload mass from the aircraft's total 5–8 kg payload capacity. That figure is an aircraft-level capability, not a per-interface structural rating.

## 3. Mechanical integration

### 3.1 Reuse the released geometry

Build against the released CAD rather than measuring a printed part or marketplace listing. Relevant sources are:

- attachment spacers `2111`/`2121` (left/right) and `2131` (bottom) in the [Manufacturing Guide](../Manufacturing/Manufacturing-Guide.md#2111-2121--2131---attachment-interface-spacers);
- quick-release parts `2112`/`2122`/`2132` in the [Manufacturing Guide](../Manufacturing/Manufacturing-Guide.md#2112-2122--2132---attachment-interfaces);
- the current attachment PCB STEP model in [`src/pcb/attach_pcb`](../../src/pcb/attach_pcb/).

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

The attachment PCB carries one 100BASE-TX Ethernet link, a differential CAN pair, regulated 12 V rails, ground, and one flight-controller auxiliary signal. The V1.4 board replaces the legacy header arrangement with individual spring contacts and enlarged mating pads while retaining the original functions.

### 4.1 Functional pin map

The 12-circuit locking connector used by the attachment PCB is Molex `207760-1281`; the cable-side mating housing is Molex `204523-1201`. The current design files remain authoritative for physical orientation and pin numbering.

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
| 9 | CAN low / legacy `CAN1_N` | Current PT3 aircraft routes the payload bus as CAN2 |
| 10 | `+12V` | Main regulated 12 V payload supply |
| 11 | CAN high / legacy `CAN1_P` | Current PT3 aircraft routes the payload bus as CAN2 |
| 12 | `FMU_CH1` | Flight-controller auxiliary signal; define direction and voltage before use |

This table describes logical connectivity. Verify the connector drawing and schematic before crimping or laying out a mating PCB; never determine pin 1 from a rendered image alone.

### 4.2 Power budget and protection

Before connecting a payload, obtain written confirmation of:

- the continuous and peak current available on `+12V` and `12VSW`;
- whether the quoted limit is per port or shared across all attachment ports;
- fuse rating and population on the exact Main PCB revision;
- allowed inrush current and rail rise/fall behavior;
- whether the payload must remain off until commanded by an operator.

The PT3 Main PCB update notes mention a 2 A fuse upgrade for a switched 12 V output, but that is not a universal payload allowance. Cable gauge, connector contacts, regulator thermal limits, other active payloads, and aircraft configuration may impose a lower limit.

Every attachment should include:

- input fuse or resettable protection sized below the verified port limit;
- reverse-polarity protection where practical;
- transient suppression appropriate for the payload electronics;
- inrush limiting or staged power-up for large capacitive loads;
- local regulation and decoupling;
- a defined safe state if `12VSW`, CAN, Ethernet, or `FMU_CH1` is absent;
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

Use CAN for deterministic low-bandwidth sensors and actuators. Current PT3 payload connectors are intended to operate on CAN2 even though older attachment PCB files use `CAN1_P`/`CAN1_N` net names.

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

### 5.3 `FMU_CH1`

`FMU_CH1` is an auxiliary flight-controller signal, not a general-purpose power pin. Before using it, document:

- signal direction;
- logic voltage and tolerance;
- configured ArduPilot output/function;
- boot, disarmed, failsafe, and lost-link states;
- electrical isolation or buffering;
- the payload's safe behavior if the signal is floating or stale.

Do not connect an inductive load, motor, solenoid, or relay coil directly to `FMU_CH1`. Use a protected driver stage and an independently approved power source.

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

The [Quiver SDK Developer Guide](./Quiver-SDK-Developer-Guide.md) describes network addresses, companion services, Hub endpoints, custom apps, and service deployment. A production attachment service should:

- run under `systemd` with bounded restart behavior;
- use an environment file for configuration and secrets;
- expose a local health signal;
- use timeouts and bounded queues;
- rate-limit data sent over the cellular/cloud link;
- log connection state and counters without logging API keys;
- reject commands when the aircraft or payload is not in an allowed state;
- recover cleanly after attachment power cycling.

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
- [ ] Ethernet or CAN health test passes for at least 30 minutes
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
| CAN has no frames | Confirm target bus is CAN2, bitrate, node power, high/low polarity, common reference, and termination |
| CAN errors increase | Check duplicate node IDs, extra termination, long stubs, pair untwist, grounding, and EMI sources |
| Auxiliary output is inactive | Verify ArduPilot output assignment, disarmed behavior, signal voltage, and that `FMU_CH1` is not being treated as power |
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

## 10. Maintainer questions before final release

The following values must be confirmed per aircraft revision and should be promoted into this guide once released:

1. continuous and peak current limits for `+12V` and `12VSW`, per port and in aggregate;
2. maximum mass, bending moment, and CG offset for each interface;
3. released CAN2 bitrate, node-ID allocation policy, and termination topology;
4. `FMU_CH1` electrical levels and the standard ArduPilot output assignment;
5. approved environmental and vibration qualification levels;
6. whether any attachment revision is explicitly rated for live mating.
