"""BOM 1200 - Beams subassembly.

Cockpit support beams and battery compartment walls.

Expected STEP files in steps/:
    1211_cw_long.step               40x40x2mm aluminum tube (CW long)
    1212_ccw_back.step              40x40x2mm aluminum tube (CCW back)
    1213_ccw_front.step             40x40x2mm aluminum tube (CCW front)
    1221_battery_wall_right.step    30x2mm aluminum rectangular tube
    1222_battery_wall_left.step     30x2mm aluminum rectangular tube
"""

from pathlib import Path

from build123d import Compound

from quiver.common import load_all_steps, load_vendor_steps

_DIR = Path(__file__).parent


def make_assembly() -> Compound | None:
    """Build the beams subassembly from imported STEP files."""
    parts = list(load_all_steps(_DIR).values())
    parts += list(load_vendor_steps(_DIR).values())
    if not parts:
        return None
    return Compound(children=parts)
