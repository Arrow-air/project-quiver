"""BOM 4000 - Harness subassembly.

Busbars connecting the main PCB and battery PCB, standing on the BC PCB
terminal lugs. The positive and negative busbars are mirror images of
each other across the YZ plane.

Custom parts in steps/:
    4010_busbar_negative.step   Negative busbar, 40.3mm tall (dZ +26.2)
    4010_busbar_positive.step   Positive busbar, 40.3mm tall (dZ +26.2)

The STEPs are the Fusion v148 3322/3323 busbars (the same models as the
Manufacturing Guide), in their component frames.
"""

from pathlib import Path

from build123d import Compound

from quiver.common import load_step, place

_DIR = Path(__file__).parent

# Z offset onto the BC PCB terminal lugs (Fusion v148 occurrence transform)
_BUSBAR_DZ = 26.2


def make_assembly() -> Compound | None:
    """Build the harness subassembly from imported STEP files."""
    children = []

    for name in ["4010_busbar_negative", "4010_busbar_positive"]:
        part = load_step(_DIR, name)
        if part:
            children.append(place(part, (0, 0, _BUSBAR_DZ)))

    if not children:
        return None
    return Compound(children=children, label="Harness")
