"""BOM 3200 - Peripheral subassembly.

Sensors, telemetry, GNSS receiver, and other peripheral equipment.

Vendor parts in steps/vendor/:
    (add vendor peripheral models here)
"""

from pathlib import Path

from build123d import Compound

from quiver.common import load_all_steps, load_vendor_steps

_DIR = Path(__file__).parent


def make_assembly() -> Compound | None:
    """Build the peripheral subassembly from imported STEP files."""
    parts = list(load_all_steps(_DIR).values())
    parts += list(load_vendor_steps(_DIR).values())
    if not parts:
        return None
    return Compound(children=parts)
