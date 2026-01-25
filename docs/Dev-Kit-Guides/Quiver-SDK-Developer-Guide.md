# Quiver SDK Developer Guide

## 1\. Introduction

### 1.1 What is Quiver SDK?

The Quiver SDK is a Python-based development toolkit that enables developers to build applications for both companion computers and payload devices in the Quiver ecosystem. It provides a standardized interface for communicating with Quiver Hub, the web-based control center that serves as the central coordination point for drone operations.

**Core Capabilities:**

- **Telemetry Forwarding**: Collect and stream flight controller data (MAVLink) and sensor data (UAVCAN) to Quiver Hub  
- **File Management**: Download configuration files, scripts, and firmware updates from Hub to companion computer  
- **Remote Job Execution**: Poll for and execute jobs dispatched from Hub (config updates, service restarts, data collection)  
- **Payload Data & Command Linkup**: Bridge between Hub and payload devices, enabling real-time sensor data streaming and command routing

### 1.2 Architecture Overview

The Quiver system architecture centers around a companion computer (Raspberry Pi) that acts as the intelligent bridge between the flight controller, payload devices, and the cloud-based Quiver Hub. The companion computer connects to Quiver Hub over wireless/cellular internet for command and control, while locally managing three payload ports (C1, C2, C3) through an integrated network switch that provides both Ethernet and CAN bus connectivity.

**Network Topology:**  
![][image1]  
**Connection Details:**

- **Wireless/Internet**: Companion ↔ Quiver Hub (HTTPS REST API, WebSocket telemetry)  
- **Ethernet**: Companion ↔ Integrated Switch ↔ Payload ports (192.168.144.11/.12/.13)  
- **CAN Bus**: Payloads ↔ Flight Controller/ Companion (DroneCAN protocol)  
- **Wireless RF Link**: Mission Planner ↔ Flight Controller (MAVLink over telemetry radio)

**Component Roles:**

**Companion Computer** (Raspberry Pi 4/5): Executes Python SDK applications, polls Quiver Hub for jobs, forwards telemetry from flight controller and payloads, manages payload lifecycle (discovery, configuration, data routing). Connects to flight controller via CAN bus for MAVLink telemetry and to Quiver Hub via WiFi or cellular for cloud communication.

**Integrated Network Switch**: Built into the Quiver drone hardware, this component provides Ethernet switching for three payload ports (C1, C2, C3) and CAN bus interface to the flight controller. Automatically assigns static IPs to payloads (192.168.144.11 for C1, .12 for C2, .13 for C3). Developers do not need to configure or manage this component directly.

**Payloads (C1/C2/C3)**: Modular sensor or actuator devices connected via Ethernet (for data-heavy sensors like cameras, LiDAR) or CAN bus (for lightweight sensors and actuators). Each payload runs its own firmware and communicates with the companion computer using standard protocols (HTTP REST, WebSocket, DroneCAN).

**Flight Controller** (Pixhawk 6X/32v6, Cube Pilot+): Runs ArduPilot or PX4 autopilot firmware. Provides MAVLink telemetry (attitude, position, GPS, battery) to the companion computer via CAN bus. Receives commands from Mission Planner via wireless RF telemetry link. Shares CAN bus with payloads for DroneCAN communication.

**Quiver Hub**: Cloud-hosted web application providing operator interface, job queue management, telemetry visualization, file storage, and REST API for companion computer communication. Accessible from any web browser with internet connectivity.

**Mission Planner**: Ground control software for flight planning and real-time monitoring. Connects to the flight controller via wireless RF telemetry link (typically 915 MHz or 433 MHz radio). Communicates using MAVLink protocol for mission upload, parameter configuration, and live telemetry display.

### 1.3 Prerequisites

Before developing with the Quiver SDK, ensure you have the required hardware and software components. The companion computer (Raspberry Pi) serves as your primary development target, while the flight controller provides the foundation for flight operations and telemetry.

**Hardware Requirements:**

**Companion Computer**: Raspberry Pi 4 (4GB+ RAM) or Raspberry Pi 5 recommended. Earlier models lack sufficient processing power for multi-threaded telemetry forwarding and payload management. The Pi must have cellular connectivity for internet access to Quiver Hub.

**Flight Controller**: Pixhawk 6X, Pixhawk 32v6, or Cube Pilot+ running ArduPilot or PX4 firmware. These controllers provide MAVLink telemetry over Ethernet and support DroneCAN for payload integration. The flight controller must be configured with appropriate parameters for Ethernet and CAN bus communication.

**Integrated Network Switch**: Built into Quiver drone hardware, this component is pre-configured and requires no user setup. It provides Ethernet ports for payloads (C1, C2, C3) and CAN bus connectivity.

**Payloads** (optional): Sensors or actuators with Ethernet (cameras, LiDAR, compute modules) or CAN bus connectivity (battery monitors, servos, environmental sensors). Payloads must implement standard communication protocols (HTTP REST for Ethernet devices, DroneCAN for CAN devices).

**Software Requirements:**

**Operating System**: Raspberry Pi OS (64-bit) or Ubuntu 22.04 for ARM64. 64-bit OS required for MAVSDK and modern Python packages. Lite versions (headless) are sufficient for production deployments.

**Python**: Version 3.9 or later with pip package manager. Core SDK dependencies include `requests` (HTTP client), `aiohttp` (async HTTP), `mavsdk` (MAVLink communication), and `dronecan` (DroneCAN/UAVCAN protocol).

**Network Connectivity**: WiFi or cellular modem for internet access to Quiver Hub. The Companion computer must maintain persistent connection for job polling and telemetry streaming. Cellular modems (4G/LTE) Necessary.

**Development Skills**: Basic Python programming (async/await, threading, HTTP requests), familiarity with Linux command line (systemd, networking, file permissions), understanding of networking concepts (IP addressing, ports, protocols), and basic knowledge of MAVLink/DroneCAN protocols.

**Optional Components:**

**Ground Control Software**: Mission Planner (Windows) or QGroundControl (cross-platform) for flight planning, parameter configuration, and real-time monitoring. Connects to the flight controller via RF telemetry link.

**CAN Interface Tools**: `can-utils` package for debugging DroneCAN communication (`candump`, `cansend`, `canplayer`), oscilloscope or logic analyzer for signal-level troubleshooting of CAN bus issues.

---

## 2\. Core Components

The Quiver SDK consists of two primary Python applications that run on the companion computer: the Quiver Hub Client for bidirectional job management, and the Telemetry Forwarder for streaming flight data to the cloud. These components work together to provide a complete solution for remote drone management and monitoring.

### 2.1 Quiver Hub Client (`raspberry_pi_client.py`)

The Quiver Hub Client implements a polling-based job execution system that enables operators to remotely manage the companion computer from the Quiver Hub web interface. The client periodically checks for pending jobs, executes them locally, and reports completion status back to the Hub.

**Purpose**: Bidirectional communication between companion computer and Quiver Hub for remote management and control.

**Key Features**:

- **Job Polling**: Queries Hub every 5 seconds (configurable) for pending jobs assigned to this drone  
- **Job Execution**: Executes jobs locally based on type (file downloads, config updates, custom commands)  
- **Status Reporting**: Reports job completion status (success/failure) and error messages back to Hub  
- **Extensible Architecture**: Developers can add custom job handlers for application-specific tasks

**Built-in Job Types**:

- `upload_file`: Downloads a file from Hub's S3 storage to specified path on companion computer  
- `update_config`: Updates JSON configuration file with new settings from Hub  
- **Custom Job Types**: Developers can implement handlers for restart\_service, run\_script, collect\_logs, etc.

**Usage Example**:

```shell
python3 raspberry_pi_client.py \
  --server https://your-hub.com \
  --drone-id quiver_001 \
  --api-key abc123 \
  --poll-interval 5
```

The client runs as a long-lived process (typically as a systemd service) and maintains persistent connection to Hub. Authentication uses API keys generated in the Hub admin interface. Each drone has a unique identifier (`drone-id`) used for job routing and telemetry association.

### 2.2 Telemetry Forwarder (`telemetry_forwarder.py`)

The Telemetry Forwarder collects real-time flight data from multiple sources (flight controller via MAVLink, battery via UAVCAN) and streams it to Quiver Hub for visualization and logging. It uses a multi-threaded architecture to handle concurrent data collection and HTTP transmission without blocking.

**Purpose**: Collect flight controller telemetry and sensor data, aggregate into unified format, and stream to Quiver Hub.

**Data Sources**:

- **MAVLink** (via MAVSDK): Attitude (roll/pitch/yaw), position (lat/lon/alt), GPS (satellites, fix type, HDOP), battery (voltage, current, remaining %), flight mode, armed status  
- **UAVCAN** (via dronecan): Battery pack voltage, current draw, temperature, cell voltages, state of charge

**Architecture**: The forwarder uses three concurrent threads to maximize throughput while maintaining data freshness:

1. **MAVLink Thread**: Subscribes to flight controller telemetry streams using MAVSDK async API. Updates shared telemetry dictionary with latest values. Runs continuously, blocking on MAVLink message reception.  
     
2. **UAVCAN Thread**: Listens for DroneCAN battery messages on CAN bus. Parses BatteryInfo messages and updates the shared telemetry dictionary. Runs continuously, spinning DroneCAN node.  
     
3. **HTTP Thread**: Aggregates data from shared dictionary, formats as JSON, and POSTs to Hub at 10 Hz (configurable). Uses request queue to handle backpressure if Hub is slow or unreachable.

**Data Flow**:

```
Flight Controller (MAVLink) ──┐
                               ├──> Telemetry Dict ──> HTTP Queue ──> Quiver Hub
Battery (UAVCAN) ─────────────┘     (thread-safe)      (rate-limited)
```

**Usage Example**:

```shell
export WEB_SERVER_URL=https://your-hub.com/api/rest/telemetry/ingest
export API_KEY=abc123
export DRONE_ID=quiver_001
export MAVLINK_URL=udpin://0.0.0.0:14540
export CAN_INTERFACE=can0
export UPDATE_RATE_HZ=10

python3 telemetry_forwarder.py
```

The forwarder runs as a systemd service and automatically reconnects if the flight controller reboots or the network connection drops. Telemetry data is buffered locally if Hub is temporarily unreachable, then transmitted when connectivity is restored.

### 2.3 Payload Forwarders (Point Clouds, Cameras, etc.)

Beyond the core telemetry forwarder, developers can create specialized forwarders for high-bandwidth sensor data such as LiDAR point clouds, camera streams, or environmental sensor arrays. These forwarders follow a similar pattern but use WebSocket or chunked HTTP POST for real-time streaming.

**Common Pattern**:

1. Read sensor data from hardware interface (Ethernet, CAN)  
2. Transform to standard format (point clouds as x/y/z coordinates, images as JPEG/H.264)  
3. Stream to Hub via WebSocket (for real-time visualization) or HTTP POST (for logging)  
4. Handle backpressure by dropping frames or compressing data if network is saturated

**Example: RPLidar Point Cloud Forwarder**:

- Reads 2D laser scan data from RPLidar sensor via serial port  
- Converts polar coordinates (angle, distance) to Cartesian (x, y, z=0)  
- Sends point cloud via WebSocket to Hub for real-time 3D visualization  
- Includes quality/intensity values for each point

Developers can use the telemetry forwarder as a template for building custom sensor forwarders, adapting the threading model and data formats to their specific sensor requirements.

---

## 3\. Developer Workflows

Understanding the end-to-end workflows helps developers see how their code fits into the larger Quiver ecosystem. This section describes common user interactions and the corresponding data flows through the system.

### 3.1 User Flow: Monitoring Telemetry

An operator wants to monitor a drone's flight in real-time from the Quiver Hub web interface.

**Steps**:

1. Operator opens Quiver Hub in web browser and navigates to "Flight Telemetry" app  
2. Selects drone "quiver\_001" from dropdown menu  
3. Hub establishes WebSocket connection to backend server  
4. Backend subscribes to telemetry stream for quiver\_001  
5. Telemetry forwarder on companion computer POSTs data to Hub REST API every 100ms  
6. Hub backend receives POST, validates API key, stores in time-series database  
7. Hub backend broadcasts telemetry to all connected WebSocket clients for quiver\_001  
8. Browser receives telemetry via WebSocket, updates attitude indicator, GPS map, battery gauge  
9. Operator sees live updates with \<200ms latency (network dependent)

**Data Flow**:

```
Companion Pi → telemetry_forwarder.py → HTTPS POST → Hub API → Database
                                                              ↓
                                                         WebSocket
                                                              ↓
                                                      Browser UI (live updates)
```

This workflow demonstrates the pub-sub pattern used throughout Quiver: companion computers push data to Hub via REST API, Hub stores and broadcasts to all interested clients via WebSocket.

### 3.2 User Flow: Uploading Configuration File

An operator needs to update the companion computer's configuration file without SSH access.

**Steps**:

1. Operator opens Quiver Hub and navigates to "Drone Management" → "quiver\_001" → "Files"  
2. Clicks "Upload File" button, selects `config.json` from local computer  
3. Hub uploads file to S3 storage, generates unique file ID  
4. Operator specifies target path: `/home/pi/config/config.json`  
5. Hub creates "upload\_file" job in database with payload: `{fileId, targetPath, filename}`  
6. Job status: "pending"  
7. Companion computer's `raspberry_pi_client.py` polls Hub every 5 seconds  
8. Client finds pending job, calls `droneJobs.getPendingJobs` API  
9. Client acknowledges job (status: "in\_progress"), calls `droneJobs.acknowledgeJob`  
10. Client downloads file from S3 using presigned URL from `droneJobs.getFile`  
11. Client saves file to `/home/pi/config/config.json`, creates directory if needed  
12. Client reports completion, calls `droneJobs.completeJob` with `success: true`  
13. Operator sees "Completed" status in Hub UI, with timestamp and execution duration

**Data Flow**:

```
Browser → Upload File → S3 Storage
                    ↓
                Create Job → Database (status: pending)
                    ↓
Companion Pi → Poll Jobs → Find pending → Acknowledge → Download from S3
                                                      ↓
                                              Save to filesystem
                                                      ↓
                                              Report completion → Database (status: completed)
                                                                          ↓
                                                                   Browser UI (refresh)
```

This workflow demonstrates the job queue pattern: Hub creates jobs, companion computer polls and executes, Hub tracks status. This approach works reliably even with intermittent network connectivity.

### 3.3 Developer Flow: Adding New Sensor

A developer wants to integrate a new temperature/humidity sensor and visualize data in Hub.

**Steps**:

1. **Hardware Setup**: Connect DHT22 sensor to Raspberry Pi GPIO pins  
2. **Write Python Script**: Create `dht22_forwarder.py` that reads sensor every 5 seconds  
3. **Format Data**: Structure as JSON with timestamp, droneId, sensorType, and data fields  
4. **POST to Hub**: Send HTTP POST to `/api/rest/sensor-data/ingest` with API key header  
5. **Test Locally**: Run script, verify data appears in Hub's raw sensor data logs  
6. **Create Visualization**: Use Hub's UI Builder to create custom app with temperature/humidity charts  
7. **Deploy**: Install script as systemd service on companion computer  
8. **Monitor**: Check logs, verify data streaming, adjust sample rate if needed

**Code Example** (simplified):

```py
import requests
import Adafruit_DHT
from datetime import datetime
import time

SENSOR = Adafruit_DHT.DHT22
PIN = 4
HUB_URL = "https://your-hub.com/api/rest/sensor-data/ingest"
API_KEY = "abc123"
DRONE_ID = "quiver_001"

while True:
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
    
    data = {
        "droneId": DRONE_ID,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "sensorType": "dht22",
        "data": {
            "temperature_c": temperature,
            "humidity_percent": humidity
        }
    }
    
    requests.post(HUB_URL, json=data, headers={"x-api-key": API_KEY})
    time.sleep(5)
```

This workflow demonstrates the extensibility of Quiver: developers can add new sensors by following a simple pattern (read, format, POST) without modifying core SDK code.

---

## 4\. API Reference (Python)

This section provides Python code examples for interacting with the Quiver Hub REST API. All examples use the `requests` library for synchronous HTTP calls. For production code, consider using `aiohttp` for async/await patterns.

### 4.1 Quiver Hub REST API

The Hub exposes a tRPC-based REST API for job management and telemetry ingestion. All endpoints require authentication via API key.

#### Get Pending Jobs

Retrieve all jobs assigned to a specific drone that are in "pending" status.

```py
import requests
import json

def get_pending_jobs(server_url, drone_id, api_key):
    """Fetch pending jobs from Quiver Hub"""
    url = f"{server_url}/api/trpc/droneJobs.getPendingJobs"
    params = {
        'input': json.dumps({
            'json': {
                'droneId': drone_id,
                'apiKey': api_key
            }
        })
    }
    
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    
    data = response.json()
    jobs = data['result']['data']['json']['jobs']
    return jobs

# Usage
jobs = get_pending_jobs(
    server_url="https://your-hub.com",
    drone_id="quiver_001",
    api_key="abc123"
)

for job in jobs:
    print(f"Job {job['id']}: {job['type']}")
```

**Response Format**:

```json
{
  "result": {
    "data": {
      "json": {
        "jobs": [
          {
            "id": 123,
            "type": "upload_file",
            "status": "pending",
            "payload": {
              "fileId": "abc123",
              "targetPath": "/home/pi/config.json",
              "filename": "config.json"
            },
            "createdAt": "2026-01-08T10:00:00Z"
          }
        ]
      }
    }
  }
}
```

#### Acknowledge Job

Mark a job as "in\_progress" to prevent other clients from executing it concurrently.

```py
def acknowledge_job(server_url, job_id, drone_id, api_key):
    """Acknowledge a job (mark as in progress)"""
    url = f"{server_url}/api/trpc/droneJobs.acknowledgeJob"
    payload = {
        'json': {
            'jobId': job_id,
            'apiKey': api_key,
            'droneId': drone_id
        }
    }
    
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()

# Usage
acknowledge_job(
    server_url="https://your-hub.com",
    job_id=123,
    drone_id="quiver_001",
    api_key="abc123"
)
```

#### Complete Job

Report job completion status (success or failure) with optional error message.

```py
def complete_job(server_url, job_id, drone_id, api_key, success, error_message=None):
    """Mark a job as completed"""
    url = f"{server_url}/api/trpc/droneJobs.completeJob"
    payload = {
        'json': {
            'jobId': job_id,
            'apiKey': api_key,
            'droneId': drone_id,
            'success': success,
            'errorMessage': error_message
        }
    }
    
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()

# Usage - success
complete_job(
    server_url="https://your-hub.com",
    job_id=123,
    drone_id="quiver_001",
    api_key="abc123",
    success=True
)

# Usage - failure
complete_job(
    server_url="https://your-hub.com",
    job_id=124,
    drone_id="quiver_001",
    api_key="abc123",
    success=False,
    error_message="File not found: /path/to/file"
)
```

#### Post Telemetry

Send flight controller telemetry to Hub for storage and real-time streaming.

```py
from datetime import datetime

def post_telemetry(server_url, api_key, drone_id, telemetry_data):
    """Post telemetry data to Quiver Hub"""
    url = f"{server_url}/api/rest/telemetry/ingest"
    headers = {'x-api-key': api_key}
    
    data = {
        'droneId': drone_id,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        **telemetry_data
    }
    
    response = requests.post(url, json=data, headers=headers, timeout=5)
    response.raise_for_status()
    return response.json()

# Usage
telemetry = {
    'attitude': {'roll': 2.5, 'pitch': -1.2, 'yaw': 45.0},
    'position': {'latitude': 37.7749, 'longitude': -122.4194, 'altitude': 123.45},
    'gps': {'satellites': 12, 'fix_type': '3d', 'hdop': 0.9},
    'battery': {'voltage': 22.2, 'current': 15.5, 'remaining_percent': 75}
}

post_telemetry(
    server_url="https://your-hub.com",
    api_key="abc123",
    drone_id="quiver_001",
    telemetry_data=telemetry
)
```

### 4.2 MAVLink Integration (MAVSDK)

MAVSDK provides a high-level Python API for communicating with ArduPilot and PX4 flight controllers. It handles MAVLink message parsing, connection management, and async/await patterns.

#### Connect to Flight Controller

Establish connection to flight controller via CAN bus (using MAVLink-over-CAN) or UDP (for simulation).

```py
from mavsdk import System
import asyncio

async def connect_to_flight_controller():
    """Connect to flight controller via MAVLink"""
    drone = System()
    
    # For CAN bus connection (production)
    # await drone.connect(system_address="serial:///dev/ttyACM0:57600")
    
    # For UDP connection (simulation/testing)
    await drone.connect(system_address="udpin://0.0.0.0:14540")
    
    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Connected to flight controller")
            break
    
    return drone

# Usage
drone = asyncio.run(connect_to_flight_controller())
```

**Connection Strings**:

- UDP (simulation): `udpin://0.0.0.0:14540` (listens for MAVLink on port 14540\)  
- Serial (direct): `serial:///dev/ttyACM0:57600` (57600 baud)  
- TCP (network): `tcp://192.168.1.100:5760` (connects to IP:port)

#### Subscribe to Telemetry Streams

MAVSDK provides async iterators for each telemetry stream. Use `async for` to continuously receive updates.

```py
async def subscribe_attitude(drone):
    """Subscribe to attitude telemetry (roll, pitch, yaw)"""
    async for attitude in drone.telemetry.attitude_euler():
        print(f"Roll: {attitude.roll_deg:.1f}°, "
              f"Pitch: {attitude.pitch_deg:.1f}°, "
              f"Yaw: {attitude.yaw_deg:.1f}°")

async def subscribe_position(drone):
    """Subscribe to position telemetry (lat, lon, alt)"""
    async for position in drone.telemetry.position():
        print(f"Lat: {position.latitude_deg:.6f}, "
              f"Lon: {position.longitude_deg:.6f}, "
              f"Alt: {position.absolute_altitude_m:.1f}m")

async def subscribe_gps(drone):
    """Subscribe to GPS info (satellites, fix type, HDOP)"""
    async for gps_info in drone.telemetry.gps_info():
        print(f"Satellites: {gps_info.num_satellites}, "
              f"Fix: {gps_info.fix_type}, "
              f"HDOP: {gps_info.hdop:.2f}")

async def subscribe_battery(drone):
    """Subscribe to battery telemetry"""
    async for battery in drone.telemetry.battery():
        print(f"Voltage: {battery.voltage_v:.2f}V, "
              f"Current: {battery.current_battery_a:.2f}A, "
              f"Remaining: {battery.remaining_percent:.0f}%")

# Run multiple subscriptions concurrently
async def main():
    drone = await connect_to_flight_controller()
    
    await asyncio.gather(
        subscribe_attitude(drone),
        subscribe_position(drone),
        subscribe_gps(drone),
        subscribe_battery(drone)
    )

asyncio.run(main())
```

**Available Telemetry Streams**:

- `attitude_euler()`: Roll, pitch, yaw in degrees  
- `attitude_quaternion()`: Quaternion representation  
- `position()`: Latitude, longitude, altitude  
- `velocity_ned()`: North, East, Down velocity (m/s)  
- `gps_info()`: Satellites, fix type, HDOP  
- `battery()`: Voltage, current, remaining %  
- `flight_mode()`: Current flight mode (MANUAL, STABILIZE, AUTO, etc.)  
- `armed()`: Armed status (boolean)  
- `in_air()`: In-air status (boolean)

### 4.3 UAVCAN Integration (dronecan)

DroneCAN (formerly UAVCAN) is a CAN bus protocol for connecting sensors and actuators to flight controllers. The `dronecan` Python library provides message parsing and node management.

#### Setup CAN Interface

Initialize CAN interface and create DroneCAN node with unique node ID.

```py
import dronecan
from dronecan.driver.socketcan import SocketCAN

def setup_can_interface(interface='can0', bitrate=1000000, node_id=111):
    """Setup CAN interface and create DroneCAN node"""
    # Initialize CAN driver (SocketCAN for Linux)
    can_driver = SocketCAN(interface, bitrate=bitrate)
    
    # Create DroneCAN node with unique ID
    node = dronecan.make_node(can_driver, node_id=node_id)
    
    # Set node info (optional, for identification)
    node_info = dronecan.uavcan.protocol.GetNodeInfo.Response()
    node_info.name = "quiver_telemetry_bridge"
    node_info.software_version.major = 1
    node_info.software_version.minor = 0
    node.node_info = node_info
    
    print(f"DroneCAN node initialized on {interface} with ID {node_id}")
    return node

# Usage
node = setup_can_interface(interface='can0', node_id=111)
```

**CAN Interface Setup** (run once on companion computer):

```shell
# Bring up CAN interface
sudo ip link set can0 up type can bitrate 1000000

# Verify interface is up
ip link show can0
```

#### Subscribe to Battery Messages

Listen for DroneCAN BatteryInfo messages and extract voltage, current, temperature.

```py
def battery_callback(event):
    """Callback for DroneCAN BatteryInfo messages"""
    msg = event.message
    
    print(f"Battery Info:")
    print(f"  Voltage: {msg.voltage:.2f}V")
    print(f"  Current: {msg.current:.2f}A")
    print(f"  Temperature: {msg.temperature:.1f}°C")
    print(f"  State of Charge: {msg.state_of_charge_pct:.0f}%")
    print(f"  Full Charge Capacity: {msg.full_charge_capacity_wh:.1f}Wh")

def subscribe_battery_info(node):
    """Subscribe to DroneCAN BatteryInfo messages"""
    # Register callback for BatteryInfo messages
    node.add_handler(
        dronecan.uavcan.equipment.power.BatteryInfo,
        battery_callback
    )
    
    print("Subscribed to BatteryInfo messages")
    
    # Spin node (blocking, processes CAN messages)
    try:
        node.spin()
    except KeyboardInterrupt:
        print("Shutting down...")

# Usage
node = setup_can_interface()
subscribe_battery_info(node)
```

**Common DroneCAN Message Types**:

- `uavcan.equipment.power.BatteryInfo`: Battery voltage, current, temperature, SoC  
- `uavcan.equipment.gnss.Fix`: GPS position, velocity, accuracy  
- `uavcan.equipment.air_data.StaticPressure`: Barometric pressure  
- `uavcan.equipment.air_data.StaticTemperature`: Air temperature  
- `uavcan.equipment.ahrs.MagneticFieldStrength`: Magnetometer data

---

## 5\. Practical Tutorials

These tutorials provide complete, working examples that developers can use as templates for their own applications. Each tutorial builds on the previous one, introducing new concepts and techniques.

### 5.1 Tutorial: Simple Temperature Sensor

**Goal**: Read Raspberry Pi CPU temperature and send to Quiver Hub every 5 seconds.

**Hardware**: Raspberry Pi (any model), no external sensors required.

**Concepts**: Basic HTTP POST, JSON formatting, infinite loop with sleep.

```py
#!/usr/bin/env python3
"""
Simple CPU temperature sensor forwarder
Reads Raspberry Pi CPU temp and sends to Quiver Hub
"""

import requests
import time
from datetime import datetime

# Configuration
SERVER_URL = "https://your-hub.com"
API_KEY = "abc123"
DRONE_ID = "quiver_001"
SAMPLE_INTERVAL = 5  # seconds

def read_cpu_temp():
    """Read CPU temperature from system file"""
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp_millidegrees = int(f.read().strip())
            return temp_millidegrees / 1000.0
    except FileNotFoundError:
        print("Warning: CPU temp file not found, returning dummy value")
        return 25.0

def send_telemetry(temperature):
    """Send temperature data to Quiver Hub"""
    url = f"{SERVER_URL}/api/rest/sensor-data/ingest"
    headers = {'x-api-key': API_KEY}
    
    data = {
        'droneId': DRONE_ID,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'sensorType': 'cpu_temperature',
        'data': {
            'temperature_c': temperature
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=5)
        response.raise_for_status()
        print(f"Sent: {temperature:.1f}°C")
    except requests.exceptions.RequestException as e:
        print(f"Error sending telemetry: {e}")

def main():
    """Main loop"""
    print(f"Starting CPU temperature monitor for {DRONE_ID}")
    print(f"Sending to: {SERVER_URL}")
    print(f"Sample interval: {SAMPLE_INTERVAL}s")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            temp = read_cpu_temp()
            send_telemetry(temp)
            time.sleep(SAMPLE_INTERVAL)
    except KeyboardInterrupt:
        print("\nShutting down...")

if __name__ == '__main__':
    main()
```

**Deployment**:

1. Save as `/home/pi/quiver/cpu_temp_monitor.py`  
2. Make executable: `chmod +x cpu_temp_monitor.py`  
3. Test: `python3 cpu_temp_monitor.py`  
4. Install as systemd service (see Section 6.1)

**Expected Output**:

```
Starting CPU temperature monitor for quiver_001
Sending to: https://your-hub.com
Sample interval: 5s
Press Ctrl+C to stop
Sent: 42.3°C
Sent: 43.1°C
Sent: 42.8°C
```

### 5.2 Tutorial: Custom Job Handler

**Goal**: Extend Quiver Hub Client to handle a custom "restart\_service" job type.

**Hardware**: Raspberry Pi with systemd services.

**Concepts**: Extending QuiverHubClient class, subprocess execution, error handling.

```py
#!/usr/bin/env python3
"""
Extended Quiver Hub Client with custom job handler
Adds support for restarting systemd services remotely
"""

import subprocess
from typing import Dict, Optional, Tuple
from raspberry_pi_client import QuiverHubClient  # Import base class

class ExtendedQuiverHubClient(QuiverHubClient):
    """Extended client with custom job handlers"""
    
    def handle_restart_service_job(self, job: Dict) -> Tuple[bool, Optional[str]]:
        """
        Handle a restart_service job
        
        Job payload format:
        {
            "serviceName": "quiver-telemetry"
        }
        """
        try:
            payload = job.get('payload', {})
            service_name = payload.get('serviceName')
            
            if not service_name:
                return False, "Missing serviceName in job payload"
            
            self.logger.info(f"Restarting service: {service_name}")
            
            # Execute systemctl restart
            result = subprocess.run(
                ['sudo', 'systemctl', 'restart', service_name],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.logger.info(f"Service {service_name} restarted successfully")
                return True, None
            else:
                error_msg = result.stderr.strip() or "Unknown error"
                self.logger.error(f"Failed to restart {service_name}: {error_msg}")
                return False, error_msg
                
        except subprocess.TimeoutExpired:
            return False, "Service restart timed out after 30 seconds"
        except Exception as e:
            self.logger.error(f"Error handling restart_service job: {e}")
            return False, str(e)
    
    def process_job(self, job: Dict):
        """
        Override process_job to handle custom job types
        """
        job_id = job.get('id')
        job_type = job.get('type')
        
        self.logger.info(f"Processing job {job_id}: {job_type}")
        
        # Acknowledge the job
        if not self.acknowledge_job(job_id):
            self.logger.error(f"Failed to acknowledge job {job_id}, skipping")
            return
        
        # Execute the job based on type
        success = False
        error_message = None
        
        try:
            if job_type == 'upload_file':
                success, error_message = self.handle_upload_file_job(job)
            elif job_type == 'update_config':
                success, error_message = self.handle_update_config_job(job)
            elif job_type == 'restart_service':
                # Custom job type
                success, error_message = self.handle_restart_service_job(job)
            else:
                error_message = f"Unknown job type: {job_type}"
                self.logger.warning(error_message)
        
        except Exception as e:
            error_message = f"Unexpected error: {str(e)}"
            self.logger.error(error_message)
        
        # Report completion
        self.complete_job(job_id, success, error_message)

# Usage (replace QuiverHubClient with ExtendedQuiverHubClient in main())
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Extended Quiver Hub Client')
    parser.add_argument('--server', required=True)
    parser.add_argument('--drone-id', required=True)
    parser.add_argument('--api-key', required=True)
    parser.add_argument('--poll-interval', type=int, default=5)
    
    args = parser.parse_args()
    
    client = ExtendedQuiverHubClient(
        server_url=args.server,
        drone_id=args.drone_id,
        api_key=args.api_key,
        poll_interval=args.poll_interval
    )
    
    client.run()
```

**Testing**:

1. Create job in Hub UI with type "restart\_service" and payload `{"serviceName": "quiver-telemetry"}`  
2. Client will pick up job, execute `sudo systemctl restart quiver-telemetry`  
3. Check logs: `sudo journalctl -u quiver-client -f`

**Sudoers Configuration** (required for passwordless sudo):

```shell
# Add to /etc/sudoers.d/quiver-client
pi ALL=(ALL) NOPASSWD: /bin/systemctl restart *
```

### 5.3 Tutorial: WebSocket Sensor Stream

**Goal**: Stream LiDAR point cloud data in real-time using WebSocket.

**Hardware**: Raspberry Pi with RPLidar A1/A2/A3 connected via USB.

**Concepts**: WebSocket client, async/await, binary data handling.

```py
#!/usr/bin/env python3
"""
RPLidar point cloud streamer using WebSocket
Streams 2D laser scan data to Quiver Hub for real-time visualization
"""

import asyncio
import socketio
from datetime import datetime
from rplidar import RPLidar

# Configuration
SERVER_URL = "https://your-hub.com"
API_KEY = "abc123"
DRONE_ID = "quiver_001"
LIDAR_PORT = "/dev/ttyUSB0"

# Create Socket.IO client
sio = socketio.AsyncClient()

@sio.event
async def connect():
    """Called when WebSocket connection is established"""
    print("Connected to Quiver Hub")
    await sio.emit('subscribe', {
        'droneId': DRONE_ID,
        'dataType': 'lidar',
        'apiKey': API_KEY
    })
    print("Subscribed to lidar channel")

@sio.event
async def disconnect():
    """Called when WebSocket connection is lost"""
    print("Disconnected from Quiver Hub")

@sio.event
async def error(data):
    """Called when server sends error message"""
    print(f"Error from server: {data}")

async def stream_lidar_data():
    """Main loop: read LiDAR scans and stream via WebSocket"""
    # Connect to Quiver Hub
    await sio.connect(f"{SERVER_URL}?apiKey={API_KEY}")
    
    # Initialize RPLidar
    lidar = RPLidar(LIDAR_PORT)
    
    try:
        print(f"Starting RPLidar on {LIDAR_PORT}")
        lidar.start_motor()
        
        for scan in lidar.iter_scans():
            # Convert scan to point cloud format
            points = []
            for quality, angle, distance in scan:
                # Convert polar to Cartesian coordinates
                angle_rad = angle * 3.14159 / 180.0
                x = distance * math.cos(angle_rad) / 1000.0  # mm to meters
                y = distance * math.sin(angle_rad) / 1000.0
                z = 0.0  # 2D LiDAR, no height
                
                points.append({
                    'x': x,
                    'y': y,
                    'z': z,
                    'intensity': quality
                })
            
            # Send point cloud via WebSocket
            await sio.emit('pointcloud_data', {
                'droneId': DRONE_ID,
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'pointCount': len(points),
                'points': points
            })
            
            print(f"Sent {len(points)} points")
            
            # Rate limit to ~10 Hz
            await asyncio.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
        await sio.disconnect()

if __name__ == '__main__':
    asyncio.run(stream_lidar_data())
```

**Dependencies**:

```shell
pip3 install python-socketio rplidar-roboticia aiohttp
```

**Expected Output**:

```
Connected to Quiver Hub
Subscribed to lidar channel
Starting RPLidar on /dev/ttyUSB0
Sent 362 points
Sent 359 points
Sent 361 points
```

**Hub Visualization**: Create custom app in Hub UI Builder with PointCloudCanvas widget to render 3D point cloud in real-time.

---

## 6\. Deployment

Production deployments require proper service management, logging, and error handling. This section covers best practices for deploying Quiver SDK applications on companion computers.

### 6.1 Systemd Service Setup

Systemd services ensure applications start automatically on boot and restart on failure. Each SDK application (client, telemetry forwarder, sensor forwarders) should run as a separate service.

**Create Service File**:

Create `/etc/systemd/system/quiver-client.service`:

```
[Unit]
Description=Quiver Hub Client
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/quiver
ExecStart=/usr/bin/python3 /home/pi/quiver/raspberry_pi_client.py \
  --server https://your-hub.com \
  --drone-id quiver_001 \
  --api-key abc123 \
  --poll-interval 5
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**Key Configuration Options**:

- `After=network-online.target`: Wait for network before starting  
- `Restart=always`: Restart on any exit (crash, manual stop, etc.)  
- `RestartSec=10`: Wait 10 seconds before restart to avoid rapid restart loops  
- `StandardOutput=journal`: Send stdout/stderr to systemd journal for centralized logging

**Enable and Start Service**:

```shell
# Reload systemd to recognize new service
sudo systemctl daemon-reload

# Enable service (start on boot)
sudo systemctl enable quiver-client.service

# Start service now
sudo systemctl start quiver-client.service

# Check status
sudo systemctl status quiver-client.service

# View logs
sudo journalctl -u quiver-client.service -f
```

**Multiple Services**:

For a complete deployment, create separate services for each component:

- `quiver-client.service`: Job polling and execution  
- `quiver-telemetry.service`: Flight controller telemetry forwarding  
- `quiver-lidar.service`: LiDAR point cloud streaming (if applicable)  
- `quiver-camera.service`: Camera streaming (if applicable)

This modular approach allows independent restart and monitoring of each component.

### 6.2 Environment Variables

Environment variables provide configuration without hardcoding values in scripts. Use a `.env` file for local development and systemd `EnvironmentFile` for production.

**Create Environment File**:

Create `/home/pi/quiver/.env`:

```shell
# Quiver Hub Configuration
WEB_SERVER_URL=https://your-hub.com/api/rest/telemetry/ingest
API_KEY=abc123
DRONE_ID=quiver_001

# MAVLink Configuration
MAVLINK_URL=udpin://0.0.0.0:14540

# CAN Bus Configuration
CAN_INTERFACE=can0

# Telemetry Configuration
UPDATE_RATE_HZ=10

# Logging Configuration
LOG_LEVEL=INFO
```

**Load in Python Script**:

```py
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv('/home/pi/quiver/.env')

# Access variables
SERVER_URL = os.getenv('WEB_SERVER_URL')
API_KEY = os.getenv('API_KEY')
DRONE_ID = os.getenv('DRONE_ID')
```

**Use in Systemd Service**:

Modify service file to load environment variables:

```
[Service]
EnvironmentFile=/home/pi/quiver/.env
ExecStart=/usr/bin/python3 /home/pi/quiver/telemetry_forwarder.py
```

**Security Note**: Protect `.env` file from unauthorized access:

```shell
chmod 600 /home/pi/quiver/.env
```

### 6.3 Logging

Structured logging helps diagnose issues in production. Use Python's `logging` module with rotating file handlers to prevent disk space exhaustion.

**Configure Logging**:

```py
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(log_file='/var/log/quiver/client.log', level=logging.INFO):
    """Configure logging with rotation"""
    # Create log directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    os.makedirs(log_dir, exist_ok=True)
    
    # Create rotating file handler (10 MB per file, keep 5 backups)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5
    )
    
    # Create console handler for stdout
    console_handler = logging.StreamHandler()
    
    # Set format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    logging.basicConfig(
        level=level,
        handlers=[file_handler, console_handler]
    )

# Usage in application
setup_logging()
logger = logging.getLogger(__name__)

logger.info("Application started")
logger.warning("Low battery voltage: 11.2V")
logger.error("Failed to connect to Hub", exc_info=True)
```

**Log Levels**:

- `DEBUG`: Detailed diagnostic information (use sparingly in production)  
- `INFO`: General informational messages (normal operation)  
- `WARNING`: Warning messages (degraded performance, recoverable errors)  
- `ERROR`: Error messages (operation failed, but application continues)  
- `CRITICAL`: Critical errors (application cannot continue)

**View Logs**:

```shell
# View systemd journal logs
sudo journalctl -u quiver-client -f

# View file logs
tail -f /var/log/quiver/client.log

# Search logs for errors
grep ERROR /var/log/quiver/*.log

# View logs from last hour
journalctl -u quiver-client --since "1 hour ago"
```

---

## 7\. Best Practices

Following these best practices ensures robust, maintainable, and production-ready applications.

### 7.1 Error Handling

Implement comprehensive error handling with retry logic for network operations and graceful degradation for sensor failures.

**HTTP Retry Strategy**:

```py
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session_with_retries():
    """Create requests session with automatic retry on failure"""
    session = requests.Session()
    
    # Configure retry strategy
    retry = Retry(
        total=3,  # Total number of retries
        backoff_factor=1,  # Wait 1s, 2s, 4s between retries
        status_forcelist=[500, 502, 503, 504],  # Retry on server errors
        allowed_methods=["GET", "POST"]  # Retry these HTTP methods
    )
    
    # Mount adapter with retry strategy
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    return session

# Usage
session = create_session_with_retries()

try:
    response = session.post(url, json=data, timeout=10)
    response.raise_for_status()
except requests.exceptions.Timeout:
    logger.error("Request timed out after 10 seconds")
except requests.exceptions.ConnectionError:
    logger.error("Failed to connect to server")
except requests.exceptions.HTTPError as e:
    logger.error(f"HTTP error: {e.response.status_code}")
except requests.exceptions.RequestException as e:
    logger.error(f"Request failed: {e}")
```

**Sensor Error Handling**:

```py
def read_sensor_with_fallback():
    """Read sensor with fallback to default value"""
    try:
        value = sensor.read()
        if value is None or value < 0:
            raise ValueError("Invalid sensor reading")
        return value
    except (IOError, ValueError) as e:
        logger.warning(f"Sensor read failed: {e}, using default value")
        return DEFAULT_VALUE
```

### 7.2 Threading Safety

When using multiple threads to access shared data, protect with locks to prevent race conditions.

**Thread-Safe Telemetry Collector**:

```py
import threading
from typing import Dict, Any

class TelemetryCollector:
    """Thread-safe telemetry data collector"""
    
    def __init__(self):
        self.data_lock = threading.Lock()
        self.telemetry = {}
    
    def update_attitude(self, roll, pitch, yaw):
        """Update attitude data (called from MAVLink thread)"""
        with self.data_lock:
            self.telemetry['attitude'] = {
                'roll': roll,
                'pitch': pitch,
                'yaw': yaw
            }
    
    def update_position(self, lat, lon, alt):
        """Update position data (called from MAVLink thread)"""
        with self.data_lock:
            self.telemetry['position'] = {
                'latitude': lat,
                'longitude': lon,
                'altitude': alt
            }
    
    def get_snapshot(self) -> Dict[str, Any]:
        """Get thread-safe copy of telemetry (called from HTTP thread)"""
        with self.data_lock:
            return self.telemetry.copy()

# Usage
collector = TelemetryCollector()

# MAVLink thread
def mavlink_thread():
    async for attitude in drone.telemetry.attitude_euler():
        collector.update_attitude(
            attitude.roll_deg,
            attitude.pitch_deg,
            attitude.yaw_deg
        )

# HTTP thread
def http_thread():
    while True:
        telemetry = collector.get_snapshot()
        send_to_hub(telemetry)
        time.sleep(0.1)
```

### 7.3 Configuration Management

Centralize configuration in a single file with validation and defaults.

**Configuration Class**:

```py
import json
from pathlib import Path
from typing import Dict, Any

class Config:
    """Configuration manager with validation and defaults"""
    
    DEFAULT_CONFIG = {
        'server_url': 'http://localhost:3000',
        'drone_id': 'quiver_001',
        'api_key': '',
        'poll_interval': 5,
        'update_rate_hz': 10,
        'mavlink_url': 'udpin://0.0.0.0:14540',
        'can_interface': 'can0'
    }
    
    def __init__(self, config_file='/home/pi/config/quiver_config.json'):
        self.config_file = Path(config_file)
        self.data = {}
        self.load()
    
    def load(self):
        """Load configuration from file or use defaults"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.data = json.load(f)
                # Merge with defaults (add missing keys)
                for key, value in self.DEFAULT_CONFIG.items():
                    if key not in self.data:
                        self.data[key] = value
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON in {self.config_file}, using defaults")
                self.data = self.DEFAULT_CONFIG.copy()
        else:
            logger.info(f"Config file not found, using defaults")
            self.data = self.DEFAULT_CONFIG.copy()
            self.save()
    
    def save(self):
        """Save configuration to file"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def get(self, key: str, default=None) -> Any:
        """Get configuration value"""
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        self.data[key] = value
        self.save()

# Usage
config = Config()
server_url = config.get('server_url')
drone_id = config.get('drone_id')
```

---

## 8\. Troubleshooting

Common issues and solutions for Quiver SDK deployments.

### 8.1 Connection Issues

**Problem**: Client cannot reach Quiver Hub

**Symptoms**:

- `requests.exceptions.ConnectionError: Failed to establish connection`  
- Logs show "Connection refused" or "Name or service not known"

**Solutions**:

1. **Check network connectivity**:

```shell
ping your-hub.com
# Should show replies if network is working
```

2. **Verify DNS resolution**:

```shell
nslookup your-hub.com
# Should return IP address
```

3. **Test HTTPS endpoint**:

```shell
curl -I https://your-hub.com/api/health
# Should return HTTP 200 OK
```

4. **Check firewall**:

```shell
sudo ufw status
# Ensure outbound HTTPS (port 443) is allowed
```

5. **Verify API key**:  
- Check Hub dashboard for correct API key  
- Ensure no extra spaces or newlines in key  
6. **Check system time**:

```shell
timedatectl
# HTTPS certificates require accurate time
sudo timedatectl set-ntp true
```

### 8.2 MAVLink Connection Failures

**Problem**: Cannot connect to flight controller

**Symptoms**:

- MAVSDK timeout waiting for connection  
- No telemetry data received  
- Logs show "No system found"

**Solutions**:

1. **Verify CAN interface is up**:

```shell
ip link show can0
# Should show "UP" state

# If down, bring it up:
sudo ip link set can0 up type can bitrate 1000000
```

2. **Check MAVLink traffic**:

```shell
# Install mavproxy for debugging
pip3 install mavproxy

# Monitor MAVLink messages
mavproxy.py --master=udpin:0.0.0.0:14540
# Should show HEARTBEAT messages if FC is connected
```

3. **Verify flight controller parameters**:  
- ArduPilot: `CAN_P1_DRIVER = 1` (enable CAN port 1\)  
- ArduPilot: `CAN_D1_PROTOCOL = 1` (MAVLink on CAN)  
- PX4: `UAVCAN_ENABLE = 2` (enable UAVCAN)  
4. **Check baud rate** (if using serial):

```shell
# Flight controller must match companion computer baud rate
# Common rates: 57600, 115200, 921600
```

5. **Try different connection strings**:

```py
# UDP (simulation)
await drone.connect("udpin://0.0.0.0:14540")

# Serial (direct)
await drone.connect("serial:///dev/ttyACM0:57600")

# TCP (network)
await drone.connect("tcp://192.168.1.100:5760")
```

### 8.3 CAN Bus Issues

**Problem**: No UAVCAN messages received

**Symptoms**:

- DroneCAN node spins but no callbacks triggered  
- `candump can0` shows no traffic  
- Battery data not updating

**Solutions**:

1. **Verify CAN interface exists**:

```shell
ip link show can0
# If not found, check hardware connections
```

2. **Check CAN bitrate**:

```shell
# Must match flight controller bitrate (typically 1 Mbps)
sudo ip link set can0 up type can bitrate 1000000
```

3. **Monitor CAN traffic**:

```shell
# Install can-utils
sudo apt install can-utils

# Dump all CAN messages
candump can0
# Should show messages if bus is active
```

4. **Check termination resistors**:  
- CAN bus requires 120Ω resistors at each end  
- Use multimeter to measure resistance between CAN\_H and CAN\_L (should be \~60Ω)  
5. **Verify node IDs**:  
- Each DroneCAN node must have unique ID (1-127)  
- Companion computer typically uses high ID (100+) to avoid conflicts  
6. **Check wiring**:  
- CAN\_H and CAN\_L must not be swapped  
- Use twisted pair cable for CAN bus  
- Keep cable length \< 40m for 1 Mbps bitrate

---

## 9\. Extension Points

The Quiver SDK is designed for extensibility. Developers can add new capabilities without modifying core code.

### 9.1 Adding New Data Sources

To integrate a new sensor or data source, follow this pattern:

1. **Create Python script** to read sensor data  
2. **Format as JSON** with timestamp and drone ID  
3. **POST to Hub** using `/api/rest/sensor-data/ingest` endpoint  
4. **Create visualization** in Hub UI Builder

**Example: DHT22 Temperature/Humidity Sensor**:

```py
import Adafruit_DHT
import requests
from datetime import datetime

SENSOR = Adafruit_DHT.DHT22
PIN = 4

while True:
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)
    
    data = {
        "droneId": "quiver_001",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "sensorType": "dht22",
        "data": {
            "temperature_c": temperature,
            "humidity_percent": humidity
        }
    }
    
    requests.post(
        "https://your-hub.com/api/rest/sensor-data/ingest",
        json=data,
        headers={"x-api-key": "abc123"}
    )
    
    time.sleep(5)
```

### 9.2 Custom Job Types

To add custom job types, extend the `QuiverHubClient` class:

1. **Implement handler method** (returns `Tuple[bool, Optional[str]]`)  
2. **Register in `process_job()`** method  
3. **Create job in Hub UI** with custom type and payload

**Example: Run Shell Script Job**:

```py
def handle_run_script_job(self, job: Dict) -> Tuple[bool, Optional[str]]:
    """Execute a shell script"""
    payload = job.get('payload', {})
    script_path = payload.get('scriptPath')
    
    if not os.path.exists(script_path):
        return False, f"Script not found: {script_path}"
    
    try:
        result = subprocess.run(
            ['bash', script_path],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            return True, None
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)
```

### 9.3 Integration with External Systems

The Quiver SDK can integrate with external systems using standard protocols.

**ROS/ROS2 Integration**:

```py
import rclpy
from sensor_msgs.msg import NavSatFix

def gps_callback(msg):
    """Forward ROS GPS message to Quiver Hub"""
    data = {
        "droneId": "quiver_001",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "position": {
            "latitude": msg.latitude,
            "longitude": msg.longitude,
            "altitude": msg.altitude
        }
    }
    
    requests.post(HUB_URL, json=data, headers={"x-api-key": API_KEY})

# Subscribe to ROS topic
rclpy.init()
node = rclpy.create_node('quiver_bridge')
subscription = node.create_subscription(NavSatFix, '/gps/fix', gps_callback, 10)
rclpy.spin(node)
```

**ArduPilot Lua Scripts**:

```
-- Trigger Quiver Hub job via MAVLink command
function trigger_job()
    gcs:send_text(0, "Triggering Quiver Hub job")
    -- Send MAVLink command to companion computer
    -- Companion computer receives command and creates job in Hub
end

return trigger_job, 1000  -- Run every 1000ms
```

---

## 10\. Reference

Quick reference for dependencies, commands, and file locations.

### 10.1 Dependencies

**Core Dependencies**:

```shell
pip3 install requests aiohttp mavsdk dronecan python-socketio python-dotenv
```

**Optional Dependencies**:

```shell
# For DHT sensors
pip3 install Adafruit_DHT

# For RPLidar
pip3 install rplidar-roboticia

# For ROS integration
pip3 install rclpy sensor-msgs

# For advanced HTTP features
pip3 install urllib3
```

### 10.2 Useful Commands

**Service Management**:

```shell
# Check service status
sudo systemctl status quiver-client

# View logs (follow mode)
sudo journalctl -u quiver-client -f

# Restart service
sudo systemctl restart quiver-client

# Enable service (start on boot)
sudo systemctl enable quiver-client

# Disable service
sudo systemctl disable quiver-client
```

**API Testing**:

```shell
# Test telemetry endpoint
curl -X POST https://your-hub.com/api/rest/telemetry/ingest \
  -H "x-api-key: abc123" \
  -H "Content-Type: application/json" \
  -d '{"droneId":"quiver_001","timestamp":"2026-01-08T10:00:00Z","test":true}'

# Test job polling endpoint
curl "https://your-hub.com/api/trpc/droneJobs.getPendingJobs?input=%7B%22json%22%3A%7B%22droneId%22%3A%22quiver_001%22%2C%22apiKey%22%3A%22abc123%22%7D%7D"
```

**CAN Bus**:

```shell
# Bring up CAN interface
sudo ip link set can0 up type can bitrate 1000000

# Monitor CAN traffic
candump can0

# Send CAN message (testing)
cansend can0 123#DEADBEEF

# Check CAN statistics
ip -details -statistics link show can0
```

**MAVLink**:

```shell
# Monitor MAVLink traffic
mavproxy.py --master=udpin:0.0.0.0:14540

# Test MAVLink connection
mavproxy.py --master=serial:/dev/ttyACM0:57600
```

### 10.3 File Locations

**Application Files**:

- Client script: `/home/pi/quiver/raspberry_pi_client.py`  
- Telemetry forwarder: `/home/pi/quiver/telemetry_forwarder.py`  
- Custom sensor scripts: `/home/pi/quiver/sensors/`

**Configuration**:

- Environment variables: `/home/pi/quiver/.env`  
- JSON configuration: `/home/pi/config/quiver_config.json`

**Logs**:

- Application logs: `/var/log/quiver/*.log`  
- Systemd journal: `journalctl -u quiver-*`

**System Services**:

- Service files: `/etc/systemd/system/quiver-*.service`  
- Sudoers config: `/etc/sudoers.d/quiver-client`

**Network**:

- CAN interface: `/sys/class/net/can0/`  
- Network config: `/etc/network/interfaces` or `/etc/netplan/`

[image1]: <data:image/png;base64,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>