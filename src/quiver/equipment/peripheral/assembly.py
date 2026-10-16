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

Position constants are center-of-mass coordinates measured from the
Fusion 360 PT3 master model (Quiver_PT3_Drone_Assembly v148). The
rotations reproduce each Fusion occurrence transform; several vendor
STEPs are in their Fusion component's own frame.
"""

from pathlib import Path

from build123d import Axis, Compound, Location

from quiver.common import load_step, place_at

_DIR = Path(__file__).parent

# Target center-of-mass positions for parts needing transforms
# (Fusion v148 world placement; checked by tests/test_fusion_sync.py).
_OA_LIDAR_POS = (-100.00, 2.42, 99.10)             # seated in the 2412 top cap
_RADAR_ALT_POS = (-42.99, 143.00, -139.86)
_GNSS_DZ = 2.30                                    # raw Z=85.03, ref Z=87.33
_OA_RADAR_POS = (1.64, 165.07, -96.05)
_PPP_ADAPTER_POS = (-111.95, 82.97, 44.37)         # on the 2341 mounting board
_DRONE_BEACON_POS = (-94.19, 115.50, 47.00)        # on the 2341 mounting board
_POWER_SWITCH_POS = (-73.26, -145.32, 32.50)       # moved with the 2411 enclosure update
_TELEMETRY_POS = (99.47, 2.14, -7.22)


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
        gnss.move(Location((0, 0, _GNSS_DZ)))
        children.append(gnss)

    # --- Parts needing CoM translation ---

    lidar = load_step(_DIR, "3210_oa_lidar", vendor=True)
    if lidar:
        place_at(lidar, *_OA_LIDAR_POS)
        children.append(lidar)

    # The switch STEP still carries its position from before the enclosure
    # update; Fusion moved it to the left (-X) side of the front face.
    power_switch = load_step(_DIR, "3260_power_switch", vendor=True)
    if power_switch:
        place_at(power_switch, *_POWER_SWITCH_POS)
        children.append(power_switch)

    # --- Parts needing rotation + CoM translation ---

    telemetry = load_step(_DIR, "3280_telemetry", vendor=True)
    if telemetry:
        telemetry = telemetry.rotate(Axis.Z, 180)
        place_at(telemetry, *_TELEMETRY_POS)
        children.append(telemetry)

    # The STEP holds the radar tilted 5 deg in its Fusion component frame;
    # the occurrence turns it 180 deg and cancels the tilt (face vertical).
    oa_radar = load_step(_DIR, "3290_oa_radar", vendor=True)
    if oa_radar:
        oa_radar = oa_radar.rotate(Axis.Y, 180).rotate(Axis.X, -5)
        place_at(oa_radar, *_OA_RADAR_POS)
        children.append(oa_radar)

    radar_alt = load_step(_DIR, "3220_radar_altimeter", vendor=True)
    if radar_alt:
        radar_alt = radar_alt.rotate(Axis.Z, 180)
        place_at(radar_alt, *_RADAR_ALT_POS)
        children.append(radar_alt)

    ppp = load_step(_DIR, "3201_ppp_adapter", vendor=True)
    if ppp:
        ppp = ppp.rotate(Axis.Z, -45)
        place_at(ppp, *_PPP_ADAPTER_POS)
        children.append(ppp)

    beacon = load_step(_DIR, "3202_drone_beacon", vendor=True)
    if beacon:
        beacon = beacon.rotate(Axis.Z, 135)
        place_at(beacon, *_DRONE_BEACON_POS)
        children.append(beacon)

    if not children:
        return None
    return Compound(children=children, label="Peripheral")
