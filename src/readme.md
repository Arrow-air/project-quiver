# Quiver Source

Design sources for the Arrow Quiver multi-purpose quadcopter platform.

## Directory layout

| Directory | Purpose | Primary tools |
|---|---|---|
| `quiver/` | CAD assembly — build123d Python package that composes STEP files into the full drone | [build123d](https://github.com/gumyr/build123d) |
| `pcb/` | PCB designs — KiCad projects for the four custom boards | [KiCad](https://www.kicad.org/) |
| `printing/` | 3D printing — slicer profiles and print settings for 3D-printed parts | |
| `manufacturing/` | Manufacturing outputs — DXFs and cut sheets for CNC/laser-cut metal parts | |

## How sources connect

Each tool produces STEP files that feed into the CAD assembly:

```
pcb/battery_pcb/  ──(STEP export)──►  quiver/equipment/pcb/steps/
pcb/main_pcb/     ──(STEP export)──►  quiver/equipment/pcb/steps/
Fusion 360        ──(STEP export)──►  quiver/airframe_structure/plates/steps/
                                      quiver/supporting_structure/.../steps/
                                      ...
```

The `quiver/` package then composes all STEP files into the full drone
assembly. See `quiver/README.md` for the BOM-based folder structure.
