"""BOM 2400 - Cockpit Enclosure subassembly.

Weatherproof cockpit enclosure that covers the electronics bay on top
of the upper plate. Hinged at the back (+Y) and latched at the front
(-Y) on both sides.

    Top view (looking down, cap removed):

            (+Y)
            |
        [HL]====[HR]            Hinge anchors (back edge)
        /                \\
        |                |
        |   Enclosure    |      Main enclosure shell
        |                |
        \\                /
        [LL]    [LR]            Latch clips (front corners)
            |
            (-Y)

    Side view:

        [Top cap]               Z ~ 50..101  (domed cap)
        ==================
        |  Main enclosure |     Z ~ -39..54  (shell, sits on upper plate)
        ==================
        |  Upper plate    |     Z = 20..21

    [HL]/[HR] = hinge anchors at Y ~ 153..160
    [LL]/[LR] = latch clips at Y ~ -103..-80

STEP files in steps/:
    2411_main_enclosure.step        Main cockpit enclosure shell
    2412_enclosure_top_cap.step     Domed top cap
    2420_hinge.step                 Hinge anchor (used 2x, mirrored)
    2430_latch.step                 Latch clip (used 2x, mirrored)

Poses are full rigid transforms (see quiver.common.place) from the Fusion
360 v148 master.
"""

from pathlib import Path

from build123d import Compound, Plane

from quiver.common import PETG, load_step, place

_DIR = Path(__file__).parent

# Right-side poses: STEP origin (mm), intrinsic XYZ rotation (deg). Each
# pair is placed on the right side first, then mirrored across YZ, as in
# the Fusion v148 master.
_RIGHT_HINGE_POSE = ((223.25, -92.4688, 20.25), (90, 0, 0))
_RIGHT_LATCH_POSE = ((153.9, -91.3494, 43.7995), (0, 0, -90))


def make_assembly() -> Compound | None:
    """Build the cockpit enclosure subassembly from imported STEP files."""
    children = []

    # --- Enclosure shell (2410) ---

    enclosure = load_step(_DIR, "2411_main_enclosure")
    if enclosure:
        enclosure.color = PETG
        children.append(enclosure)

    top_cap = load_step(_DIR, "2412_enclosure_top_cap")
    if top_cap:
        top_cap.color = PETG
        children.append(top_cap)

    # --- Hinge anchors (2420) ---

    # Right hinge — rotX(90) stands the raw STEP up.
    right_hinge = load_step(_DIR, "2420_hinge")
    if right_hinge:
        right_hinge.color = PETG
        place(right_hinge, *_RIGHT_HINGE_POSE)
        children.append(right_hinge)

        # Left hinge — mirror the positioned right hinge across YZ plane.
        left_hinge = right_hinge.mirror(Plane.YZ)
        left_hinge.color = PETG
        children.append(left_hinge)

    # --- Latch clips (2430) ---

    # Right latch — rotZ(-90) swaps X/Y to match the reference orientation.
    right_latch = load_step(_DIR, "2430_latch")
    if right_latch:
        right_latch.color = PETG
        place(right_latch, *_RIGHT_LATCH_POSE)
        children.append(right_latch)

        # Left latch — mirror the positioned right latch across YZ plane.
        left_latch = right_latch.mirror(Plane.YZ)
        left_latch.color = PETG
        children.append(left_latch)

    if not children:
        return None
    return Compound(children=children, label="Cockpit Enclosure")
