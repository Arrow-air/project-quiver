"""BOM 3300 - PCB subassembly.

Custom PCB 3D models for the distributed board architecture.

Expected STEP files in steps/:
    3311_battery_pcb.step       Battery PCB - power switching and protection
    3321_main_pcb.step          Main PCB - power/data distribution hub
    3331_fc_pcb.step            Flight Controller PCB - Pix32 V6 adapter board
    3341_attach_pcb.step        Attachment Interface PCB x3

Vendor parts in steps/vendor/:
    (add vendor component models here, e.g. Pix32 V6 enclosure)
"""

from pathlib import Path

from build123d import Compound

from quiver.common import load_all_steps, load_vendor_steps

_DIR = Path(__file__).parent


def make_assembly() -> Compound | None:
    """Build the PCB subassembly from imported STEP files."""
    parts = list(load_all_steps(_DIR).values())
    parts += list(load_vendor_steps(_DIR).values())
    if not parts:
        return None
    return Compound(children=parts)
