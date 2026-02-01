"""Attachment interfaces - Quick-release payload plates (Part 31).

Three modular quick-release mounting points for payloads.

Expected STEP files in steps/:
    attach_plate_bottom.step    Bottom attachment interface plate
    attach_plate_left.step      Left attachment interface plate
    attach_plate_right.step     Right attachment interface plate
"""

from pathlib import Path

from build123d import Compound

from quiver.common import load_all_steps, load_vendor_steps

_DIR = Path(__file__).parent


def make_assembly() -> Compound | None:
    """Build the attachment interfaces from imported STEP files."""
    parts = list(load_all_steps(_DIR).values())
    parts += list(load_vendor_steps(_DIR).values())
    if not parts:
        return None
    return Compound(children=parts)
