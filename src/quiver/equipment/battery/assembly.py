"""BOM 3400 - Battery subassembly.

Tattu 30Ah battery pack, positioned at center-bottom of the airframe.
No transform needed — exported with correct position baked in.

Vendor parts in steps/vendor/:
    3410_battery.step       Tattu 4.0 30Ah battery pack (no transform)
"""

from pathlib import Path

from build123d import Compound

from quiver.common import load_step

_DIR = Path(__file__).parent


def make_assembly() -> Compound | None:
    """Build the battery subassembly from imported STEP files."""
    battery = load_step(_DIR, "3410_battery", vendor=True)
    if not battery:
        return None
    return Compound(children=[battery], label="Battery")
