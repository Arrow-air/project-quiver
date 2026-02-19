# Quiver CAD Assembly

Parametric CAD for the Arrow Quiver multi-purpose quadcopter platform,
built with [build123d](https://github.com/gumyr/build123d).

## Folder structure

The project follows the Quiver Bill of Materials (BOM) hierarchy. Top-level
folders map to BOM categories (1000–5000), and subfolders map to subcategories
(XX00). Folder names are descriptive (no numeric prefixes); BOM numbers appear
in STEP file names and module docstrings.

| BOM  | Category / Subcategory    | Folder path                                       |
|------|---------------------------|----------------------------------------------------|
| 1000 | Airframe Structure        | `airframe_structure/`                              |
| 1100 | Plates                    | `airframe_structure/plates/`                       |
| 1200 | Beams                     | `airframe_structure/beams/`                        |
| 1300 | Landing Gear              | `airframe_structure/landing_gear/`                 |
| 1400 | Motor Arm                 | `airframe_structure/motor_arm/`                    |
| 2000 | Supporting Structure      | `supporting_structure/`                            |
| 2100 | Attachment Interface      | `supporting_structure/attachment_interface/`        |
| 2200 | Battery Slider            | `supporting_structure/battery_slider/`             |
| 2300 | Equipment Mount           | `supporting_structure/equipment_mount/`            |
| 2400 | Cockpit Enclosure         | `supporting_structure/cockpit_enclosure/`          |
| 3000 | Equipment                 | `equipment/`                                       |
| 3100 | Propulsion System         | `equipment/propulsion/`                            |
| 3200 | Peripheral                | `equipment/peripheral/`                            |
| 3300 | PCB                       | `equipment/pcb/`                                   |
| 3400 | Battery                   | `equipment/battery/`                               |
| 4000 | Harness                   | `harness/`                                         |

Two additional folders live outside the BOM hierarchy:

- **`attachments/designs/`** — Community payload attachment designs
- **`variants/`** — Major structural variant builds

## STEP file naming

STEP files use BOM component numbers as prefixes for traceability:

```
{XXXX}_{descriptive_name}.step
```

Examples:
- `1111_upper_plate.step`
- `1211_cw_long.step`
- `3111_motor.step`

## Custom vs vendor parts

Each subcategory has a `steps/` directory for STEP files:

- **`steps/`** — Custom-designed parts (exported from Fusion 360 or built
  parametrically)
- **`steps/vendor/`** — Supplier-provided STEP models for off-the-shelf
  components (motors, tubes, hinges, etc.)

## Running the assembly

Export the full drone as a STEP file:

```bash
python -m quiver.assembly
```

View in the ocp-vscode 3D viewer:

```bash
python -m quiver.assembly --show
```

Export to a custom path:

```bash
python -m quiver.assembly -o path/to/output.step
```

## Assembly hierarchy

The top-level `assembly.py` composes three BOM categories. Each category
composes its subcategories, and each subcategory loads STEP files from its
`steps/` directory.

```
quiver.assembly
├── airframe_structure.assembly    (1000)
│   ├── plates.assembly            (1100)
│   ├── beams.assembly             (1200)
│   ├── landing_gear.assembly      (1300)
│   └── motor_arm.assembly         (1400)
├── supporting_structure.assembly  (2000)
│   ├── attachment_interface.assembly (2100)
│   ├── battery_slider.assembly    (2200)
│   ├── equipment_mount.assembly   (2300)
│   └── cockpit_enclosure.assembly (2400)
└── equipment.assembly             (3000)
    ├── propulsion.assembly        (3100)
    ├── peripheral.assembly        (3200)
    ├── pcb.assembly               (3300)
    └── battery.assembly           (3400)
```
