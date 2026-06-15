"""Smoke tests for the full Quiver drone assembly.

These guard against the failure mode where a missing or broken STEP file
silently produces a partial assembly (subassembly builders return None for
absent parts), and against placement regressions when part transforms or
STEP files change.

Baselines were measured against the PT3 model (build123d 0.10.0). If a
deliberate design change shifts them, update the constants here in the
same commit and note why.
"""

import re
from pathlib import Path

import pytest

QUIVER_DIR = Path(__file__).parent.parent / "quiver"

# Expected subassembly labels, by BOM category (see src/quiver/README.md).
EXPECTED_TREE = {
    "Airframe Structure": {"Plates", "Beams", "Landing Gear", "Motor Arm"},
    "Supporting Structure": {
        "Attachment Interface",
        "Battery Slider",
        "Equipment Mount",
        "Cockpit Enclosure",
    },
    "Equipment": {"Propulsion", "Peripheral", "PCB", "Battery"},
    "Harness": {"4010_busbar_negative", "4010_busbar_positive"},
}

# Full-assembly bounding box (mm), dominated by the propeller sweep and
# landing gear. Tolerance is generous enough for tessellation noise but
# tight enough to catch a mispositioned part.
BBOX_MIN = (-673.6, -664.5, -547.9)
BBOX_MAX = (673.6, 673.6, 193.7)
BBOX_TOL = 1.0

TOTAL_SOLIDS = 1242


def test_top_level_structure(assembly):
    assert assembly.label == "Quiver Drone"
    labels = [c.label for c in assembly.children]
    assert labels == list(EXPECTED_TREE)


def test_subassemblies_present(assembly):
    for category in assembly.children:
        expected = EXPECTED_TREE[category.label]
        actual = {c.label for c in category.children}
        missing = expected - actual
        assert not missing, f"{category.label} is missing subassemblies: {missing}"


def test_bounding_box(assembly):
    bb = assembly.bounding_box()
    actual_min = (bb.min.X, bb.min.Y, bb.min.Z)
    actual_max = (bb.max.X, bb.max.Y, bb.max.Z)
    for axis, (a, e) in enumerate(zip(actual_min, BBOX_MIN)):
        assert a == pytest.approx(e, abs=BBOX_TOL), f"bbox min axis {axis}: {a} != {e}"
    for axis, (a, e) in enumerate(zip(actual_max, BBOX_MAX)):
        assert a == pytest.approx(e, abs=BBOX_TOL), f"bbox max axis {axis}: {a} != {e}"


def test_total_solid_count(assembly):
    assert len(assembly.solids()) == TOTAL_SOLIDS


def _step_references(module_dir: Path) -> set[str]:
    """BOM-numbered STEP names referenced by string literal in a module."""
    refs = set()
    for py in module_dir.glob("*.py"):
        refs |= set(re.findall(r'"(\d{4}_\w+)"', py.read_text()))
    return refs


def _step_files(module_dir: Path) -> set[str]:
    steps = module_dir / "steps"
    return {p.stem for p in steps.rglob("*.step")}


@pytest.mark.parametrize(
    "module_dir",
    sorted(d.parent for d in QUIVER_DIR.rglob("steps") if d.is_dir()),
    ids=lambda d: str(d.relative_to(QUIVER_DIR)),
)
def test_step_files_match_code(module_dir):
    """Every STEP file on disk is referenced in code, and vice versa."""
    refs = _step_references(module_dir)
    files = _step_files(module_dir)
    missing = refs - files
    orphans = files - refs
    assert not missing, f"referenced in code but no STEP file: {sorted(missing)}"
    assert not orphans, f"STEP file never referenced in code: {sorted(orphans)}"
