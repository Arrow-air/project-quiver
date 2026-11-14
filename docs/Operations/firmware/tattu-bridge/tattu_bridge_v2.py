"""Tattu raw CAN to DroneCAN bridge, version 2 (2026-11-14), for the 14S Tattu 4.0 pack.

Based on tattu_bridge.py, which stays in this folder unchanged. Why a second version:
with tattu_bridge.py the flight controller shows voltage, SoC and temperature, but its
consumed mAh count runs backwards, so BATT2_LOW_MAH, BATT2_CRT_MAH and BATT2_ARM_MAH
never act. See Initial-Configuration-Guide.md section 7.2.

Changes against tattu_bridge.py:

1. Current is negated. The pack reports discharge as negative, ArduPilot expects positive.
2. BatteryInfo carries remaining_capacity_wh and full_charge_capacity_wh, and a
   BatteryInfoAux message follows it. With both, ArduPilot takes consumed mAh from the
   BMS count (persists across boots) and stops integrating current itself. This is the
   same path the 30 Ah pack with the native DroneCAN BMS uses.
3. The full payload is parsed: 14 cell voltages, cycle count, health, capacities, error word.
4. A decode is rejected unless the cell voltages sum to the pack voltage. The transfer CRC
   cannot be checked because the data type signature of the Tattu message is not published.
5. The listener socket filters on the Tattu CAN ID.

Offline check: test/replay_bridge.py replays a real capture through this file.
"""
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
TATTU_CAN_ID    = 0x01109216   # priority 1, data type 4242, source node 22
MY_NODE_ID      = 110
BATTERY_ID      = 0

CELL_COUNT      = 14
FRAMES_PER_TRANSFER = 8            # 7 frames of 8 bytes + 1 frame of 6 bytes
PAYLOAD_LEN     = 52           # after the 2 byte transfer CRC

# Used only to express capacity in Wh. ArduPilot divides by the same value again,
# so consumed mAh does not depend on it. consumed_wh on the FC does.
NOMINAL_VOLTAGE_V = CELL_COUNT * 3.7

# Pack current is int16 in 10 mA steps, negative on discharge (measured 2026-11-12 at idle:
# 90 mAh in 12.8 min against a raw reading of -40 to -50). Not yet checked at flight current.
CURRENT_A_PER_LSB = -0.01

# Sanity bounds for a 14S pack
VOLTAGE_MIN_V    = 38.0
VOLTAGE_MAX_V    = 62.0
CURRENT_MAX_A    = 400.0
CELL_SUM_TOL_V   = 1.0         # cells must sum to pack voltage within this
SEQUENCE_TIMEOUT = 0.2         # s, a transfer takes about 10 ms on the wire
ERROR_LOG_PERIOD = 10.0        # s


class TattuBridge:
    def __init__(self):
        self.collecting = False
        self.frames = []
        self.last_frame_time = 0
        self.bus = None
        self.node = None
        self.last_error_log = 0
        self.rejects = 0

    def connect(self):
        try:
            self.bus = can.interface.Bus(
                channel=CAN_INTERFACE, interface='socketcan',
                can_filters=[{"can_id": TATTU_CAN_ID, "can_mask": 0x1FFFFFFF, "extended": True}])
            log.info(f"Listener connected on {CAN_INTERFACE}.")

            driver = SocketCAN(CAN_INTERFACE)
            self.node = dronecan.node.Node(driver, node_id=MY_NODE_ID)

            node_info = dronecan.uavcan.protocol.GetNodeInfo.Response()
            node_info.name = 'org.tattu.bridge'
            node_info.software_version.major = 2
            self.node.node_info = node_info
            self.node.mode   = dronecan.uavcan.protocol.NodeStatus().MODE_OPERATIONAL
            self.node.health = dronecan.uavcan.protocol.NodeStatus().HEALTH_OK

            log.info(f"DroneCAN node {MY_NODE_ID} started.")
        except Exception as e:
            log.error(f"Connection error: {e}")
            sys.exit(1)

    def _reject(self, why):
        self.rejects += 1
        log.warning(f"{why}, discarding (rejects so far: {self.rejects})")

    def decode(self):
        """Reassemble one Tattu transfer. Returns a dict, or None if the decode is not trusted."""
        if len(self.frames[0]) < 3:
            return self._reject(f"Frame 0 too short ({len(self.frames[0])} bytes)")

        data = bytearray(self.frames[0][2:-1])       # skip the 2 byte CRC, drop the tail byte
        for f in self.frames[1:]:
            data.extend(f[:-1])                      # drop the tail byte

        if len(data) != PAYLOAD_LEN:
            return self._reject(f"Payload is {len(data)} bytes, expected {PAYLOAD_LEN}")

        (vendor, model, mv, cur, temp_c, soc, cycles, health) = struct.unpack_from('<2sHHhhHHh', data, 0)
        cells_mv = struct.unpack_from(f'<{CELL_COUNT}H', data, 16)
        design_mah, remaining_mah, error_word = struct.unpack_from('<HHI', data, 16 + 2 * CELL_COUNT)

        voltage_v = mv / 1000.0
        current_a = cur * CURRENT_A_PER_LSB
        cells_v   = [c / 1000.0 for c in cells_mv]

        if not (VOLTAGE_MIN_V <= voltage_v <= VOLTAGE_MAX_V):
            return self._reject(f"Voltage out of range: {voltage_v:.2f} V")
        if abs(sum(cells_v) - voltage_v) > CELL_SUM_TOL_V:
            return self._reject(f"Cells sum to {sum(cells_v):.2f} V, pack reads {voltage_v:.2f} V")
        if abs(current_a) > CURRENT_MAX_A:
            return self._reject(f"Current out of range: {current_a:.1f} A")
        if not (0 <= soc <= 100):
            return self._reject(f"SoC out of range: {soc} %")
        if design_mah == 0 or remaining_mah > design_mah * 1.1:
            return self._reject(f"Capacity fields implausible: {remaining_mah} of {design_mah} mAh")

        return dict(vendor=vendor, model=model, voltage_v=voltage_v, current_a=current_a,
                    temp_c=temp_c, soc=soc, cycles=cycles, health=health, cells_v=cells_v,
                    design_mah=design_mah, remaining_mah=remaining_mah, error_word=error_word)

    def broadcast(self, d):
        """Publish BatteryInfo, then BatteryInfoAux. Order matters: the FC reads the Wh
        fields stored from BatteryInfo when it handles the aux message."""
        info = dronecan.uavcan.equipment.power.BatteryInfo()
        info.battery_id              = BATTERY_ID
        info.voltage                 = d['voltage_v']
        info.current                 = d['current_a']
        info.temperature             = d['temp_c'] + 273.15
        info.state_of_charge_pct     = d['soc']
        info.state_of_health_pct     = max(0, min(100, d['health']))
        info.remaining_capacity_wh   = d['remaining_mah'] / 1000.0 * NOMINAL_VOLTAGE_V
        info.full_charge_capacity_wh = d['design_mah'] / 1000.0 * NOMINAL_VOLTAGE_V
        info.status_flags            = info.STATUS_FLAG_IN_USE
        info.model_instance_id       = d['model']
        self.node.broadcast(info)

        aux = dronecan.ardupilot.equipment.power.BatteryInfoAux()
        aux.battery_id      = BATTERY_ID
        aux.voltage_cell    = d['cells_v']
        aux.cycle_count     = d['cycles']
        aux.nominal_voltage = NOMINAL_VOLTAGE_V
        aux.is_powering_off = False
        self.node.broadcast(aux)

        # The bit meanings of the Tattu error word are not documented, so it is logged only.
        if d['error_word'] and time.time() - self.last_error_log > ERROR_LOG_PERIOD:
            self.last_error_log = time.time()
            log.warning(f"Pack error word is 0x{d['error_word']:08X}")

        log.debug(f"Broadcast: {d['voltage_v']:.2f} V  {d['current_a']:.2f} A  {d['soc']} %  "
                  f"{d['remaining_mah']}/{d['design_mah']} mAh  {d['temp_c']} C")

    def _process_tattu_frame(self, msg):
        """Handle one raw Tattu CAN frame."""
        now = time.time()

        if self.collecting and (now - self.last_frame_time > SEQUENCE_TIMEOUT):
            log.debug("Sequence timeout, resetting")
            self.collecting = False
            self.frames = []

        # Start of transfer: tail byte 0x80. The pack never uses 0x80 as a tail on other frames
        # (observed tails: 80, 21, 02, 23, 04, 25, 06, 67).
        if len(msg.data) > 0 and msg.data[-1] == 0x80:
            if self.collecting and 0 < len(self.frames) < FRAMES_PER_TRANSFER:
                log.warning(f"Start frame arrived at frame {len(self.frames)}, restarting collection")
            self.collecting = True
            self.frames = []

        if self.collecting:
            self.frames.append(bytes(msg.data))
            self.last_frame_time = now

            if len(self.frames) == FRAMES_PER_TRANSFER:
                d = self.decode()
                if d is not None:
                    self.broadcast(d)
                self.collecting = False
                self.frames = []

    def run(self):
        self.connect()
        log.info("Bridge running...")

        while True:
            try:
                # Drain all pending Tattu frames before the DroneCAN spin
                while True:
                    raw = self.bus.recv(timeout=0)
                    if raw is None:
                        break
                    if raw.arbitration_id == TATTU_CAN_ID:
                        self._process_tattu_frame(raw)

                # DroneCAN housekeeping (NodeStatus, GetNodeInfo)
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
