"""BOM 1200 - Beams subassembly.

Cockpit support beams and battery compartment walls.

The cockpit beams form an X shape sandwiched between the upper and middle
plates. Looking down from above (top view):

            (+Y)
            |
    CCW     |       /
    back  \\ |      / CW long
            \\|   /
            \\| /
    (-X) ----+---- (+X)
            /|\\
            / |  \\
    CW   /  |     \\ CCW
    long    |   front
            |
            (-Y)

The CW long beam spans the full diagonal. The two CCW beams span the
other diagonal, with a gap at the center where they meet the CW beam.
Each CCW beam covers one half of its diagonal. Both are the same part
(1212): the front one is the back one turned 180 deg about Z. (Fusion v148
has the front one as a separate component, 1213, but the two are identical.)

The battery walls are vertical rectangular tubes on the left (-X) and
right (+X) sides, running the full 300mm depth between the middle and
lower plates. Both are the same part: the left one is the right one turned
180 deg about Y. Fusion v148 draws the left wall as a mirror image, but the
wall is symmetric where it mates, so every hole lands in the same place.

Expected STEP files in steps/:
    1211_cw_long.step               40x40x1mm aluminum tube (CW long)
    1212_ccw_back.step              40x40x1mm aluminum tube (CCW, used 2x)
    1221_battery_wall.step          100x30x2mm aluminum tube, 300mm (used 2x)

Poses are full rigid transforms (see quiver.common.place) from the Fusion
360 v148 master.
"""

from pathlib import Path

from build123d import Compound

from quiver.common import ALUMINUM, load_step, place

_DIR = Path(__file__).parent

# (STEP file, position mm, intrinsic XYZ rotation deg)
_PARTS = [
    ("1211_cw_long", (-102.4526, -102.4526, 0), (0, 0, -45)),
    ("1212_ccw_back", (-14.2128, 14.2128, 0), (0, 0, 45)),  # back
    ("1212_ccw_back", (14.2128, -14.2128, 0), (0, 0, -135)),  # front
    ("1221_battery_wall", (-135, -150, -71), (0, 180, 0)),  # left
    ("1221_battery_wall", (135, 150, -71), (180, 0, 0)),  # right
]


def make_assembly() -> Compound | None:
    """Build the beams subassembly from imported STEP files."""
    children = []
    for name, pos, rot in _PARTS:
        part = load_step(_DIR, name)
        if part:
            part.color = ALUMINUM
            children.append(place(part, pos, rot))

    if not children:
        return None
    return Compound(children=children, label="Beams")
