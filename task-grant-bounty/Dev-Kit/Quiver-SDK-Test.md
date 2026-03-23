# Quiver SDK Test Information note

## Status

`Valid: True`

`Revision History: 2025-12-03 – Consolidated Arrow's unified payload/companion SDK discussion and RPLidar C1 terrain mapping documentation.  `

`Replacement Log: None – first canonical information-note for this effort.  `

`Reference: Forum topic “Exploring a Unified Payload and Companion Computer SDK for Quiver” (2025-10-31 onward) and the RPLidar C1 Terrain Mapping System documentation set (README, SETUP_GUIDE, QUICK_REFERENCE, DEPLOYMENT_CONFIG, SYSTEM_SUMMARY).`

---

## Project Description

This project explores and implements a concrete Minimum Viable Product (MVP) for a **unified payload and companion computer SDK for the Quiver UAV platform**, using an **RPLidar C1 terrain-mapping payload** as the primary reference case.

Within the broader Arrow DAO context, Quiver is evolving from a modular UAV into a general-purpose aerial robotics platform. The forum concept envisions:

- A **Payload and Companion Computer SDK** that allows third parties to integrate new sensors, actuators, and modules without modifying core firmware or reverse-engineering protocols.
- An SDK layered on top of **MAVLink/MAVSDK** and related open standards, providing predictable APIs, templates, and code patterns for both flight and payload integration.
- A development paradigm where Quiver is treated as a **“programmable aerial computer”**, enabling onboard applications, autonomous logic, and tight coupling between payloads, the companion computer, and ground control systems.

As an early concrete instantiation of this idea, the RPLidar C1 terrain mapping system demonstrates the **companion-computer-mediated integration path** described in the forum topic:

> (Payload: RPLidar C1 → Raspberry Pi) → (Attachment Interface: Ethernet TCP/UDP) → (Companion Computer: RPi 4/5 with 4G/5G module → HTTP POST) → (Web Portal: Simple Web Server → Simple live web visualization)

The documentation set provided (README, SETUP_GUIDE, QUICK_REFERENCE, DEPLOYMENT_CONFIG, SYSTEM_SUMMARY) describes a **production-ready implementation** of this pipeline:

- The **RPLidar C1** sensor captures 360° scans at ~10 Hz.
- A **Raspberry Pi** handles low-level serial I/O and streams accumulated point clouds via TCP.
- A **companion computer** receives these scans and forwards them to a web server over HTTPS.
- A **web server and browser client** visualize the point cloud in real time via WebSocket.

This implementation serves two primary purposes:

1. **Functional Payload Demonstrator** – Deliver a working end-to-end mapping solution with clear installation, configuration, and troubleshooting guidance.
2. **SDK Architecture Prototype** – Provide a concrete, well-documented example of how payloads, companion computers, and web interfaces can interoperate, informing the design of a generalized Quiver SDK for future payloads (e.g., cameras, rangefinders, flight telemetry displays).

---

## Methodology

### 1. System Architecture and Data Flow

The RPLidar terrain mapping system is structured as a **multi-node pipeline**:

1. **Payload Sensor Layer**
   - Hardware: **SLAMTEC RPLidar C1** lidar sensor.
   - Interface: USB serial, 460800 baud, 8N1.
   - Function: Continuous 360° distance measurements, with packets encoding quality, angle, and distance.

2. **Payload Processor / Edge Streamer (Raspberry Pi)**
   - Role: Dedicated node for real-time sensor interfacing and point cloud generation.
   - Responsibilities:
     - Connects to the RPLidar via `/dev/ttyUSB0` (configurable).
     - Executes the RPLidar C1 library to:
       - Set motor speed (typically 600 RPM).
       - Initiate scanning (`start_scan()`).
       - Accumulate full 360° scans before sending (ensuring dense, non-sparse point clouds).
     - Serializes each complete scan into JSON and streams scans over TCP to the companion computer.
   - Services:
     - `rplidar-streamer.service` (systemd) manages lifecycle and auto-start.
   - Data Format:
     - TCP payloads use a length-prefixed JSON format, carrying `timestamp`, `scan_id`, and an array of points with angle, distance, and quality.

3. **Companion Computer Forwarder**
   - Role: Network and compute hub closer to the Quiver flight controller, aligned with the Arrow DAO vision of a **companion-computer-centered SDK**.
   - Responsibilities:
     - Listens on a configurable TCP port (default 5555) for scan data from the Raspberry Pi.
     - Uses Python with `aiohttp` to forward scans via **HTTP POST** to a web server REST API.
     - Includes API key authentication via `X-API-Key` HTTP header.
     - Uses asynchronous I/O to maintain high throughput (10 Hz scan rate) with low latency (<200 ms).
   - Services:
     - `rplidar-forwarder.service` (systemd) manages the forwarder process and ensures automatic startup and restart.

4. **Web Server and Browser Visualization**
   - Web server provides:
     - REST endpoint `/api/rest/pointcloud/ingest` for ingesting point clouds.
     - WebSocket broadcast channel for pushing data to browsers.
     - A web-based interface (e.g., the referenced “RPLidar Terrain Mapping Visualization” and later the “Quiver Hub” interface) that renders the incoming point cloud in real time.
   - Browser:
     - Subscribes via WebSocket.
     - Renders 360° point clouds at ~10 Hz, showing terrain structure, obstacles, and environment.

This chain directly parallels the SDK architecture path described in the forum discussion and can be generalized for other payloads (camera feeds, flight attitude/position overlays, rangefinder-based visualizations, etc.).

### 2. Deployment and Installation Approach

The documentation set standardizes deployment into **repeatable, script-driven steps**:

1. **Raspberry Pi Installation**
   - Recommended path uses an `install.sh` script in `raspberry_pi/`:
     - Installs Python dependencies (`pyserial`) with appropriate flags.
     - Creates a persistent directory (`~/rplidar_streamer`).
     - Copies `rplidar_c1.py`, `pointcloud_streamer.py`, and related files.
     - Ensures serial permissions (`dialout` group, permissions on `/dev/ttyUSB0`).
     - Installs and enables `rplidar-streamer.service`.

2. **Companion Computer Installation**
   - Similarly scripted via `companion_computer/install.sh`:
     - Installs Python dependencies (`aiohttp`).
     - Creates `~/rplidar_forwarder`.
     - Copies `pointcloud_forwarder.py`, `forwarder.env`, service files.
     - Installs and enables `rplidar-forwarder.service`.
     - Uses the `forwarder.env` file as the single source of truth for TCP port, web server URL, and API key.

3. **Manual Installation**
   - Both Raspberry Pi and companion computer procedures include manual alternatives mirroring the scripted steps (creating directories, copying files, installing systemd units, enabling services) to aid debugging, customization, or environments where scripts are restricted.

4. **Service Management and Operations**
   - Daily operations rely on standard systemd commands:
     - `systemctl status/restart/stop rplidar-streamer`
     - `systemctl status/restart/stop rplidar-forwarder`
   - Real-time logs via `journalctl -u <service> -f` provide live visibility of system behavior, scan counts, and error conditions.

### 3. Configuration, Network Topology, and Environment Variables

A dedicated deployment configuration document defines an explicit **network topology** and associated environment variables:

- **Network Layout (Current Example)**
  - Raspberry Pi: `192.168.144.11`
  - Companion Computer: `192.168.144.15`
  - Web Server: development URL (HTTPS) with specific ingest endpoint.
  - TCP:
    - Raspberry Pi streams to companion computer on port `5555`.
  - HTTPS:
    - Companion computer posts to `/api/rest/pointcloud/ingest` on the web server.

- **Raspberry Pi Configuration**
  - `RPLIDAR_PORT=/dev/ttyUSB0`
  - `RPLIDAR_RPM=600`
  - `TCP_HOST=192.168.144.15`
  - `TCP_PORT=5555`
  - `SCAN_RATE_HZ=10`

- **Companion Computer Configuration (forwarder.env)**
  - `TCP_PORT=5555`
  - `WEB_SERVER_URL=<web_server_url>/api/rest/pointcloud/ingest`
  - `API_KEY=<configured_api_key>`

- **Web Server Configuration**
  - Expects API key in `X-API-Key` header to authenticate ingest requests.
  - Exposes WebSocket channels for browser clients.

- **Firewall and Connectivity**
  - Raspberry Pi: outbound TCP to companion (`5555`) must be allowed.
  - Companion: inbound TCP (`5555`) and outbound HTTPS (port 443).
  - Web server: inbound HTTPS (443) from the companion.

Configuration files (e.g., `forwarder.env`, systemd units) are provided with tested defaults, enabling operators to replicate the **working configuration** reliably across test setups.

### 4. Testing, Troubleshooting, and Validation

The methodology includes embedded validation and troubleshooting procedures:

1. **Network Reachability**
   - `ping` checks between Raspberry Pi and companion.
   - `nc -zv <companion_ip> 5555` from Raspberry Pi to validate TCP connectivity.
   - `curl` POST tests from the companion to the web server ingest endpoint, verifying API key and JSON format.

2. **Service and Log Verification**
   - Continuous `journalctl -u` tailing on both nodes to:
     - Confirm motor startup and scan acquisition on the Raspberry Pi.
     - Confirm scan forwarding and HTTP response codes on the companion.

3. **Expected Log Patterns**
   - Raspberry Pi:
     - Messages indicating connection to `/dev/ttyUSB0`, motor speed setting, scan start, TCP connection establishment, and periodic summaries such as:
       - “Streaming at 10 Hz…”
       - “Sent X scans, Y points total, Z points in last scan.”
   - Companion Computer:
     - “Listening on ('0.0.0.0', 5555)”
     - “Forwarding to <WEB_SERVER_URL>”
     - “Forwarded X scans (0 errors)”

4. **Common Issues and Remedies**
   - **Serial Port Permission Denied**: resolved by adding user to `dialout` and adjusting `/dev/ttyUSB0` permissions.
   - **Motor Not Spinning**: behavior clarified—motor only starts when `start_scan()` is called after setting motor speed and waiting for stabilization.
   - **Sparse Visualization**: mitigated by ensuring the streamer accumulates full 360° scans before transmitting.
   - **Low Data Rate**: diagnosis via network latency, CPU load, and HTTP response times, with wired connections recommended for reliability.

### 5. Alignment with Quiver SDK Vision

The implementation is intentionally structured to **mirror the companion-computer-mediated SDK architecture** described in the forum discussion:

- Uses **standardized data formats (JSON)** with clear fields (`timestamp`, `scan_id`, `points[]` with angle, distance, quality).
- Separates concerns cleanly:
  - Payload interface (sensor + Raspberry Pi).
  - Companion-level orchestration and networking.
  - Web/server level APIs and visualization.
- Provides a concrete testbed for:
  - Mission logic and intelligent behavior running on the companion computer.
  - Higher-bandwidth, high-rate telemetry (point clouds).
  - Integration with web-based dashboards and potential ground station plugins.

This methodology is intended to be **repeatable for other payload types**, serving as a template for future SDK modules.

---

## Results / Findings

### 1. Functional Outcomes

1. **Working End-to-End Terrain Mapping Pipeline**
   - The system achieves:
     - **Scan rate**: Target 10 Hz, typical 8–12 Hz.
     - **Points per scan**: 250–500, with a typical value around 350 points.
     - **End-to-end latency**: Approximately 100–150 ms from acquisition to browser display.
   - Real-time browser visualization provides a continuous 360° point cloud, demonstrating that the pipeline is capable of near-real-time terrain mapping suitable for aerial robotics use.

2. **Robust Deployment and Operations Model**
   - Scripted installations significantly reduce manual configuration steps and potential errors.
   - Systemd integration on both Raspberry Pi and companion computer ensures auto-start on boot, resilience to failures, and standardized log management.
   - The combination of quick-reference commands and detailed setup guidance supports both novice and advanced operators.

3. **Validated Networked Architecture**
   - TCP and HTTPS-based data transport across distinct nodes has been proven viable in a controlled test environment.
   - API-key-based authentication at the web server confirms that secure endpoints can be integrated without compromising ease of use.

### 2. Technical Insights and Constraints

1. **RPLidar C1 Behavior**
   - The motor and scanning control sequence is non-trivial:
     - `set_motor_speed()` alone is insufficient to start the motor.
     - A proper sequence (set speed → wait for stabilization → `start_scan()`) is required for reliable operation.
   - Accumulating complete 360° scans before transmission is key to high-quality visualization; sending partial scans leads to sparse and noisy displays.

2. **Bandwidth and Latency Characteristics**
   - The chosen combination of:
     - Length-prefixed TCP JSON messages.
     - Async HTTP POST forwarding.
     - WebSocket broadcasting.
   - Yields acceptable performance for high-frequency lidar payloads; however, it also highlights potential bottlenecks in:
     - Network quality (wired vs. wireless).
     - Web server throughput.
     - Browser rendering performance under higher-density point clouds.

3. **Configuration Sensitivity**
   - Static IP assignments, port alignment, and consistent environment variable usage are critical.
   - Small misconfigurations (e.g., incorrect IP, port mismatches, outdated API key) manifest as silent failures or intermittent data loss, underscoring the need for:
     - Clear configuration documentation.
     - Simple validation commands for each hop.

4. **Security and Environment Separation**
   - The use of a **development web server URL** and a specific API key indicates that the current system is in a **test/development** state.
   - Production deployment will require:
     - New, securely managed API keys.
     - Stable production domains.
     - Hardened firewall and TLS configurations.

### 3. Alignment with SDK Vision and Open Questions

1. **Evidence of Viability for Companion-Based SDK**
   - The RPLidar terrain mapping pipeline concretely demonstrates:
     - How a payload can be abstracted into a standalone module with clearly defined inputs and outputs.
     - How the companion computer can serve as an **intelligent integration layer**, aligning with the forum’s concept of running mission logic, perception, mapping, and OTA management on the companion.
   - This validates the **“companion-computer-mediated integration”** path as a practical and powerful foundation for an SDK.

2. **Emerging Ecosystem Elements**
   - The forum thread notes:
     - A test GitHub repository for the RPLidar test implementation.
     - A Quiver Hub web interface repository for the visualization front-end.
     - A Quiver Payload Architecture document as a broader architectural reference.
   - Together with the documentation set, these indicate a **growing ecosystem** of components around a unified payload/companion SDK concept.

3. **Unresolved Architectural Questions**
   - The forum explicitly raises several open questions that remain to be fully addressed:
     - Should the SDK remain purely MAVSDK-based, or evolve toward **ROS2** for broader robotics compatibility?
     - Should the companion computer be **standardized hardware** or an **open performance class** that supports multiple options?
     - Can the same framework extend beyond aerial platforms to ground robots, fixed installations, or hybrid systems under a common protocol and network stack?
   - These questions represent important design decisions for the long-term direction of the Quiver SDK.

---

## Next Steps / Recommendations

### 1. Productization and Hardening of the Current MVP

1. **Promote from Development to Staging/Production**
   - Migrate from the current development web server to a stable staging/production environment.
   - Rotate and securely manage API keys:
     - Separate keys for development, staging, and production.
     - Document key rotation procedures and storage best practices.
   - Review and tighten firewall rules, TLS configurations, and access control.

2. **Standardize Configuration Profiles**
   - Define configuration profiles for:
     - Local lab testing.
     - Field trials.
     - Production deployments.
   - Capture these profiles in version-controlled configuration files and environment templates to enable repeatable deployments.

3. **Operational Playbooks**
   - Codify day-to-day operations:
     - Start/stop/restart flows for all services.
     - Recovery procedures after network outages or node restarts.
     - Log inspection guidelines and common error patterns.

### 2. Generalization into a Quiver Payload/Companion SDK

1. **Extract Reusable SDK Components**
   - Identify and refactor:
     - Common data models (e.g., timestamped point clouds, telemetry messages).
     - Transport abstractions (TCP framing, HTTP/REST client, WebSocket integration).
     - Service management patterns (systemd units, environment-based configuration).
   - Package these into reusable libraries or templates for future payload implementations (lidar, cameras, rangefinders, flight telemetry).

2. **Define Stable APIs and Schemas**
   - Specify:
     - Canonical JSON schemas or equivalent message formats for sensor data, actuator commands, and mission events.
     - High-level APIs in Python/C++ for:
       - Telemetry.
       - Mission control.
       - Payload management.
   - Align these schemas and APIs with MAVLink/MAVSDK conventions where appropriate.

3. **Quiver Developer Manual and Reference Image**
   - Develop a **“Quiver Developer Manual”** that:
     - Introduces the SDK architecture.
     - Provides step-by-step guides for building, deploying, and debugging payload modules.
     - Includes example payloads (RPLidar terrain mapping, webcam streaming, rangefinder-based altitude visualizations, flight-attitude dashboard).
   - Build and distribute a **companion computer reference image** with:
     - Pre-installed SDK tools.
     - Standard telemetry routing.
     - Logging, OTA update, and diagnostic utilities.

### 3. Ecosystem and Interface Development

1. **Quiver Hub / Web Interface Evolution**
   - Integrate the lidar visualization into a broader **Quiver Hub** interface that:
     - Hosts multiple payload views (lidar, video, telemetry).
     - Provides mission status, logs, and configuration editing.
   - Define a standard mechanism for modular UI plugins corresponding to SDK payload modules.

2. **Ground Control Integration**
   - Extend existing GCS tools (e.g., Mission Planner, QGroundControl) with plugins that:
     - Discover and list registered Quiver payloads.
     - Expose basic configuration and control surfaces.
     - Link to or embed web-based visualizations.

3. **Developer Ecosystem and Registry**
   - Establish:
     - A public repository (or registry) of verified payload integrations following the SDK guidelines.
     - Contribution standards (code style, documentation, testing).
     - A lightweight certification process for payload modules intended for wider Quiver deployments.

### 4. Future Technical Investigations

1. **ROS2 vs. MAVSDK-Centric Architecture**
   - Perform a focused technical evaluation of:
     - Keeping the SDK purely MAVSDK-based.
     - Introducing ROS2 as a primary or optional compatibility layer.
   - Criteria should include:
     - Ecosystem maturity.
     - Performance characteristics for high-bandwidth payloads.
     - Integration complexity with existing Quiver avionics.

2. **Hardware Abstraction for Companion Computer**
   - Define minimum performance and connectivity requirements for companion computers (CPU, RAM, storage, network interfaces, radio support).
   - Decide whether to:
     - Certify a small set of recommended boards (e.g., RPi 4/5, specific x86 SBCs).
     - Or support a broader set of hardware via a clearly documented compatibility matrix.

3. **Scalability and Multi-Payload Coordination**
   - Extend the current single-lidar pipeline to multi-payload scenarios:
     - Simultaneous lidar + camera payloads.
     - Synchronized data streams for mapping and perception.
     - Coordinated control commands managed by the companion computer.

## References

- Arrow DAO forum topic: **“Exploring a Unified Payload and Companion Computer SDK for Quiver”** – conceptual framing of the Quiver SDK, architecture paths (direct-to-flight-controller and companion-computer-mediated), and example payload chains (including the RPLidar C1 mapping flow).  
  URL: https://dao.arrowair.com/t/exploring-a-unified-payload-and-companion-computer-sdk-for-quiver/138

- **DEPLOYMENT_CONFIG.md – Deployment Configuration**  
  Source for working IP addresses, ports, environment variables, data flow diagrams, performance targets, and troubleshooting notes for the RPLidar terrain mapping system.

- **QUICK_REFERENCE.md – RPLidar Terrain Mapping Quick Reference**  
  Source for condensed installation commands, configuration values, service management commands, testing procedures, expected logs, and performance metrics.

- **README.md – RPLidar C1 Terrain Mapping System Documentation Index**  
  High-level overview of the documentation set, roles of each document (SETUP_GUIDE, QUICK_REFERENCE, DEPLOYMENT_CONFIG, SYSTEM_SUMMARY), and navigation guidance for setup, configuration, and operations.

- **SETUP_GUIDE.md – RPLidar C1 Terrain Mapping System Setup Guide**  
  Complete installation and configuration instructions for Raspberry Pi and companion computer, detailed explanations of environment variables, protocol details (serial, TCP, HTTP), troubleshooting guidance, and library API references for the RPLidar C1 class.

- **SYSTEM_SUMMARY.md – RPLidar C1 Terrain Mapping System Summary**  
  Overview of system purpose, features, contents of the package, system requirements, key performance figures, known issues and solutions, and technical details on protocol and data pipeline implementation.
