"""Example payload attachment — a blank plate on the bottom interface.

This is a template for community attachment designs. Copy this package,
rename it, and replace the placeholder plate with your payload. The
drone offers three quick-release interfaces (bottom, left, right); see
quiver/supporting_structure/attachment_interface/assembly.py (BOM 2100)
for their positions and the interface plate geometry, and
task-grant-bounty/equipment/attachment/ for payload requirements
(mass and envelope limits, connector pinout).

A design package must provide make_assembly() returning the payload as
a Compound positioned in drone coordinates (origin at the airframe
center, +Z up, +Y forward), or None if its STEP files are missing.
Parametric geometry like this template always builds.

View your design in place on the drone:

    python -m quiver.attachments.designs.example_plate.assembly --show
"""

import argparse

from build123d import Box, Compound, Location

from quiver.common import PETG

# Drone-side quick-release plate on the bottom interface sits at
# Z = -160.70 (center of mass; see attachment_interface/assembly.py).
# Its drone-facing hardware is roughly 10 mm thick, so a payload
# mounting plate hangs below it.
_INTERFACE_Z = -160.70
_PLATE_TOP_Z = -171.0

# Placeholder payload plate dimensions (mm) — replace with your design.
_PLATE_X = 100
_PLATE_Y = 100
_PLATE_THICKNESS = 6


def make_assembly() -> Compound | None:
    """Build the example payload positioned on the bottom interface."""
    plate = Box(_PLATE_X, _PLATE_Y, _PLATE_THICKNESS)
    plate.color = PETG
    plate.label = "Example Payload Plate"
    plate.move(Location((0, 0, _PLATE_TOP_Z - _PLATE_THICKNESS / 2)))
    return Compound(children=[plate], label="Example Attachment")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Example attachment design")
    parser.add_argument("--show", action="store_true",
                        help="Open in ocp-vscode viewer, in place on the drone")
    args = parser.parse_args()

    design = make_assembly()
    if args.show:
        from ocp_vscode import show

        from quiver.assembly import make_assembly as make_drone

        drone = make_drone()
        shapes = [s for s in (drone, design) if s is not None]
        show(*shapes, deviation=0.5, angular_tolerance=0.5)
    else:
        bb = design.bounding_box()
        print(f"{design.label}: {len(design.solids())} solid(s), "
              f"bbox {bb.min} to {bb.max}")
