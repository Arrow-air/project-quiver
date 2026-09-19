"""Shared fixtures for the Quiver CAD test suite.

Building the full assembly imports ~170 MB of STEP geometry and takes about
a minute, so it is done once per session and shared by all tests.
"""

import pytest

from quiver.assembly import make_assembly


@pytest.fixture(scope="session", params=["here4", "holybro-f9p"])
def assembly(request):
    asm = make_assembly(primary_gps=request.param)
    assert asm is not None, "make_assembly() returned None — no STEP files loaded"
    return asm
