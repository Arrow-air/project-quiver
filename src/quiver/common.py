"""Shared utilities for Quiver CAD assembly."""

from pathlib import Path

from build123d import Color, Compound, import_step
from OCP.BRepBuilderAPI import BRepBuilderAPI_Copy

# Material colors for visualization
ALUMINUM = Color(0.75, 0.75, 0.76)
CARBON_FIBER = Color(0.10, 0.10, 0.12)
PCB_GREEN = Color(0.0, 0.5, 0.2)
PETG = Color(0.30, 0.32, 0.38)
FOAM = Color(0.85, 0.55, 0.2)  # orange EPP foam

STEPS_DIR = "steps"
VENDOR_DIR = "vendor"


def _load_from(directory: Path) -> dict[str, Compound]:
    """Load all STEP files from a directory."""
    if not directory.exists():
        return {}
    parts = {}
    for step_file in sorted(directory.glob("*.step")):
        parts[step_file.stem] = _flatten(import_step(str(step_file)))
    return parts


def _flatten(compound: Compound) -> Compound:
    """Deep-copy a Compound to bake internal placement transforms into geometry.

    STEP files can carry nested placement transforms on sub-parts. These
    interact badly with subsequent rotate/move calls in the OCP CAD Viewer
    (the viewer may not correctly compose parent and child transforms).
    Deep-copying with BRepBuilderAPI_Copy collapses all transforms into the
    vertex data so the geometry is self-contained.
    """
    copier = BRepBuilderAPI_Copy(compound.wrapped, True, True)
    copier.Perform(compound.wrapped)
    flat = Compound(copier.Shape())
    flat.label = compound.label
    return flat


def load_step(subassembly_dir: Path, filename: str, vendor: bool = False) -> Compound | None:
    """Import a STEP file from a subassembly's steps/ directory.

    The imported geometry is flattened (internal placement transforms are
    baked into vertices) so that subsequent rotate/move calls render
    correctly in the OCP CAD Viewer.

    Args:
        subassembly_dir: Path to the subassembly module directory.
        filename: Name of the STEP file (with or without .step extension).
        vendor: If True, load from steps/vendor/ instead of steps/.

    Returns:
        The imported Compound, or None if the file doesn't exist yet.
    """
    if not filename.endswith(".step"):
        filename = f"{filename}.step"
    steps_path = subassembly_dir / STEPS_DIR
    if vendor:
        steps_path = steps_path / VENDOR_DIR
    step_path = steps_path / filename
    if not step_path.exists():
        return None
    return _flatten(import_step(str(step_path)))


def load_all_steps(subassembly_dir: Path) -> dict[str, Compound]:
    """Load custom STEP files from a subassembly's steps/ directory.

    Returns:
        Dict mapping stem name to imported Compound. Empty if no files found.
    """
    return _load_from(subassembly_dir / STEPS_DIR)


def load_vendor_steps(subassembly_dir: Path) -> dict[str, Compound]:
    """Load vendor/supplier STEP files from steps/vendor/.

    Returns:
        Dict mapping stem name to imported Compound. Empty if no files found.
    """
    return _load_from(subassembly_dir / STEPS_DIR / VENDOR_DIR)
