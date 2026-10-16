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
Each CCW beam covers one half of its diagonal. The CCW front beam is the
mirror image of the CCW back beam, not a second copy of it.

The battery walls are vertical rectangular tubes on the left (-X) and
right (+X) sides, running the full 300mm depth between the middle and
lower plates. The left wall is the mirror image of the right wall.

Expected STEP files in steps/:
    1211_cw_long.step               40x40x1mm aluminum tube (CW long)
    1212_ccw_back.step              40x40x1mm aluminum tube (CCW back)
    1213_ccw_front.step             40x40x1mm aluminum tube (CCW front, mirror of 1212)
    1221_battery_wall_left.step     100x30x2mm aluminum tube, 300mm (left, mirror of 1222)
    1222_battery_wall_right.step    100x30x2mm aluminum tube, 300mm (right)

Poses are full rigid transforms (see quiver.common.place) from the Fusion
360 v148 master. Each STEP is in its Fusion component frame: 1212 and 1213
share one frame (the front beam's geometry sits on the far side of it), so
they also share a pose.
"""

from pathlib import Path

from build123d import Compound

from quiver.common import ALUMINUM, load_step, place

_DIR = Path(__file__).parent

# (STEP file, position mm, intrinsic XYZ rotation deg)
_PARTS = [
    ("1211_cw_long", (-102.4526, -102.4526, 0), (0, 0, -45)),
    ("1212_ccw_back", (-14.2128, 14.2128, 0), (0, 0, 45)),
    ("1213_ccw_front", (-14.2128, 14.2128, 0), (0, 0, 45)),
    ("1221_battery_wall_left", (-135, 150, -71), (0, 0, 180)),
    ("1222_battery_wall_right", (135, 150, -71), (180, 0, 0)),
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
