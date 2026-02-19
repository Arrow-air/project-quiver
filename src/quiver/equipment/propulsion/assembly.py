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
        BL(CCW)     BR(CW)
            |

Each motor is aligned along the arm diagonal via rotX(90) to point
the shaft upward, then rotZ(arm_angle) to face the correct corner.

CW propellers (3112) are on FR and BR arms.
CCW propellers (3122) are on FL and BL arms.

Vendor parts in steps/vendor/:
    3111_motor.step         Motor (used 4x)
    3112_propeller.step     CW propeller (used 2x: FR, BR)
    3122_propeller.step     CCW propeller (used 2x: FL, BL)
"""

from pathlib import Path

from build123d import Axis, Compound, Location

from quiver.common import load_step

_DIR = Path(__file__).parent

# Target center-of-mass positions (from Fusion reference).
# Each corner follows the same pattern, scaled by X/Y signs.
_MOTOR_XY = 446.74
_MOTOR_Z = 15.57
_PROP_XY = 449.43
_PROP_Z = 56.27

# Corner definitions: (arm_angle, X_sign, Y_sign, propeller_step, is_cw)
_CORNERS = [
    ( -45,  1,  1, "3112_propeller", True),    # FR — CW
    (  45, -1,  1, "3122_propeller", False),   # FL — CCW
    (-135,  1, -1, "3112_propeller", True),    # BR — CW
    ( 135, -1, -1, "3122_propeller", False),   # BL — CCW
]


def make_assembly() -> Compound | None:
    """Build the propulsion subassembly from imported STEP files."""
    children = []

    for arm_angle, sx, sy, prop_file, is_cw in _CORNERS:
        # --- Motor ---
        # rotX(90) aligns the motor shaft upward (+Z), then rotZ rotates
        # to face the arm diagonal.
        motor = load_step(_DIR, "3111_motor", vendor=True)
        if motor:
            motor = motor.rotate(Axis.X, 90)
            motor = motor.rotate(Axis.Z, arm_angle)
            com = motor.center()
            motor.move(Location((
                sx * _MOTOR_XY - com.X,
                sy * _MOTOR_XY - com.Y,
                _MOTOR_Z - com.Z,
            )))
            children.append(motor)

        # --- Propeller ---
        # CW props (3112) need rotX(180) to flip, then rotZ to align.
        # CCW props (3122) only need rotZ to align.
        prop = load_step(_DIR, prop_file, vendor=True)
        if prop:
            if is_cw:
                prop = prop.rotate(Axis.X, 180)
                prop = prop.rotate(Axis.Z, 270 + arm_angle)
            else:
                prop = prop.rotate(Axis.Z, 90 + arm_angle)
            com = prop.center()
            prop.move(Location((
                sx * _PROP_XY - com.X,
                sy * _PROP_XY - com.Y,
                _PROP_Z - com.Z,
            )))
            children.append(prop)

    if not children:
        return None
    return Compound(children=children, label="Propulsion")
