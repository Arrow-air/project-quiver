"""BOM 1400 - Motor Arm subassembly.

Four foldable motor arms, one at each corner of the plate stack. Each arm
has a connector clamped between the upper and middle plates and a carbon-
fiber tube extending diagonally outward. Looking from above:

              (+Y)
               |
        FL     |     FR
          \\    |    /
           \\   |   /
    --------+--------  (+X)
           /   |   \\
          /    |    \\
        BL     |     BR
               |

Each connector and tube is the same part, rotated 90 deg per corner.
The arms radiate outward at 45 deg diagonals from the plate center.

Vendor parts in steps/vendor/:
    1411_arm_connector.step     Foldable arm connector (used 4x)

Generated parts:
    1412 Arm tube — 30mm OD, 2mm wall carbon-fiber tube, 360mm long (used 4x)
"""

from pathlib import Path

from build123d import Axis, Compound, Cylinder, Location, Part

from quiver.common import ALUMINUM, CARBON_FIBER, load_step

_DIR = Path(__file__).parent

# Arm tube dimensions (carbon-fiber tube)
_TUBE_OD = 30        # outer diameter (mm)
_TUBE_WALL = 2       # wall thickness (mm)
_TUBE_LENGTH = 360   # length (mm)

# Distance from plate center to each part along the 45-deg diagonal axes
_CONNECTOR_OFFSET = 102.52   # connector center, ~145mm along diagonal
_TUBE_OFFSET = 161.28        # tube center, ~228mm along diagonal

# (rotation angle, X sign, Y sign)
_ARM_POSITIONS = [
    ( -45,  1,  1),   # FR — front right
    (  45, -1,  1),   # FL — front left
    (-135,  1, -1),   # BR — back right
    ( 135, -1, -1),   # BL — back left
]


def _make_arm_tube() -> Part:
    """Generate a carbon-fiber arm tube (hollow cylinder along Y)."""
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
            connector = connector.rotate(Axis.Z, angle)
            connector.move(Location((sx * _CONNECTOR_OFFSET, sy * _CONNECTOR_OFFSET, 0)))
            children.append(connector)

        tube = _make_arm_tube()
        tube.color = CARBON_FIBER
        tube = tube.rotate(Axis.Z, angle)
        tube.move(Location((sx * _TUBE_OFFSET, sy * _TUBE_OFFSET, 0)))
        children.append(tube)

    if not children:
        return None
    return Compound(children=children, label="Motor Arm")
