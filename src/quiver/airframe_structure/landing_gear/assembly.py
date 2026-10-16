"""BOM 1300 - Landing Gear subassembly.

Four angled legs extending below the lower plate, connected by two
horizontal cross-tubes. Foam sleeves cushion the landing points.

    Front view (not to scale):

            [A]======[A]            Lower plate (Z = -125)
            /          \\           [A] = adapter bolted to plate
            /          \\
            / vertical  \\          21 deg outward tilt
        /      tubes      \\
    =[F][J]====      ====[J][F]=    Horizontal tubes (Z ~ -528)
                                    [J] = tube joint, [F] = foam sleeve

Each leg has three parts stacked along its axis:
    1. An aluminum adapter (1331/1332) bolted to the lower plate
    2. A carbon-fiber vertical tube (1310) angled 21 deg outward
    3. A tube joint (1341/1342) connecting to the horizontal tube

The adapters and tube joints are handed: the FL and BR legs use mirror
images of the FR and BL parts, so all four legs are mirror-symmetric.

The two horizontal cross-tubes (1320) run front-to-back (along Y),
one on each side, connecting the left and right pairs of legs.
Foam sleeves (1350) wrap around the horizontal tubes at each landing
point, near where the legs meet the cross-tubes.

Looking from above, the four legs are at the same Y positions
(+/-123mm) but spread outward in X as they descend:

                (+Y)
                |
        FL ---  |  --- FR        Y = +123
                |
        (-X) --+-- (+X)
                |
        BL ---  |  --- BR        Y = -123
                |

Vendor parts in steps/vendor/:
    1331_main_adapter.step      Aluminum adapter, FR/BL hand (used 2x)
    1332_main_adapter.step      Aluminum adapter, FL/BR hand (used 2x, mirror of 1331)

Parts in steps/:
    1341_tube_joint.step        Tube joint, FR/BL hand (used 2x)
    1342_tube_joint.step        Tube joint, FL/BR hand (used 2x, mirror of 1341)

Generated parts:
    1310 Vertical tube  -- 30mm OD, 1mm wall CF tube, 400mm long (used 4x)
    1320 Horizontal tube -- 30mm OD, 1mm wall CF tube, 500mm long (used 2x)
    1350 Foam sleeve    -- 40mm OD, 30mm ID foam sleeve, 66mm long (used 4x)

Poses are full rigid transforms (see quiver.common.place) from the Fusion
360 v148 master. The mirror-hand STEPs are mirrored about their own YZ
plane, so one pose pattern, signed per corner, places every leg.
"""

from pathlib import Path

from build123d import Compound, Cylinder, Part

from quiver.common import ALUMINUM, CARBON_FIBER, FOAM, PETG, load_step, place

_DIR = Path(__file__).parent

# Carbon-fiber tube dimensions (shared by vertical and horizontal tubes)
_TUBE_OD = 30        # outer diameter (mm)
_TUBE_WALL = 1       # wall thickness (mm); 30x28 tube, matches BOM + Fusion v148
_VERT_TUBE_LENGTH = 400    # vertical tube length (mm)
_HORIZ_TUBE_LENGTH = 500   # horizontal tube length (mm)

# Foam sleeve dimensions (cushioning around horizontal tube at landing points)
_FOAM_OD = 40        # outer diameter (mm)
_FOAM_LENGTH = 66    # length along tube axis (mm)

# Leg tilt from vertical (degrees), outward in X (Fusion v148).
_TILT_ANGLE = 21.0

# All four legs sit at the same Y offset from the drone center.
_LEG_Y = 123.0

# X and Z positions along each leg (top to bottom), signed per corner:
# sx for X, sy for Y. For the adapter and joint these place the STEP
# origin; the generated tubes are centered on their origin.
_ADAPTER_X, _ADAPTER_Z = 122.886, -135.7875
_VERT_TUBE_X, _VERT_TUBE_Z = 194.5596, -322.5036
_JOINT_X, _JOINT_Z = 273.4005, -527.8913

# Horizontal tube axis, through the tube joints
_HORIZ_TUBE_X, _HORIZ_TUBE_Z = _JOINT_X, _JOINT_Z

# Foam sleeves sit near the ends of each horizontal tube, concentric on it
# (Fusion v148 draws them 2 mm above the tube axis).
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
        # FR and BL use the 1331/1341 hand, FL and BR its mirror image.
        right_hand = sx * sy > 0
        # Each STEP stands along its own Z axis; rotZ turns it to face the
        # corner, rotY tilts it outward with the leg.
        leg_rot = (0, -sx * _TILT_ANGLE, sx * 90)

        # --- Main adapter (bolted to the lower plate) ---
        adapter = load_step(
            _DIR, "1331_main_adapter" if right_hand else "1332_main_adapter", vendor=True)
        if adapter:
            adapter.color = ALUMINUM
            place(adapter, (sx * _ADAPTER_X, sy * _LEG_Y, _ADAPTER_Z), leg_rot)
            children.append(adapter)

        # --- Vertical tube (generated, angled outward) ---
        v_tube = _make_tube(_VERT_TUBE_LENGTH, "1310-VerticalTube")
        v_tube.color = CARBON_FIBER
        place(v_tube, (sx * _VERT_TUBE_X, sy * _LEG_Y, _VERT_TUBE_Z), (0, -sx * _TILT_ANGLE, 0))
        children.append(v_tube)

        # --- Tube joint (connects vertical to horizontal tube) ---
        joint = load_step(_DIR, "1341_tube_joint" if right_hand else "1342_tube_joint")
        if joint:
            joint.color = PETG
            place(joint, (sx * _JOINT_X, sy * _LEG_Y, _JOINT_Z), leg_rot)
            children.append(joint)

    # --- Horizontal cross-tubes (generated, running front-to-back) ---
    for sx in [1, -1]:
        h_tube = _make_tube(_HORIZ_TUBE_LENGTH, "1320-HorizontalTube")
        h_tube.color = CARBON_FIBER
        place(h_tube, (sx * _HORIZ_TUBE_X, 0, _HORIZ_TUBE_Z), (90, 0, 0))  # along Y
        children.append(h_tube)

    # --- Foam sleeves (generated, cushioning at landing points) ---
    # Cylindrical sleeves that wrap around the horizontal tubes near each leg.
    for sx, sy in _CORNERS:
        foam_outer = Cylinder(radius=_FOAM_OD / 2, height=_FOAM_LENGTH)
        foam_inner = Cylinder(radius=_TUBE_OD / 2, height=_FOAM_LENGTH)
        foam = foam_outer - foam_inner
        place(foam, (sx * _HORIZ_TUBE_X, sy * _FOAM_Y, _HORIZ_TUBE_Z), (90, 0, 0))  # along Y
        foam.label = "1350-Foam"
        foam.color = FOAM
        children.append(foam)

    if not children:
        return None
    return Compound(children=children, label="Landing Gear")
