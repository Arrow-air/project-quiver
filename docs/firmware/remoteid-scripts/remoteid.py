#!/usr/bin/env python3
"""
Quiver Remote ID broadcaster for DroneBeacon db201
Runs on the onboard Raspberry Pi.

- Reads operator/drone config from config.yaml
- Connects to ArduPilot via MAVLink (PPP network or serial)
- Waits for first GPS fix, locks that position as operator location
- Sends OPEN_DRONE_ID_* messages at 1 Hz until shutdown

Install:
    pip3 install pymavlink pyyaml

Run:
    python3 remoteid.py

Run as a service: see remoteid.service
"""

import time
import sys
import os
import logging
import yaml
from pymavlink import mavutil
from pymavlink.dialects.v20 import ardupilotmega as mavlink2

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
log = logging.getLogger("remoteid")

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.yaml")


def load_config():
    with open(CONFIG_FILE) as f:
        return yaml.safe_load(f)


def encode_uas_id(uas_id_str: str, max_len: int = 20) -> bytes:
    """Encode UAS ID string to fixed-length byte array."""
    encoded = uas_id_str.encode("ascii", errors="replace")[:max_len]
    return encoded.ljust(max_len, b"\x00")


def wait_for_gps_fix(conn, min_fix_type: int = 3, timeout_sec: int = 300):
    """Wait for GPS fix >= min_fix_type. Returns (lat_deg, lon_deg, alt_m)."""
    log.info(f"Waiting for GPS fix (type >= {min_fix_type})...")
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        msg = conn.recv_match(type=["GPS_RAW_INT", "GLOBAL_POSITION_INT"], blocking=True, timeout=2)
        if msg is None:
            continue
        if msg.get_type() == "GPS_RAW_INT":
            if msg.fix_type >= min_fix_type and msg.lat != 0:
                lat = msg.lat / 1e7
                lon = msg.lon / 1e7
                alt = msg.alt / 1000.0
                log.info(f"GPS fix acquired: {lat:.6f}, {lon:.6f}, alt={alt:.1f}m (fix_type={msg.fix_type})")
                return lat, lon, alt
        elif msg.get_type() == "GLOBAL_POSITION_INT":
            if msg.lat != 0:
                lat = msg.lat / 1e7
                lon = msg.lon / 1e7
                alt = msg.alt / 1000.0
                log.info(f"GPS position: {lat:.6f}, {lon:.6f}, alt={alt:.1f}m")
                return lat, lon, alt
    raise TimeoutError(f"No GPS fix after {timeout_sec}s")


def send_basic_id(conn, cfg):
    """Send OPEN_DRONE_ID_BASIC_ID."""
    uas_id_bytes = encode_uas_id(cfg["uas_id"])
    conn.mav.open_drone_id_basic_id_send(
        0, 0,           # target system, target component (0 = broadcast)
        [0] * 20,       # id_or_mac (empty = use uas_id)
        int(cfg["id_type"]) if "id_type" in cfg else int(cfg["uas_id_type"]),
        int(cfg["ua_type"]),
        list(uas_id_bytes),
    )


def send_operator_id(conn, cfg):
    """Send OPEN_DRONE_ID_OPERATOR_ID."""
    op_id = cfg["operator_id"].encode("ascii", errors="replace")[:20].ljust(20, b"\x00")
    conn.mav.open_drone_id_operator_id_send(
        0, 0,           # target system, target component
        [0] * 20,       # id_or_mac
        int(cfg["operator_id_type"]),
        list(op_id),
    )


def send_system(conn, cfg, operator_lat, operator_lon):
    """Send OPEN_DRONE_ID_SYSTEM with fixed operator location."""
    conn.mav.open_drone_id_system_send(
        0, 0,                           # target system, target component
        [0] * 20,                       # id_or_mac
        0,                              # operator_location_type: 0=takeoff/fixed
        int(operator_lat * 1e7),        # operator_lat (degE7)
        int(operator_lon * 1e7),        # operator_lon (degE7)
        1,                              # area_count
        0,                              # area_radius
        -1000,                          # area_ceiling (no limit)
        -1000,                          # area_floor (no limit)
        int(cfg.get("ua_type", 2)),     # category_eu
        0,                              # class_eu
        0.0,                            # operator_altitude_geo
        int(time.time()),               # timestamp
    )


def main():
    cfg = load_config()
    log.info(f"Config loaded: UAS_ID={cfg['uas_id']}, Operator={cfg['operator_id']}")
    log.info(f"Connecting to ArduPilot: {cfg['connection']}")

    # Connect (retry loop — wait for FC to boot and PPP to come up)
    conn = None
    while conn is None:
        try:
            conn = mavutil.mavlink_connection(cfg["connection"], autoreconnect=True)
            conn.wait_heartbeat(timeout=10)
            log.info(f"Connected — system {conn.target_system}, component {conn.target_component}")
        except Exception as e:
            log.warning(f"Connection failed ({e}), retrying in 5s...")
            conn = None
            time.sleep(5)

    # Wait for GPS fix and lock operator location
    try:
        operator_lat, operator_lon, operator_alt = wait_for_gps_fix(conn)
    except TimeoutError:
        log.warning("GPS fix timeout — using 0,0 as operator location (will update on next reboot with fix)")
        operator_lat, operator_lon = 0.0, 0.0

    log.info(f"Operator location locked at: {operator_lat:.6f}, {operator_lon:.6f}")
    log.info("Broadcasting Remote ID messages...")

    interval = 1.0 / max(cfg.get("rate_hz", 1), 1)

    while True:
        try:
            send_basic_id(conn, cfg)
            send_operator_id(conn, cfg)
            send_system(conn, cfg, operator_lat, operator_lon)
        except Exception as e:
            log.warning(f"Send error: {e}")

        time.sleep(interval)


if __name__ == "__main__":
    main()
