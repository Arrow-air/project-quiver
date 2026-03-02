# Remote ID Pi Script

Automatically broadcasts OpenDroneID data from the Raspberry Pi to the DroneBeacon db201 via ArduPilot's MAVLink OpenDroneID interface.

## What it does

- Reads operator/drone IDs from `config.yaml`
- Connects to ArduPilot over the PPP network (or serial)
- Waits for first GPS fix, locks that position as the operator location
- Sends `OPEN_DRONE_ID_BASIC_ID`, `OPEN_DRONE_ID_OPERATOR_ID`, and `OPEN_DRONE_ID_SYSTEM` at 1 Hz
- Operator location stays fixed until reboot (no GCS GPS required)

## Setup

### 1. Install dependencies

```bash
pip3 install pymavlink pyyaml
```

### 2. Copy files to the Pi

```bash
mkdir -p ~/remoteid
cp remoteid.py config.yaml ~/remoteid/
```

### 3. Edit config

```bash
nano ~/remoteid/config.yaml
```

Set your `uas_id`, `operator_id`, and `connection` string.

**Connection options:**
- PPP network (when PPP is up): `tcp:192.168.13.14:5760`
- Direct serial: `/dev/serial0:921600`
- UDP (if FC broadcasts): `udpin:0.0.0.0:14550`

Check your FC's PPP-assigned IP with `ip addr show ppp0` on the Pi.

### 4. Test manually

```bash
python3 ~/remoteid/remoteid.py
```

You should see it connect, wait for GPS, then log "Broadcasting Remote ID messages..."

### 5. Install as a systemd service (auto-start on boot)

```bash
sudo cp remoteid.service /etc/systemd/system/
# Edit the paths in the service file if needed
sudo systemctl daemon-reload
sudo systemctl enable remoteid
sudo systemctl start remoteid

# Check status
sudo systemctl status remoteid
journalctl -u remoteid -f
```

## ArduPilot parameters required

In addition to this script, set in Mission Planner:

```
DID_ENABLE = 1
DID_CANDRIVER = 1
DID_MAVPORT = -1
```

The script handles the operator/drone ID configuration — no need to set those in Mission Planner manually anymore.

## Notes

- The operator location is locked on first GPS fix and held until reboot. This satisfies most regulatory requirements for fixed-location operations.
- The script retries connection automatically — safe to start before the FC has booted.
- For EU operations, set `operator_id_type: 1` (EASA) and `operator_id` to your EASA operator registration number.
