"""Arms subassembly - Foldable motor arms (Parts 9-10).

Four foldable carbon-fiber motor arms with aluminum connectors.

Expected STEP files in steps/:
    arm_connector.step    Part 9  - Aluminum arm connector (30mm)

Vendor parts in steps/vendor/:
    arm_tube.step         Part 10 - Carbon-fiber tube (360mm, 30x2mm)
    motor.step            Hobbywing XRotor X6 Plus motor
    propeller.step        Propeller

Note: The drone uses 4 of each part. The assembly mirrors and rotates
these to all four positions. Export one of each from Fusion.
"""

from pathlib import Path

from build123d import Compound

from quiver.common import load_all_steps, load_vendor_steps

_DIR = Path(__file__).parent


def make_assembly() -> Compound | None:
    """Build the motor arm subassembly from imported STEP files."""
    parts = list(load_all_steps(_DIR).values())
    parts += list(load_vendor_steps(_DIR).values())
    if not parts:
        return None
    return Compound(children=parts)
