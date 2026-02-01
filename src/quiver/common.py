"""Shared utilities for Quiver CAD assembly."""

from pathlib import Path

from build123d import Color, Compound, import_step

# Material colors for visualization
ALUMINUM = Color(0.75, 0.75, 0.76)
CARBON_FIBER = Color(0.15, 0.15, 0.15)
PCB_GREEN = Color(0.0, 0.5, 0.2)
PETG = Color(0.2, 0.2, 0.2)

STEPS_DIR = "steps"
VENDOR_DIR = "vendor"


def _load_from(directory: Path) -> dict[str, Compound]:
    """Load all STEP files from a directory."""
    if not directory.exists():
        return {}
    parts = {}
    for step_file in sorted(directory.glob("*.step")):
        parts[step_file.stem] = import_step(str(step_file))
    return parts


def load_step(subassembly_dir: Path, filename: str, vendor: bool = False) -> Compound | None:
    """Import a STEP file from a subassembly's steps/ directory.

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
    return import_step(str(step_path))


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
