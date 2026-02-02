"""BOM 1400 - Motor Arm subassembly.

Foldable motor arm structure (connectors and tubes). The drone uses 4
of each part, mirrored and rotated to all four positions.

Expected STEP files in steps/:
    1411_arm_connector.step     Aluminum arm connector (30mm)

Vendor parts in steps/vendor/:
    1412_arm_tube.step          Carbon-fiber tube (360mm, 30x2mm)
"""

from pathlib import Path

from build123d import Compound

from quiver.common import load_all_steps, load_vendor_steps

_DIR = Path(__file__).parent


def make_assembly() -> Compound | None:
    """Build the motor arm subassembly from imported STEP files."""
    parts = list(load_all_steps(_DIR).values())
    parts += list(load_vendor_steps(_DIR).values())
    if not parts:
        return None
    return Compound(children=parts)
