"""BOM 2200 - Battery Slider subassembly.

Two battery sliders mounted on the inner faces of the battery walls,
one on each side. Each slider holds the battery in place and allows
quick insertion/removal along the Y axis.

    Top view (looking down):

            (+Y)
            |
        ===============     Battery compartment
        |  [L]   [R]  |    (between battery walls)
        ===============
            |
            (-Y)

    [L] = left slider (X = -115.5)
    [R] = right slider (X = +115.5)

The raw STEP file is oriented for the left side. The right slider is
the same part turned 180 deg about Y to face the opposite wall, as in
the Fusion v148 master (not a mirror-image variant).

STEP files in steps/:
    2211_battery_slider.step    Battery slider (used 2x)

Poses are full rigid transforms (see quiver.common.place) from the Fusion
360 v148 master.
"""

from pathlib import Path

from build123d import Compound

from quiver.common import PETG, load_step, place

_DIR = Path(__file__).parent

# Poses: STEP origin (mm), intrinsic XYZ rotation (deg)
_LEFT_POSE = ((-120.0, 12.0, -71.0), (0, 0, 0))
_RIGHT_POSE = ((120.0, 12.0, -71.0), (0, 180, 0))


def make_assembly() -> Compound | None:
    """Build the battery slider subassembly from imported STEP files."""
    children = []

    left = load_step(_DIR, "2211_battery_slider")
    if left:
        left.color = PETG
        children.append(place(left, *_LEFT_POSE))

    right = load_step(_DIR, "2211_battery_slider")
    if right:
        right.color = PETG
        children.append(place(right, *_RIGHT_POSE))

    if not children:
        return None
    return Compound(children=children, label="Battery Slider")
