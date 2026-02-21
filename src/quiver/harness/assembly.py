"""BOM 4000 - Harness subassembly.

Busbars connecting the main PCB and battery PCB. The positive and
negative busbars are mirror images of each other across the YZ plane.
Both need a Z offset to sit on the BC PCB terminal lugs.

Custom parts in steps/:
    4010_busbar_negative.step   Negative busbar (dZ +34.01)
    4010_busbar_positive.step   Positive busbar (dZ +34.01)
    4020_dev_kit.step           Wire routing and dev kit model
"""

import sys
from pathlib import Path
from build123d import Compound, Location, import_step, Shape, Kind
from quiver.common import load_step

# Resolve absolute path
_DIR = Path(__file__).resolve().parent

# Z offsets for component placement
_BUSBAR_DZ = 0    # Set to 0 for debugging; standard is 34.01
_DEV_KIT_DZ = 0   # Dedicated offset for the Dev Kit and cables

def load_all_geometry(path_dir: Path, name: str) -> Compound | None:
    """
    Alternative loader that captures non-solid geometry (like surfaces/wires).
    Useful for heavy files where cables might be exported as shells.
    """
    filepath = path_dir / "steps" / f"{name}.step"
    if not filepath.exists():
        return None
    
    try:
        # Import the raw geometry without filtering for solids only
        raw_shape = import_step(str(filepath))
        
        # If it's already a compound, return it; otherwise wrap it
        if isinstance(raw_shape, Compound):
            return raw_shape
        return Compound(children=[raw_shape])
    except Exception as e:
        print(f"Error loading {name} with raw importer: {e}")
        return None

def make_assembly() -> Compound | None:
    """Build the harness subassembly from imported STEP files."""
    children = []

    # 1. Load Busbars (Standard loading works fine for these)
    for name in ["4010_busbar_negative", "4010_busbar_positive"]:
        part = load_step(_DIR, name)
        if part:
            part.move(Location((0, 0, _BUSBAR_DZ)))
            children.append(part)

    # 2. Load Dev Kit and Cables
    # We bypass load_step and use our raw loader to catch Surfaces/Shells (cables)
    print(f"Attempting RAW import of 4020_dev_kit to capture all surface geometry...")
    dev_kit = load_all_geometry(_DIR, "4020_dev_kit")
    
    if dev_kit:
        print("✅ Dev Kit and raw geometry (including surfaces) loaded.")
        dev_kit.move(Location((0, 0, _DEV_KIT_DZ)))
        children.append(dev_kit)
    else:
        print("❌ Failed to load Dev Kit.")

    if not children:
        return None
        
    return Compound(children=children, label="Harness")