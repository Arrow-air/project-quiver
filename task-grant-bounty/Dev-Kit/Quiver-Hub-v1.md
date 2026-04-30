# Information Note — Quiver Hub Software / Quiver Hub V1 M1–M3

## 1. Status

`Valid`

**Revision History:** 2026-02-21  
**Replacement Log:** TBD  
**Reference:** None

## 2. Subject

Work completed in fulfilment of the Quiver Hub Software development stream and the Quiver Hub V1 Grant, including Milestones M1–M3.

## 3. Project Description

Quiver Hub is a modular, cloud-hosted web application that functions as a ground-control and data operations centre for the Project Quiver UAV ecosystem. Its purpose is to unify real-time flight and payload telemetry, post-flight analytics, drone configuration management, companion-computer job execution, file/log handling, OTA update handling, and developer-extensible apps into a single operator interface that can support multiple drones and multiple concurrent data streams.

The platform is designed around a hub-and-spoke concept. A persistent application sidebar enables rapid switching between operational tools, including telemetry dashboards, mapping/visualisation, camera control, analytics, logs, OTA workflows, diagnostics, remote logs, and installed custom applications. Alongside this, the App Store and App Builder framework allow third-party or project-specific developers to publish custom data-pipeline applications without modifying the core Hub code.

Quiver Hub is intended to be paired with an onboard companion computer, typically a Raspberry Pi-class system. The companion computer relays telemetry and payload data to the Hub, receives commands or jobs from the Hub, and acts as the bridge between the aircraft, the operator interface, and any payload or onboard services. This creates a bidirectional control and data plane between the aircraft and operators.

For the M1–M3 grant phase, I focused on delivering the first practical operational core of Quiver Hub V1 by closing the most immediate gaps needed to make the Hub usable for real operational workflows. The milestone scope covered:

- **M1: Hub Security Baseline**  
  I established the initial job-security and artefact-integrity foundations for the Hub.

- **M2: Logs v1 Module**  
  I built the first working log retrieval and handling flow between the flight controller, the companion computer, and the Hub UI.

- **M3: OTA v1 Module**  
  I built the first firmware upload, validation, staging, dispatch, and flashing flow for remote update operations.

## 4. Methodology

### 4.1 Architecture and interface strategy

I implemented Quiver Hub around a three-tier architecture:

1. **Browser-based frontend** for operator workflows, app experiences, real-time dashboards, configuration tools, logs, OTA workflows, analytics, and custom app rendering.
2. **Node.js server** as the API, real-time streaming, parsing, persistence, job orchestration, and storage-coordination layer.
3. **Companion-computer fleet** for onboard data acquisition, telemetry relay, payload relay, and job execution.

I separated the system into two primary communication planes:

- **Operator plane: browser ↔ server**  
  This handles typed CRUD operations, configuration management, app installation, log metadata, firmware management, and live dashboard subscriptions.

- **Drone plane: companion ↔ server**  
  This handles authenticated ingestion endpoints for sensor and telemetry data, file/log uploads, and a reverse-command job queue for remote operations.

### 4.2 Real-time streaming and CRUD control plane

I used typed RPC for most browser-to-server operations to reduce integration errors and accelerate frontend development. This pattern supports drone registration, API key management, log metadata, app installation, firmware operations, and other configuration workflows.

I used WebSocket-based streaming for high-frequency live data, including telemetry, LiDAR data, camera status, and app data. This supports multi-client subscription patterns and room-based distribution, allowing Hub clients to subscribe to specific drones, applications, or streams.

### 4.3 Companion-computer integration workflow

I implemented companion-computer relay services to:

- collect telemetry from MAVLink and UAVCAN sources and post periodic snapshots to Hub ingestion endpoints;
- relay payload streams, including LiDAR scans and camera status, to the Hub;
- poll the Hub for pending jobs;
- acknowledge jobs;
- execute jobs locally;
- and report completion or failure status back to the Hub.

I standardised deployment for companion services using system-level service management, including autostart, restart-on-failure behaviour, and structured logging practices.

### 4.4 Job-based execution model

For the Logs v1 and OTA v1 work, I used a job-based execution model in which the Hub dashboard dispatches work through the backend, and the Raspberry Pi companion polls, acknowledges, and executes those jobs against the flight controller and related subsystems.

This gave me a consistent way to implement both log-handling and OTA workflows while also creating the basis for future security and permission hardening.

The job queue model also supports broader Hub operations, including file downloads, configuration changes, service restarts, firmware flashing, and other remote companion-computer actions.

### 4.5 Extensibility model: App Store and App Builder

I designed the platform so that apps are first-class entities. Each app can define:

- an ingest mode, such as a custom endpoint, stream subscription, or passthrough mode;
- an optional server-side parsing step, using Python parser sandbox execution to convert raw payloads into structured schema fields;
- and a UI schema describing operator widgets bound to those fields.

I implemented app versioning and rollback so that developers can publish updates while retaining the ability to revert to a known-good configuration.

### 4.6 Persistence and artefact storage

I persisted operational metadata in a relational database. This includes users, drones, API keys, installs, app definitions, app versions, app installation state, job state, log metadata, telemetry snapshots, scan metadata, and file metadata.

I stored binary artefacts in S3-compatible object storage. This includes flight logs, drone-delivered files, scripts, configuration files, notes, media, and other large binary artefacts. The database retains metadata and URLs rather than storing large file bytes directly.

### 4.7 Quality and verification approach

I validated end-to-end workflows using representative pipelines, including:

- LiDAR stream → Hub ingest → real-time visualisation;
- telemetry stream → Hub ingest → dashboard rendering;
- camera status/control → Hub relay → operator control loop;
- job queue → companion polling → local execution → status reporting;
- FC log scan/download → companion retrieval → Hub storage → browser download or analytics forwarding;
- firmware upload → hash generation → flash job dispatch → companion-side verification → FC flash flow.

I used iterative integration with field operations to ensure that the Hub user experience, data rates, and job workflows remained usable under real connectivity constraints.

## 5. System Scope and Primary Capabilities

### 5.1 Operational dashboarding

I implemented real-time operational dashboarding for:

- flight telemetry visualisation, including attitude, GPS, battery, and status;
- payload visualisation, notably LiDAR point clouds;
- camera status monitoring;
- and gimbal command relay.

### 5.2 Post-flight tooling

I implemented post-flight tooling for client-side ArduPilot DataFlash log parsing. This includes:

- charts;
- maps;
- timeline filtering;
- log comparison;
- summary export;
- multiple chart categories, including attitude, navigation, power, vibration, radio, and EKF;
- flight mode timeline with click-to-filter and brush-select zoom;
- track map rendering;
- and compare mode for side-by-side log analysis.

### 5.3 Fleet and connectivity management

I implemented fleet and connectivity management capabilities, including:

- drone registry;
- per-drone API key issuance;
- API key lifecycle controls;
- connection tests across endpoints;
- file upload;
- job dispatch to companion computers;
- and generation of configuration snippets for companion relay setup.

### 5.4 Developer extensibility

I implemented the developer extensibility layer through:

- App Store install/uninstall model;
- App Builder wizard;
- custom ingest endpoints;
- stream subscriptions;
- server-side Python parser execution;
- transformation of payloads into structured schema output;
- Runtime App Renderer;
- UI widgets bound to live data streams;
- app versioning;
- and rollback support.

## 6. Architecture Overview

### 6.1 Browser-based frontend

The browser-based frontend is a single-page application that provides:

- app sidebar navigation;
- app windows for core apps and installed apps;
- real-time subscriptions to streams and per-drone rooms;
- operational dashboards;
- app experiences;
- logs and OTA interfaces;
- drone configuration tools;
- flight analytics;
- and runtime rendering for custom apps.

### 6.2 Node.js server

The Node.js server acts as the API, real-time, parsing, storage, and orchestration layer. It provides:

- typed CRUD operations through tRPC over HTTP;
- REST endpoints for companion-computer ingestion, authenticated with API keys;
- Socket.IO server for real-time broadcast and command relay;
- database persistence for drones, users, API keys, app installs, logs, telemetry snapshots, scan metadata, custom app definitions, app data records, job state, and file metadata;
- S3-compatible object storage integration for large binary artefacts, including logs, media, notes, and drone-delivered files;
- and a Python 3.11 subprocess sandbox for custom payload parsing in App Builder workflows.

### 6.3 Companion-computer fleet

The companion-computer fleet runs onboard relay and job-runner services. These services:

- POST sensor payloads to Hub REST ingestion endpoints;
- relay MAVLink and UAVCAN telemetry snapshots;
- relay LiDAR scans, camera status, and custom app payloads;
- poll for pending jobs;
- acknowledge jobs;
- execute local tasks;
- and report completion or failure.

## 7. Data Flows

The primary system data flows are:

- **Companion → Hub ingestion via REST:** LiDAR scans, telemetry snapshots, camera status, custom app payloads, and flight log uploads.
- **Hub → Browser distribution via WebSocket:** Incoming or parsed data is broadcast through Socket.IO to subscribed clients, scoped by drone, app, or stream rooms.
- **Browser → Hub operations via tRPC:** User-driven CRUD and configuration changes, including drone registration, key management, app installation, log management, firmware management, and configuration workflows.
- **Hub → Companion commands via job queue:** Operators create jobs; the companion polls, acknowledges, executes, and reports completion or failure.

## 8. Applications and UI Modules

### 8.1 Core navigation sidebar

I implemented a persistent app launcher with core apps, installed apps, and a store entry point.

### 8.2 LiDAR Terrain Mapping

I implemented the LiDAR Terrain Mapping core app with:

- real-time RPLidar visualisation;
- 2D and 3D views;
- demo/synthetic mode for offline UI testing;
- scan statistics;
- and connection indicators.

### 8.3 Flight Telemetry

I implemented the Flight Telemetry core app with dashboard panels for:

- attitude;
- position;
- GPS state;
- battery, including flight-controller and UAVCAN battery sources;
- and flight status.

### 8.4 Camera Feed and Gimbal Control

I implemented the Camera Feed and Gimbal Control core app with:

- camera/gimbal status display;
- UI controls for camera commands;
- and command forwarding from the Hub to the companion computer.

### 8.5 Flight Analytics

I implemented the Flight Analytics core app with:

- browser-side DataFlash parsing, without requiring server-side binary parsing;
- multiple chart categories, including attitude, navigation, power, vibration, radio, and EKF;
- flight mode timeline;
- click-to-filter behaviour;
- brush-select zoom;
- track map rendering;
- summary export;
- and compare mode for side-by-side log analysis.

### 8.6 Drone Configuration

I implemented the Drone Configuration admin utility with:

- drone registry;
- API key lifecycle controls;
- connection test tooling;
- file upload;
- job dispatch management;
- and generation of configuration snippets for companion relay setup.

### 8.7 App Store, App Builder, and App Renderer

I implemented:

- App Store install/uninstall model;
- App Builder wizard;
- custom ingest endpoints;
- stream subscriptions;
- server-side Python parser execution;
- app versioning;
- rollback;
- and Runtime App Renderer for binding widgets to live data streams.

### 8.8 Logs and OTA Updates

The earlier Quiver Hub Software status described Logs and OTA as indicated or placeholder areas with backend job/file mechanisms already present as foundations. In the M1–M3 phase, I then built out the Logs v1 and OTA v1 functionality into operational workflows, including UI, backend routes, companion-side handling, artefact storage, and job execution.

### 8.9 Diagnostics and Remote Logs

As part of the operational tooling associated with Logs and OTA, I delivered dedicated views for:

- FC Logs;
- OTA Updates;
- Diagnostics;
- and Remote Logs.

### 8.10 Mission Planner

Mission Planner remains an indicated/future area, with a UI placeholder present and mapping component indicated in the codebase. Further development could implement comprehensive mission planning, including autonomous path planning and control as a later milestone.

## 9. Backend Interfaces

### 9.1 tRPC routers

The conceptual backend contract includes tRPC routers for:

- auth;
- pointcloud;
- telemetry;
- drones;
- droneJobs;
- flightLogs;
- appBuilder;
- app management;
- log-management workflows;
- firmware-management workflows;
- and diagnostics or remote-log workflows.

### 9.2 REST endpoints for companion computers

The REST endpoint layer supports:

- health and connection checks;
- point cloud ingest;
- telemetry ingest;
- camera status ingest;
- custom payload ingest;
- flight log upload;
- firmware or file retrieval flows where needed;
- and companion-computer authenticated communication using per-drone API keys.

### 9.3 WebSocket events

The WebSocket layer supports:

- room subscription controls;
- subscribe/unsubscribe patterns;
- stream broadcasts for pointcloud, telemetry, camera_status, and app_data;
- companion registration events;
- and camera command relay.

## 10. Persistence, Storage, Authentication, and Authorization

### 10.1 Relational database

I used relational database persistence, with MySQL / TiDB indicated, for:

- users;
- drones;
- API keys;
- telemetry snapshots;
- scan metadata;
- custom app definitions;
- app versions;
- installation state;
- app data records;
- drone job queue state;
- file metadata;
- flight log metadata;
- and related notes/media pointers.

### 10.2 S3-compatible object storage

I used S3-compatible object storage for:

- drone-delivered files;
- scripts;
- configuration files;
- flight logs;
- binary media;
- notes;
- and other large artefacts.

The database stores metadata and URLs rather than file bytes.

### 10.3 User-plane authentication and authorization

For the user plane, I used OAuth-based login with session cookies. A role model is indicated, including user/admin roles.

### 10.4 Drone-plane authentication

For the drone plane, I used per-drone API keys to authenticate companion-computer REST ingestion operations. The key lifecycle is managed from the configuration UI.

## 11. M1–M3 Grant Delivery

### 11.1 M1: Hub Security Baseline

I carried out and documented a formal job-security analysis covering:

- artefact integrity;
- job allow-listing;
- job reliability;
- and job permissions.

From that work, I implemented the most immediately critical security foundations needed for the M1–M3 phase.

A key result was the introduction of firmware artefact integrity verification. I made the Hub compute and store a SHA-256 hash when firmware is uploaded, pass that hash through the `flash_firmware` job payload, and verify it on the companion before any flashing takes place. If the hash does not match, the flash is aborted and the temporary file is cleaned up.

I also implemented the job reliability layer, including:

- retry handling;
- expiry behaviour;
- timeout reaping;
- locking / mutex protections;
- and cleanup behaviour for stuck or failed work.

Some elements of the job-security pipeline, particularly job allow-listing and job permissions, were intentionally left as planned follow-on work. This was not because they were overlooked, but because they are more appropriately completed as part of the next stage of platform development alongside the broader Quiver SDK / quiver-hub integration layer, rather than being forced prematurely into the M1–M3 delivery window.

### 11.2 M2: Logs v1

I built the first complete FC-to-companion-to-Hub logs pipeline.

On the companion side, I implemented a three-tier strategy for log access:

- check local cache first;
- attempt HTTP access to FC logs;
- and fall back to FTP / MAVFTP-style retrieval where needed.

On the Hub side, I built the supporting routes and UI flows needed to make this usable from the dashboard.

Within the logs flow, I enabled users to:

- trigger scan jobs;
- browse discovered logs;
- request downloads from the flight controller;
- store retrieved logs in the Hub;
- download them through the browser;
- and forward completed logs into analytics workflows.

This moved the Hub from being a conceptual control surface toward a working operational tool for handling real flight data.

### 11.3 M3: OTA v1

I built the first operational OTA firmware workflow for Quiver Hub.

This included:

- firmware upload;
- firmware record creation;
- SHA-256 hashing;
- job dispatch for flashing;
- staged delivery through the companion;
- and the flash request flow to the flight controller.

The OTA flow was designed around a staged and validated process rather than ad hoc manual update handling. The companion downloads the firmware artefact, verifies its integrity, extracts metadata, temporarily serves the artefact where needed for the flight-controller-side pull flow, and then completes the flash-and-reboot sequence.

I also built the Hub-side management functions needed to support this flow, including:

- listing firmware;
- uploading firmware;
- requesting flash jobs;
- and clearing failed firmware records.

## 12. Implementation Status

### 12.1 Implemented platform capabilities

The following platform capabilities have been implemented:

- LiDAR app;
- telemetry dashboard;
- camera status/control relay;
- flight analytics;
- drone configuration;
- App Store;
- App Builder;
- App Renderer;
- app versioning and rollback;
- job queue;
- REST ingest endpoints;
- core real-time streaming;
- companion-computer relay workflows;
- drone registry and API key lifecycle;
- file upload and job dispatch;
- client-side flight log parsing;
- browser-side dashboards and app windows;
- authenticated companion-computer ingestion;
- Logs v1 operational workflow;
- OTA v1 operational workflow;
- Diagnostics view;
- Remote Logs view;
- artefact integrity verification;
- job reliability hardening;
- and Hub-side job/API scaffolding for log-handling and firmware-handling workflows.

### 12.2 Indicated, planned, or future capabilities

The following areas remain indicated, planned, or suitable for further development:

- Mission Planner UI;
- comprehensive mission planning;
- autonomous path planning and control;
- wider job allow-listing hardening;
- wider job permissions hardening;
- select analytics enhancements;
- further SDK formalisation;
- further SDK encapsulation;
- functional expansion for easier payload deployment;
- migration from Manus to standalone deployment;
- local individual-system deployment strategy;
- hosted scalable SaaS deployment strategy;
- multi-user and fleet scaling readiness;
- documentation alignment and versioning;
- and database migration / backup / operational tooling.

## 13. Results and Deliverables

Through the Quiver Hub Software work and the M1–M3 grant phase, I delivered the first practical operational core of Quiver Hub V1.

Specifically, I delivered:

- a modular, cloud-hosted Quiver Hub operator interface;
- a three-tier architecture covering browser frontend, Node.js backend, and companion-computer fleet;
- typed browser-to-server operations;
- REST-based companion-computer ingestion;
- WebSocket-based real-time distribution;
- drone registry and per-drone API key management;
- LiDAR Terrain Mapping;
- Flight Telemetry dashboards;
- Camera Feed and Gimbal Control;
- Flight Analytics with browser-side DataFlash parsing;
- Drone Configuration admin utility;
- App Store;
- App Builder;
- Runtime App Renderer;
- app versioning and rollback;
- relational persistence for operational metadata;
- S3-compatible storage for large binary artefacts;
- companion-computer relay and job execution services;
- documented and partially implemented security baseline;
- artefact integrity verification;
- job reliability protections;
- working Logs v1 pipeline for scan, discovery, retrieval, storage, browser download, and analytics forwarding;
- working OTA v1 foundation for firmware upload, hashing, staged delivery, dispatch, and flash execution;
- frontend operational tooling covering FC Logs, OTA Updates, Diagnostics, and Remote Logs;
- and Hub-side job and API scaffolding needed to support the log-handling and firmware-handling workflows.

## 14. Remarks

This phase should be understood as the delivery of the first operational core of Quiver Hub V1, not the completion of the entire long-term Hub / SDK architecture.

What I completed in M1–M3 was the most immediately valuable and practical slice of work needed to make the Hub materially functional: security foundations, logs handling, and OTA handling.

Where parts of the security pipeline remain marked as planned, that should be understood as a deliberate sequencing decision. I identified those items at this stage, but they are more appropriately completed in the next layer of platform maturation alongside the wider Quiver SDK / quiver-hub development path.

Further development of Quiver Hub could implement comprehensive mission planning, including autonomous path planning and control as M4. This could then lead into multiple deployment strategies, including a local individual-system deployment and a hosted scalable SaaS platform as M5.

Beyond these stages, further development should continue SDK formalisation, SDK encapsulation, and functional expansion to make payload deployment easier.

## 15. Next Steps / Recommendations

### 15.1 Documentation alignment and versioning

I recommend establishing a single current architecture location and a versioning convention, using tagged releases or dated architecture snapshots.

I also recommend updating the top-level README content to match the February 2026 architecture reference and the current operational status of the Hub.

### 15.2 Mission Planner and Logs / OTA application buildout

I recommend continuing the Mission Planner application buildout, including comprehensive mission planning, autonomous path planning, and control.

The Logs and OTA application area has now moved beyond placeholder status through the M1–M3 work, but it should continue to be refined as part of broader operational hardening.

### 15.3 Generalise implementation away from Manus

I recommend migrating the system from Manus-bound implementation assumptions toward standalone deployment, so that the Hub can be deployed, maintained, and scaled independently.

### 15.4 Multi-user and fleet scaling readiness

I recommend confirming the database migration strategy and operational tooling, including backups and schema migration workflows.

I also recommend validating tenant/user app installation isolation, including per-user versus global installs, against the intended deployment model.

### 15.5 Deployment strategy

I recommend developing both:

- a local individual-system deployment model;
- and a hosted scalable SaaS platform model.

These two paths would allow Quiver Hub to serve both tightly controlled local deployments and broader fleet/operator deployments.

### 15.6 SDK maturation

I recommend continuing the Quiver SDK development path, including:

- SDK formalisation;
- SDK encapsulation;
- clearer developer interfaces;
- payload deployment support;
- and tighter alignment between Quiver Hub, companion-computer workflows, and the SDK integration layer.

## 16. Attachments / References

- [Project_Quiver_Comprehensive_Report.docx (February 2026)](https://docs.google.com/document/d/1PV6ZbxMznKGOcB-1apQRKTJj1SvPWsqL/edit?usp=drive_link&ouid=100810036488839960524&rtpof=true&sd=true) — includes Quiver Hub overview as part of Project Quiver “Software Platform and SDK”.
- [quiver-hub-architecture.md (February 2026)](https://drive.google.com/file/d/1SRoIoOvWjVlcZD9T3QRP-PfCDkmZqkid/view?usp=sharing) — Quiver Hub architecture and feature reference, including UI apps, backend endpoints, database tables, and companion workflows.
- [Quiver Hub repository, dev branch](https://github.com/Pan-Robotics/Quiver-Hub/tree/dev)
- [Quiver Hub Information Note](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/Dev-Kit/Quiver-Hub-Software.md)
- [Quiver SDK Information Note](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/Dev-Kit/Quiver-SDK.md)
- [Quiver SDK Test Information Note](https://github.com/Arrow-air/project-quiver/blob/main/task-grant-bounty/Dev-Kit/Quiver-SDK-Test.md)
- [Job Security Analysis](https://github.com/Pan-Robotics/Arrow-Quiver-Hub/blob/main/docs/JOB_SECURITY_ANALYSIS.md)
- [Logs OTA Pipeline](https://github.com/Pan-Robotics/Arrow-Quiver-Hub/blob/main/docs/LOGS_OTA_PIPELINE.md)
- [Quiver SDK Repo](https://github.com/Arrow-air/quiver-sdk)
