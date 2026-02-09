"""BOM 2300 - Equipment Mount subassembly.

3D-printed mounts for PCBs, sensors, and GNSS antenna.

Most STEP files are exported from Fusion 360 with correct X/Y positions
baked in. Three parts have baked-in Z offsets that differ from the
reference assembly and need explicit correction.

    Side view (not to scale):

                  [GNSS]          Z ~ 28..79  (on upper plate)
         [PCB mount]              Z ~ 15..27  (on upper plate, tabs through)
        ==========================
        |  Upper plate            |
        ==========================
              |        |
              |        |
        ==========================
        |  Middle plate           |
        ==========================
              |        |
           [BC mount]  |          Z ~ -20..19 (battery PCB mount)
           [BC cover]  |          Z ~ -22..22 (battery PCB cover)
              |        |
        ==========================
        |  Lower plate            |        Z = -125
        ===+==================+===
           |                  |
         [Sensor]                 Z ~ -132..-70 (altitude sensor)

STEP files in steps/:
    2311_main_pcb_mount.step        Main PCB mount (Z offset needed)
    2312_bc_pcb_mount.step          Battery PCB mount
    2313_bc_pcb_cover.step          Battery PCB cover
    2321_altitude_sensor_mount.step Radar/LiDAR altimeter mount
    2331_gnss_mount_base.step       GNSS antenna mount base (Z offset needed)
    2332_gnss_mount_clamp.step      GNSS antenna mount clamp (Z offset needed)
    2341_ppp_beacon_mount.step      PPP/beacon mount
"""

from pathlib import Path

from build123d import Compound, Location

from quiver.common import PETG, load_step

_DIR = Path(__file__).parent

# Z corrections for parts whose Fusion export offset differs from
# the reference assembly. Derived by comparing raw STEP CoM against
# the 2000-SupportStructure.step reference.
_MAIN_PCB_MOUNT_DZ = 13.15       # raw Z=9.96, ref Z=23.11
_GNSS_BASE_DZ = -11.95           # raw Z=66.67, ref Z=54.72
_GNSS_CLAMP_DZ = -3.85           # raw Z=81.85, ref Z=78.00


def make_assembly() -> Compound | None:
    """Build the equipment mount subassembly from imported STEP files."""
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

    gnss_base = load_step(_DIR, "2331_gnss_mount_base")
    if gnss_base:
        gnss_base.color = PETG
        gnss_base.move(Location((0, 0, _GNSS_BASE_DZ)))
        children.append(gnss_base)

    gnss_clamp = load_step(_DIR, "2332_gnss_mount_clamp")
    if gnss_clamp:
        gnss_clamp.color = PETG
        gnss_clamp.move(Location((0, 0, _GNSS_CLAMP_DZ)))
        children.append(gnss_clamp)

    # --- PPP / beacon mount (2340) ---

    ppp_beacon = load_step(_DIR, "2341_ppp_beacon_mount")
    if ppp_beacon:
        ppp_beacon.color = PETG
        children.append(ppp_beacon)

    if not children:
        return None
    return Compound(children=children, label="Equipment Mount")
