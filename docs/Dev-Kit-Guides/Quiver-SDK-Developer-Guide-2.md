# Quiver SDK Developer Guide

**Version:** April 2026

---

## 1. System Overview

Quiver Hub is a cloud-hosted web application that provides real-time visualization, remote management, and data logging for UAV operations. The companion computer (Raspberry Pi) runs Python services that bridge the flight controller, payload devices, and Hub over HTTPS and WebSocket. Operators interact through the Hub web UI; the companion computer handles all local hardware communication and data forwarding autonomously.

The system supports five concurrent data pipelines: telemetry (MAVLink + UAVCAN), point cloud (LiDAR), camera (WebRTC via go2rtc), FC logs and OTA firmware, and custom payload apps. Each pipeline has a dedicated companion service, REST endpoint, and WebSocket broadcast channel.

---

## 2. Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        QUIVER HUB (Cloud)                       │
│  React UI · tRPC · REST API · Socket.IO · S3 · TiDB            │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTPS / WSS (cellular or WiFi)
┌──────────────────────────┴──────────────────────────────────────┐
│              COMPANION COMPUTER  (Raspberry Pi)                  │
│  192.168.144.50                                                  │
│                                                                  │
│  Services:                                                       │
│    raspberry_pi_client.py   — Job polling & file delivery        │
│    telemetry_forwarder.py   — MAVLink + UAVCAN → Hub            │
│    logs_ota_service.py      — FC logs, OTA, diagnostics          │
│    camera_stream_service.py — go2rtc + Tailscale stream mgmt     │
│    siyi_camera_controller.py— Gimbal control (SIYI UDP SDK)      │
│                                                                  │
│  Connects to FC via Ethernet (MAVLink) and CAN bus (DroneCAN)    │
└──────────┬──────────────────────────────┬───────────────────────┘
           │ Ethernet                     │ CAN bus
┌──────────┴──────────┐     ┌─────────────┴───────────────────────┐
│  FLIGHT CONTROLLER  │     │  PAYLOAD PORTS (C1 / C2 / C3)       │
│  192.168.144.51     │     │  Ethernet: 192.168.144.100–.199     │
│  ArduPilot + Lua    │     │  CAN: DroneCAN protocol             │
│  net_webserver.lua  │     │  Sensors, cameras, actuators        │
│  (port 8080)        │     └─────────────────────────────────────┘
└─────────────────────┘
```

---

## 3. Network Configuration

The Quiver network is flat — no DHCP runs on the Pi (Siyi firmware conflicts with DHCP servers). All IPs are static on the `192.168.144.0/24` subnet.

### Reserved Addresses (Do Not Use)

| IP | Device |
|---|---|
| 192.168.144.11 | Siyi air unit |
| 192.168.144.12 | Siyi ground unit |
| 192.168.144.20 | Android GCS (Siyi reserved) |
| 192.168.144.25 | Siyi A8 Mini camera |
| 192.168.144.60 | Siyi camera reserved |
| 192.168.144.50 | Raspberry Pi (companion computer) |
| 192.168.144.51 | Flight controller |

### Payload Port Assignments

Developer-assigned static range: `192.168.144.100` – `192.168.144.199`

| Port | Recommended IP |
|---|---|
| Bottom (J31) | 192.168.144.100 |
| Side 1 (J29) | 192.168.144.101 |
| Side 2 (J30) | 192.168.144.102 |

### Key Connections

| Path | Protocol | Details |
|---|---|---|
| Companion → Hub | HTTPS + WSS | REST API, Socket.IO (cellular/WiFi) |
| Companion → FC | Ethernet (MAVLink) | `192.168.144.51`, also CAN bus for DroneCAN |
| Companion → FC Web Server | HTTP | `http://192.168.144.51:8080` (net_webserver.lua, FC log access) |
| Companion → Payloads | Ethernet | `192.168.144.100–.199` via integrated switch |
| Companion → Siyi Camera | Ethernet | `192.168.144.25` (RTSP stream + UDP SDK) |
| Mission Planner → FC | RF telemetry | 915 MHz / 433 MHz radio (MAVLink) |

---

## 4. Companion Services

All services run as systemd units, auto-restart on failure, and log to journald. Configuration lives in `$HOME/quiver/forwarder.env`.

### 4.1 Hub Client (`raspberry_pi_client.py`)

Polls Hub for pending jobs every 5 seconds, executes them locally, reports completion. Uses mutex locking (`lockedBy` companion ID) to prevent double-execution across multiple companions.

**Job types:** `upload_file` (S3 → local path), `update_config` (JSON write), `restart_service` (systemd restart).

```
CLI: python3 raspberry_pi_client.py \
       --server $QUIVER_HUB_URL --drone-id $DRONE_ID \
       --api-key $API_KEY --poll-interval 5 --debug
```

### 4.2 Telemetry Forwarder (`telemetry_forwarder.py`)

Three-thread architecture: MAVLink thread (MAVSDK async), UAVCAN thread (dronecan node), HTTP thread (POST at 10 Hz). Aggregates attitude, position, GPS, battery, flight mode, and armed status into a thread-safe dictionary and streams to Hub.

```
Flow: FC (MAVLink) ──┐
                      ├→ TelemetryDict → HTTP Queue → POST /api/rest/telemetry/ingest
      Battery (CAN) ──┘   (lock-protected)  (10 Hz)
```

### 4.3 Logs & OTA Service (`logs_ota_service.py`)

Manages FC log discovery, download, upload, OTA firmware flashing, system diagnostics, and remote log streaming. Key classes:

| Class | Role |
|---|---|
| `LogsOtaService` | Main orchestrator — starts all subsystems, manages Socket.IO connection |
| `FCLogSyncer` | Background sync loop — discovers FC logs via HTTP (`net_webserver.lua` on port 8080), caches locally, three-tier resolution: local cache → HTTP → MAVFTP |
| `DiagnosticsCollector` | Collects CPU/memory/disk/network stats + FC web server health check (HTTP HEAD ping), reports every cycle |
| `HubClient` | REST/tRPC client for reporting log lists, progress, uploads, diagnostics |
| `CompanionSocketManager` | Socket.IO connection for real-time job dispatch and log streaming |

**Job types:** `scan_fc_logs`, `download_fc_log`, `flash_firmware`.

**FC log upload:** Prefers multipart (`/api/rest/logs/fc-upload-multipart`) with automatic fallback to base64 JSON (`/api/rest/logs/fc-upload`).

```
CLI: python3 logs_ota_service.py \
       --server $QUIVER_HUB_URL --drone-id $DRONE_ID \
       --api-key $API_KEY --fc-webserver-url http://192.168.144.51:8080 \
       --log-store-dir /var/lib/quiver/fc_logs --debug
```

### 4.4 Camera Stream Service (`camera_stream_service.py`)

Manages go2rtc process lifecycle, Tailscale funnel for public WHEP access, and stream registration with Hub. Monitors Siyi camera availability and auto-registers/unregisters streams.

### 4.5 SIYI Camera Controller (`siyi_camera_controller.py`)

Bridges Hub Socket.IO commands to the Siyi gimbal via UDP SDK (`192.168.144.25:37260`). Supports pan/tilt, zoom, photo capture, video record, and gimbal mode switching.

---

## 5. Hub REST API — Complete Endpoint Reference

All REST endpoints require the `x-api-key` header (API key generated in Hub Drone Configuration page) unless noted otherwise.

### Core Data Pipelines

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/rest/pointcloud/ingest` | Ingest RPLidar point cloud scans |
| POST | `/api/rest/telemetry/ingest` | Ingest MAVLink + UAVCAN telemetry |
| POST | `/api/rest/payload/{appId}/ingest` | Ingest custom app payload data |

### Camera Pipeline

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/rest/camera/status` | Report camera status/metadata |
| POST | `/api/rest/camera/stream-register` | Register a WebRTC stream URL |
| POST | `/api/rest/camera/stream-unregister` | Unregister a stream |
| GET | `/api/rest/camera/stream-status/{droneId}` | Get stream status |
| POST | `/api/rest/camera/whep-proxy/{droneId}` | WHEP signaling proxy for WebRTC playback |

### Logs & OTA Pipeline

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/rest/logs/fc-list` | Report discovered FC log list |
| POST | `/api/rest/logs/fc-progress` | Report download/upload progress |
| POST | `/api/rest/logs/fc-upload` | Upload FC log (base64 JSON — legacy fallback) |
| POST | `/api/rest/logs/fc-upload-multipart` | Upload FC log (multipart form — preferred) |
| GET | `/api/rest/logs/fc-download/{logId}` | Download FC log to browser (session-auth, not API key) |
| POST | `/api/rest/firmware/progress` | Report firmware flash progress |
| POST | `/api/rest/diagnostics/report` | Report system diagnostics + FC web server health |

### Flight Analytics & System

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/rest/flightlog/upload` | Upload flight log for analysis (browser-only) |
| GET | `/api/rest/health` | Health check |
| POST | `/api/rest/test-connection` | Test API key + drone connectivity |

### tRPC Job Polling

| Procedure | Purpose |
|---|---|
| `droneJobs.getPendingJobs` | Poll for pending jobs assigned to this drone |
| `droneJobs.acknowledgeJob` | Lock a job for execution (mutex) |
| `droneJobs.completeJob` | Report job success + result data |
| `droneJobs.failJob` | Report job failure + error message |

---

## 6. WebSocket Events (Socket.IO)

Connect to `wss://<hub-url>` with Socket.IO client. Events are organized by direction.

### Client → Hub (Subscribe)

| Event | Payload | Purpose |
|---|---|---|
| `subscribe` | `{droneId}` | Subscribe to a drone's data channels |
| `unsubscribe` | `{droneId}` | Unsubscribe |
| `subscribe_app` | `{appId}` | Subscribe to custom app data |
| `subscribe_camera` | `{droneId}` | Subscribe to camera events |
| `subscribe_logs` | `{droneId}` | Subscribe to FC log events |
| `subscribe_stream` | `{droneId}` | Subscribe to log stream lines |

### Client → Hub (Commands)

| Event | Payload | Purpose |
|---|---|---|
| `camera_command` | `{droneId, command, params}` | Send gimbal/camera command |
| `log_stream_request` | `{droneId, service, lines}` | Request journald log stream |

### Companion → Hub

| Event | Payload | Purpose |
|---|---|---|
| `register_companion` | `{droneId, apiKey, companionId}` | Register companion connection |
| `camera_status` | `{droneId, ...status}` | Report camera status |
| `camera_response` | `{droneId, ...response}` | Respond to camera command |
| `log_stream_line` | `{droneId, service, line}` | Stream journald log line |

### Hub → Client (Broadcasts)

| Event | Data | Purpose |
|---|---|---|
| `pointcloud_update` | Point cloud frame | New LiDAR scan available |
| `telemetry_update` | Telemetry snapshot | New telemetry data |
| `app_data` | Parsed payload | Custom app data update |
| `camera_status` | Camera state | Camera status change |
| `camera_stream` | Stream info | Stream registered/unregistered |
| `fc_log_progress` | Progress object | FC log download/upload progress |
| `firmware_progress` | Progress object | Firmware flash progress |
| `diagnostics` | System stats + fcWebserver | Diagnostics report (includes FC web server health) |
| `log_stream` | Log line | Journald log stream line |

---

## 7. Play-by-Play: Setting Up a New Drone

This section walks through the complete setup sequence from bare hardware to a fully connected drone streaming data to Hub.

### Step 1: Generate API Key

Open Quiver Hub → Drone Configuration → select or create a drone → API Keys section → click "Generate Key". Copy the key — it is shown only once.

### Step 2: Configure the .env File

On the Raspberry Pi, create `$HOME/quiver/forwarder.env`:

```
QUIVER_HUB_URL=https://your-quiver-hub.com
QUIVER_DRONE_ID=quiver_001
QUIVER_API_KEY=<paste-key-here>
FC_WEBSERVER_URL=http://192.168.144.51:8080
FC_LOG_STORE_DIR=/var/lib/quiver/fc_logs
```

The Drone Configuration page in Hub has a ".env File" card that generates this file with all endpoints pre-filled. Copy it directly.

### Step 3: Install Companion Services

Run the install scripts in order. Each prompts for Hub URL, drone ID, and API key, then creates the systemd service.

```bash
cd $HOME/quiver/companion_scripts
chmod +x install_*.sh

./install_hub_client.sh          # Job polling
./install_telemetry_forwarder.sh # Telemetry streaming
./install_logs_ota.sh            # FC logs + OTA + diagnostics
./install_camera_services.sh     # Camera stream + SIYI controller
```

### Step 4: Verify Connectivity

```bash
# Check all services are running
sudo systemctl status quiver-hub-client telemetry-forwarder logs-ota camera-stream siyi-camera

# Test Hub connectivity
curl -X POST https://your-hub.com/api/rest/test-connection \
  -H "x-api-key: <your-key>" \
  -H "Content-Type: application/json" \
  -d '{"droneId":"quiver_001"}'

# Test FC web server (from Pi)
curl -I http://192.168.144.51:8080/

# Check CAN bus
sudo ip link set can0 up type can bitrate 1000000
candump can0  # should show DroneCAN traffic
```

### Step 5: Verify in Hub UI

Open Quiver Hub in a browser. You should see:

1. **Telemetry App** — Attitude indicator, position, GPS, battery updating in real-time
2. **RPLidar App** — Point cloud rendering (if LiDAR connected)
3. **Camera App** — Live WebRTC stream (if camera configured)
4. **Logs & OTA App** — FC web server health indicator (green dot), discovered FC logs after first scan
5. **Drone Configuration** — "Connected" badge, test connection success

### Step 6: Dispatch a Job (Optional)

From Drone Configuration → Job History → create a job:

- **Scan FC Logs:** Triggers the companion to discover all FC log files and report them to Hub
- **Download FC Log:** Downloads a specific log from FC → uploads to Hub S3 → available for browser download
- **Flash Firmware:** Serves firmware via HTTP for FC pull (Approach C), verifies via `AUTOPILOT_VERSION` git hash comparison
- **Deliver File:** Downloads a file from Hub S3 to a target path on the Pi

---

## 8. FC Web Server Setup (ArduPilot)

The flight controller runs several Lua scripting applets that provide HTTP access to the SD card, accept file uploads, and enable OTA firmware pulling. These are the primary access paths for log sync and firmware flash; MAVFTP is the fallback for log operations only.

### Enable on the Flight Controller

Set these parameters via Mission Planner or MAVProxy:

| Parameter | Value | Purpose |
|---|---|---|
| `SCR_ENABLE` | 1 | Enable Lua scripting engine |
| `SCR_VM_I_COUNT` | 200000 | VM instruction count (recommended) |
| `SCR_HEAP_SIZE` | 200000 | Heap size in bytes (recommended) |
| `WEB_ENABLE` | 1 | Enable the web server |
| `WEB_BIND_PORT` | 8080 | HTTP listen port |
| `NET_ENABLE` | 1 | Enable networking stack |
| `NET_IPADDR0–3` | 192.168.144.51 | FC static IP |
| `NET_NETMASK` | 24 | Subnet mask |
| `NET_GWADDR0–3` | 192.168.144.50 | Gateway (Pi) |
| `FWPULL_ENABLE` | 1 | Enable firmware pull from companion (required for OTA flash) |

### Lua Scripts on the FC SD Card

Copy these applets to `APM/scripts/` on the FC SD card:

| Script | Purpose |
|---|---|
| `net_webserver.lua` | Serves the SD card over HTTP on port 8080 (directory listings, file downloads). Primary log access path. |
| `net_webserver_put.lua` | Extends the web server with HTTP PUT support for file uploads to the SD card. Includes 30-second stall timeout and partial file cleanup. |
| `firmware_puller.lua` | Polls the companion's HTTP server at `http://192.168.144.50:8080/firmware.abin` when `FWPULL_ENABLE=1`. Downloads firmware to SD card as `ardupilot.abin`, triggering ArduPilot's built-in flash-on-boot mechanism. Includes 30-second stall timeout. |

Reboot the FC after copying scripts. Verify from the Pi:

```bash
curl http://192.168.144.51:8080/
# Should return HTML directory listing
```

The companion's `FCLogSyncer` automatically uses the `net_webserver.lua` endpoint for background log sync and on-demand downloads. The `firmware_puller.lua` script is used by the OTA flash flow (Approach C) to pull firmware from the companion's temporary HTTP server.

---

## 9. Building a Custom Payload App

The App Builder lets you create custom data pipeline apps that receive sensor data, parse it, and display it in real-time widgets. There are three data source modes, each covered step-by-step below.

### 9.1 Concepts

Every custom app has three layers:

| Layer | What It Does |
|---|---|
| **Data Source** | How data enters the app — REST endpoint, stream subscription, or passthrough |
| **Parser** | Python script that transforms raw JSON into typed display fields (SCHEMA dict) |
| **UI** | Grid of widgets (gauges, charts, LEDs, text, canvas) bound to SCHEMA fields |

The App Builder walks you through all three. The result is a published app that appears in the App Store for any user to install and see in their sidebar.

---

### 9.2 Mode A: Custom Endpoint (External Sensor → REST → Parser → UI)

Use this when you have a sensor on the companion computer (or any external device) that will POST JSON to the Hub.

**Step 1 — Open the App Builder.** In the Hub sidebar, click the "+" button at the bottom → App Store → "Start Building" button.

**Step 2 — Enter app info.** Fill in the app name (e.g., "Weather Station") and a short description. These appear in the App Store listing.

**Step 3 — Select "Custom Endpoint" as the data source.** This is the default. It creates a dedicated REST endpoint at `/api/rest/payload/{appId}/ingest` that accepts JSON POST requests.

**Step 4 — Write or upload a parser.** The parser is a Python script with two required elements:

```python
def parse_payload(raw_data: dict) -> dict:
    """Transform raw incoming JSON into display fields."""
    return {
        "temperature": raw_data.get("temp_raw", 0) / 100.0,
        "humidity": raw_data.get("hum_raw", 0) / 100.0,
    }

SCHEMA = {
    "temperature": {"type": "number", "unit": "°C", "min": -50, "max": 60},
    "humidity":    {"type": "number", "unit": "%",  "min": 0,   "max": 100},
}
```

The `SCHEMA` dict defines every field the UI Builder can bind to. Supported types: `"number"`, `"string"`, `"boolean"`. You can either type the code in the editor or click the upload button to load a `.py` file from disk.

**Step 5 — Test the parser.** Paste sample JSON into the "Test Data" box (matching what your sensor will actually send) and click "Run Test". The output panel shows the parsed result and execution time. Fix any errors before proceeding.

**Step 6 — Continue to UI Builder.** Click "Continue to UI Builder". The system extracts the SCHEMA from your parser and opens the drag-and-drop UI Builder.

**Step 7 — Design the UI.** The UI Builder has:

| Element | How to Use |
|---|---|
| Widget palette (left) | Click a widget type to add it: Text, Gauge, Line Chart, Bar Chart, LED, Canvas, Connection Status |
| Grid canvas (center) | Widgets appear in a grid. Set row, column, row span, and column span for each |
| Property editor (right) | Select a widget to configure: title, data binding (pick a SCHEMA field), colors, min/max, units |
| Layout columns | Adjust the grid column count (default 3) |
| Preview mode | Toggle to see how the app will look with live data |

Bind each widget to a SCHEMA field using the "Data Field" dropdown. For example, bind a Gauge widget to `temperature` and set min=-50, max=60.

#### Widget Reference

| Widget | Type Key | Data Type | Configurable Properties | Best For |
|---|---|---|---|---|
| **Text Display** | `text` | number, string | `label`, `fontSize`, `showUnit`, `decimalPlaces` | Single values, labels, formatted numbers |
| **Gauge** | `gauge` | number | `label`, `min`, `max`, `showValue` | Bounded numeric values (temperature, pressure, battery) |
| **Line Chart** | `line-chart` | number | `title`, `maxDataPoints`, `lineColor` | Time-series trends (sensor readings over time) |
| **Bar Chart** | `bar-chart` | number | `title`, `orientation`, `barColor` | Comparing discrete values side by side |
| **LED Indicator** | `led` | boolean | `label`, `onColor`, `offColor`, `size` | Binary status (armed/disarmed, connected/disconnected) |
| **Map** | `map` | number (lat/lon pair) | `zoom`, `markerColor` | Geographic position display |
| **Video** | `video` | string (URL) | `autoplay`, `controls` | Live camera feeds or recorded video |
| **Canvas** | `canvas` | any | `backgroundColor`, `renderMode` | Custom visualizations (point clouds, diagrams) |
| **Connection Status** | `connection_status` | — (auto) | — | Data flow indicator (green when data arriving) |

Every widget except Connection Status requires a data binding to a SCHEMA field. Map widgets need two bindings (latitude and longitude fields). Video widgets bind to a field that contains a stream URL.

**Step 8 — Save and publish.** Click "Save App". The app is saved to the database with status `published`. It now appears in the App Store under "Custom Apps".

**Step 9 — Install the app.** Go to App Store → find your app → click "Install". The app icon appears in your sidebar.

**Step 10 — Send data from the companion.** On the Raspberry Pi, create a forwarder script:

```python
import requests, time, os

url = os.environ["QUIVER_HUB_URL"] + "/api/rest/payload/YOUR_APP_ID/ingest"
headers = {"x-api-key": os.environ["QUIVER_API_KEY"], "Content-Type": "application/json"}

while True:
    data = read_sensor()  # your sensor reading function
    requests.post(url, json={"temp_raw": data["temp"], "hum_raw": data["hum"]}, headers=headers)
    time.sleep(1)
```

The `appId` is visible in the App Store card or in the browser URL when viewing the app. The Hub executes your parser on each POST, stores the result, and broadcasts it via WebSocket to all connected clients viewing the app.

**Step 11 — Verify.** Open the app in the Hub sidebar. Widgets should update in real-time as the companion sends data. The connection status indicator shows green when data is flowing.

---

### 9.3 Mode B: Stream Subscription (Mix Existing Pipeline Data → UI)

Use this when you want to combine data from existing pipelines (telemetry, LiDAR, camera, other custom apps) into a single dashboard — no companion-side code needed.

**Step 1 — Open App Builder** (same as Mode A, Steps 1–2).

**Step 2 — Select "Subscribe to Streams" as the data source.**

**Step 3 — Pick streams and fields.** The stream picker shows all available data sources:

| Stream | Event | Example Fields |
|---|---|---|
| Telemetry | `telemetry_update` | `attitude.roll`, `attitude.pitch`, `position.lat`, `battery.voltage` |
| Point Cloud | `pointcloud_update` | `points`, `scan_count`, `point_count` |
| Camera | `camera_status` | `recording`, `connected`, `resolution` |
| Custom Apps | `app_data` | Fields from other custom apps |

Check the streams you want, then expand each to select individual fields. Fields from different streams are merged into a single flat data object. If field names collide, the system auto-prefixes with the stream name, or you can set custom aliases.

**Step 4 — Continue to UI Builder.** The SCHEMA is auto-generated from your selected fields. Click "Continue to UI Builder".

**Step 5 — Design and save** (same as Mode A, Steps 7–9).

**Step 6 — Verify.** The app automatically subscribes to the selected WebSocket events. No companion-side forwarder is needed — data flows from the existing pipelines through the Hub's WebSocket rooms directly to your app's widgets.

---

### 9.4 Mode C: Passthrough (Raw JSON → UI, No Parser)

Use this for quick prototyping when your sensor already outputs clean JSON matching the display format.

**Step 1 — Open App Builder** (same as Mode A, Steps 1–2).

**Step 2 — Select "Passthrough" as the data source.**

**Step 3 — Define the SCHEMA only.** In the code editor, write just the SCHEMA dict (no `parse_payload` function needed):

```python
SCHEMA = {
    "speed":    {"type": "number", "unit": "m/s", "min": 0, "max": 50},
    "armed":    {"type": "boolean"},
    "status":   {"type": "string"},
}
```

**Step 4 — Continue to UI Builder, design, save, install** (same as Mode A, Steps 6–9).

**Step 5 — Send data.** POST raw JSON to `/api/rest/payload/{appId}/ingest`. The Hub skips the parser and passes the JSON directly to storage and WebSocket broadcast. Your JSON keys must match the SCHEMA field names exactly.

---

### 9.5 Editing an Existing App

Go to the App Management page (App Store → "Manage Apps" button). Click the edit icon on any app to re-open the App Builder in edit mode. Changes are versioned — each save increments the version number. Installed users see the update immediately.

---

### 9.6 Data Flow Summary

```
Mode A (Custom Endpoint):
  Sensor → companion script → POST /payload/{appId}/ingest → parser executes → store + broadcast → UI widgets

Mode B (Stream Subscription):
  Existing pipeline → WebSocket event → Hub routes to app room → UI widgets (no REST, no parser)

Mode C (Passthrough):
  Sensor → companion script → POST /payload/{appId}/ingest → skip parser → store + broadcast → UI widgets
```

---

## 10. Operational Walkthroughs

### 10.1 Adding a Custom Job Type

Custom jobs let you trigger arbitrary tasks on the companion computer from the Hub UI. The job lifecycle is: **create → poll → acknowledge → execute → complete/fail**.

**Step 1 — Define the handler.** In `raspberry_pi_client.py`, add a method to the `QuiverHubClient` class:

```pseudo
def handle_my_custom_job(self, job):
    payload = job['payload']        # JSON payload from Hub
    # ... execute your task ...
    return (True, None)             # success
    # or: return (False, "error")   # failure
```

**Step 2 — Register the job type in `process_job()`.** Add an `elif` branch:

```pseudo
def process_job(self, job):
    if job['type'] == 'my_custom_job':
        return self.handle_my_custom_job(job)
    return super().process_job(job)
```

**Step 3 — Restart the companion service** so it picks up the new handler:

```bash
sudo systemctl restart quiver-hub-client
```

**Step 4 — Create the job from Hub UI.** Open Drone Configuration → select the target drone → scroll to Job History → click "New Job". Fill in:

| Field | Value |
|---|---|
| Type | `my_custom_job` |
| Payload | `{"param1": "value1", "param2": 42}` (any valid JSON) |

Click "Create". The job enters `pending` status.

**Step 5 — Watch the lifecycle.** The companion polls every 5 seconds. When it picks up the job:

1. **Acknowledge** — status changes to `in_progress`, `lockedBy` set to this companion's ID (prevents double-execution)
2. **Execute** — your `handle_my_custom_job()` runs
3. **Complete** — if `(True, None)` returned, status → `completed`; if `(False, "error")`, status → `failed` with error message

The Job History table in Hub updates in real-time via tRPC polling. Failed jobs can be retried (up to `maxRetries`).

**Step 6 — Verify.** Check the job row in Hub shows `completed`. On the Pi, check logs:

```bash
sudo journalctl -u quiver-hub-client -f
```

**Built-in job types for reference:**

| Job Type | Handler | Service | What It Does |
|---|---|---|---|
| `upload_file` | `handle_upload_file_job` | `raspberry_pi_client.py` | Download file from Hub S3 → save to target path on Pi |
| `update_config` | `handle_update_config_job` | `raspberry_pi_client.py` | Write JSON config to a file on Pi |
| `scan_fc_logs` | `handle_scan_fc_logs` | `logs_ota_service.py` | List cached FC logs from manifest → report to Hub |
| `download_fc_log` | `handle_download_fc_log` | `logs_ota_service.py` | Serve cached log → upload to Hub S3 (multipart preferred) |
| `flash_firmware` | `handle_flash_firmware` | `logs_ota_service.py` | Download firmware from S3 → serve via HTTP for FC pull (Approach C) → MAVLink reboot → verify via `AUTOPILOT_VERSION` |

---

### 10.2 Camera Stream Setup

This sets up live WebRTC video from the SIYI A8 Mini camera through the Hub.

**Step 1 — Verify camera connectivity.** From the Pi:

```bash
curl -I rtsp://192.168.144.25:8554/sub.264
# Or test with ffprobe:
ffprobe rtsp://192.168.144.25:8554/sub.264
```

**Step 2 — Install go2rtc.** The install script handles this:

```bash
cd $HOME/quiver/companion_scripts
./install_camera_services.sh
```

This installs go2rtc, sets up the Tailscale funnel, and creates the systemd service.

**Step 3 — Configure the stream.** The service auto-detects the camera and creates a go2rtc config pointing to the RTSP source. Two streams are available:

| Stream | RTSP URL | Resolution |
|---|---|---|
| Main | `rtsp://192.168.144.25:8554/main.264` | 4K |
| Sub | `rtsp://192.168.144.25:8554/sub.264` | 720p (recommended for low-latency) |

Select the stream with `--stream sub` or `--stream main` in the service CLI args.

**Step 4 — Verify Tailscale funnel.** The service auto-detects the funnel URL and registers it with Hub:

```bash
tailscale funnel status
# Should show the go2rtc port being funneled
```

**Step 5 — Verify in Hub.** Open the Camera Feed app in the sidebar. You should see:

- Live WebRTC video stream with latency stats (RTT, jitter, bitrate, FPS)
- Gimbal controls: pan/tilt joystick, zoom slider (1x–6x), photo capture, video record toggle
- Connection quality indicator (green/yellow/red bars)

**Step 6 — Gimbal control.** The SIYI camera controller bridges Hub Socket.IO commands to the gimbal via UDP SDK (`192.168.144.25:37260`). Supported commands:

| Command | Socket.IO Event | Effect |
|---|---|---|
| Pan/Tilt | `camera_command` → `{type: "rotate", yawSpeed, pitchSpeed}` | Move gimbal |
| Center | `camera_command` → `{type: "center"}` | Return to forward position |
| Nadir | `camera_command` → `{type: "nadir"}` | Point straight down |
| Zoom | `camera_command` → `{type: "zoom", level}` | Set zoom 1x–6x |
| Photo | `camera_command` → `{type: "photo"}` | Capture still image |
| Record | `camera_command` → `{type: "recordToggle"}` | Start/stop video recording |

---

### 10.3 FC Log Download Workflow

This walks through discovering, downloading, and saving FC logs to your local PC.

**Step 1 — Open the Logs & OTA app** in the Hub sidebar. Select the target drone from the dropdown.

**Step 2 — Check FC Web Server health.** Look at the health indicator in the FC Logs tab header. A green dot with latency means the FC web server is reachable. Red means unreachable — check the FC is powered and `net_webserver.lua` is running (see Section 8).

**Step 3 — Scan for logs.** Click the "Scan FC Logs" button. This dispatches a `scan_fc_logs` job to the companion. The companion reads its local manifest (populated by `FCLogSyncer` background sync) and reports the log list to Hub. Logs appear in the table within seconds.

**Step 4 — Download a log.** For each log in the table:

| Log Status | Action | What Happens |
|---|---|---|
| `discovered` | Click download icon | Dispatches `download_fc_log` job → companion serves cached file → uploads to Hub S3 → auto-triggers browser download when done |
| `completed` | Click blue save icon | Immediately triggers browser download via proxy (`GET /api/rest/logs/fc-download/{logId}`) — no companion needed |
| `failed` | Click retry icon | Re-dispatches the download job |

**Step 5 — Monitor progress.** During download, a progress bar shows the upload percentage. Toast notifications track the lifecycle: "Downloading from FC..." → "Uploading to Hub..." → "Ready for download".

**Step 6 — Save to PC.** For completed logs, the blue save icon triggers a browser download via the server-side proxy. The proxy streams the file from S3 with `Content-Disposition: attachment; filename="00000042.BIN"`, so the browser opens a native Save dialog.

---

### 10.4 OTA Firmware Flash Workflow

This walks through uploading new firmware to the flight controller over the air. The flash uses **Approach C (FC HTTP Pull)** exclusively — the companion serves the firmware via a temporary HTTP server and the FC pulls it using `firmware_puller.lua`.

**Prerequisites:** Ensure `firmware_puller.lua` is installed on the FC SD card at `APM/scripts/firmware_puller.lua` and the `FWPULL_ENABLE` parameter is set to `1`. Also ensure `aiohttp` is installed on the companion Pi (`pip install --break-system-packages aiohttp`).

**Step 1 — Open the Logs & OTA app** → OTA Updates tab.

**Step 2 — Upload firmware.** Click "Upload Firmware". Select an `.abin` file (ArduPilot binary). The file uploads to Hub S3 with a SHA-256 hash computed automatically for integrity verification.

**Step 3 — Flash firmware.** Click "Flash" on the uploaded firmware entry. This dispatches a `flash_firmware` job to the companion.

**Step 4 — Monitor the flash process.** The companion executes these stages:

| Stage | What Happens |
|---|---|
| **Step 1: Download** | Companion downloads `.abin` from Hub S3, verifies SHA-256 hash, extracts git hash from file header |
| **Step 2: Cleanup** | HTTP check for existing `ardupilot*.abin` on FC (via `net_webserver.lua`) |
| **Step 3: Serve** | Companion starts `aiohttp` server on port 8080, FC pulls firmware via `firmware_puller.lua` |
| **Step 4: Reboot** | Companion sends MAVLink reboot command to FC |
| **Step 5: Wait** | Poll FC web server for up to 120s until it comes back online |
| **Step 6: Verify** | Reconnect MAVSDK, query `AUTOPILOT_VERSION`, compare git hash against `.abin` header |

Progress is reported in real-time via `POST /api/rest/firmware/progress` and broadcast to the UI via the `firmware_progress` WebSocket event. The progress bar and stage label update live.

**Step 5 — Verify.** After flash completes, the dashboard card displays the confirmed firmware version with a verification badge: green **ShieldCheck** if the git hash matches the `.abin` header, or amber **ShieldAlert** if there is a mismatch. For older flash records (before this feature), a "Version info not available" note is shown.

**Managing stuck updates.** If a flash gets stuck (status shows `transferring`, `flashing`, or `verifying` indefinitely), use the red **Cancel** button on the card to remove it. The **Clear Failed & Stuck** button removes all failed and stuck records in bulk.

---

### 10.5 Diagnostics & Remote Log Streaming

This walks through monitoring companion health and streaming service logs remotely.

**Step 1 — Open the Logs & OTA app** → Diagnostics tab.

**Step 2 — View system health.** The diagnostics panel shows real-time metrics reported by the companion every 10 seconds:

| Metric | Source |
|---|---|
| CPU usage (%) | `psutil.cpu_percent()` |
| Memory usage (%) | `psutil.virtual_memory()` |
| Disk usage (%) | `psutil.disk_usage('/')` |
| CPU temperature (°C) | `/sys/class/thermal/thermal_zone0/temp` |
| Network I/O (bytes sent/received) | `psutil.net_io_counters()` |
| Service statuses | `systemctl is-active` for each Quiver service |
| FC web server health | HTTP HEAD ping to `http://192.168.144.51:8080` (reachable/unreachable + latency) |

**Step 3 — Stream service logs.** Switch to the Log Stream tab. Select a service from the dropdown (e.g., `logs-ota`, `telemetry-forwarder`, `camera-stream`). Click "Start Streaming".

The companion runs `journalctl -u <service> -f -n <lines>` and streams each line to Hub via Socket.IO (`log_stream_line` event). Lines appear in the terminal-style viewer in real-time with a green "Live" badge.

**Step 4 — Filter and search.** Use the search box to filter log lines by keyword. Click "Clear" to reset the buffer. Click "Stop" to end the stream.

---

### 10.6 Integrating External Systems

The REST API accepts standard HTTP from any client:

| System | Integration Pattern |
|---|---|
| ROS/ROS2 | Subscribe to a topic, POST to `/api/rest/telemetry/ingest` or `/payload/{appId}/ingest` in the callback |
| ArduPilot Lua | Use `net_webserver.lua` CGI handlers to push data to the companion, which forwards to Hub |
| MQTT bridge | Subscribe to MQTT topics, forward to Hub REST endpoints |
| Node-RED | HTTP request node → Hub REST endpoint |

---

## 11. Quick Reference

### Dependencies

```bash
pip3 install requests aiohttp mavsdk dronecan python-socketio python-dotenv
```

### File Locations

| Path | Purpose |
|---|---|
| `$HOME/quiver/forwarder.env` | Shared environment configuration |
| `$HOME/quiver/raspberry_pi_client.py` | Hub client script |
| `$HOME/quiver/telemetry_forwarder.py` | Telemetry forwarder script |
| `$HOME/quiver/logs_ota_service.py` | Logs & OTA service script |
| `$HOME/quiver/camera_stream_service.py` | Camera stream service script |
| `$HOME/quiver/siyi_camera_controller.py` | SIYI camera controller script |
| `/var/lib/quiver/fc_logs/` | Local FC log cache (FCLogSyncer) |
| `/var/log/quiver/*.log` | Application logs |
| `/etc/systemd/system/quiver-*.service` | Systemd service files |
| `APM/scripts/net_webserver.lua` | FC: HTTP server for SD card access (port 8080) |
| `APM/scripts/net_webserver_put.lua` | FC: HTTP PUT support for file uploads |
| `APM/scripts/firmware_puller.lua` | FC: Firmware pull from companion HTTP server (OTA flash) |

### Useful Commands

```bash
# Service management
sudo systemctl status quiver-hub-client
sudo systemctl restart telemetry-forwarder
sudo journalctl -u logs-ota -f

# CAN bus
sudo ip link set can0 up type can bitrate 1000000
candump can0

# MAVLink debugging
mavproxy.py --master=udpin:0.0.0.0:14540

# Test Hub endpoint
curl -X POST $QUIVER_HUB_URL/api/rest/health
```

### MAVLink Connection Strings

| Type | Connection String |
|---|---|
| UDP (simulation) | `udpin://0.0.0.0:14540` |
| Serial (direct) | `serial:///dev/ttyACM0:57600` |
| TCP (network) | `tcp://192.168.144.51:5760` |

### Common DroneCAN Messages

| Message | Data |
|---|---|
| `uavcan.equipment.power.BatteryInfo` | Voltage, current, temperature, SoC |
| `uavcan.equipment.gnss.Fix` | GPS position, velocity, accuracy |
| `uavcan.equipment.air_data.StaticPressure` | Barometric pressure |
| `uavcan.equipment.ahrs.MagneticFieldStrength` | Magnetometer data |
