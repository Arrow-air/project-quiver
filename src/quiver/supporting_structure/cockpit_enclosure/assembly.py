"""BOM 2400 - Cockpit Enclosure subassembly.

Weatherproof cockpit enclosure that covers the electronics bay on top
of the upper plate. Hinged at the back (+Y) and latched at the front
(-Y) on both sides.

    Top view (looking down, cap removed):

              (+Y)
               |
          [HL]====[HR]          Hinge anchors (back edge)
         /              \\
        |                |
        |   Enclosure    |      Main enclosure shell
        |                |
         \\              /
          [LL]    [LR]          Latch clips (front corners)
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
"""

from pathlib import Path

from build123d import Axis, Compound, Location, Plane

from quiver.common import PETG, load_step

_DIR = Path(__file__).parent

# Target center-of-mass positions (from Fusion reference).
# Each pair is placed on the right side first, then mirrored across YZ.
_RIGHT_HINGE_POS = (96.35, 155.83, 49.88)
_RIGHT_LATCH_POS = (157.96, -91.35, 44.73)


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

    # Right hinge — rotX(90) aligns the raw STEP to the correct orientation,
    # then translate to the reference CoM position.
    right_hinge = load_step(_DIR, "2420_hinge")
    if right_hinge:
        right_hinge.color = PETG
        right_hinge = right_hinge.rotate(Axis.X, 90)
        com = right_hinge.center()
        right_hinge.move(Location((
            _RIGHT_HINGE_POS[0] - com.X,
            _RIGHT_HINGE_POS[1] - com.Y,
            _RIGHT_HINGE_POS[2] - com.Z,
        )))
        children.append(right_hinge)

        # Left hinge — mirror the positioned right hinge across YZ plane.
        left_hinge = right_hinge.mirror(Plane.YZ)
        left_hinge.color = PETG
        children.append(left_hinge)

    # --- Latch clips (2430) ---

    # Right latch — rotZ(-90) swaps X/Y to match the reference orientation,
    # then translate to the reference CoM position.
    right_latch = load_step(_DIR, "2430_latch")
    if right_latch:
        right_latch.color = PETG
        right_latch = right_latch.rotate(Axis.Z, -90)
        com = right_latch.center()
        right_latch.move(Location((
            _RIGHT_LATCH_POS[0] - com.X,
            _RIGHT_LATCH_POS[1] - com.Y,
            _RIGHT_LATCH_POS[2] - com.Z,
        )))
        children.append(right_latch)

        # Left latch — mirror the positioned right latch across YZ plane.
        left_latch = right_latch.mirror(Plane.YZ)
        left_latch.color = PETG
        children.append(left_latch)

    if not children:
        return None
    return Compound(children=children, label="Cockpit Enclosure")
