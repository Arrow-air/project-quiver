# Security and Safety Policy

Project Quiver is flight hardware. Some defects are not just bugs — a
firmware parameter, electrical design, or structural issue can endanger
people on the ground.

## Reporting a vulnerability or safety-critical defect

Please do **not** open a public issue for anything that could cause harm
if exploited or flown uncorrected. Instead:

1. Use GitHub's
   [private vulnerability reporting](https://github.com/Arrow-air/project-quiver/security/advisories/new)
   for this repository, or
2. Contact the maintainers privately on the
   [Arrow Discord](https://discord.gg/arrow) (message a member of the
   drone engineering team).

Include the affected prototype generation (PT1–PT3, Dev-Kit), the
relevant files or parameters, and reproduction or analysis steps.

## Scope

- Flight firmware configurations and ArduPilot parameter sets in `docs/Operations/firmware/`
- PCB designs in `src/pcb/` (power protection, battery management)
- Structural CAD in `src/quiver/` (load-bearing parts)
- Companion software and tooling in this repository

Non-safety bugs (documentation, tooling, CAD visualization) can go
straight to the public issue tracker.
