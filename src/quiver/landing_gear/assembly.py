"""Landing gear subassembly (Parts 11-15).

Carbon-fiber tube landing gear with aluminum adapters and 3D-printed joints.

Expected STEP files in steps/:
    main_adapter.step        Part 13 - Aluminum adapter (30mm) x4
    tube_joint.step          Part 15 - 3D-printed PETG-CF joint x4

Vendor parts in steps/vendor/:
    vertical_tube.step       Part 11 - Carbon-fiber tube (400mm, 30x2mm) x4
    horizontal_tube.step     Part 12 - Carbon-fiber tube (500mm, 30x2mm) x2
    enclosure_hinge.step     Part 14 - Zinc die-cast hinge x2
"""

from pathlib import Path

from build123d import Compound

from quiver.common import load_all_steps, load_vendor_steps

_DIR = Path(__file__).parent


def make_assembly() -> Compound | None:
    """Build the landing gear subassembly from imported STEP files."""
    parts = list(load_all_steps(_DIR).values())
    parts += list(load_vendor_steps(_DIR).values())
    if not parts:
        return None
    return Compound(children=parts)
