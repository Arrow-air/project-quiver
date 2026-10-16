"""BOM 1400 - Motor Arm subassembly.

Four foldable motor arms, one at each corner of the plate stack. Each arm
has a connector clamped between the upper and middle plates and a carbon-
fiber tube extending diagonally outward. Looking from above:

            (+Y)
            |
        FL  |    FR
        \\   |   /
            \\  |  /
    --------+--------  (+X)
            /  |  \\
        /   |   \\
        BL  |    BR
            |

Each connector and tube is the same part, rotated 90 deg per corner.
The arms radiate outward at 45 deg diagonals from the plate center.

Vendor parts in steps/vendor/:
    1411_arm_connector.step     Foldable arm connector (used 4x)

Generated parts:
    1412 Arm tube — 30mm OD, 1mm wall carbon-fiber tube, 360mm long (used 4x)

Poses are full rigid transforms (see quiver.common.place) from the Fusion
360 v148 master.
"""

from pathlib import Path

from build123d import Axis, Compound, Cylinder, Part

from quiver.common import ALUMINUM, CARBON_FIBER, load_step, place

_DIR = Path(__file__).parent

# Arm tube dimensions (carbon-fiber tube)
_TUBE_OD = 30        # outer diameter (mm)
_TUBE_WALL = 1       # wall thickness (mm); 30x28 tube, matches BOM + Fusion v148
_TUBE_LENGTH = 360   # length (mm)

# X and Y offsets (signed per corner) along the 45-deg diagonals
_CONNECTOR_OFFSET = 102.5233  # connector STEP origin, ~145mm along the diagonal
_TUBE_OFFSET = 161.2839       # inner end of the tube, ~228mm along the diagonal

# (rotation angle, X sign, Y sign)
_ARM_POSITIONS = [
    ( -45,  1,  1),   # FR — front right
    (  45, -1,  1),   # FL — front left
    (-135,  1, -1),   # BR — back right
    ( 135, -1, -1),   # BL — back left
]


def _make_arm_tube() -> Part:
    """Generate a carbon-fiber arm tube, running along +Y from its origin."""
    outer = Cylinder(radius=_TUBE_OD / 2, height=_TUBE_LENGTH, align=None)
    inner = Cylinder(radius=_TUBE_OD / 2 - _TUBE_WALL, height=_TUBE_LENGTH, align=None)
    tube = outer - inner
    tube = tube.rotate(Axis.X, -90)
    tube.label = "1412-Arm"
    return tube


def make_assembly() -> Compound | None:
    """Build the motor arm subassembly from imported STEP files."""
    children = []

    for angle, sx, sy in _ARM_POSITIONS:
        connector = load_step(_DIR, "1411_arm_connector", vendor=True)
        if connector:
            connector.color = ALUMINUM
            place(connector, (sx * _CONNECTOR_OFFSET, sy * _CONNECTOR_OFFSET, 0), (0, 0, angle))
            children.append(connector)

        tube = _make_arm_tube()
        tube.color = CARBON_FIBER
        place(tube, (sx * _TUBE_OFFSET, sy * _TUBE_OFFSET, 0), (0, 0, angle))
        children.append(tube)

    if not children:
        return None
    return Compound(children=children, label="Motor Arm")
