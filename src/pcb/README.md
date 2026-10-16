# PCB Designs

KiCad projects for the Quiver's distributed PCB architecture.

## Board projects

| Directory | BOM | KiCad project | Description |
|---|---|---|---|
| `battery_pcb/` | 3320 | `Front_PCB` (V1.3) | Battery PCB — power switching and protection |
| `main_pcb/` | 3310 | `Quiver_PT3_Main_PCB-rounded` (V1.2) | Main PCB — power and data distribution hub. V1.2 is the board on the Dev-Kit aircraft. |
| `fc_pcb/` | 3330 | `Quiver_PT3_FC_PCB` | Flight Controller PCB — Pix32 V6 adapter board |
| `attach_pcb/` | 3331 | `QuiverAttachPCB` (V1.4) | Attachment Interface PCB (x3) |

Production gerbers live in each project's `production/` folder. Design
history, update notes, and superseded board revisions remain with the
bounty tasks under
[`task-grant-bounty/pt3/electronics/`](../../task-grant-bounty/pt3/electronics/).

## STEP export workflow

Each KiCad project can export a 3D STEP model of the assembled board
(`kicad-cli pcb export step --subst-models <board>.kicad_pcb`). The CAD
assembly uses these models:

```
pcb/<board>/  ──(KiCad 3D export)──►  ../quiver/equipment/pcb/steps/vendor/{BOM}_{name}.step
```

For example, `main_pcb` is `3310_main_pcb.step` and `battery_pcb` is
`3320_bc_pcb.step` in `../quiver/equipment/pcb/steps/vendor/`.

The CAD models also carry parts whose 3D models are not in these KiCad
libraries: `3320_bc_pcb.step` includes the 3324 heatsink with its screws
and a few connector and component bodies. A plain KiCad export is missing
them, so before replacing a CAD model, check that its board body matches
the KiCad source and carry those parts over. The board bodies in 3310 and
3320 match the V1.2 and V1.3 sources exactly.
