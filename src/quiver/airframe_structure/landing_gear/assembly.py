"""BOM 1300 - Landing Gear subassembly.

Four angled legs extending below the lower plate, connected by two
horizontal cross-tubes. Foam sleeves cushion the landing points.

    Front view (not to scale):

            [A]======[A]            Lower plate (Z = -125)
             /        \             [A] = adapter bolted to plate
            /          \
           /  vertical  \           ~21 deg outward tilt
          /    tubes     \
    =[F][J]====      ====[J][F]=    Horizontal tubes (Z ~ -528)
                                    [J] = tube joint, [F] = foam sleeve

Each leg has three parts stacked along its axis:
  1. A vendor aluminum adapter (1330) bolted to the lower plate
  2. A carbon-fiber vertical tube (1310) angled ~21 deg outward
  3. A 3D-printed tube joint (1340) connecting to the horizontal tube

The two horizontal cross-tubes (1320) run front-to-back (along Y),
one on each side, connecting the left and right pairs of legs.
Foam sleeves (1350) wrap around the horizontal tubes at each landing
point, near where the legs meet the cross-tubes.

Looking from above, the four legs are at the same Y positions
(+/-123mm) but spread outward in X as they descend:

                (+Y)
                 |
          FL --- | --- FR        Y = +123
                 |
         (-X) --+-- (+X)
                 |
          BL --- | --- BR        Y = -123
                 |

Vendor parts in steps/vendor/:
    1330_main_adapter.step      Aluminum adapter (used 4x)

Custom parts in steps/:
    1340_tube_joint.step        3D-printed PETG-CF joint (used 4x)

Generated parts:
    1310 Vertical tube  -- 30mm OD, 2mm wall CF tube, 400mm long (used 4x)
    1320 Horizontal tube -- 30mm OD, 2mm wall CF tube, 500mm long (used 2x)
    1350 Foam sleeve    -- 40mm OD, 30mm ID foam sleeve, 66mm long (used 4x)
"""

import math
from pathlib import Path

from build123d import Axis, Compound, Cylinder, Location, Part

from quiver.common import ALUMINUM, CARBON_FIBER, FOAM, PETG, load_step

_DIR = Path(__file__).parent

# Carbon-fiber tube dimensions (shared by vertical and horizontal tubes)
_TUBE_OD = 30        # outer diameter (mm)
_TUBE_WALL = 2       # wall thickness (mm)
_VERT_TUBE_LENGTH = 400    # vertical tube length (mm)
_HORIZ_TUBE_LENGTH = 500   # horizontal tube length (mm)

# Foam sleeve dimensions (cushioning around horizontal tube at landing points)
_FOAM_OD = 40        # outer diameter (mm)
_FOAM_LENGTH = 66    # length along tube axis (mm)

# Vertical tube tilt angle from vertical (degrees).
# The legs splay outward from the plate corners. The tilt is derived
# from the horizontal run (145.84mm in X) and vertical drop (376.47mm
# in Z) between the adapter and tube joint centers.
_TILT_ANGLE = math.degrees(math.atan2(145.84, 376.47))  # ~21.18 deg

# All four legs sit at the same Y offset from the drone center.
_LEG_Y = 123.00

# X and Z positions along each leg axis (top to bottom).
# X is the horizontal offset from drone center; Z is the vertical
# position. Signs are applied per-corner: sx for X, sy for Y.
_ADAPTER_X = 123.22     # adapter center
_ADAPTER_Z = -141.48

_VERT_TUBE_X = 194.56   # vertical tube midpoint
_VERT_TUBE_Z = -322.50

_JOINT_X = 269.12       # tube joint center
_JOINT_Z = -518.09

# Horizontal tube axis position
_HORIZ_TUBE_X = 273.40  # X offset (left/right symmetry)
_HORIZ_TUBE_Z = -527.89 # Z position

# Foam sleeves sit near the ends of each horizontal tube
_FOAM_Y = 217.00    # 250 - 66/2: flush with tube ends

# Corner definitions: (X sign, Y sign)
_CORNERS = [
    ( 1,  1),   # FR -- front right
    (-1,  1),   # FL -- front left
    ( 1, -1),   # BR -- back right
    (-1, -1),   # BL -- back left
]


def _make_tube(length: float, label: str) -> Part:
    """Generate a carbon-fiber tube (hollow cylinder, centered at origin)."""
    outer = Cylinder(radius=_TUBE_OD / 2, height=length)
    inner = Cylinder(radius=_TUBE_OD / 2 - _TUBE_WALL, height=length)
    tube = outer - inner
    tube.label = label
    return tube


def make_assembly() -> Compound | None:
    """Build the landing gear subassembly from imported STEP files."""
    children = []

    for sx, sy in _CORNERS:
        # --- Main adapter (vendor, bolted to lower plate) ---
        # The STEP file is exported at a neutral orientation. We first
        # rotate it into the XZ plane (rotZ), then tilt it to match the
        # leg angle (rotY). Because the STEP geometry isn't centered at
        # the origin, the rotation shifts the center of mass — so we
        # compute the actual CoM after rotation and correct the offset.
        adapter = load_step(_DIR, "1330_main_adapter", vendor=True)
        if adapter:
            adapter.color = ALUMINUM
            adapter = adapter.rotate(Axis.Z, 90 * sx)
            adapter = adapter.rotate(Axis.Y, -_TILT_ANGLE * sx)
            com = adapter.center()
            adapter.move(Location((
                sx * _ADAPTER_X - com.X,
                sy * _LEG_Y - com.Y,
                _ADAPTER_Z - com.Z,
            )))
            children.append(adapter)

        # --- Vertical tube (generated, angled outward) ---
        # Generated tubes are symmetric and centered at the origin,
        # so no CoM correction is needed — just tilt and translate.
        v_tube = _make_tube(_VERT_TUBE_LENGTH, "1310-VerticalTube")
        v_tube.color = CARBON_FIBER
        v_tube = v_tube.rotate(Axis.Y, -_TILT_ANGLE * sx)
        v_tube.move(Location((
            sx * _VERT_TUBE_X,
            sy * _LEG_Y,
            _VERT_TUBE_Z,
        )))
        children.append(v_tube)

        # --- Tube joint (custom, connects vertical to horizontal tube) ---
        # Same rotation + CoM correction pattern as the adapter.
        joint = load_step(_DIR, "1340_tube_joint")
        if joint:
            joint.color = PETG
            joint = joint.rotate(Axis.Z, 90 * sx)
            joint = joint.rotate(Axis.Y, -_TILT_ANGLE * sx)
            com = joint.center()
            joint.move(Location((
                sx * _JOINT_X - com.X,
                sy * _LEG_Y - com.Y,
                _JOINT_Z - com.Z,
            )))
            children.append(joint)

    # --- Horizontal cross-tubes (generated, running front-to-back) ---
    for sx in [1, -1]:
        h_tube = _make_tube(_HORIZ_TUBE_LENGTH, "1320-HorizontalTube")
        h_tube.color = CARBON_FIBER
        h_tube = h_tube.rotate(Axis.X, 90)  # orient along Y
        h_tube.move(Location((
            sx * _HORIZ_TUBE_X,
            0,
            _HORIZ_TUBE_Z,
        )))
        children.append(h_tube)

    # --- Foam sleeves (generated, cushioning at landing points) ---
    # Cylindrical sleeves that wrap around the horizontal tubes near each leg.
    for sx, sy in _CORNERS:
        foam_outer = Cylinder(radius=_FOAM_OD / 2, height=_FOAM_LENGTH)
        foam_inner = Cylinder(radius=_TUBE_OD / 2, height=_FOAM_LENGTH)
        foam = foam_outer - foam_inner
        foam = foam.rotate(Axis.X, 90)  # orient along Y
        foam.move(Location((
            sx * _HORIZ_TUBE_X,
            sy * _FOAM_Y,
            _HORIZ_TUBE_Z,
        )))
        foam.label = "1350-Foam"
        foam.color = FOAM
        children.append(foam)

    if not children:
        return None
    return Compound(children=children, label="Landing Gear")
