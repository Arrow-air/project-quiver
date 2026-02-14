"""BOM 3300 - PCB subassembly.

Custom PCBs for the distributed board architecture.

    Main PCB (3310)  — power/data distribution hub, sits on the upper plate
    BC PCB (3320)    — front PCB, dZ offset to match reference
    Attach PCBs (3331) — one per attachment interface (right, left, rear)

        Top view:
                    (+Y)
                    |
                Main PCB (3310)
            ┌────────────────┐
    Left    │                │  Right
    Attach  │    center      │  Attach
    PCB     │                │  PCB
            └────────────────┘
                BC PCB (3320)
                    |
                Rear Attach PCB

Vendor parts in steps/vendor/:
    3310_main_pcb.step      Main PCB assembly (no transform, extract_solids >=50mm³)
    3320_bc_pcb.step        BC PCB (dZ -4.30, extract_solids >=1mm³)
    3331_attach_pcb.step    Attachment interface PCB (used 3x, rotated per position)
"""

from pathlib import Path

from build123d import Axis, Compound, Location

from quiver.common import load_step

_DIR = Path(__file__).parent

# BC PCB Z offset (raw Z=14.10, reference Z=9.81).
_BC_PCB_DZ = -4.30

# Target center-of-mass positions for the three attachment PCBs
# (from Fusion reference 3330-AttachmentPCBs.step).
_RIGHT_ATTACH_POS = (183.29, -0.52, -72.02)
_LEFT_ATTACH_POS = (-183.29, 0.52, -72.02)
_REAR_ATTACH_POS = (0.52, -0.14, -158.90)


def make_assembly() -> Compound | None:
    """Build the PCB subassembly from imported STEP files."""
    children = []

    # --- Main PCB — no transform needed ---
    # extract_solids with min_solid_volume drops tiny SMD components
    # that overwhelm the viewer (1607 → ~206 solids).

    main_pcb = load_step(
        _DIR, "3310_main_pcb", vendor=True,
        extract_solids=True, min_solid_volume=50.0,
    )
    if main_pcb:
        children.append(main_pcb)

    # --- BC PCB — Z offset only ---

    bc_pcb = load_step(
        _DIR, "3320_bc_pcb", vendor=True,
        extract_solids=True, min_solid_volume=1.0,
    )
    if bc_pcb:
        bc_pcb.move(Location((0, 0, _BC_PCB_DZ)))
        children.append(bc_pcb)

    # --- Attachment PCBs — one per interface, each rotated + translated ---

    # Right: rotY(90) + CoM translate
    right = load_step(_DIR, "3331_attach_pcb", vendor=True)
    if right:
        right = right.rotate(Axis.Y, 90)
        com = right.center()
        right.move(Location((
            _RIGHT_ATTACH_POS[0] - com.X,
            _RIGHT_ATTACH_POS[1] - com.Y,
            _RIGHT_ATTACH_POS[2] - com.Z,
        )))
        children.append(right)

    # Left: rotX(180) + rotY(90) + CoM translate
    left = load_step(_DIR, "3331_attach_pcb", vendor=True)
    if left:
        left = left.rotate(Axis.X, 180)
        left = left.rotate(Axis.Y, 90)
        com = left.center()
        left.move(Location((
            _LEFT_ATTACH_POS[0] - com.X,
            _LEFT_ATTACH_POS[1] - com.Y,
            _LEFT_ATTACH_POS[2] - com.Z,
        )))
        children.append(left)

    # Rear: rotX(180) + rotZ(270) + CoM translate
    rear = load_step(_DIR, "3331_attach_pcb", vendor=True)
    if rear:
        rear = rear.rotate(Axis.X, 180)
        rear = rear.rotate(Axis.Z, 270)
        com = rear.center()
        rear.move(Location((
            _REAR_ATTACH_POS[0] - com.X,
            _REAR_ATTACH_POS[1] - com.Y,
            _REAR_ATTACH_POS[2] - com.Z,
        )))
        children.append(rear)

    if not children:
        return None
    return Compound(children=children, label="PCB")
