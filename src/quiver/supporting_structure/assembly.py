"""BOM 2000 - Supporting Structure assembly.

Composes attachment interface, battery slider, equipment mount,
and cockpit enclosure subcategories.
"""

from build123d import Compound

from quiver.supporting_structure.attachment_interface.assembly import (
    make_assembly as attachment_interface,
)
from quiver.supporting_structure.battery_slider.assembly import (
    make_assembly as battery_slider,
)
from quiver.supporting_structure.equipment_mount.assembly import (
    make_assembly as equipment_mount,
)
from quiver.supporting_structure.cockpit_enclosure.assembly import (
    make_assembly as cockpit_enclosure,
)


def make_assembly() -> Compound | None:
    """Build the complete supporting structure from all subcategories."""
    subassemblies = [
        attachment_interface(),
        battery_slider(),
        equipment_mount(),
        cockpit_enclosure(),
    ]
    children = [s for s in subassemblies if s is not None]
    if not children:
        return None
    return Compound(children=children)
