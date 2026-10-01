"""Check the revised printable bodies against Fusion's measured world bounds."""

import json
from pathlib import Path

import pytest

PROVENANCE = Path(__file__).parents[1] / "quiver/fusion-mechanical-provenance.json"
PARTS = json.loads(PROVENANCE.read_text())["parts"]


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
