# PCB Designs

KiCad projects for the Quiver's distributed PCB architecture.

## Board projects

| Directory | BOM | Description |
|---|---|---|
| `battery_pcb/` | 3311 | Battery PCB — power switching and protection |
| `main_pcb/` | 3321 | Main PCB — power and data distribution hub |
| `fc_pcb/` | 3331 | Flight Controller PCB — Pix32 V6 adapter board |
| `attach_pcb/` | 3341 | Attachment Interface PCB (x3) |

## STEP export workflow

Each KiCad project can export a 3D STEP model of the assembled board.
These STEP files go into the CAD assembly tree:

```
pcb/<board>/  ──(KiCad 3D export)──►  ../quiver/equipment/pcb/steps/{BOM}_{name}.step
```

For example, exporting `battery_pcb` produces `3311_battery_pcb.step`, which
should be placed in `../quiver/equipment/pcb/steps/`.
