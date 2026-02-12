---
title: Information Note - Comprehensive Main Enclosure Modification
author: Dow Fisher KBM
status: draft
tags: quiver, information-note
---

# Information Note - Comprehensive Main Enclosure Modification

Quiver PT3
Heavy-Lift Multipurpose UAV (<25 kg MTOW)

Table of content
[toc]

## 1. Project Description

Since the initial design release, the main enclosure and the cockpit lid are becoming highly used components, offering important protection for PCB and flight controller wiring against desert flight environment.

For the latest evolution, certain modifications were performed to comply with following requirements :

1. Electrical engineering personnel asked for cable anchor with zip-tie-friendly.
2. An embedded 360 LiDAR mounting slot for the SLAMTEC RPLIDAR S2L.
3. Water proof performance upgrade for the contact between the enclosure and the lid. 
4. A mounting plate for Ethernet adapter and Remote-ID beacon module.

## 2. Methodologies

All modifications are performed based on original enclosure design for evolution. The LiDAR mounting slot was designed based on the 3D model S2L LiDAR module, also the new module mounting plate was designed based on the corresponding Ethernet adapter and Remote-ID beacon module.

### 2.1. Cable anchors

The design of cable anchors including better 3D printing slicing and curved shape for accommodate with zip-tie and large cable, and anchors spread by array and mirror feature for a even distribution. Total amounts of these anchors are designed for more than current need, this decision is to reserve amount for future use.

![cable_anchor_array.jpg](https://hackmd.io/_uploads/SJgsPYFlwZg.jpg)
_A single anchor feature highlighted in the image._

### 2.2. Embedded LiDAR mount
The installation slot of SL2 LiDAR were designed for minimize the profile of LiDAR module, meanwhile avoiding blocking the optical path of laser beam. Those large space and gaps are intended to reserve better cleaning and drying space around the LiDAR module.

![lidar_installation_slot_total.jpg](https://hackmd.io/_uploads/HkcblqeDWe.jpg)

Cable entry was design to pass though the electrical connectors of LiDAR module, also for adhesive or sealing material application. 

|Wall Gaps|Mount Base|
|-|-|
|![lidar_installation_slot_gap.jpg](https://hackmd.io/_uploads/HJEQlcxD-e.jpg)|![lidar_mounting_slot_gap_base.jpg](https://hackmd.io/_uploads/r1EQlqgw-g.jpg)|

For the inside features of the installation slot, multiple support beams and fillets are designed for better lid structural integrity.

![lidar_installation_slot_inside.jpg](https://hackmd.io/_uploads/HySKgqlP-g.jpg)
_With the 3D model of LiDAR module connector and cable harnessing._

### 2.3. Water proof sealing

(Add water proof sealing groove for lid, and the lip for enclosure)
(groove design for applying 30A hardness liquid silicone)

After the water splashing and spraying test in Germany, the original splash proof eaves design on the lid has been found insufficient in performance. A combination of groove and lip has been introduced in this version.
 
(refined inner corner shapes for better 3d printing)

Requires ...

### 2.4. Module mounting plate

(designed for better maintainability with double screw-install and 45 degree angle tilted insert)

## Results and Deliverables 

(new 3d model with new and refined things)

All improvements are integrated in the same piece of enclosure parts, including the inserts of module mounting plate. The module mounting plate is interchangeable between inserts of left and right corner.

The newly designed enclosure parts can replace the original enclosure.

(enclosure 3d printing slicing procedure might get complicated)
(The 3D printing and slicing orientation are limited for the ideal quality)

(exploded screenshot)

**(End of content)**

## Remarks

Feb-04-2026 0400UTC: 
- Delaying this documentation due to the ongoing 3D printing manufacturing issue.