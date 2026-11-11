"""Every placed part matches its recorded world pose.

The records in quiver/part-poses.json were frozen from the Fusion 360 v148
master when it was retired; the build123d model is now the source of truth.
A part turned 180 deg about its own center keeps its centroid and often its
bounds, but its vertices move, so each record also holds reference vertices.

After moving a part on purpose, re-record it with
``python -m quiver.placement record <key or label>``.
"""

import json
from collections import Counter
from pathlib import Path

import numpy as np
import pytest

from quiver.placement import centroid, part_instances, records_for

POSES = json.loads((Path(__file__).parents[1] / "quiver/part-poses.json").read_text())["parts"]

CENTROID_TOL = 0.02   # mm
BOUNDS_TOL = 0.05     # mm, bounding boxes carry a little tolerance slack
VERTEX_TOL = 0.01     # mm


@pytest.fixture(scope="module")
def instances(assembly):
    """Part instances by label, each with its centroid and vertex array."""
    out = {}
    for label, parts in part_instances(assembly).items():
        out[label] = [
            (part, np.array(centroid(part)), np.array([tuple(v) for v in part.vertices()]))
            for part in parts
        ]
    return out


def test_every_instance_is_recorded(assembly, instances):
    built = Counter({label: len(parts) for label, parts in instances.items()})
    recorded = Counter(record["label"] for record in records_for(POSES, assembly))
    assert built == recorded


@pytest.mark.parametrize("record", POSES, ids=lambda r: r["key"])
def test_part_pose(assembly, instances, record):
    if not records_for([record], assembly):
        pytest.skip(f"record applies to the {record['primary_gps']} build")
    candidates = instances.get(record["label"])
    assert candidates, f"{record['label']} is not in the assembly"
    expected = np.array(record["centroid_mm"])
    part, actual, vertices = min(candidates, key=lambda c: np.linalg.norm(c[1] - expected))

    assert tuple(actual) == pytest.approx(tuple(expected), abs=CENTROID_TOL)
    box = part.bounding_box()
    for got, want in zip((box.min, box.max), record["bounds_mm"]):
        assert tuple(got) == pytest.approx(tuple(want), abs=BOUNDS_TOL)
    for probe in record["probes_mm"]:
        gap = np.linalg.norm(vertices - np.array(probe), axis=1).min()
        assert gap < VERTEX_TOL, f"no vertex within {VERTEX_TOL} mm of {probe} (nearest {gap:.3f} mm)"
