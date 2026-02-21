"""BOM 4000 - Harness subassembly.

Busbars connecting the main PCB and battery PCB. The positive and
negative busbars are mirror images of each other across the YZ plane.
Both need a Z offset to sit on the BC PCB terminal lugs.

Custom parts in steps/:
    4010_busbar_negative.step   Negative busbar (dZ +34.01)
    4010_busbar_positive.step   Positive busbar (dZ +34.01)
    4020_dev_kit.step           Wire routing and dev kit model
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

    # 1. Load Busbars (Standard loading)
    for name in ["4010_busbar_negative", "4010_busbar_positive"]:
        part = load_step(_DIR, name)
        if part:
            part.move(Location((0, 0, _BUSBAR_DZ)))
            children.append(part)

    # 2. Load Dev Kit (Enhanced loading for complex electrical geometry)
    # We use extract_solids=True to prevent 'face ignored' errors and 
    # min_solid_volume=0 to ensure tiny connectors/pins are not deleted.
    dev_kit = load_step(_DIR, "4020_dev_kit", extract_solids=True, min_solid_volume=0)
    if dev_kit:
        # Note: If the dev kit appears too high or buried, adjust this offset.
        # It currently uses the same offset as the busbars.
        dev_kit.move(Location((0, 0, _BUSBAR_DZ)))
        children.append(dev_kit)

    if not children:
        return None
        
    return Compound(children=children, label="Harness")