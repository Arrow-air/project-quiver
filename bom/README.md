# Quiver Bill of Materials — Master Data

These YAML files are the **source of truth** for what goes into a Quiver
Dev-Kit. The procurement CSV and the docs BOM page are generated from
them — never edit those by hand:

```sh
python -m quiver.bom validate   # check the data
python -m quiver.bom render     # regenerate docs/Manufacturing/BOM.md + quiver-bom.csv
```

CI rejects changes where the generated outputs are stale, and the test
suite cross-checks part IDs and quantities against the CAD assembly.

## Files

| File | Contents |
|---|---|
| `meta.yaml` | Document revision, vehicle config, dates |
| `1000-airframe-structure.yaml` | Plates, beams, landing gear, motor arms |
| `2000-supporting-structure.yaml` | Interfaces, sliders, mounts, enclosure |
| `3000-equipment.yaml` | Propulsion, sensors, PCBs, battery |
| `4000-harness.yaml` | Busbars, harness assemblies, harness supplies |
| `fasteners.yaml` | Screws, rivets, inserts, washers (`FAST-`) |
| `consumables.yaml` | Adhesives, filament (`CONS-`), tools (`TOOL-`) |

## Item schema

```yaml
- id: "1310"             # 4-digit CAD BOM id, or FAST-/CONS-/TOOL-/HAR-/HSUP- prefix
  name: Landing Gear Vertical Tube
  qty: 4                 # per vehicle; "AR" (as required) for CONS/TOOL only
  sourcing: cut-to-length  # laser-cut | 3d-print | cut-to-length | cots | pcb-assembly | harness
  material: Carbon fiber 3K     # required for make items
  finish: ...                   # optional
  spec: 30x28 mm tube           # what a shop needs to quote
  design_ref: src/quiver/...    # repo path; must exist
  production_bom: src/pcb/...   # pcb-assembly items only
  unit_cost_usd: 45.00          # indicative, per purchased unit
  purchase:                     # only when order qty differs from vehicle qty
    qty: 2
    note: 1000 mm stock yields two legs
  included_in: "3280"           # part arrives inside another item's kit
  since: A                      # revision that introduced the item
  notes: ...
```

Rules enforced by `validate`:

- IDs are unique across all files; 4-digit IDs must be quoted strings.
- 4-digit IDs must match the CAD label for modeled parts (tested in CI
  against the assembly: the BOM `qty` must cover the CAD instance count).
- `cots` items need at least one supplier with a part number or URL,
  unless `included_in` points at the item whose kit supplies them.
- Make items (`laser-cut`, `3d-print`, `cut-to-length`) should carry a
  `design_ref`; missing ones are warnings until the drawing lands.

## Revision policy

`meta.yaml: revision` is the revision manufacturers pin against. Bump it
(A → B → …) whenever a change affects what a manufacturer buys or
builds, update `date`, and note the change in a PR. While `status:
draft`, items marked `TBC` in their notes are unconfirmed — resolve all
TBCs before declaring a revision final.
