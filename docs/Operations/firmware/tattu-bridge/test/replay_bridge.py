"""Replay a candump-style capture of the Tattu pack through a bridge script, offline.

usage: python replay_bridge.py <capture.log> [module]
    module = tattu_bridge (default) or tattu_bridge_v2

No CAN hardware is needed. Needs the `dronecan` package (pip install dronecan).
python-can is stubbed if it is not installed. Broadcast messages are captured instead of sent.
For BatteryInfo + BatteryInfoAux pairs the script also prints the consumed mAh that ArduPilot
would derive (AP_BattMonitor_DroneCAN::handle_battery_info_aux), with float16 rounding applied.
"""
import math, os, struct, sys, types

try:
    import can  # noqa: F401
except ImportError:
    sys.modules["can"] = types.ModuleType("can")
import dronecan

try:
    import dronecan.driver.socketcan  # noqa: F401  (needs fcntl, so Linux only)
except ImportError:
    _sc = types.ModuleType("dronecan.driver.socketcan")
    _sc.SocketCAN = object
    sys.modules["dronecan.driver.socketcan"] = _sc

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.dont_write_bytecode = True
module_name = sys.argv[2] if len(sys.argv) > 2 else "tattu_bridge"
bridge_mod = __import__(module_name)


def f16(x):
    return struct.unpack("<e", struct.pack("<e", x))[0]


frames = []
for line in open(sys.argv[1]):
    if line.startswith("#") or "#" not in line:
        continue
    frames.append((float(line[1:line.index(")")]), bytes.fromhex(line.strip().split("#")[1])))

# drive the bridge clock from capture timestamps so its sequence timeout is exercised
now = [0.0]
bridge_mod.time = types.SimpleNamespace(time=lambda: now[0], sleep=lambda s: None)
sent = []
b = bridge_mod.TattuBridge()
b.node = types.SimpleNamespace(broadcast=lambda m: sent.append((now[0], m)), health=0, mode=0)
for t, d in frames:
    now[0] = t
    b._process_tattu_frame(types.SimpleNamespace(data=d))

starts = sum(1 for _, d in frames if d[-1] == 0x80)
info = [(t, m) for t, m in sent if dronecan.get_dronecan_data_type(m).full_name.endswith("BatteryInfo")]
aux = [(t, m) for t, m in sent if dronecan.get_dronecan_data_type(m).full_name.endswith("BatteryInfoAux")]
print(f"module {module_name}: frames {len(frames)}, start frames {starts}, BatteryInfo {len(info)}, BatteryInfoAux {len(aux)}")
gaps = [b2[0] - a[0] for a, b2 in zip(info, info[1:])]
print(f"BatteryInfo interval s: min {min(gaps):.2f} max {max(gaps):.2f} mean {sum(gaps) / len(gaps):.2f}")


def spread(name, vals):
    vals = sorted(set(round(v, 3) for v in vals))
    print(f"  {name:26s} {vals[:6]}{' ...' if len(vals) > 6 else ''}")


spread("voltage V", [m.voltage for _, m in info])
spread("current A", [m.current for _, m in info])
spread("temperature C", [m.temperature - 273.15 for _, m in info])
spread("state_of_charge_pct", [m.state_of_charge_pct for _, m in info])
spread("state_of_health_pct", [m.state_of_health_pct for _, m in info])
spread("remaining_capacity_wh", [m.remaining_capacity_wh for _, m in info])
spread("full_charge_capacity_wh", [m.full_charge_capacity_wh for _, m in info])

if aux:
    _, a = aux[-1]
    _, i = info[-1]
    cells = [f16(v) for v in a.voltage_cell]
    print(f"  cells V (float16)          {[round(c, 3) for c in cells]}")
    print(f"  cell count {len(cells)}, cycle_count {a.cycle_count}, nominal_voltage {a.nominal_voltage:.2f}")
    nom = f16(a.nominal_voltage)
    full_ah = f16(i.full_charge_capacity_wh) / nom
    rem_ah = f16(i.remaining_capacity_wh) / nom
    print(f"  FC consumed_mah            {(full_ah - rem_ah) * 1000:.0f}  (FC remaining {rem_ah * 1000:.0f} mAh of {full_ah * 1000:.0f})")
    step_wh = 2 ** (math.floor(math.log2(i.remaining_capacity_wh)) - 10)
    print(f"  note: float16 Wh fields give consumed mAh steps of roughly {step_wh / nom * 1000:.0f} mAh")
else:
    print("  no BatteryInfoAux: the FC integrates the bridged current itself (consumed starts at 0 each boot)")
print(f"  rejects {getattr(b, 'rejects', 'n/a')}")
