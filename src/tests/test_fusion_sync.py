"""Check revised bodies and equipment placements against the Fusion master."""

import json
from pathlib import Path

import pytest

PROVENANCE = Path(__file__).parents[1] / "quiver/fusion-mechanical-provenance.json"
PARTS = json.loads(PROVENANCE.read_text())["parts"]
PLACEMENTS = json.loads(PROVENANCE.read_text())["equipment_placements"]


def _find(node, label):
    if node.label == label:
        return node
    for child in node.children:
        result = _find(child, label)
        if result is not None:
            return result
    return None


@pytest.mark.parametrize("record", PARTS, ids=lambda r: Path(r["path"]).stem)
def test_synced_body_world_bounds(assembly, record):
    """Detect double placement or stale offsets, especially the PCB adapter."""
    part = _find(assembly, Path(record["path"]).stem)
    assert part is not None
    body = max(part.solids(), key=lambda solid: abs(solid.volume))
    box = body.bounding_box()
    transform = record["world_transform_cm"]
    # These six source occurrences have identity rotation; assert that
    # before using the independently recorded Fusion world translations.
    assert [transform[i] for i in (0, 5, 10)] == [1.0, 1.0, 1.0]
    for actual, source in zip((box.min, box.max), record["direct_body_bounds_mm"]):
        for axis in range(3):
            expected = source[axis] + 10 * transform[4 * axis + 3]
            assert tuple(actual)[axis] == pytest.approx(expected, abs=0.02)


def _centroid(shape):
    """Volume-weighted centroid of the solids. Compound.center() weights by
    signed volume, so inverted solids in vendor STEPs would skew it."""
    solids = shape.solids()
    weights = [abs(solid.volume) for solid in solids]
    centers = [tuple(solid.center()) for solid in solids]
    return tuple(
        sum(w * c[axis] for w, c in zip(weights, centers)) / sum(weights)
        for axis in range(3)
    )


@pytest.mark.parametrize("record", PLACEMENTS, ids=lambda r: r["label"])
def test_equipment_world_placement(assembly, record):
    """Catch flipped or offset vendor parts: a 180 deg turn about the center
    of mass keeps the centroid but moves the bounds of an asymmetric part."""
    part = _find(assembly, record["label"])
    assert part is not None
    if record.get("compare") == "largest_solid":
        part = max(part.solids(), key=lambda solid: abs(solid.volume))
    box = part.bounding_box()
    for actual, expected in zip((box.min, box.max), record["world_bounds_mm"]):
        assert tuple(actual) == pytest.approx(expected, abs=0.02)
    assert _centroid(part) == pytest.approx(record["world_centroid_mm"], abs=0.02)
