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
_BUSBAR_DZ = 34.01

def make_assembly() -> Compound | None:
    """Build the harness subassembly from imported STEP files."""
    children = []

    # List of components to load
    # Note: 4020_dev_kit often requires extract_solids=True if it contains 
    # complex nested hierarchies from electrical CAD.
    components = [
        {"name": "4010_busbar_negative", "extract": False},
        {"name": "4010_busbar_positive", "extract": False},
        {"name": "4020_dev_kit", "extract": True}, 
    ]

    for comp in components:
        name = comp["name"]
        # Attempt to load the step file
        part = load_step(_DIR, name, extract_solids=comp["extract"], min_solid_volume=0)
        
        if part:
            print(f"✅ [Harness] Successfully loaded: {name}")
            # Apply the vertical offset to align with PCB lugs
            part.move(Location((0, 0, _BUSBAR_DZ)))
            children.append(part)
        else:
            # This will print to your terminal if the file is missing or named incorrectly
            print(f"❌ [Harness] ERROR: Could not find '{name}.step' in {_DIR}/steps/")

    if not children:
        return None
        
    return Compound(children=children, label="Harness")