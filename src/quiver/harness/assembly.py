"""BOM 4000 - Harness subassembly.

Busbars connecting the main PCB and battery PCB. The positive and
negative busbars are mirror images of each other across the YZ plane.
Both need a Z offset to sit on the BC PCB terminal lugs.

Custom parts in steps/:
    4010_busbar_negative.step   Negative busbar (dZ +34.01)
    4010_busbar_positive.step   Positive busbar (dZ +34.01)
"""

from pathlib import Path

from build123d import Compound, Location

from quiver.common import load_step

_DIR = Path(__file__).parent

# Z offset to place busbar bottoms on the BC PCB terminal lugs.
# Raw busbar bottom Z=-16.48, lug top Z=17.53 (with BC PCB dZ=-4.30).
_BUSBAR_DZ = 34.01


def make_assembly() -> Compound | None:
    """Build the harness subassembly from imported STEP files."""
    children = []

    for name in ["4010_busbar_negative", "4010_busbar_positive"]:
        part = load_step(_DIR, name)
        if part:
            part.move(Location((0, 0, _BUSBAR_DZ)))
            children.append(part)

    if not children:
        return None
    return Compound(children=children, label="Harness")
