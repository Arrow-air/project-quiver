---
title: Information Note - Quiver Structure Weight Reduction 1
tags: quiver, information-note
---

# Information Note - Quiver Structure Weight Reduction 1
Quiver PT3
Heavy-Lift Multipurpose UAV (<25 kg MTOW)

Table of content
[toc]

## 1. Structure weight reduction Design

### 1.1 Description of attempted weight loss
Considering reduce the weight of the aircraft from metal structures, material thickness of following components has been reduced on a test frame: 

| Part Name           | Original Thickness | New Thickness |
| --------            | -------- | -------- |
| 1101-UpperPlate     | 2 mm     | 1 mm     |
| 1102-MidPlate       | 2 mm     | 1 mm     |
| 1103-LowerPlate     | 4 mm     | 2 mm     |
| 1211-CW_Long        | 2 mm     | 1 mm     |
| 1212 and 1213_Square_Short | 2 mm  | 1 mm     |
| 1222 and 1221-Wall     | 2 mm     | 1 mm     |

|Original|Initial Decision|
|:-:|:-:|
|![design_old.jpg](https://hackmd.io/_uploads/rJfscUCL-g.jpg)|![design_decision.jpg](https://hackmd.io/_uploads/H19FsU0Ube.jpg)|

### 1.2 Simulation for the design

With the initial finite element analysis in the design space, result shows that the lower airframe parts (consisting of the 1221 and 1222-Wall and the 1103-LowerPlate) is having significant amount of deformation movement due to the thin structure. 

Meanwhile the upper part of the airframe (consisting of 1101-UpperPlate; 1102-MidPlate; 1211-CW_Long; 1212, 1213_Square_Short) is stable and rigid.

![deformation_FEA.jpg](https://hackmd.io/_uploads/HyECBrCIbl.jpg)
_FEA result of movement by 300 N side facing static force at the attachment interface. 
(Unit: mm)_

## 2. On-site testing

### 2.1 Results after assembling the test frame 
The upper airframe still appeared to be very stable. However, a visual and interacting inspection to the drone assembly shows that the lower airframe parts already no longer had the required rigidity. 

![wobble_left.jpg](https://hackmd.io/_uploads/Skg4u6LRI-g.jpg)
![wobble_right.jpg](https://hackmd.io/_uploads/HyV_p8RUZg.jpg)
_The wall parts deformation cause airframe wobbling horizontally while interacting (static imagery)._

Significant horizontal movement in the lateral direction of the lower plate was appeared due to the reduced material thickness of the 1221 and 1222-Wall. In order to proceed with a test flight, a 3D printed support part was screwed into the center of the walls and reduced lateral movement amount by approx. 50 %.

|![support_2.jpg](https://hackmd.io/_uploads/rkBfkDA8-l.jpg)|![support_1.jpg](https://hackmd.io/_uploads/rkBzJPAUWe.jpg)|
|-|-|

_Dark colored support structure in the very middle of both wall structures._

### 2.2 Results after a test flight without payload
After a test flight without payload, visual confirmation believe that the drone had normal flight behavior overall. 
However, after evaluating the logs, it was determined that the vibrations in the lateral direction had increased. The most likely cause for this is the aforementioned freedom of movement of the 1221 and 1222-walls, also lead to part 1103-LowerPlate movement.

### 2.3 Results after a test flight with maximum payload (around 7kg)
The drone was airworthy, but there were such strong oscillations that the flight had to be aborted quickly. Due to the additional weight of the payload, the frame was no longer rigid enough and began to sway. The drone had to continuously counteract the oscillation and tried to stabilize itself. Flight safety cannot be guaranteed under these conditions.

## 3. Outcome and final decision

It was decided to maintain the weight reduction for the following upper airframe parts:

| Part                | Original thickness| New thickness |
| --------            | --------| --------|
| 1101-UpperPlate     |2 mm     | 1 mm    |
| 1102-MidPlate       |2 mm     | 1 mm    |
| 1211-CW_Long        |2 mm     | 1 mm    |
| 1212 and 1213_Square_Short |2 mm  |1 mm |

The parts of the lower airframe or battery bay will not be changed at this time:

| Part     | Original thickness | New thickness |
| -------- | -------- | --------|
| 1103-LowerPlate     |4 mm     |4 mm **(No change)**|
| 1222 and 1221-Wall  |2 mm     |2 mm **(No change)**|

![design_final.jpg](https://hackmd.io/_uploads/ryHr5IC8bx.jpg)

This new configuration result for a slight reduction in weight, with maintaining sufficient structural support for the battery bay and heavy lifting payloads. Further tests may be carried out in the future.

