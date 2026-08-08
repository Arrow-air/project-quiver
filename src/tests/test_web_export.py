"""Tests for the docs-site GLB exporter."""

import importlib
import json

import pytest

from quiver import web_export


def test_all_registered_subassemblies_importable():
    """Every manifest entry must point at a real make_assembly()."""
    for _, _, label, _, module_path in web_export._SUBASSEMBLIES:
        module = importlib.import_module(module_path)
        assert callable(getattr(module, "make_assembly", None)), (
            f"{label}: {module_path} has no make_assembly()"
        )


def test_export_writes_glb_and_manifest(tmp_path, monkeypatch):
    """End-to-end export of one small subassembly (no node pipeline)."""
    plates = [s for s in web_export._SUBASSEMBLIES if s[2] == "Plates"]
    monkeypatch.setattr(web_export, "_SUBASSEMBLIES", plates)

    manifest = web_export.export_models(tmp_path, optimize=False)

    glb = tmp_path / "1100_plates.glb"
    assert glb.exists() and glb.stat().st_size > 1000
    assert glb.read_bytes()[:4] == b"glTF"
    on_disk = json.loads((tmp_path / "manifest.json").read_text())
    assert on_disk == manifest
    assert on_disk["categories"][0]["models"][0]["file"] == "1100_plates.glb"
    assert on_disk["draco"] is False


def test_committed_manifest_matches_files():
    """The checked-in models directory is internally consistent."""
    models_dir = web_export._DEFAULT_OUTPUT
    if not models_dir.exists():
        pytest.skip("no committed models directory")
    manifest = json.loads((models_dir / "manifest.json").read_text())
    for cat in manifest["categories"]:
        for model in cat["models"]:
            assert (models_dir / model["file"]).exists(), model["file"]
