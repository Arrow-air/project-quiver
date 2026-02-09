"""BOM 2100 - Attachment Interface subassembly.

Three quick-release mounting points for attaching payloads to the drone.
Each mounting point consists of a spacer bolted to the airframe and a
quick-release interface plate that the payload clips into.

    Front view (cross-section through battery compartment):

                 ========    Upper plate
                  |    |
        [P][S]====|    |====[S][P]    Right/Left interfaces
                  |    |              on battery walls
                 ========    Lower plate
                  [S]
                  [P]        Bottom interface
                             under lower plate

    [S] = spacer, [P] = interface plate (quick-release)

The left and right interfaces mount on the outer face of the battery
walls (X = +/-150). The bottom interface hangs from the underside of
the lower plate (Z = -125).

STEP files in steps/:
    2111_attach_spacer.step         Spacer for left/right walls (used 2x)
    2112_attach_plate.step          Quick-release interface plate (used 3x)
    2131_attach_spacer_bottom.step  Spacer for bottom, with wiring notch (used 1x)
"""

from pathlib import Path

from build123d import Axis, Compound, Location

from quiver.common import load_step

_DIR = Path(__file__).parent

# Interface plate target positions (center of mass, from Fusion reference).
# The plate STEP contains only the drone-side of the quick-release mechanism
# (Fixed_Top + press pins + springs). The mechanism direction runs along
# local -Y in the raw STEP file. Each mounting point needs two rotations:
#   1. A primary rotation to aim the mechanism outward (away from drone).
#   2. A 180-deg flip to correct the internal feature orientation.
_RIGHT_PLATE_POS = (185.65, -0.02, -71.00)
_LEFT_PLATE_POS = (-185.65, 0.02, -71.00)
_BOTTOM_PLATE_POS = (0.0, 0.0, -160.70)


def make_assembly() -> Compound | None:
    """Build the attachment interface subassembly from imported STEP files."""
    children = []

    # --- Right side (2110) ---

    # The spacer STEP has a baked-in position on the left side (X = -165).
    # Rotate 180 deg around Z to mirror it to the right side (X = +165).
    right_spacer = load_step(_DIR, "2111_attach_spacer")
    if right_spacer:
        right_spacer = right_spacer.rotate(Axis.Z, 180)
        children.append(right_spacer)

    right_plate = load_step(_DIR, "2112_attach_plate")
    if right_plate:
        right_plate = right_plate.rotate(Axis.Z, 90)    # mechanism faces +X (outward)
        right_plate = right_plate.rotate(Axis.X, 180)    # flip to match reference
        com = right_plate.center()
        right_plate.move(Location((
            _RIGHT_PLATE_POS[0] - com.X,
            _RIGHT_PLATE_POS[1] - com.Y,
            _RIGHT_PLATE_POS[2] - com.Z,
        )))
        children.append(right_plate)

    # --- Left side (2120) ---

    # The spacer STEP is already at the correct left-side position.
    left_spacer = load_step(_DIR, "2111_attach_spacer")
    if left_spacer:
        children.append(left_spacer)

    left_plate = load_step(_DIR, "2112_attach_plate")
    if left_plate:
        left_plate = left_plate.rotate(Axis.Z, -90)     # mechanism faces -X (outward)
        left_plate = left_plate.rotate(Axis.X, 180)      # flip to match reference
        com = left_plate.center()
        left_plate.move(Location((
            _LEFT_PLATE_POS[0] - com.X,
            _LEFT_PLATE_POS[1] - com.Y,
            _LEFT_PLATE_POS[2] - com.Z,
        )))
        children.append(left_plate)

    # --- Bottom (2130) ---

    # The bottom spacer STEP is already at the correct position.
    # It has a wiring notch that the left/right spacer does not.
    bottom_spacer = load_step(_DIR, "2131_attach_spacer_bottom")
    if bottom_spacer:
        children.append(bottom_spacer)

    bottom_plate = load_step(_DIR, "2112_attach_plate")
    if bottom_plate:
        bottom_plate = bottom_plate.rotate(Axis.X, 90)   # mechanism faces -Z (downward)
        bottom_plate = bottom_plate.rotate(Axis.Z, 180)   # flip to match reference
        com = bottom_plate.center()
        bottom_plate.move(Location((
            _BOTTOM_PLATE_POS[0] - com.X,
            _BOTTOM_PLATE_POS[1] - com.Y,
            _BOTTOM_PLATE_POS[2] - com.Z,
        )))
        children.append(bottom_plate)

    if not children:
        return None
    return Compound(children=children, label="Attachment Interface")
