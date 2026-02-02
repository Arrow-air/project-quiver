"""BOM 1000 - Airframe Structure assembly.

Composes plates, beams, landing gear, and motor arm subcategories.
"""

from build123d import Compound

from quiver.airframe_structure.plates.assembly import make_assembly as plates
from quiver.airframe_structure.beams.assembly import make_assembly as beams
from quiver.airframe_structure.landing_gear.assembly import make_assembly as landing_gear
from quiver.airframe_structure.motor_arm.assembly import make_assembly as motor_arm


def make_assembly() -> Compound | None:
    """Build the complete airframe structure from all subcategories."""
    subassemblies = [
        plates(),
        beams(),
        landing_gear(),
        motor_arm(),
    ]
    children = [s for s in subassemblies if s is not None]
    if not children:
        return None
    return Compound(children=children)
