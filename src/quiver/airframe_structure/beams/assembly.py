"""BOM 1200 - Beams subassembly.

Cockpit support beams and battery compartment walls.

The cockpit beams form an X shape sandwiched between the upper and middle
plates. Looking down from above (top view):

         (-X)
          |
    CCW   |   CW long
    back  |  /
      \\   | /
       \\  |/
    ----+----  (+Y)
       /|\\
      / | \\
     /  |  CCW
    CW  |  front
    long|
         (+X)

The CW long beam spans the full diagonal. The two CCW back beams span
the other diagonal, with a gap at the center where they meet the CW beam.
Each CCW beam covers one half of its diagonal.

The battery walls are vertical rectangular tubes on the left (-X) and
right (+X) sides, running the full 300mm depth between the middle and
lower plates.

Expected STEP files in steps/:
    1211_cw_long.step               40x40x1mm aluminum tube (CW long)
    1212_ccw_back.step              40x40x1mm aluminum tube (CCW, used 2x)
    1221_battery_wall.step          30x300mm, 2mm wall aluminum tube (used 2x)
"""

from pathlib import Path

from build123d import Axis, Compound, Location

from quiver.common import load_step

_DIR = Path(__file__).parent

# Beam rotation angle for the X pattern (degrees from Y axis)
BEAM_ANGLE = 45

# The CW long beam STEP is oriented along Y with its center at Y=144.89.
# We center it at the origin before rotating.
_CW_LONG_CENTER_Y = 144.89

# The CCW beams sit on the opposite diagonal, offset perpendicular to their
# length by half the beam width (20mm) so they butt up against the CW beam
# at the center. 20mm * cos(45) = 14.14, rounded to match Fusion geometry.
_CCW_PERP_OFFSET = 14.23

# Battery wall positions (wall center X, Y shift to center, Z shift to sit
# between mid plate Z=-21 and lower plate Z=-125)
_WALL_X = 135       # center of 30mm wall at edge of 300mm plate
_WALL_Y = -150      # center 300mm wall on the 300mm plate
_WALL_Z = -71       # center 100mm wall between Z=-121 and Z=-21


def make_assembly() -> Compound | None:
    """Build the beams subassembly from imported STEP files."""
    children = []

    # --- Cockpit support beams (X pattern) ---

    cw_long = load_step(_DIR, "1211_cw_long")
    if cw_long:
        cw_long.move(Location((0, -_CW_LONG_CENTER_Y, 0)))
        cw_long = cw_long.rotate(Axis.Z, -BEAM_ANGLE)
        children.append(cw_long)

    ccw_back = load_step(_DIR, "1212_ccw_back")
    if ccw_back:
        ccw_back = ccw_back.rotate(Axis.Z, BEAM_ANGLE)
        ccw_back.move(Location((-_CCW_PERP_OFFSET, _CCW_PERP_OFFSET, 0)))
        children.append(ccw_back)

    ccw_front = load_step(_DIR, "1212_ccw_back")
    if ccw_front:
        ccw_front = ccw_front.rotate(Axis.Z, -(180 - BEAM_ANGLE))
        ccw_front.move(Location((_CCW_PERP_OFFSET, -_CCW_PERP_OFFSET, 0)))
        children.append(ccw_front)

    # --- Battery compartment walls ---

    wall_left = load_step(_DIR, "1221_battery_wall")
    if wall_left:
        wall_left = wall_left.rotate(Axis.Y, 180)
        wall_left.move(Location((-_WALL_X, _WALL_Y, _WALL_Z)))
        children.append(wall_left)

    wall_right = load_step(_DIR, "1221_battery_wall")
    if wall_right:
        wall_right = wall_right.rotate(Axis.X, 180)
        wall_right.move(Location((_WALL_X, -_WALL_Y, _WALL_Z)))
        children.append(wall_right)

    if not children:
        return None
    return Compound(children=children, label="Beams")
