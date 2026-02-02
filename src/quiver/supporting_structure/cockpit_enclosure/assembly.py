"""BOM 2400 - Cockpit Enclosure subassembly.

Main weatherproof cockpit enclosure with caps, anchors, and clips.

Expected STEP files in steps/:
    2411_main_enclosure.step        Main cockpit enclosure
    2412_enclosure_top_cap.step     Enclosure top cap
    2421_enclosure_anchor.step      Enclosure anchor x4
    2431_enclosure_cap_clip.step    Enclosure cap clip x4
"""

from pathlib import Path

from build123d import Compound

from quiver.common import load_all_steps, load_vendor_steps

_DIR = Path(__file__).parent


def make_assembly() -> Compound | None:
    """Build the cockpit enclosure subassembly from imported STEP files."""
    parts = list(load_all_steps(_DIR).values())
    parts += list(load_vendor_steps(_DIR).values())
    if not parts:
        return None
    return Compound(children=parts)
