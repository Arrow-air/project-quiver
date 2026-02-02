"""BOM 2100 - Attachment Interface subassembly.

Spacers and quick-release plates for the three payload mounting points.

Expected STEP files in steps/:
    2111_attach_spacer_right.step     Right attachment interface spacer
    2112_attach_plate_right.step      Right attachment interface plate
    2121_attach_spacer_left.step      Left attachment interface spacer
    2122_attach_plate_left.step       Left attachment interface plate
    2131_attach_spacer_bottom.step    Bottom attachment interface spacer
    2132_attach_plate_bottom.step     Bottom attachment interface plate
"""

from pathlib import Path

from build123d import Compound

from quiver.common import load_all_steps, load_vendor_steps

_DIR = Path(__file__).parent


def make_assembly() -> Compound | None:
    """Build the attachment interface subassembly from imported STEP files."""
    parts = list(load_all_steps(_DIR).values())
    parts += list(load_vendor_steps(_DIR).values())
    if not parts:
        return None
    return Compound(children=parts)
