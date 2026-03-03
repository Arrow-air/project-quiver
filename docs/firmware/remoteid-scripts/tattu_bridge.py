import can
import struct
import time
import sys
import logging
import dronecan
from dronecan.driver.socketcan import SocketCAN

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger("tattu_bridge")

# --- Configuration ---
CAN_INTERFACE   = 'can0'
TATTU_CAN_ID    = 0x01109216
MY_NODE_ID      = 110
TARGET_BITRATE  = 1000000

# Sanity bounds for a 14S Tattu pack — adjust if using a different pack
VOLTAGE_MIN_V   = 38.0   # 14S @ 2.7V/cell
VOLTAGE_MAX_V   = 60.0   # 14S @ 4.3V/cell
CURRENT_MAX_A   = 400.0  # absolute max, reject anything beyond this

# If SOC was above this threshold and we suddenly read 0%, treat as decode error
SOC_JUMP_THRESHOLD = 10   # % — won't ignore if last SOC was also low


class TattuBridge:
    def __init__(self):
        self.collecting = False
        self.frames = []
        self.last_frame_time = 0
        self.bus = None
        self.node = None

        # Last-known-good state — broadcast stale values rather than 0%
        self.last_voltage = None
        self.last_current = None
        self.last_temp    = None
        self.last_soc     = None
        self.last_good_ts = 0

    def connect(self):
        try:
            self.bus = can.interface.Bus(channel=CAN_INTERFACE, interface='socketcan')
            log.info(f"Listener connected on {CAN_INTERFACE}.")

            driver = SocketCAN(CAN_INTERFACE)
            self.node = dronecan.node.Node(driver, node_id=MY_NODE_ID)

            node_info = dronecan.uavcan.protocol.GetNodeInfo.Response()
            node_info.name = 'org.tattu.bridge'
            node_info.software_version.major = 1
            self.node.node_info = node_info
            self.node.mode   = dronecan.uavcan.protocol.NodeStatus().MODE_OPERATIONAL
            self.node.health = dronecan.uavcan.protocol.NodeStatus().HEALTH_OK

            log.info(f"DroneCAN node {MY_NODE_ID} started.")
        except Exception as e:
            log.error(f"Connection error: {e}")
            sys.exit(1)

    def decode_and_broadcast(self):
        """Reassemble 8 raw Tattu frames, validate, and broadcast via DroneCAN."""
        full_data = bytearray()

        # --- Frame length validation ---
        for i, frame in enumerate(self.frames):
            min_len = 7 if i == 0 else 7
            if len(frame) < min_len:
                log.warning(f"Frame {i} too short ({len(frame)} bytes), discarding sequence")
                return

        # --- Reassembly ---
        full_data.extend(self.frames[0][2:7])        # Frame 0: skip 2-byte CRC, take 5 bytes
        for i in range(1, 8):
            full_data.extend(self.frames[i][0:7])    # Frames 1-7: take first 7 bytes each

        if len(full_data) < 12:
            log.warning(f"Reassembled data too short ({len(full_data)} bytes), discarding")
            return

        # --- Parse ---
        def read_u16(idx): return struct.unpack_from('<H', full_data, idx)[0]
        def read_i16(idx): return struct.unpack_from('<h', full_data, idx)[0]

        idx = 0
        vendor = read_u16(idx); idx += 2
        model  = read_u16(idx); idx += 2
        volts  = read_u16(idx); idx += 2
        amps   = read_i16(idx); idx += 2
        temp   = read_i16(idx); idx += 2
        soc    = read_u16(idx); idx += 2

        voltage_v   = volts / 1000.0
        current_a   = amps / 100.0
        temp_kelvin = temp + 273.15

        # --- Sanity validation ---
        # Reject obviously bad decodes before they confuse the FC
        if not (VOLTAGE_MIN_V <= voltage_v <= VOLTAGE_MAX_V):
            log.warning(f"Voltage out of range: {voltage_v:.2f}V — bad decode, discarding")
            return

        if abs(current_a) > CURRENT_MAX_A:
            log.warning(f"Current out of range: {current_a:.1f}A — bad decode, discarding")
            return

        if not (0 <= soc <= 100):
            log.warning(f"SOC out of range: {soc}% — bad decode, discarding")
            return

        # BUG FIX: Reject sudden 0% drop if last known SOC was above threshold
        # This is the main cause of the spurious 0% readings.
        if soc == 0 and self.last_soc is not None and self.last_soc > SOC_JUMP_THRESHOLD:
            log.warning(
                f"SOC jumped from {self.last_soc}% to 0% — likely frame misalignment, "
                f"holding last value"
            )
            # Rebroadcast last known good instead
            soc        = self.last_soc
            voltage_v  = self.last_voltage
            current_a  = self.last_current
            temp_kelvin = self.last_temp

        # --- Store last known good ---
        self.last_voltage = voltage_v
        self.last_current = current_a
        self.last_temp    = temp_kelvin
        self.last_soc     = soc
        self.last_good_ts = time.time()

        # --- Build and broadcast DroneCAN BatteryInfo ---
        msg = dronecan.uavcan.equipment.power.BatteryInfo()
        msg.battery_id            = 0
        msg.voltage               = voltage_v
        msg.current               = current_a
        msg.temperature           = temp_kelvin
        msg.state_of_charge_pct   = soc
        msg.status_flags          = (
            dronecan.uavcan.equipment.power.BatteryInfo().STATUS_FLAG_IN_USE
        )
        msg.model_instance_id     = model

        self.node.broadcast(msg)
        log.debug(f"Broadcast: {voltage_v:.2f}V  {current_a:.1f}A  {soc}%  {temp_kelvin-273.15:.1f}°C")

        # Keep node alive
        self.node.health = dronecan.uavcan.protocol.NodeStatus().HEALTH_OK
        self.node.mode   = dronecan.uavcan.protocol.NodeStatus().MODE_OPERATIONAL

    def _process_tattu_frame(self, msg):
        """Handle one raw Tattu CAN frame."""
        now = time.time()

        # BUG FIX: Reset on timeout *before* start-frame check
        if self.collecting and (now - self.last_frame_time > 0.2):
            log.debug("Sequence timeout, resetting")
            self.collecting = False
            self.frames = []

        # Start-frame detection: last byte == 0x80
        # BUG FIX: Only treat as start if we're NOT mid-sequence,
        # or if we've already collected a full 8 (shouldn't happen, but guard anyway).
        # This prevents a mid-sequence frame that happens to end in 0x80 from
        # resetting an in-progress good sequence.
        if len(msg.data) > 0 and msg.data[-1] == 0x80:
            if self.collecting and 0 < len(self.frames) < 8:
                log.warning(
                    f"0x80 tail detected mid-sequence at frame {len(self.frames)}, "
                    f"restarting collection"
                )
            self.collecting = True
            self.frames = []

        if self.collecting:
            self.frames.append(bytes(msg.data))
            self.last_frame_time = now

            if len(self.frames) == 8:
                self.decode_and_broadcast()
                self.collecting = False

    def run(self):
        self.connect()
        log.info("Bridge running...")

        while True:
            try:
                # BUG FIX: Drain ALL pending Tattu frames before handing
                # control to DroneCAN spin. The original code processed only
                # one frame per loop iteration, causing frame drops when the
                # Tattu burst arrives faster than the loop runs.
                while True:
                    raw = self.bus.recv(timeout=0)  # non-blocking
                    if raw is None:
                        break
                    if raw.arbitration_id == TATTU_CAN_ID:
                        self._process_tattu_frame(raw)

                # DroneCAN housekeeping (heartbeats, service requests)
                self.node.spin(0.005)

            except KeyboardInterrupt:
                log.info("Stopping.")
                break
            except Exception as e:
                log.warning(f"Loop error: {e}")
                time.sleep(0.1)


if __name__ == "__main__":
    bridge = TattuBridge()
    bridge.run()
