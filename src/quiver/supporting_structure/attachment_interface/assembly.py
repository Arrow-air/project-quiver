"""BOM 2100 - Attachment Interface subassembly.

Three quick-release mounting points for attaching payloads to the drone.
Each mounting point consists of a spacer bolted to the airframe and a
quick-release interface plate that the payload clips into.

    Front view (cross-section through battery compartment):

                ========    Upper plate
                |    |
        [P][S]==|    |==[S][P]    Right/Left interfaces
                |    |            on battery walls
                ========    Lower plate
                [S]
                [P]          Bottom interface
                            under lower plate

    [S] = spacer, [P] = interface plate (quick-release)

The left and right interfaces mount on the outer face of the battery
walls (X = +/-150). The bottom interface hangs from the underside of
the lower plate (Z = -125).

STEP files in steps/:
    2111_attach_spacer.step         Spacer for left/right walls (used 2x)
    2112_attach_plate.step          Quick-release interface plate (used 3x)
    2131_attach_spacer_bottom.step  Spacer for bottom, with wiring notch (used 1x)

Poses are full rigid transforms (see quiver.common.place) from the Fusion
360 v148 master.
"""

from pathlib import Path

from build123d import Compound

from quiver.common import ALUMINUM, PETG, load_step, place

_DIR = Path(__file__).parent

# Interface plate poses (STEP origin mm, intrinsic XYZ deg). The plate STEP
# contains only the drone side of the quick-release mechanism (Fixed_Top +
# press pins + springs), with the mechanism along local -Y. rotZ aims it
# outward, rotX(180) flips it to the drone-side orientation.
_RIGHT_PLATE_POSE = ((164.7019, 3.8438, -22.9383), (180, 0, 90))     # mechanism faces +X
_LEFT_PLATE_POSE = ((-164.7019, -3.8438, -22.9383), (180, 0, -90))   # mechanism faces -X
# Fusion's bottom fixed top is a slightly different body, turned 0.02 deg
# off square; this pose keeps it square, fitted to the press pins and springs.
_BOTTOM_PLATE_POSE = ((3.8438, -48.1421, -139.7019), (-90, 0, 180))  # mechanism faces -Z

# The spacer STEP is baked at the left position (X = -165). Fusion's right
# occurrence is the same block turned 180 deg about Y (transform diag
# -1,+1,-1), which also lifts it by 142 mm; the origin moves down to match.
_RIGHT_SPACER_POSE = ((0, 0, -142), (0, 180, 0))


def make_assembly() -> Compound | None:
    """Build the attachment interface subassembly from imported STEP files."""
    children = []

    # --- Right side (2110) ---

    right_spacer = load_step(_DIR, "2111_attach_spacer")
    if right_spacer:
        right_spacer.color = PETG
        children.append(place(right_spacer, *_RIGHT_SPACER_POSE))

    right_plate = load_step(_DIR, "2112_attach_plate")
    if right_plate:
        right_plate.color = ALUMINUM
        children.append(place(right_plate, *_RIGHT_PLATE_POSE))

    # --- Left side (2120) ---

    # The spacer STEP is already at the correct left-side position.
    left_spacer = load_step(_DIR, "2111_attach_spacer")
    if left_spacer:
        left_spacer.color = PETG
        children.append(left_spacer)

    left_plate = load_step(_DIR, "2112_attach_plate")
    if left_plate:
        left_plate.color = ALUMINUM
        children.append(place(left_plate, *_LEFT_PLATE_POSE))

    # --- Bottom (2130) ---

    # The bottom spacer STEP is already at the correct position.
    # It has a wiring notch that the left/right spacer does not.
    bottom_spacer = load_step(_DIR, "2131_attach_spacer_bottom")
    if bottom_spacer:
        bottom_spacer.color = PETG
        children.append(bottom_spacer)

    bottom_plate = load_step(_DIR, "2112_attach_plate")
    if bottom_plate:
        bottom_plate.color = ALUMINUM
        children.append(place(bottom_plate, *_BOTTOM_PLATE_POSE))

    if not children:
        return None
    return Compound(children=children, label="Attachment Interface")
