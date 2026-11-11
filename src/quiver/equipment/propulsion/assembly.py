"""BOM 3100 - Propulsion System subassembly.

Four motor+propeller sets, one at the tip of each arm. Adjacent
corners spin opposite directions (CW/CCW) for yaw control.

    Top view (looking down):

            (+Y)
            |
        FL(CCW)     FR(CW)
        \\   |      /
            \\  |  /
    (-X) ---+--- (+X)
            /  |  \\
        /   |      \\
        BL(CW)      BR(CCW)
            |

Each motor STEP stands its shaft up with rotX(90), then faces the arm
diagonal: intrinsic rotation (90, arm_angle, 0).

Diagonal corners share a direction: CW on FR+BL, CCW on FL+BR, so the
two spin directions balance yaw (a Quad X layout: FRAME_CLASS 1,
FRAME_TYPE 1). Same-side pairing would leave a net yaw torque.

Vendor parts in steps/vendor/:
    3111_motor.step         Motor (used 4x)
    3112_propeller.step     CW propeller (used 2x: FR, BL)
    3122_propeller.step     CCW propeller (used 2x: FL, BR)

Poses are full rigid transforms (see quiver.common.place) from the Fusion
360 v148 master. The propeller STEPs have their origin ~325 mm from the
hub, so their positions look arbitrary; the CW props are flipped with
rotX(180). Fusion's BL propeller is turned 180 deg about its own shaft
relative to FR, which a center-of-mass check could not see.
"""

from pathlib import Path

from build123d import Compound

from quiver.common import load_step, place

_DIR = Path(__file__).parent

# Motor STEP origin, signed per corner along the arm diagonals
_MOTOR_XY = 449.4299

# Corner definitions: (arm_angle, X_sign, Y_sign, propeller STEP, propeller pose)
_CORNERS = [
    ( -45,  1,  1, "3112_propeller", ((551.8022, 140.4902, 43.9307), (180, 0, 135))),    # FR — CW
    (  45, -1,  1, "3122_propeller", ((-347.0576, 758.3697, 43.9307), (0, 0, 135))),     # FL — CCW
    (-135,  1, -1, "3122_propeller", ((347.0576, -758.3697, 43.9307), (0, 0, -45))),     # BR — CCW
    ( 135, -1, -1, "3112_propeller", ((-347.0576, -758.3697, 43.9307), (180, 0, 135))),  # BL — CW
]


def make_assembly() -> Compound | None:
    """Build the propulsion subassembly from imported STEP files."""
    children = []

    for arm_angle, sx, sy, prop_file, prop_pose in _CORNERS:
        motor = load_step(_DIR, "3111_motor", vendor=True)
        if motor:
            place(motor, (sx * _MOTOR_XY, sy * _MOTOR_XY, 0), (90, arm_angle, 0))
            children.append(motor)

        prop = load_step(_DIR, prop_file, vendor=True)
        if prop:
            children.append(place(prop, *prop_pose))

    if not children:
        return None
    return Compound(children=children, label="Propulsion")
