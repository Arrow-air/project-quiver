"""BOM 3200 - Peripheral subassembly.

Sensors, telemetry, GNSS receiver, and other peripheral equipment
mounted around the drone airframe.

Most parts are exported from Fusion 360 with correct positions baked in.
Parts that need transforms are noted below.

Vendor parts in steps/vendor/:
    3201_ppp_adapter.step       PPP ethernet adapter (rotZ 45, on BL diagonal)
    3202_drone_beacon.step      Drone beacon db201 (rotZ 135, on BL diagonal)
    3210_oa_lidar.step          Obstacle avoidance LiDAR (translate only)
    3220_radar_altimeter.step   Radar altimeter (rotZ 180)
    3230_front_telemetry.step   Front telemetry antenna (no transform)
    3240_rear_telemetry.step    Rear telemetry antenna (no transform)
    3250_gnss_wren_mini.step    GNSS receiver (Z offset only, extract_solids)
    3260_power_switch.step      Power switch (no transform)
    3270_camera.step            Camera (no transform)
    3280_telemetry.step         Telemetry air unit (no transform)
    3290_oa_radar.step          Obstacle avoidance radar (translate only)
"""

from pathlib import Path

from build123d import Axis, Compound, Location

from quiver.common import load_step

_DIR = Path(__file__).parent

# Target center-of-mass positions for parts needing transforms
# (from Fusion reference 3000-Equipment.step).
_OA_LIDAR_POS = (-100.00, 2.42, 95.10)
_RADAR_ALT_POS = (-47.99, 143.00, -139.86)
_GNSS_DZ = 2.30                                    # raw Z=85.03, ref Z=87.33
_OA_RADAR_POS = (-1.64, 165.07, -96.05)
_PPP_ADAPTER_POS = (-119.14, 118.84, 51.77)
_DRONE_BEACON_POS = (-98.92, 99.37, 48.50)


def make_assembly() -> Compound | None:
    """Build the peripheral subassembly from imported STEP files."""
    children = []

    # --- Parts already at correct position (no transform) ---

    for name in [
        "3230_front_telemetry",
        "3240_rear_telemetry",
        "3260_power_switch",
        "3270_camera",
        "3280_telemetry",
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
        com = lidar.center()
        lidar.move(Location((
            _OA_LIDAR_POS[0] - com.X,
            _OA_LIDAR_POS[1] - com.Y,
            _OA_LIDAR_POS[2] - com.Z,
        )))
        children.append(lidar)

    oa_radar = load_step(_DIR, "3290_oa_radar", vendor=True)
    if oa_radar:
        com = oa_radar.center()
        oa_radar.move(Location((
            _OA_RADAR_POS[0] - com.X,
            _OA_RADAR_POS[1] - com.Y,
            _OA_RADAR_POS[2] - com.Z,
        )))
        children.append(oa_radar)

    # --- Parts needing rotation + CoM translation ---

    radar_alt = load_step(_DIR, "3220_radar_altimeter", vendor=True)
    if radar_alt:
        radar_alt = radar_alt.rotate(Axis.Z, 180)
        com = radar_alt.center()
        radar_alt.move(Location((
            _RADAR_ALT_POS[0] - com.X,
            _RADAR_ALT_POS[1] - com.Y,
            _RADAR_ALT_POS[2] - com.Z,
        )))
        children.append(radar_alt)

    ppp = load_step(_DIR, "3201_ppp_adapter", vendor=True)
    if ppp:
        ppp = ppp.rotate(Axis.Z, 45)
        com = ppp.center()
        ppp.move(Location((
            _PPP_ADAPTER_POS[0] - com.X,
            _PPP_ADAPTER_POS[1] - com.Y,
            _PPP_ADAPTER_POS[2] - com.Z,
        )))
        children.append(ppp)

    beacon = load_step(_DIR, "3202_drone_beacon", vendor=True)
    if beacon:
        beacon = beacon.rotate(Axis.Z, 135)
        com = beacon.center()
        beacon.move(Location((
            _DRONE_BEACON_POS[0] - com.X,
            _DRONE_BEACON_POS[1] - com.Y,
            _DRONE_BEACON_POS[2] - com.Z,
        )))
        children.append(beacon)

    if not children:
        return None
    return Compound(children=children, label="Peripheral")
