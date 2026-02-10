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
mirrored via rotY(180) to face the opposite wall.

STEP files in steps/:
    2211_battery_slider.step    Battery slider (used 2x)
"""

from pathlib import Path

from build123d import Axis, Compound, Location

from quiver.common import PETG, load_step

_DIR = Path(__file__).parent

# Target center-of-mass positions (from Fusion reference).
_RIGHT_POS = (115.50, 16.78, -71.00)
_LEFT_POS = (-115.50, 16.78, -71.00)


def make_assembly() -> Compound | None:
    """Build the battery slider subassembly from imported STEP files."""
    children = []

    # Left slider — the STEP file is already in the correct orientation.
    left = load_step(_DIR, "2211_battery_slider")
    if left:
        left.color = PETG
        com = left.center()
        left.move(Location((
            _LEFT_POS[0] - com.X,
            _LEFT_POS[1] - com.Y,
            _LEFT_POS[2] - com.Z,
        )))
        children.append(left)

    # Right slider — mirror across YZ plane to face the opposite wall.
    right = load_step(_DIR, "2211_battery_slider")
    if right:
        right.color = PETG
        right = right.rotate(Axis.Y, 180)
        com = right.center()
        right.move(Location((
            _RIGHT_POS[0] - com.X,
            _RIGHT_POS[1] - com.Y,
            _RIGHT_POS[2] - com.Z,
        )))
        children.append(right)

    if not children:
        return None
    return Compound(children=children, label="Battery Slider")
