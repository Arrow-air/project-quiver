"""Enclosure subassembly - Electronics mounts and weatherproof enclosure (Parts 16-30).

3D-printed components for mounting electronics, sensors, and the main
weatherproof cockpit enclosure.

Expected STEP files in steps/:
    battery_slider.step          Part 16 - Battery slider x2
    bc_pcb_cover.step            Part 17 - Battery PCB cover
    altitude_sensor_mount.step   Part 18 - Radar/LiDAR altimeter mount
    enclosure_anchor.step        Part 19 - Enclosure anchor x4
    camera_mount.step            Part 20 - Camera mount
    attach_spacer_left.step      Part 21 - Attachment interface spacer (left)
    attach_spacer_right.step     Part 22 - Attachment interface spacer (right)
    attach_spacer_bottom.step    Part 23 - Attachment interface spacer (bottom)
    gnss_mount_base.step         Part 24 - GNSS antenna mount base
    gnss_mount_clamp.step        Part 25 - GNSS antenna mount clamp
    main_pcb_mount.step          Part 26 - Main PCB mount
    main_enclosure.step          Part 27 - Main cockpit enclosure
    enclosure_top_cap.step       Part 28 - Enclosure top cap
    enclosure_cap_clip.step      Part 29 - Enclosure cap clip x4
    bc_pcb_mount.step            Part 30 - Battery PCB mount
"""

from pathlib import Path

from build123d import Compound

from quiver.common import load_all_steps, load_vendor_steps

_DIR = Path(__file__).parent


def make_assembly() -> Compound | None:
    """Build the enclosure subassembly from imported STEP files."""
    parts = list(load_all_steps(_DIR).values())
    parts += list(load_vendor_steps(_DIR).values())
    if not parts:
        return None
    return Compound(children=parts)
