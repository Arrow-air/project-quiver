"""BOM 1100 - Plates subassembly.

Three-layer aluminum plate sandwich forming the core airframe.

Expected STEP files in steps/:
    1111_upper_plate.step       2mm aluminum upper plate
    1112_middle_plate.step      2mm aluminum middle plate
    1113_lower_plate.step       4mm aluminum lower plate
"""

from pathlib import Path

from build123d import Compound

from quiver.common import load_all_steps, load_vendor_steps

_DIR = Path(__file__).parent


def make_assembly() -> Compound | None:
    """Build the plates subassembly from imported STEP files."""
    parts = list(load_all_steps(_DIR).values())
    parts += list(load_vendor_steps(_DIR).values())
    if not parts:
        return None
    return Compound(children=parts)
