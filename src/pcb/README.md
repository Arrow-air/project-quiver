# PCB Designs

KiCad projects for the Quiver's distributed PCB architecture.

## Board projects

| Directory | BOM | KiCad project | Description |
|---|---|---|---|
| `battery_pcb/` | 3311 | `Front_PCB` | Battery PCB — power switching and protection |
| `main_pcb/` | 3321 | `Quiver_PT3_Main_PCB` | Main PCB — power and data distribution hub |
| `fc_pcb/` | 3331 | `Quiver_PT3_FC_PCB` | Flight Controller PCB — Pix32 V6 adapter board |
| `attach_pcb/` | 3341 | `QuiverAttachPCB` (V1.4) | Attachment Interface PCB (x3) |

Production gerbers live in each project's `production/` folder. Design
history, update notes, and superseded board revisions remain with the
bounty tasks under
[`task-grant-bounty/pt3/electronics/`](../../task-grant-bounty/pt3/electronics/).

## STEP export workflow

Each KiCad project can export a 3D STEP model of the assembled board.
These STEP files go into the CAD assembly tree:

```
pcb/<board>/  ──(KiCad 3D export)──►  ../quiver/equipment/pcb/steps/{BOM}_{name}.step
```

For example, exporting `battery_pcb` produces `3311_battery_pcb.step`, which
should be placed in `../quiver/equipment/pcb/steps/`.
