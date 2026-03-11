# Quiver SDK Information Note

# Status

`Valid: True`
`Revision History: 2026-01-25 — compiled from Arrow DAO forum discussion and the Quiver SDK developer guide outline.  `
`Replacement Log: TBD  `
`Reference: Quiver SDK Development — Unified Payload + Companion Computer SDK`

# Project Description

Quiver SDK development aims to formalize Quiver as an extensible aerial robotics platform by providing a unified software development kit for both (a) onboard companion computers and (b) modular payload devices. The SDK is intended to let third parties integrate sensors, actuators, and onboard intelligence without modifying flight-controller firmware or reverse-engineering interfaces. The desired outcome is a predictable, repeatable integration surface built on open standards (primarily MAVLink/MAVSDK and DroneCAN/UAVCAN), with common patterns for telemetry ingestion, job dispatch/execution, file distribution, payload data streaming, and operator-facing visualization through Quiver Hub.

Within the Quiver system, a Raspberry Pi-class companion computer functions as the bridge between the flight controller, payload ports (Ethernet and CAN), and Quiver Hub (cloud/web). The SDK’s role is to standardize how this bridge is implemented and extended (templates, APIs, data formats, and reference apps), while enabling an ecosystem of community-built payload “pipelines” and operator UI affordances (e.g., tabs, plugins, and an app-store-like catalog).

# Methodology

## Platform and integration strategy
- Establish a dual-path payload integration model:
  - Direct-to-flight-controller integration for deterministic, low-latency payloads (e.g., via CAN/UART and MAVLink module patterns).
  - Companion-computer-mediated integration for high-bandwidth payloads and advanced onboard compute (perception, mapping, OTA utilities, log management, mission logic).
- Build on open standards:
  - MAVLink/MAVSDK for flight telemetry and control-plane interactions.
  - DroneCAN/UAVCAN for CAN-bus payloads (e.g., battery, rangefinder, sensors).
  - HTTPS REST and WebSocket (or Socket.IO-style streaming) for cloud ingestion and real-time dashboards in Quiver Hub.

## Companion computer reference architecture (software)
- Deliver the SDK primarily as Python tooling targeting Raspberry Pi 4/5-class devices.
- Provide two core reference processes (long-lived services):
  1. Quiver Hub Client: polling-based job execution and file/config synchronization.
  2. Telemetry Forwarder: multi-source telemetry acquisition (MAVLink + DroneCAN) and streaming to Hub at configurable rates.
- Use production-grade operational practices:
  - Systemd units for auto-start, restart-on-failure, and centralized logging.
  - Environment-variable configuration (.env + systemd EnvironmentFile).
  - Structured logging with rotation and clear log-level guidance.

## Data and control interfaces
- Define standardized, versioned message formats for:
  - Flight telemetry snapshots (attitude, position, GPS, battery, mode, armed/in-air flags).
  - Payload sensor data streams (point clouds, camera frames, environmental sensors).
  - Job payload schemas (upload_file, update_config, and extensible custom job types).
- Implement thread-safe aggregation patterns:
  - Concurrent collectors (async iterators for MAVSDK, event handlers for DroneCAN) feeding a shared state protected by locks.
  - A separate transmission loop with rate limiting and buffering/backpressure behavior.

## Developer enablement approach
- Provide templates and example pipelines (MVP payloads first) to validate end-to-end developer experience:
  - LiDAR mapping visualization pipeline.
  - Camera feed pipeline.
  - Flight controller + battery telemetry visualization pipeline.
- Package the SDK repository for reproducible deployment/testing (clear module separation and docs).

# Results / Findings

##  Core SDK scope (companion computer)
- A Python-based SDK layer intended to run on a companion computer and provide standardized access to:
  - Telemetry forwarding (MAVLink + Sensor sources) to Quiver Hub.
  - File management (downloading configs/scripts/firmware from Hub to companion).
  - Remote job execution (Hub-dispatched tasks; extensible job handlers).
  - Payload data and command bridging between Hub and payload devices.

## System architecture and topology
- Companion computer mediates:
  - Cloud link: Companion ↔ Quiver Hub over HTTPS REST + WebSocket-style telemetry delivery.
  - Local Ethernet payload network: Companion ↔ integrated switch ↔ payload ports with static addressing conventions (C1/C2/C3).
  - Local CAN bus: payloads, flight controller, Companion share DroneCAN/UAVCAN connectivity.
- Flight controller remains the MAVLink source of record for core aircraft state, while companion computer aggregates and relays to Hub.

## Reference implementation patterns captured in documentation
- Job queue pattern (Hub creates jobs; companion polls, acknowledges, executes, then completes with status).
- Telemetry forwarding pattern (multi-threaded, multi-source collection; periodic ingestion to Hub REST endpoint; resilience to connectivity loss).
- Extension patterns for:
  - New Payload  (read → normalize → POST ingest endpoint → visualize in Hub).
  - Custom job types (extend client class; implement handler; add routing in process_job).

## Unified SDK concept and ecosystem direction
- The proposed “unified SDK” frames Quiver as a programmable aerial computer:
  - A shared language/API surface across payloads, companion computers, and ground interfaces.
  - Emphasis on templates, high-level APIs via MAVSDK, standardized data/event formats, and reusable example apps.
  - Inclusion of OTA and log management utilities (noted: MAVLink FTP microservice as a prime candidate mechanism).
- MVP payload pipelines developed for early validation:
  - RPLidar C1 → Raspberry Pi → companion forwarder → HTTP POST → web visualization.
  - Siyi A8 Mini → Raspberry Pi → companion forwarder → HTTP POST → Camera feed.
  - Flight controller + Battery telemetry → companion forwarder → HTTP POST → Telemetry display.
- Development progress signals captured:
  - Active efforts to repackage and reformat codebases for deployment/testing (library + streamer + forwarder + docs separation).
  - Identified need for a “REST File Get Client” to support two-way file/data I/O (not only one-way ingestion and manual file placement).
  - Product-facing concept expansion toward a tabbed interface, pipeline selection “app store,” and UI builder for operator dashboards.

# Next Steps / Recommendations

## SDK definition and packaging
- Publish a minimum viable SDK specification:
  - Supported interfaces (MAVSDK, DroneCAN, REST/WebSocket, Peaq On-chain IDs), supported transport patterns, and stability/versioning commitments.
  - Canonical payload pipeline contract (discovery/config, data schema, command routing, health reporting).
- Formalize repository layout and packaging:
  - Separate reusable libraries from reference apps and hardware-specific adapters.
  - Provide installable Python packages, pinned dependency sets, and a companion-computer reference image (or scripted bootstrap) for dev kits.

## Core platform capabilities to implement next
- Two-way file/data synchronization:
  - Implement secure “get/pull” support for remote retrieval of files/config/artifacts initiated by the companion (and/or payload) with audit logging.
- Telemetry and payload streaming hardening:
  - Define buffering/backpressure strategy (drop policy vs. queue growth), offline persistence, and reconnect logic requirements.
- Security and identity model:
  - Standardize API key provisioning, rotation, and scoping (per drone/payload).
  - Add integrity checks for downloaded artifacts (hash/signature) for OTA and configuration updates.
  - Add Unique Drone and User ID System
 - Abstraction and Encapsulation
	 - "import Quiver" esq library with easy function calls
 -  Scalable Quiver Hub Application Multi-user Deployment

## MVP validation plan (developer experience)
- Deliver and document at least three end-to-end example pipelines as acceptance tests:
  1. Flight telemetry + battery telemetry to Hub dashboard (baseline health).
  2. LiDAR point cloud or scan stream to a minimal visualization widget.
  3. Camera feed pipeline with controls and operator UI display.
- Provide a hardware test bill-of-materials and a repeatable test protocol:
  - Include connectivity assumptions (4G/5G modem, Ethernet, CAN setup) and verification steps (candump/mavproxy/curl smoke tests).

## Ground interface evolution
- Decide near-term integration approach:
  - Quiver Hub as the primary web control/visualization plane with a plugin-like model for payload apps.
  - Optional plugins for established GCS tools (Mission Planner/QGroundControl) where operationally required.
- Define “app store” governance model:
  - Packaging format, metadata, certification/testing requirements, and distribution mechanism for community payload pipelines.

# References

- [Arrow DAO forum thread: “Exploring a Unified Payload and Companion Computer SDK for Quiver”](https://dao.arrowair.com/t/exploring-a-unified-payload-and-companion-computer-sdk-for-quiver/138)
- [Quiver SDK Developer Guide Outline (core capabilities, architecture, components, workflows, deployment, best practices, troubleshooting)](https://docs.google.com/document/d/14LEl2I1rTLOXBXKH8iOEXKVzFXmx_lGKYRHIo25UzRY/edit?tab=t.0#heading=h.88pw31x5vqk1)
- [Quiver Payload Architecture](https://docs.google.com/document/d/1piAkRYOBp3DNlqsq-xqWAqSJv4HmXw0SDB0vZK-dyQM/edit?tab=t.0#heading=h.aczyuw2yex2w)
