# Quiver Hub Software

## 1. Status

`Valid: True  `
`Revision History: 2026-02-21`
`Replacement Log: TBD  `
`Reference: Quiver-SDK`

---

## 2. Project Description

Quiver Hub is a modular, cloud-hosted web application that functions as a ground-control and data operations center for the Project Quiver UAV ecosystem. Its purpose is to unify real-time flight and payload telemetry, post-flight analytics, drone configuration management, and developer-extensible “apps” into a single operator interface that can support multiple drones and multiple concurrent data streams.

The platform is designed around a hub-and-spoke concept: a persistent application sidebar enables rapid switching between operational tools (telemetry dashboards, mapping/visualization, camera control, analytics), while an App Store and App Builder framework enables third-party developers to publish custom data-pipeline applications without modifying core Hub code. Quiver Hub is intended to be paired with an onboard companion computer (typically a Raspberry Pi-class system) that relays sensor data and receives command/jobs from Hub, forming a bi-directional control and data plane between aircraft and operators.

---

## 3. Methodology

### 3.1 Architecture and interface strategy
- We implemented a three-tier architecture:
  1) Browser-based frontend for operator workflows and app experiences.  
  2) Node.js server as the API, real-time streaming, parsing, and persistence layer.  
  3) Companion-computer fleet for onboard data acquisition and job execution.
- We separated the system into two primary communication planes:
  - Operator plane (browser ↔ server): typed CRUD operations and configuration management, plus real-time streams for live dashboards.
  - Drone plane (companion ↔ server): authenticated ingestion endpoints for sensor/telemetry data and a reverse-command job queue for remote operations.

### 3.2 Real-time streaming and CRUD control plane
- We used typed RPC for most browser-to-server operations to reduce integration errors and accelerate frontend development (e.g., drone registration, key management, log metadata, app installs).
- We used WebSocket-based streaming for high-frequency live data (telemetry, LiDAR, camera status) to support multi-client subscription patterns and room-based distribution.

### 3.3 Companion-computer integration workflow
- We implemented Python relay services on the companion computer to:
  - Collect telemetry (MAVLink + UAVCAN sources) and post periodic snapshots to Hub ingestion endpoints.
  - Relay payload streams (e.g., LiDAR scans, camera status) to Hub.
  - Poll the Hub for pending jobs, acknowledge them, execute them locally, and report completion status.
- We standardized deployment for companion services using system-level service management (e.g., autostart, restart-on-failure) and structured logging practices.

### 3.4 Extensibility model (App Store + App Builder)
- We designed the platform so that “apps” are first-class entities with:
  - An ingest mode (custom endpoint, stream subscription, or passthrough).
  - An optional server-side parsing step (Python parser sandbox execution) that converts raw payloads into structured schema fields.
  - A UI schema describing operator widgets bound to those fields.
- We implemented app versioning and rollback so that developers can publish updates while retaining the ability to revert to a known-good configuration.

### 3.5 Persistence and artifact storage
- We persisted operational metadata (drones, installs, app definitions, job state, log metadata) in a relational database.
- We stored binary artifacts (flight logs, drone-delivered files, media, notes) in S3-compatible object storage, retaining only metadata and URLs in the database.

### 3.6 Quality and verification approach
- We validated end-to-end workflows using representative pipelines:
  - LiDAR stream → Hub ingest → real-time visualization.
  - Telemetry stream → Hub ingest → dashboard rendering.
  - Camera status/control → Hub relay → operator control loop.
  - Job queue → companion polling → local execution → status reporting.
- We used iterative integration with field operations to ensure that Hub UX, data rates, and job workflows remained usable under real connectivity constraints.


---

## 4. Results / Findings

### 4.1 System Scope and Primary Capabilities
- **Operational dashboarding (real time):**
  - Flight telemetry visualization (attitude, GPS, battery, status).
  - Payload visualization (notably LiDAR point clouds).
  - Camera status monitoring and gimbal command relay.
- **Post-flight tooling:**
  - Client-side flight log parsing (ArduPilot DataFlash) with charts, maps, timeline filtering, log comparison, and summary export.
- **Fleet and connectivity management:**
  - Drone registry and per-drone API key issuance.
  - Connection tests across endpoints.
  - File upload and job dispatch to companion computers.
- **Developer extensibility:**
  - App Store install/uninstall model.
  - App Builder wizard enabling custom ingest endpoints or stream subscriptions.
  - Server-side Python parser execution to transform payloads into structured schema output.
  - Runtime App Renderer that binds UI widgets to live data streams.

### 4.2 Architecture Overview (Three-Tier Model)
Quiver Hub is structured as:
1. **Browser-based frontend (single-page application):**
   - App sidebar navigation and app windows (core apps + installed apps).
   - Real-time subscriptions to streams and per-drone rooms.
2. **Node.js server (API + realtime + storage coordination):**
   - Typed CRUD operations via tRPC over HTTP.
   - REST endpoints intended for companion computer ingestion (authenticated with API keys).
   - Socket.IO server for real-time broadcast and command relay.
   - Database persistence for drones, user app installs, logs, telemetry snapshots, and custom app definitions.
   - S3-compatible object storage integration for large binary artifacts (logs, media, drone-delivered files).
   - Python 3.11 subprocess sandbox for custom payload parsing (App Builder parsers).
3. **Companion computer fleet (on-drone):**
   - Python relay scripts POST sensor payloads to Hub REST ingest endpoints.
   - A polling-based job runner pulls pending jobs (file downloads, config changes, service restarts) from Hub and executes them locally.

### 4.3 Data Flows
Primary flows described by the documentation:
- **Companion → Hub ingestion (REST):** LiDAR scans, telemetry snapshots, camera status, custom app payloads, flight log uploads.
- **Hub → Browser distribution (WebSocket):** Hub broadcasts incoming/parsed data via Socket.IO to subscribed clients (scoped by drone/app/stream rooms).
- **Browser → Hub operations (tRPC):** User-driven CRUD and configuration changes (drone registration, key management, app installation, log management).
- **Hub → Companion commands (job queue):** Operator creates jobs; companion polls, acknowledges, executes, and reports completion/failure.

### 4.4 Applications and UI Modules (Functional Summary)
- **Core navigation sidebar:** Persistent app launcher with core apps, installed apps, and a store entry point.
- **LiDAR Terrain Mapping (core app):**
  - Real-time RPLidar visualization with 2D and 3D views.
  - Demo/synthetic mode for offline UI testing.
  - Scan statistics and connection indicators.
- **Flight Telemetry (core app):**
  - Dashboard panels for attitude, position, GPS state, battery (flight controller and UAVCAN), and flight status.
- **Camera Feed & Gimbal Control (core app):**
  - Camera/gimbal status display.
  - UI controls emitting camera command events that are forwarded to the companion computer.
- **Flight Analytics (core app):**
  - Browser-side DataFlash parsing (no server-side binary parsing requirement).
  - Multiple chart categories (attitude, navigation, power, vibration, radio, EKF).
  - Flight mode timeline with click-to-filter and brush-select zoom.
  - Track map rendering and summary export.
  - Compare mode for side-by-side log analysis.
- **Drone Configuration (admin utility):**
  - Drone registry and API key lifecycle controls.
  - Connection test tooling.
  - File upload and job dispatch management.
  - Generation of configuration snippets for companion relay setup.
- **Logs & OTA Updates (indicated/future):**
  - UI placeholder present; backend job/file mechanisms described as foundational.
- **Mission Planner (indicated/future):**
  - UI placeholder present; mapping component indicated in codebase.

### 4.5 Backend Interfaces (Conceptual Contract)
- **tRPC routers:** Auth, pointcloud, telemetry, drones, droneJobs, flightLogs, appBuilder, and app management procedures.
- **REST endpoints (for companion computers):**
  - Health and connection checks.
  - Ingest endpoints for point clouds, telemetry, camera status, custom payloads.
  - Flight log upload endpoint.
- **WebSocket events (Socket.IO):**
  - Room subscription controls (subscribe/unsubscribe patterns).
  - Stream broadcasts (pointcloud, telemetry, camera_status, app_data).
  - Companion registration event and camera command relay.

### 4.6 Persistence and Storage Model
- **Relational database (MySQL / TiDB indicated):**
  - Users, drones, API keys.
  - Telemetry snapshots and scan metadata.
  - Custom app definitions, versions, installation state, and app data records.
  - Drone job queue state and file metadata.
  - Flight log metadata and related notes/media pointers.
- **S3-compatible object storage:**
  - Drone-delivered files (scripts/configs) and flight logs (binary).
  - Notes and media attached to logs.
  - Database stores metadata and URLs rather than file bytes.

### 4.7 Authentication and Authorization
- **User plane:** OAuth-based login with session cookies; role model indicated (user/admin).
- **Drone plane:** Per-drone API keys used to authenticate companion computer REST ingest operations; key lifecycle managed from the configuration UI.

### 4.8 Implementation Status
- Implemented: LiDAR app, telemetry dashboard, camera status/control relay, flight analytics, drone configuration, App Store, App Builder, App Renderer, app versioning/rollback, job queue, REST ingest endpoints, core realtime streaming.
- Indicated/placeholder: Logs & OTA UI, Mission Planner UI, and select analytics enhancements.

---

## 5. Next Steps / Recommendations


1. **Documentation alignment and versioning**
   - Establish a single “current architecture” location and a versioning convention (tagged releases or dated architecture snapshots).
   - Update top-level README content to match the February 2026 architecture reference and current operational status.

2. **Logs & OTA UI, Mission Planner UI**
   - Mission Planner and Lags & OTA Application Buildout

3. **Generalise Implementation Away from Manus**
   - Mirgate System from Manus to standalone deployment


4. **Multi-user / fleet scaling readiness**
   - Confirm database migration strategy and operational tooling (backups, schema migration workflows).
   - Validate tenant/user app installation isolation (per-user vs. global installs) against intended deployment model.

---

## 6. Attachments / References

### Provided Files (uploaded)
- [Project_Quiver_Comprehensive_Report.docx (February 2026)](https://docs.google.com/document/d/1PV6ZbxMznKGOcB-1apQRKTJj1SvPWsqL/edit?usp=drive_link&ouid=100810036488839960524&rtpof=true&sd=true)— includes Quiver Hub overview as part of Project Quiver “Software Platform and SDK”.
- [quiver-hub-architecture.md (February 2026)](https://drive.google.com/file/d/1SRoIoOvWjVlcZD9T3QRP-PfCDkmZqkid/view?usp=sharing) — “Quiver Hub — Architecture & Feature Reference”, including UI apps, backend endpoints, database tables, and companion workflows.
- GitHub repository (dev branch): https://github.com/Pan-Robotics/Quiver-Hub/tree/dev