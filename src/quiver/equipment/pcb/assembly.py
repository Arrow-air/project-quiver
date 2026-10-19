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
    3310_main_pcb.step      Main PCB, Dev-Kit V1.2 (dZ -7.40, extract_solids >=50mm³)
    3320_bc_pcb.step        BC PCB V1.3 with heatsink and connectors (dZ -23.497, extract_solids >=1mm³)
    3331_attach_pcb.step    Attachment interface PCB (used 3x, rotated per position)

The 3310 and 3320 board bodies match the KiCad sources in src/pcb exactly
(Dev-Kit V1.2 main board, V1.3 battery board).

Poses are full rigid transforms (see quiver.common.place) from the Fusion
360 v148 master.
"""

from pathlib import Path

from build123d import Compound

from quiver.common import load_step, place

_DIR = Path(__file__).parent

# Main PCB Z offset: the board rests on the 2311 adapter (Fusion v148).
_MAIN_PCB_DZ = -7.40

# BC PCB Z offset: the board sits in the 2312 mount (Fusion v148).
_BC_PCB_DZ = -23.497

# Attachment PCB poses: STEP origin (mm), intrinsic XYZ rotation (deg)
_RIGHT_ATTACH_POSE = ((182.94, 133.0023, 38.1179), (0, 90, 0))
_LEFT_ATTACH_POSE = ((-182.94, -133.0023, 38.1179), (180, -90, 0))
_REAR_ATTACH_POSE = ((-133.0, 110.0, -158.55), (180, 0, 90))


def make_assembly() -> Compound | None:
    """Build the PCB subassembly from imported STEP files."""
    children = []

    # --- Main PCB — Z offset only ---
    # extract_solids with min_solid_volume drops tiny SMD components
    # that overwhelm the viewer (1607 → ~206 solids).

    main_pcb = load_step(
        _DIR, "3310_main_pcb", vendor=True,
        extract_solids=True, min_solid_volume=50.0,
    )
    if main_pcb:
        place(main_pcb, (0, 0, _MAIN_PCB_DZ))
        children.append(main_pcb)

    # --- BC PCB — Z offset only ---

    bc_pcb = load_step(
        _DIR, "3320_bc_pcb", vendor=True,
        extract_solids=True, min_solid_volume=1.0,
    )
    if bc_pcb:
        place(bc_pcb, (0, 0, _BC_PCB_DZ))
        children.append(bc_pcb)

    # --- Attachment PCBs — one per interface ---

    for pose in (_RIGHT_ATTACH_POSE, _LEFT_ATTACH_POSE, _REAR_ATTACH_POSE):
        attach = load_step(_DIR, "3331_attach_pcb", vendor=True)
        if attach:
            children.append(place(attach, *pose))

    if not children:
        return None
    return Compound(children=children, label="PCB")
