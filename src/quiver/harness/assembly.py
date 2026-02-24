"""BOM 4100 - Harness subassembly.

Contains individual wire routing, cables, and harness components.
Files are loaded dynamically from the steps/ directory to handle
multi-part CAD exports efficiently.
"""

from pathlib import Path
from build123d import Compound, Location, import_step

# Resolve absolute path to ensure STEP files are found reliably
_DIR = Path(__file__).resolve().parent

# Global Z offset for the harness assembly.
# Set to 0 for debugging/origin alignment. 
# You can change this back to 34.01 if they need to sit on the BC PCB lugs.
_HARNESS_DZ = 0

def load_wire_geometry(filepath: Path) -> Compound | None:
    """
    Alternative loader that forcefully flattens non-solid geometry (like surfaces/wires).
    Ensures cables exported as surface shells are rendered by OCP.
    """
    if not filepath.exists():
        return None
        
    try:
        # Import the raw geometry
        raw_shape = import_step(str(filepath))
        
        # FLAT-PACK DECOMPOSITION:
        # Extract all faces to ensure wires/surfaces are drawn even if they aren't solids.
        return Compound(children=raw_shape.faces())
    except Exception as e:
        print(f"Error loading {filepath.name}: {e}")
        return None

def make_assembly() -> Compound | None:
    """Build the harness subassembly from imported STEP files."""
    children = []
    steps_dir = _DIR / "steps"

    print("\n" + "="*40)
    print("LOADING MULTI-PART HARNESS ASSEMBLY")
    print("="*40)

    # 1. Dynamically find all STEP files (handles uppercase .STEP from Fusion)
    all_step_files = list(steps_dir.glob("*.STEP")) + list(steps_dir.glob("*.step"))
    
    # Filter for files containing "HAR0" to match your exact new naming convention 
    # (e.g., 4101_HAR001.STEP) and sort them sequentially.
    harness_files = sorted(set(f for f in all_step_files if "HAR0" in f.name.upper()))

    if not harness_files:
        print(f"❌ ERROR: No harness files found in {steps_dir}")
        print("="*40 + "\n")
        return None

    # 2. Loop through and load each file
    for filepath in harness_files:
        part = load_wire_geometry(filepath)
        
        if part:
            print(f"✅ Loaded: {filepath.name}")
            part.move(Location((0, 0, _HARNESS_DZ)))
            children.append(part)
        else:
            print(f"❌ Failed: {filepath.name}")

    print(f"\n✅ Successfully processed {len(children)}/{len(harness_files)} harness components.")
    print("="*40 + "\n")

    if not children:
        return None
        
    return Compound(children=children, label="Harness")