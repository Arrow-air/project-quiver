"""Unit tests for quiver.common STEP-loading utilities."""

from pathlib import Path

from build123d import Box, Compound, export_step

from quiver.common import _flatten_solids, load_step


def test_load_step_missing_file_returns_none(tmp_path):
    (tmp_path / "steps").mkdir()
    assert load_step(tmp_path, "9999_does_not_exist") is None


def test_load_step_appends_extension(tmp_path):
    steps = tmp_path / "steps"
    steps.mkdir()
    export_step(Box(10, 10, 10), str(steps / "9001_box.step"))
    part = load_step(tmp_path, "9001_box")
    assert part is not None
    assert len(part.solids()) == 1


def test_load_step_vendor_subdirectory(tmp_path):
    vendor = tmp_path / "steps" / "vendor"
    vendor.mkdir(parents=True)
    export_step(Box(10, 10, 10), str(vendor / "9002_box.step"))
    assert load_step(tmp_path, "9002_box") is None
    assert load_step(tmp_path, "9002_box", vendor=True) is not None


def test_flatten_solids_min_volume_filter():
    big = Box(10, 10, 10)  # 1000 mm³ bounding box
    small = Box(1, 1, 1)  # 1 mm³ bounding box
    compound = Compound(children=[big, small], label="mixed")
    kept = _flatten_solids(compound, min_volume=50.0)
    assert len(kept.solids()) == 1
    assert kept.label == "mixed"


def test_flatten_solids_no_filter_keeps_all():
    compound = Compound(children=[Box(10, 10, 10), Box(1, 1, 1)])
    kept = _flatten_solids(compound, min_volume=0.0)
    assert len(kept.solids()) == 2
