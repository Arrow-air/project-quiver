"""Tests for community attachment design packages.

Every package under quiver/attachments/designs/ must expose a
make_assembly() that builds without the full drone, so attachment
authors get CI feedback on their designs.
"""

import importlib
import pkgutil

import pytest

import quiver.attachments.designs as designs_pkg

DESIGN_PACKAGES = [
    m.name for m in pkgutil.iter_modules(designs_pkg.__path__) if m.ispkg
]


def test_example_design_exists():
    assert "example_plate" in DESIGN_PACKAGES


@pytest.mark.parametrize("name", DESIGN_PACKAGES)
def test_design_builds(name):
    module = importlib.import_module(f"quiver.attachments.designs.{name}.assembly")
    design = module.make_assembly()
    # None is allowed only for designs that import STEP files; the file
    # check in quiver.common warns in that case. Parametric designs
    # must return a Compound.
    if design is not None:
        assert design.label
        assert len(design.solids()) > 0
