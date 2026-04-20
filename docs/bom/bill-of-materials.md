---
title: Bill of Materials
description: Complete bill of materials for the Quiver dev-kit build
sidebar_position: 2
---

# Bill of Materials

Complete bill of materials for building a Quiver dev-kit. This list covers all structural, harness, avionics, propulsion, and equipment components.

**Estimated total cost: ~$6,977**

:::tip Data formats
This BOM is also available as a [CSV file](https://github.com/Arrow-air/project-quiver/blob/main/docs/bom/quiver-pt1-bom.csv) for spreadsheet import or programmatic use. The original version was maintained in [Google Sheets](https://docs.google.com/spreadsheets/d/1QJBaE_1iMNckU-1B3wAJMqJlpWVV4R0CgzfKqYckRh0/edit?gid=0#gid=0).
:::

:::note 3D-printed parts & aluminum structure
Items marked "See Manufacturing Guide, Assembly Section" reference the Quiver manufacturing guide for detailed specs, tolerances, and assembly instructions.
:::

---

## Harness

Connectors, wiring, and cabling for the electrical harness.

| ID | Name | Cost | Qty | Total | Supplier | Notes |
|----|------|------|-----|-------|----------|-------|
| 0044 | XT30U-M (XT30 Male) | $0.83 | 1 | $0.83 | [TME](https://www.tme.com/us/en-us/details/xt30u-m/dc-power-connectors/amass/) | |
| 0045 | XT60U-M (XT60 Male) | $0.70 | 4 | $2.81 | [TME](https://www.tme.com/us/en-us/details/xt60u-m/dc-power-connectors/amass/) | |
| 0050 | Phoenix PTSM 2-pos plug | — | 1 | — | [Mouser](https://mou.sr/3TUNxPr) | |
| 0052 | Phoenix PTSM 4-pos plug | — | 18 | — | [Mouser](https://mou.sr/4bSpp8f) | |
| 0053 | Phoenix PTSM 5-pos plug | — | 5 | — | [Mouser](https://mou.sr/4nxik2l) | |
| 0054 | Phoenix PTSM 6-pos plug | — | 5 | — | [Mouser](https://mou.sr/44ach9V) | |
| 0066 | Hook Up Wire 26AWG PTFE (10 colors) | — | 1 kit | — | [Remington Industries](https://www.remingtonindustries.com/hook-up-wire/custom-hook-up-wire-26-awg-ptfe-stranded-kit-2-spool-sizes-available-choose-10-colors/) | 15ft per color |
| 0068 | Molex 12-pin connector (207760-1281) | $1.51 | 6 | $9.06 | [Mouser](https://www.mouser.com/ProductDetail/Molex/207760-1281) | |
| 0069 | Molex 12-ckt receptacle (204523-1201) | $0.42 | 6 | $2.54 | [Mouser](https://www.mouser.com/ProductDetail/Molex/204523-1201) | Cable-side connector |
| 0070 | Mill-Max Spring-Loaded Connector | $8.60 | 6 | $51.60 | [Mouser](https://www.mouser.com/ProductDetail/Mill-Max/813-22-010-30-000101) | Can populate with just 1 |
| 0071 | Mill-Max Low Profile SLC Target | $3.63 | 6 | $21.78 | [Mouser](https://www.mouser.com/ProductDetail/Mill-Max/419-10-210-30-054000) | Can populate with just 1 |
| 0073 | Arctic MX-4 Thermal Paste 20g | $12.00 | 1 | $12.00 | [Amazon](https://a.co/d/bZ7soGb) | For battery connector PCB |
| 0076 | Attachment Interface cable (Molex 79758-1149) | $1.29 | 50 | $64.50 | [Mouser](https://www.mouser.com/ProductDetail/Molex/79758-1149) | |
| — | JST GH pre-made cables (3, 4, 5, 6, 9 pos) | — | — | — | — | Variety pack |

---

## Propulsion

| ID | Name | Cost | Qty | Total | Supplier | Notes |
|----|------|------|-----|-------|----------|-------|
| 31X1 | XRotor X6 PLUS | $86.00 | 4 | $344.00 | [HobbyWing](https://www.hobbywing.com/en/products/xrotor-x6-plus269) | Integrated ESC + motor + props |
| 0076 | Spare Propellers | $25.00 | 4 | $100.00 | — | |
| — | Battery and charger | $848.00 | 1 | $848.00 | — | |

---

## Airframe Structure

Aluminum plates, tubes, and carbon fiber components.

### Primary Structure

| ID | Name | Qty | Material / Spec | Supplier | Notes |
|----|------|-----|-----------------|----------|-------|
| 1111 | Upper Plate | 1 | Aluminum | rapiddirect.com | See Manufacturing Guide |
| 1112 | Mid Plate | 1 | Aluminum | rapiddirect.com | See Manufacturing Guide |
| 1113 | Lower Plate | 1 | Aluminum | rapiddirect.com | See Manufacturing Guide |
| 1211 | CW Long | 1 | Aluminum tube | rapiddirect.com | See Manufacturing Guide |
| 121X | CCW Short | 2 | Aluminum tube | rapiddirect.com | See Manufacturing Guide |
| 122X | Battery Wall | 2 | Aluminum tube | rapiddirect.com | See Manufacturing Guide |

### Landing Gear

| ID | Name | Cost | Qty | Total | Supplier | Notes |
|----|------|------|-----|-------|----------|-------|
| 131X | Vertical Tubes | $45.00 | 5 | $225.00 | [RJXHobby](https://www.rjxhobby.com/carbon-fiber/carbon-fiber-tube/rjx-1pcs-colored-3k-carbon-fiber-tube-1000mm-od-21-30mm) | 30×28×1000mm CF, any color |
| 132X | Horizontal Tubes | $45.00 | 5 | $225.00 | [RJXHobby](https://www.rjxhobby.com/carbon-fiber/carbon-fiber-tube/rjx-1pcs-colored-3k-carbon-fiber-tube-1000mm-od-21-30mm) | 30×28×1000mm CF, any color |
| 133X | Top Connectors | $30.00 | 4 | $120.00 | [RJXHobby](https://www.rjxhobby.com/rjx-1pcs-20mm-quick-release-tripod-aluminum-tilt-fixed-seat-landing-gear-connector-1) | 30mm |
| 134X | Tube Joints (Aluminum T-Adapter) | $13.99 | 4 | $55.96 | [INNLOI](https://www.innloi.com/productinfo/448455.html) | 30mm — replaces 3D-printed version |
| 135X | Shock Absorber | $14.00 | 1 | $14.00 | [Amazon](https://a.co/d/ggzWXc4) | For wrapping bottom tubes |

### Motor Arms

| ID | Name | Cost | Qty | Total | Supplier | Notes |
|----|------|------|-----|-------|----------|-------|
| 14X1 | Motor Arm Connectors | $25.00 | 4 | $100.00 | [AliExpress](https://www.alibaba.com/product-detail/30-40mm-Folding-arm-tube-Drone_1600762096177.html) | 30mm option |
| 14X2 | Motor Arm Tubes | $45.00 | 5 | $225.00 | [RJXHobby](https://www.rjxhobby.com/carbon-fiber/carbon-fiber-tube/rjx-1pcs-colored-3k-carbon-fiber-tube-1000mm-od-21-30mm) | 30×28×1000mm CF, any color |

---

## Secondary Structure

3D-printed parts and purchased components for mounts, enclosures, and adapters.

### 3D-Printed Parts

| ID | Name | Qty | Notes |
|----|------|-----|-------|
| 21X1 | Attachment Interface Spacer Left & Right | 2 | See Manufacturing Guide |
| 2131 | Attachment Interface Spacer Bottom | 1 | See Manufacturing Guide |
| 221X | Battery Sliders | 2 | See Manufacturing Guide |
| 2311 | Main PCB Mount | 1 | See Manufacturing Guide |
| 2312 | BC PCB Mount | 1 | See Manufacturing Guide |
| 2313 | BC PCB Cover | 1 | See Manufacturing Guide |
| 2321 | Sensor Mount | 1 | See Manufacturing Guide |
| 2331 | GNSS Mount | 1 | See Manufacturing Guide |
| 2341 | PPP Adapter & Beacon Mount | 1 | See Manufacturing Guide |
| 2411 | Main Enclosure | 1 | See Manufacturing Guide |
| 2412 | Enclosure Top Cap | 1 | See Manufacturing Guide |

### Purchased Secondary

| ID | Name | Cost | Qty | Total | Supplier | Notes |
|----|------|------|-----|-------|----------|-------|
| 21X2 | Quick Release Adapter | $34.00 | 3 | $102.00 | [AliExpress](https://www.alibaba.com/product-detail/Quick-Release-Clip-Plate-Clamp-Quick_1600982145247.html) | Without PCB board |
| 242X | Enclosure Hinge | $10.00 | 2 | $20.00 | [JW Winco](https://www.jwwinco.com/en-us/products/3.3-Hinging-latching-locking-of-doors-and-covers/Hinges/GN-237-Zinc-Die-Cast-or-Aluminum-Hinges-Countersunk-Thru-Holes-or-Threaded-Stud-Type) | GN 237-ZD-30-30-A-SW |
| 243X | Enclosure Latch | — | 2 | — | [McMaster-Carr](https://www.mcmaster.com/6082A11/) | |

---

## Avionics & Equipment

### Sensors & Communications

| ID | Name | Cost | Qty | Total | Supplier | Notes |
|----|------|------|-----|-------|----------|-------|
| 3211 | SLAMTEC RPLIDAR S2L (OA LiDAR) | $380.00 | 1 | $380.00 | [DFRobot](https://www.dfrobot.com/product-2617.html) | Obstacle avoidance |
| 3212 | Nanoradar MR82 (OA Radar) | $285.00 | 1 | $285.00 | [Nanoradar](https://www.nanoradar.com/Products_1/7.html) | Obstacle avoidance |
| 3213 | Nanoradar NRA15 (Altimeter Radar) | $240.00 | 1 | $240.00 | [Nanoradar](https://www.nanoradar.com/Products_1/4.html) | |
| 3220 | SIYI HM30 Long Range FPV System | $282.04 | 1 | $282.04 | [Reebot](https://shop.reebot.com/products/siyi-hm30) | |
| 3231 | Power Switch | — | — | — | [Digikey](https://www.digikey.com/en/products/detail/e-switch/PVHC4F23SS344/24614861) | |
| 3241 | SIYI A8 mini Gimbal Camera | $309.58 | 1 | $309.58 | [Reebot](https://shop.reebot.com/products/siyi-a8-mini) | |
| 3251 | Here4 Multiband GNSS / F9P | $288.00 | 1 | $288.00 | [HolyBro](https://irlock.com/products/here4-multiband-rtk-gnss) | |
| 3261 | DB201 Remote ID Module | $54.00 | 1 | $54.00 | [DroneScout](https://dronescout.co/product/dronebeacon-mavlink-db201-transponder/) | |
| 3315 | Mateksys GNSS M9N-G4-3100 | $125.00 | 1 | $125.00 | [Mateksys](https://www.mateksys.com/?portfolio=m9n-g4-3100) | DroneCAN backup |
| — | Remote Control | $150.00 | 1 | $150.00 | — | |

### Electronics & Computing

| ID | Name | Cost | Qty | Total | Supplier | Notes |
|----|------|------|-----|-------|----------|-------|
| 3332 | Holybro Pix32 v6 | $296.00 | 1 | $296.00 | [HolyBro](https://holybro.com/products/pix32-v6) | Flight controller |
| 3312 | Raspberry Pi 5 | — | 1 | — | — | Companion computer |
| 3313 | GigaBlox Nano Ethernet Switch | $95.67 | 2 | $191.33 | [BotBlox](https://botblox.io/products/micro-gigabit-ethernet-switch) | |
| 3314 | PPP Adapter, CubeNode ETH | $121.98 | 1 | $121.98 | [CubePilot](https://irlock.com/products/cube-node-eth) | |

### Custom PCBs

| ID | Name | Qty | Notes |
|----|------|-----|-------|
| 3311 | Main PCB (PT3) | 1 | Source from Arrow — [GitHub](https://github.com/Arrow-air/project-quiver/tree/main/task-grant-bounty/pt3/electronics) |
| 3321 | Battery Connector PCB | 1 | Source from Arrow |
| 3322 | Busbar Positive | 1 | See Manufacturing Guide |
| 3323 | Busbar Negative | 1 | See Manufacturing Guide |
| 3324 | BC_PCB 4mm Heatsink | 1 | Local laser cutting |
| 3331 | Flight Controller PCB | 1 | Source from Arrow |
| 334X | Attachment Interface PCB | 36 | Order from JLCPCB with [gerber files](https://github.com/Arrow-air/project-quiver/tree/main/task-grant-bounty/pt3/electronics/0003-Attachment-Interface-PCB) |
| — | PCBs (generic total) | — | ~$500 estimated |

---

## Misc — Fasteners, Hardware & Tools

Detailed fastener inventory aligned with the manufacturing guide. All sourced from McMaster-Carr unless noted.

### Rivets

| ID | Name | Qty | McMaster P/N | Spec |
|----|------|-----|-------------|------|
| 5101 | Rivet 1 | 26 | [97525A224](https://www.mcmaster.com/97525A224) | 4mm Dia. for 1–2.5mm thickness |
| 5102 | Rivet 2 | 10 | [97525A251](https://www.mcmaster.com/97525A251) | 4mm Dia. for 2.5–4.5mm thickness |
| 5103 | Rivet 3 | 10 | [97525A226](https://www.mcmaster.com/97525A226) | 4mm Dia. for 4.5–6.4mm thickness |

### Screws

| ID | Name | Qty | McMaster P/N | Spec |
|----|------|-----|-------------|------|
| 5104 | Screw 1 | 8 | [91292A113](https://www.mcmaster.com/91292A113) | Socket Head M3×10 |
| 5105 | Screw 2 | 16 | [92095A190](https://www.mcmaster.com/92095A190) | Flanged Button Head M4×10 |
| 5106 | Screw 4 | 8 | [91292A114](https://www.mcmaster.com/91292A114) | Socket Head M3×12 |
| 5107 | Screw 5 | 75 | [91292A112](https://www.mcmaster.com/91292A112) | Socket Head M3×8 |
| 5108 | Screw 6 | 16 | [91292A024](https://www.mcmaster.com/91292A024) | Socket Head M3×40 |
| 5109 | Screw 7 | 4 | [92125A128](https://www.mcmaster.com/92125A128) | Hex Drive Flat Head M3×8 |
| 5110 | Screw 8 | 8 | [92125A130](https://www.mcmaster.com/92125A130) | Hex Drive Flat Head M3×10 |
| 5111 | Screw 9 | 8 | [91292A108](https://www.mcmaster.com/91292A108) | Socket Head M4×8 |
| 5112 | Screw 10 | 4 | [91292A832](https://www.mcmaster.com/91292A832) | Socket Head M2×6 |
| 5113 | Screw 11 | 27 | [97654A674](https://www.mcmaster.com/97654A674) | Flanged Button Head M3×6 |
| 5114 | Screw 12 | 4 | [92855A837](https://www.mcmaster.com/92855A837) | Socket Head M2×5 |
| 5115 | Screw 13 | 4 | [91292A012](https://www.mcmaster.com/91292A012) | Socket Head M2.5×8 |
| 5116 | Screw 14 | 4 | [91292A833](https://www.mcmaster.com/91292A833) | Socket Head M2×10 |
| 5117 | Screw 15 | 4 | [91292A191](https://www.mcmaster.com/91292A191) | Socket Head M5×8 |
| 5118 | Screw 16 | 4 | [92095A203](https://www.mcmaster.com/92095A203) | Button Head M3×40 |
| 5119 | Screw 17 | 8 | [90751A110](https://www.mcmaster.com/90751A110) | Socket Head M3×6 |
| 5120 | Screw 3 | 12 | [92095A451](https://www.mcmaster.com/92095A451) | Button Head M2×4 |

### Inserts

| ID | Name | Qty | McMaster P/N | Spec |
|----|------|-----|-------------|------|
| 5121 | Insert 1 | 50 | [94459A140](https://www.mcmaster.com/94459A140) | M3 Threaded Inserts — 5.7mm |
| 5122 | Insert 2 | 8 | [94180A351](https://www.mcmaster.com/94180A351) | M4 Threaded Inserts |
| 5123 | Insert 3 | 4 | [94180A312](https://www.mcmaster.com/94180A312) | M2 Threaded Inserts |
| 5124 | Insert 4 | 16 | [94180A331](https://www.mcmaster.com/94180A331) | M3 Threaded Inserts — 3.8mm |

### Washers & Nuts

| ID | Name | Qty | McMaster P/N | Spec |
|----|------|-----|-------------|------|
| 5125 | Washer 1 | 123 | [98689A112](https://www.mcmaster.com/98689A112) | M3 General Purpose 3.2mm ID, 6mm OD |
| 5126 | Washer 2 | 8 | [93475A230](https://www.mcmaster.com/93475A230) | M4 General Purpose 4.3mm ID, 9mm OD |
| 5127 | Washer 3 | 12 | [95610A110](https://www.mcmaster.com/95610A110) | M2 Nylon 2.2mm ID, 5mm OD |
| 5128 | Washer 4 | 4 | [95610A011](https://www.mcmaster.com/95610A011) | M2.5 Nylon 2.7mm ID, 5.6mm OD |
| 5129 | Washer 5 | 4 | [95610A704](https://www.mcmaster.com/95610A704) | M3 Nylon 3.2mm ID, 6mm OD |
| 5130 | Washer 6 | 4 | [93475A240](https://www.mcmaster.com/93475A240) | M5 General Purpose 5.3mm ID, 10mm OD |
| 5131 | Nut 1 | 16 | [90576A811](https://www.mcmaster.com/90576A811) | Nylon-Insert Locknut M3 |

### Seals, Mounts & Misc Hardware

| ID | Name | Qty | Source | Spec |
|----|------|-----|--------|------|
| 5132 | Vibration Mount | 5 | [Amazon](https://www.amazon.com/s?k=M3+rubber+anti+vibration+spacer) | M3 Rubber Anti-Vibration Spacer |
| 5133 | Grommet 1 | 4 | [Amazon](https://www.amazon.com/s?k=circular+grommet+20mm) | Circular Grommet OD: 20mm |
| 5134 | Grommet 2 | 12 | [Amazon](https://www.amazon.com/s?k=oval+grommet+27x13mm) | Oval Grommet 27×13mm |
| 5135 | Silicone Foam Seal Strip | 1 | [Amazon](https://www.amazon.com/s?k=silicone+foam+seal+strip+8mm+round) | Circular, OD: 8mm |

### Tools & Adhesives

| ID | Name | Notes |
|----|------|-------|
| 5201 | Allen key set | Metric, M2–M5 |
| 5202 | Wrench set | Metric |
| 5203 | Cordless screwdriver or drill press | |
| 5204 | Riveting tool | For 4mm rivets |
| 5205 | Double-Sided Tape | Heavy Duty |
| 5206 | Loctite Threadlocker Purple 222 | Low-strength ([McMaster 1810A28](https://www.mcmaster.com/1810A28)) |
| 5207 | Loctite Threadlocker Blue 242 | Medium-strength ([McMaster 91458A113](https://www.mcmaster.com/91458A113)) |
| 5208 | Würth Super RTV Silicone Black | 200ml, black (Model: 08933311) |

---

## Cost Summary

| Category | Estimated Cost |
|----------|---------------|
| Propulsion (motors, props, battery) | $1,292.00 |
| Avionics & Sensors | $2,432.93 |
| Custom PCBs | $500.00 |
| Airframe (aluminum, CF tubes, connectors) | $1,465.00 |
| Fasteners & Hardware | $110.00 |
| 3D Printed Parts | $150.00 |
| Harness & Connectors | $165.12 |
| Transport Case | $600.00 |
| Remote Control | $150.00 |
| **Total** | **~$6,977** |

:::info PCB assembly guides
For detailed PCB assembly instructions, interactive BOMs, and soldering guides, see the [PT3 Assembly Guides](https://github.com/Arrow-air/project-quiver/tree/main/docs/pt3-assembly-guides/PCB-assembly).
:::
