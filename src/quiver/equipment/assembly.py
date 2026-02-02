"""BOM 3000 - Equipment assembly.

Composes propulsion, peripheral, PCB, and battery subcategories.
"""

from build123d import Compound

from quiver.equipment.propulsion.assembly import make_assembly as propulsion
from quiver.equipment.peripheral.assembly import make_assembly as peripheral
from quiver.equipment.pcb.assembly import make_assembly as pcb
from quiver.equipment.battery.assembly import make_assembly as battery


def make_assembly() -> Compound | None:
    """Build the complete equipment assembly from all subcategories."""
    subassemblies = [
        propulsion(),
        peripheral(),
        pcb(),
        battery(),
    ]
    children = [s for s in subassemblies if s is not None]
    if not children:
        return None
    return Compound(children=children)
