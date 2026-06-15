# Manufacturing

DXFs, cut sheets, and fabrication drawings for CNC and laser-cut parts.

> **Status:** no fabrication drawings are checked in yet — part geometry
> currently lives in the STEP files under
> [`src/quiver/`](../quiver/) (e.g.
> `quiver/airframe_structure/plates/steps/1111_upper_plate.step`), and
> Dev-Kit foam cut profiles are in
> [`task-grant-bounty/Dev-Kit/data/`](../../task-grant-bounty/Dev-Kit/data/).
> Contributions of per-part DXFs and drawings are welcome.

## Metal parts

The following BOM subcategories contain CNC or laser-cut metal parts:

| BOM | Subcategory | Material | Parts |
|---|---|---|---|
| 1100 | Plates | Aluminum (2–4mm) | Upper, middle, and lower plates |
| 1200 | Beams | Aluminum tube (40x40x2mm, 30x2mm) | Cockpit beams, battery walls |
| 1400 | Motor Arm | Aluminum (30mm) | Arm connectors |
| 1300 | Landing Gear | Aluminum (30mm) | Main adapters |

## Organization

Store DXF and drawing files named with BOM prefixes matching the CAD
assembly convention:

```
manufacturing/
    1111_upper_plate.dxf
    1112_middle_plate.dxf
    1113_lower_plate.dxf
    ...
```
