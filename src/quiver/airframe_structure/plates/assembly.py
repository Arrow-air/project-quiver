"""BOM 1100 - Plates subassembly.

Three-layer aluminum plate sandwich forming the core airframe.
The upper and middle plates sandwich the cockpit beams (see BOM 1200).
The lower plate sits below the battery compartment walls.

    Side view (not to scale):

        ======== Upper plate (1mm)    Z = 20
        \\  /
            \\/   Cockpit beams (40mm)  Z = -20 to 20
        /\\
        /  \\
        ======== Middle plate (1mm)   Z = -21
            ||
            ||    Battery walls (100mm) Z = -121 to -21
            ||
        ======== Lower plate (4mm)    Z = -125

Expected STEP files in steps/:
    1111_upper_plate.step       1mm aluminum upper plate (300x300mm)
    1112_middle_plate.step      1mm aluminum middle plate (300x300mm)
    1113_lower_plate.step       4mm aluminum lower plate (300x300mm)
"""

from pathlib import Path

from build123d import Compound, Location

from quiver.common import ALUMINUM, load_step

_DIR = Path(__file__).parent

# Z positions for each plate (bottom surface, measured from drone center)
UPPER_PLATE_Z = 20      # top of beam sandwich
MIDDLE_PLATE_Z = -21     # bottom of beam sandwich
LOWER_PLATE_Z = -125     # below battery compartment

# The STEP files have baked-in Z offsets from the Fusion 360 export.
# We undo those and reapply the correct positions explicitly.
# All offsets reference the bottom surface of each plate.
_UPPER_STEP_OFFSET = 20   # STEP file is at Z=20..21
_MIDDLE_STEP_OFFSET = -21  # STEP file is at Z=-21..-20
_LOWER_STEP_OFFSET = -20   # STEP file is at Z=-20..-16


def make_assembly() -> Compound | None:
    """Build the plates subassembly from imported STEP files."""
    upper = load_step(_DIR, "1111_upper_plate")
    middle = load_step(_DIR, "1112_middle_plate")
    lower = load_step(_DIR, "1113_lower_plate")

    children = []

    if upper:
        upper.color = ALUMINUM
        dz = UPPER_PLATE_Z - _UPPER_STEP_OFFSET
        children.append(upper.move(Location((0, 0, dz))))
    if middle:
        middle.color = ALUMINUM
        dz = MIDDLE_PLATE_Z - _MIDDLE_STEP_OFFSET
        children.append(middle.move(Location((0, 0, dz))))
    if lower:
        lower.color = ALUMINUM
        dz = LOWER_PLATE_Z - _LOWER_STEP_OFFSET
        children.append(lower.move(Location((0, 0, dz))))

    if not children:
        return None
    return Compound(children=children, label="Plates")
