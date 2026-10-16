"""BOM 3200 - Peripheral subassembly.

Sensors, telemetry, GNSS receiver, and other peripheral equipment
mounted around the drone airframe.

Most parts are exported from Fusion 360 with correct positions baked in.
Parts that need transforms are noted below.

Vendor parts in steps/vendor/:
    3201_ppp_adapter.step       PPP ethernet adapter (rotZ -45, on the 2341 board)
    3202_drone_beacon.step      Drone beacon db201 (rotZ 135, on the 2341 board)
    3210_oa_lidar.step          Obstacle avoidance LiDAR (translate only)
    3220_radar_altimeter.step   Radar altimeter (rotZ 180)
    3230_front_telemetry.step   Front telemetry antenna (no transform)
    3240_rear_telemetry.step    Rear telemetry antenna (no transform)
    3250_gnss_wren_mini.step    GNSS receiver (Z offset only, extract_solids)
    3260_power_switch.step      Power switch (translate only)
    3270_camera.step            Camera (no transform)
    3280_telemetry.step         Telemetry air unit (rotZ 180)
    3290_oa_radar.step          Obstacle avoidance radar (rotY 180, rotX -5)

Poses are full rigid transforms (see quiver.common.place): the Fusion 360
v148 occurrence transforms (Quiver_PT3_Drone_Assembly). Several vendor
STEPs are in their Fusion component's own frame.
"""

from pathlib import Path

from build123d import Compound

from quiver.common import load_step, place

_DIR = Path(__file__).parent

# Poses for parts needing transforms: STEP origin (mm), intrinsic XYZ (deg).
# Checked against Fusion v148 by tests/test_placement.py.
_OA_LIDAR_POSE = ((-100.0, 0, -17.3), (0, 0, 0))            # seated in the 2412 top cap
_RADAR_ALT_POSE = ((5.0, 294.0, 0), (0, 0, 180))
_GNSS_DZ = 2.30                                            # not in Fusion v148; raw Z=85.03, ref Z=87.33
_OA_RADAR_POSE = ((0, -73.9027, -68.2230), (175, 0, 180))   # turned 180 about Y, tilt cancelled
_PPP_ADAPTER_POSE = ((-151.7959, -60.4492, 14.6037), (0, 0, -45))   # on the 2341 mounting board
_DRONE_BEACON_POSE = ((42.3389, 142.5650, 20.5), (0, 0, 135))       # on the 2341 mounting board
_POWER_SWITCH_POSE = ((-146.515, 0, -2.0), (0, 0, 0))     # moved with the 2411 enclosure update
_TELEMETRY_POSE = ((199.5695, 4.3628, 0), (0, 0, 180))


def make_assembly() -> Compound | None:
    """Build the peripheral subassembly from imported STEP files."""
    children = []

    # --- Parts already at correct position (no transform) ---

    for name in [
        "3230_front_telemetry",
        "3240_rear_telemetry",
        "3270_camera",
    ]:
        part = load_step(_DIR, name, vendor=True)
        if part:
            children.append(part)

    # --- Parts needing Z offset only ---

    gnss = load_step(_DIR, "3250_gnss_wren_mini", vendor=True, extract_solids=True)
    if gnss:
        place(gnss, (0, 0, _GNSS_DZ))
        children.append(gnss)

    # --- Parts needing a pose ---

    lidar = load_step(_DIR, "3210_oa_lidar", vendor=True)
    if lidar:
        children.append(place(lidar, *_OA_LIDAR_POSE))

    # The switch STEP still carries its position from before the enclosure
    # update; Fusion moved it to the left (-X) side of the front face.
    power_switch = load_step(_DIR, "3260_power_switch", vendor=True)
    if power_switch:
        children.append(place(power_switch, *_POWER_SWITCH_POSE))

    telemetry = load_step(_DIR, "3280_telemetry", vendor=True)
    if telemetry:
        children.append(place(telemetry, *_TELEMETRY_POSE))

    # The STEP holds the radar tilted 5 deg in its Fusion component frame;
    # the occurrence turns it 180 deg and cancels the tilt (face vertical).
    oa_radar = load_step(_DIR, "3290_oa_radar", vendor=True)
    if oa_radar:
        children.append(place(oa_radar, *_OA_RADAR_POSE))

    radar_alt = load_step(_DIR, "3220_radar_altimeter", vendor=True)
    if radar_alt:
        children.append(place(radar_alt, *_RADAR_ALT_POSE))

    ppp = load_step(_DIR, "3201_ppp_adapter", vendor=True)
    if ppp:
        children.append(place(ppp, *_PPP_ADAPTER_POSE))

    beacon = load_step(_DIR, "3202_drone_beacon", vendor=True)
    if beacon:
        children.append(place(beacon, *_DRONE_BEACON_POSE))

    if not children:
        return None
    return Compound(children=children, label="Peripheral")
