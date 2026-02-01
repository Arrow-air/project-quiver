"""Frame subassembly - Core airframe structure (Parts 1-8).

The frame is a three-layer aluminum plate sandwich with cockpit support
beams and battery compartment walls.

Expected STEP files in steps/:
    upper_plate.step             Part 1  - 2mm aluminum upper plate
    middle_plate.step            Part 2  - 2mm aluminum middle plate
    lower_plate.step             Part 3  - 4mm aluminum lower plate
    cockpit_beam_cw.step         Part 4  - 40x40x2mm aluminum tube (CW long)
    cockpit_beam_ccw_back.step   Part 5  - 40x40x2mm aluminum tube (CCW back)
    cockpit_beam_ccw_front.step  Part 6  - 40x40x2mm aluminum tube (CCW front)
    battery_wall_left.step       Part 7  - 30x2mm aluminum rectangular tube
    battery_wall_right.step      Part 8  - 30x2mm aluminum rectangular tube

Vendor parts in steps/vendor/:
    (none expected - all frame parts are custom)
"""

from pathlib import Path

from build123d import Compound

from quiver.common import load_all_steps, load_vendor_steps

_DIR = Path(__file__).parent


def make_assembly() -> Compound | None:
    """Build the frame subassembly from imported STEP files."""
    parts = list(load_all_steps(_DIR).values())
    parts += list(load_vendor_steps(_DIR).values())
    if not parts:
        return None
    return Compound(children=parts)
