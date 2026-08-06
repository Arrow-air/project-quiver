# Attachments

**Payload designs live in the
[payload-systems](https://github.com/Arrow-air/payload-systems) repo**, which
carries the versioned interface standard
([ICD](https://github.com/Arrow-air/payload-systems/blob/main/interface/ICD.md)),
the quick-release mating geometry, and one folder per payload project.

This package keeps only [`designs/example_plate/`](designs/example_plate/) — a
minimal parametric template that positions a placeholder payload on the bottom
interface and can render a design in place on the full drone CAD:

    python -m quiver.attachments.designs.example_plate.assembly --show

Copy it as a starting point for the CAD side of a new payload, then develop
the payload itself in payload-systems.
