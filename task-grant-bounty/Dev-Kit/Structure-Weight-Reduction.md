---
title: Information Note - Quiver Structure Weight Reduction 1
tags: quiver, information-note
---

# Information Note - Quiver Structure Weight Reduction 1
Quiver PT3
Heavy-Lift Multipurpose UAV (<25 kg MTOW)

Table of content
[toc]

## 1. Structure weight reduction design

### 1.1 Description of the attempted weight reduction
To reduce the overall weight of the aircraft's metal structures, the material thickness of the following components was reduced on a test frame:

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
|![design_old.jpg](images/Structure-Weight/1.jfif)|![design_decision.jpg](images/Structure-Weight/2.jfif)|

### 1.2 Simulation of the design

Initial finite element analysis (FEA) within the design space showed that the lower airframe parts (consisting of the 1221 and 1222-Wall and the 1103-LowerPlate) exhibited a significant amount of deformation due to the thinner structure. 

Meanwhile, the upper part of the airframe (consisting of the 1101-UpperPlate, 1102-MidPlate, 1211-CW_Long, and 1212 & 1213_Square_Short) remained stable and rigid.

![deformation_FEA.jpg](images/Structure-Weight/3.jfif)
_FEA result showing displacement caused by a 300 N lateral static force at the attachment interface. 
(Unit: mm)_

## 2. On-site testing

### 2.1 Results after assembling the test frame 
The upper airframe still appeared to be very stable. However, a visual and physical inspection of the drone assembly showed that the lower airframe parts no longer possessed the required rigidity. 

![wobble_left.jpg](images/Structure-Weight/4.jfif)
![wobble_right.jpg](images/Structure-Weight/5.jfif)
_Deformation of the wall parts caused the airframe to wobble horizontally during physical interaction (static imagery)._

Significant horizontal movement in the lateral direction of the lower plate occurred due to the reduced material thickness of the 1221 and 1222-Wall. To safely proceed with a test flight, a 3D-printed support part was screwed into the center of the walls, which reduced the lateral movement by approximately 50%.

|![support_2.jpg](images/Structure-Weight/6.jfif)|![support_1.jpg](images/Structure-Weight/7.jfif)|
|-|-|

_Dark-colored support structure installed in the center of both wall structures._

### 2.2 Results after a test flight without payload
During a test flight without a payload, visual observation suggested that the drone exhibited normal flight behavior overall. 
However, after evaluating the flight logs, it was determined that lateral vibrations had increased. The most likely cause for this was the aforementioned freedom of movement in the 1221 and 1222-Walls, which subsequently led to movement in the 1103-LowerPlate.

### 2.3 Results after a test flight with maximum payload (around 7 kg)
The drone was technically airworthy, but it experienced such strong oscillations that the flight had to be aborted quickly. Due to the additional weight of the payload, the frame was no longer rigid enough and began to sway. The drone had to continuously counteract the oscillations to try and stabilize itself. Flight safety could not be guaranteed under these conditions.

## 3. Outcome and final decision

It was decided to maintain the weight reduction for the following upper airframe parts:

| Part                | Original thickness| New thickness |
| --------            | --------| --------|
| 1101-UpperPlate     | 2 mm     | 1 mm    |
| 1102-MidPlate       | 2 mm     | 1 mm    |
| 1211-CW_Long        | 2 mm     | 1 mm    |
| 1212 and 1213_Square_Short | 2 mm  | 1 mm |

The parts of the lower airframe and battery bay will not be changed at this time:

| Part     | Original thickness | New thickness |
| -------- | -------- | --------|
| 1103-LowerPlate     | 4 mm     | 4 mm **(No change)**|
| 1222 and 1221-Wall  | 2 mm     | 2 mm **(No change)**|

![design_final.jpg](images/Structure-Weight/8.jfif)

This new configuration results in a slight reduction in overall weight while maintaining sufficient structural support for the battery bay and heavy-lift payloads. Further tests may be carried out in the future.