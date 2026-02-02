"""BOM 2300 - Equipment Mount subassembly.

3D-printed mounts for PCBs, sensors, camera, and GNSS antenna.

Expected STEP files in steps/:
    2311_main_pcb_mount.step        Main PCB mount
    2312_bc_pcb_mount.step          Battery PCB mount
    2313_bc_pcb_cover.step          Battery PCB cover
    2321_altitude_sensor_mount.step Radar/LiDAR altimeter mount
    2322_camera_mount.step          Camera mount
    2331_gnss_mount_base.step       GNSS antenna mount base
    2332_gnss_mount_clamp.step      GNSS antenna mount clamp
"""

from pathlib import Path

from build123d import Compound

from quiver.common import load_all_steps, load_vendor_steps

_DIR = Path(__file__).parent


def make_assembly() -> Compound | None:
    """Build the equipment mount subassembly from imported STEP files."""
    parts = list(load_all_steps(_DIR).values())
    parts += list(load_vendor_steps(_DIR).values())
    if not parts:
        return None
    return Compound(children=parts)
