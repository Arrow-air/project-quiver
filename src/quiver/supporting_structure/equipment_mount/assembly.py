"""BOM 2300 - Equipment Mount subassembly.

3D-printed mounts for PCBs, sensors, and GNSS antenna.

Most STEP files are exported from Fusion 360 with correct X/Y positions
baked in. The PCB adapter and F9P base need Z corrections; the Here4
mount is already in Fusion master world coordinates.

    Side view (not to scale):

                [GNSS]            Z ~ 28..79  (on upper plate)
        [PCB mount]               Z ~ 15..27  (on upper plate, tabs through)
        ==========================
        |  Upper plate            |
        ==========================
            |          |
            |          |
        ==========================
        |  Middle plate           |
        ==========================
            |          |
            [BC mount] |          Z ~ -20..19 (battery PCB mount)
            [BC cover] |          Z ~ -22..22 (battery PCB cover)
            |          |
        ==========================
        |  Lower plate            |        Z = -125
        ===+==================+===
            |                 |
        [Sensor]                  Z ~ -132..-70 (altitude sensor)

STEP files in steps/:
    2311_main_pcb_mount.step        Main PCB mount (Z offset needed)
    2312_bc_pcb_mount.step          Battery PCB mount
    2313_bc_pcb_cover.step          Battery PCB cover
    2321_altitude_sensor_mount.step Radar/LiDAR altimeter mount
    2331_gnss_mount_base.step       GNSS antenna mount base (Z offset needed)
    2333_gnss_mount_here4.step      Here4 mount (Fusion world placement)
    2341_ppp_beacon_mount.step      Original PPP/beacon mount
    2342_ppp_beacon_board.step      Additional PPP/beacon mounting board
"""

from pathlib import Path

from build123d import Compound, Location

from quiver.common import PETG, load_step
from quiver.gps import DEFAULT_PRIMARY_GPS, F9P_MOUNT_DZ, validate_primary_gps

_DIR = Path(__file__).parent

# Z corrections for parts whose Fusion export offset differs from
# the reference assembly. Derived by comparing raw STEP CoM against
# the 2000-SupportStructure.step reference.
_MAIN_PCB_MOUNT_DZ = -7.85       # Fusion v148 occurrence transform, cm -> mm


def make_assembly(primary_gps: str = DEFAULT_PRIMARY_GPS) -> Compound | None:
    """Build the equipment mount subassembly from imported STEP files."""
    validate_primary_gps(primary_gps)
    children = []

    # --- PCB mounts (2310) ---

    main_pcb = load_step(_DIR, "2311_main_pcb_mount")
    if main_pcb:
        main_pcb.color = PETG
        main_pcb.move(Location((0, 0, _MAIN_PCB_MOUNT_DZ)))
        children.append(main_pcb)

    bc_mount = load_step(_DIR, "2312_bc_pcb_mount")
    if bc_mount:
        bc_mount.color = PETG
        children.append(bc_mount)

    bc_cover = load_step(_DIR, "2313_bc_pcb_cover")
    if bc_cover:
        bc_cover.color = PETG
        children.append(bc_cover)

    # --- Sensor mount (2320) ---

    sensor = load_step(_DIR, "2321_altitude_sensor_mount")
    if sensor:
        sensor.color = PETG
        children.append(sensor)

    # --- GNSS mount (2330) ---

    if primary_gps == "here4":
        gnss_mount = load_step(_DIR, "2333_gnss_mount_here4")
    else:
        gnss_mount = load_step(_DIR, "2331_gnss_mount_base")
        if gnss_mount:
            gnss_mount.move(Location((0, 0, F9P_MOUNT_DZ)))
    if gnss_mount:
        gnss_mount.color = PETG
        children.append(gnss_mount)

    # --- PPP / beacon mount (2340) ---

    ppp_beacon = load_step(_DIR, "2341_ppp_beacon_mount")
    if ppp_beacon:
        ppp_beacon.color = PETG
        children.append(ppp_beacon)

    ppp_board = load_step(_DIR, "2342_ppp_beacon_board")
    if ppp_board:
        ppp_board.color = PETG
        children.append(ppp_board)

    if not children:
        return None
    return Compound(children=children, label="Equipment Mount")
