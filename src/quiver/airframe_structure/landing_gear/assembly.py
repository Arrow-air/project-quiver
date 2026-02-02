"""BOM 1300 - Landing Gear subassembly.

Carbon-fiber tube landing gear with aluminum adapters and 3D-printed joints.

Expected STEP files in steps/:
    1311_main_adapter.step      Aluminum adapter (30mm) x4
    1312_tube_joint.step        3D-printed PETG-CF joint x4

Vendor parts in steps/vendor/:
    1341_vertical_tube.step     Carbon-fiber tube (400mm, 30x2mm) x4
    1342_horizontal_tube.step   Carbon-fiber tube (500mm, 30x2mm) x2
    1351_enclosure_hinge.step   Zinc die-cast hinge x2
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
