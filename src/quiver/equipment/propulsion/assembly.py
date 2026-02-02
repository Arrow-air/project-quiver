"""BOM 3100 - Propulsion System subassembly.

Motors and propellers. The drone uses 4 of each, one per arm.

Vendor parts in steps/vendor/:
    3111_motor.step         Hobbywing XRotor X6 Plus motor
    3112_propeller.step     Propeller
"""

from pathlib import Path

from build123d import Compound

from quiver.common import load_all_steps, load_vendor_steps

_DIR = Path(__file__).parent


def make_assembly() -> Compound | None:
    """Build the propulsion subassembly from imported STEP files."""
    parts = list(load_all_steps(_DIR).values())
    parts += list(load_vendor_steps(_DIR).values())
    if not parts:
        return None
    return Compound(children=parts)
