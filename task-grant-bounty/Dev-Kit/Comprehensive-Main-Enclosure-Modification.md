
# Comprehensive Main Enclosure Modification

# Status
`author: Dow Fisher KBM`

`status: valid`

`revision history: V1.0`

# 1. Project Description

Since the initial design release of the enclosure assembly, the main enclosure and cockpit lid have become frequently accessed components. This acesibility required additional protection for the PCB and avionic wiring against various flight environments, such as desert dust. 

As protection requirements have increased, several modifications were implemented in this design evolution. Two versions of these modifications are provided here for a final decision.

Main modification version (by KBM):

1. Integrated zip tie compatible cable anchors as requested by electrical engineering personnel.
2. An embedded mounting slot on the lid for "SLAMTEC RPLIDAR S2L" 360 LiDAR module.
3. A liquid silicone groove design for cockpit lid water proof performance upgrade.
4. Introduced a new cockpit latches for better reliability.
5. A mounting plate for securing the Ethernet adapter and Remote-ID beacon module.

Further modification version (By Julius):

1. Alternative water proofing mechanism for the cockpit lid using a silicone strip. 
2. Improved the LiDAR mounting slot with integrated drainage and a reserved cable inlet sealant area.
3. Improved outer shape of antenna mount bases with slope for better rain drainage.
4. Minimized battery rain shield and front cable outlet geometries for better 3D printer build size compatibility.

|KBM's Version|Julius's Version|
|-|-|
|![](images/Enclosure-Modification/version_kbm_overview.jpg)|![](images/Enclosure-Modification/version_julius_overview.jpg)|
|![](images/Enclosure-Modification/version_kbm_overview_back.jpg)|![](images/Enclosure-Modification/version_julius_overview_back.jpg)|

_Comparison of the two design iterations_

# 2. Methodologies

The current evolution of KBM's version was developed from the original enclosure design using 3D models of corresponding peripherals and modules. Julius's version was subsequently built upon KBM's latest modifications.

Most inner corners of the main enclosure have been refined and smoothed to facilitate further modeling and minimize the support structures required during 3D printing.

## 2.1. Cable anchors

A new style of cable anchor has been introduced. The curved shape accommodates zip ties and large cables while optimizing the slicing process for 3D printing without supports. The anchors are distributed using array and mirror features to ensure even spacing.

The total number of anchors exceeds current requirements. This ensures spare anchors are available for any additional or temporary wiring in the future.

|KBM's Version|Julius's Version|
|-|-|
|![](images/Enclosure-Modification/cable_anchor_array_kbm.jpg)|![](images/Enclosure-Modification/cable_anchor_array_julius.jpg)|

_A highlighted single anchor feature._

## 2.2. Embedded LiDAR mount

The installation slot of the LiDAR module was designed to minimize the module's hegiht profile, while not blocking the optical path of the laser beam. 

The large gaps around the module are intended to facilitate cleaning and drainage. In Julius's version, the drainage was improved with a specialized slope. The cable outlets in both versions are sized to allow the passage of the full LiDAR electrical connector, and the geometries are compatible with sealant application.

|KBM's Version|Julius's Version|
|-|-|
|![](images/Enclosure-Modification/lidar_mounting_slot_kbm.jpg)|![](images/Enclosure-Modification/lidar_mounting_slot_julius.jpg)|
|![](images/Enclosure-Modification/lidar_mounting_slot_gap_base_kbm.jpg)|![](images/Enclosure-Modification/lidar_mounting_slot_gap_base_julius.jpg)|
|![](images/Enclosure-Modification/lidar_mounting_slot_gap_kbm.jpg)|![](images/Enclosure-Modification/lidar_mounting_slot_gap_julius.jpg)|

To reinforce the slot and mount, multiple support beams and fillets were integrated into the internal features of the lid in KBM's version:

|KBM's Version|Julius's Version|
|-|-|
|![](images/Enclosure-Modification/lidar_mounting_slot_inside_kbm.jpg)|![](images/Enclosure-Modification/lidar_mounting_slot_inside_julius.jpg)|

_Internal view of the lid, showing LiDAR cable harnessing and connector._

## 2.3. Water proof sealing

Following the water proof testing in Germany, the original splash proof slope design on the lid was found to be insufficient for moderate-to-heavy rain scenarios.

To resolve this, a waterproof "groove and lip" ring combination has been introduced between the lid and the main enclosure in both versions, though they use different sealant solutions:

|-|KBM's Version|Julius's Version|
|-|-|-|
|Design Purpose|Fill the lid groove with a layer of 30A hardness liquid silicone. Once cured, it forms a custom waterproof gasket.|Attach a circular silicone foam strip into the groove on the main enclosure to act as the waterproof seal.|
|Groove View|![](images/Enclosure-Modification/waterproof_groove_kbm.png)|![](images/Enclosure-Modification/waterproof_groove_julius.png)|
|Groove Detail View|![](images/Enclosure-Modification/waterproof_groove_detail_kbm.png)|![](images/Enclosure-Modification/waterproof_groove_detail_julius.png)|
|Lip View|![](images/Enclosure-Modification/waterproof_lip_kbm.png)|![](images/Enclosure-Modification/waterproof_lip_julius.png)|
|Cut Section|![](images/Enclosure-Modification/waterproof_section_kbm.png)|![](images/Enclosure-Modification/waterproof_section_julius.png)|
|Installation Example|![](images/Enclosure-Modification/waterproof_silicone_install_kbm.jpg)|![](images/Enclosure-Modification/waterproof_silicone_install_julius.png)|
|Installation Detail|![](images/Enclosure-Modification/waterproof_silicone_amount_kbm.png) <br>Fill the groove to half-depth with liquid silicone to achieve desired compression.|Measure and cut a certain length of 8 mm diamter "Uxcell Silicone Foam" seal strip into the groove.|
 
## 2.4. Cockpit latch replacement

The original 3D printed latches on both sides of the lid were replaced by two stainless steel draw latches. (McMaster-Carr reference: 6082A11)

The screw insert layout on both lid and enclosure has been modified to fit with the new latches.

![](images/Enclosure-Modification/new_latch.png)
\* Note: KBM's version of enclosure.

## 2.5. Module mounting plate

For securing the Ethernet adapter and Remote-ID beacon module, without applying fragile material to high-stressed structural parts (e.g. motor beam connectors), a simple, floating and triangular shaped module mounting plate has been introduced to the main enclosure's inner corner. This mounting plate is interchangeable between the left and right sides of the aircraft.

The plate's geometry is intentionally simple, allowing end users to customize it by adding or removing features as needed.

![](images/Enclosure-Modification/mounting_plate_individual.png)
\* Note: KBM's version of enclosure.

The mounting plate's corresponding screw insert bases has been added to the enclosure wall, letting the plate maintain a moderated clearance between cable anchors, avoiding conflict with any cables between them. The screw insert bases are designed to be 45 degrees upward facing, for better maintenance access and non-support 3D printing. 

|Assembly View|Isolated View|
|-|-|
|![mounting_plate_overview.png](images/Enclosure-Modification/mounting_plate_overview.png)|![mounting_plate_isolated.png](images/Enclosure-Modification/mounting_plate_isolated.png)|

\* Note: KBM's version of enclosure.

Additionally, the plates are **Not Interchangeable** between two versions due to the main enclosure geometry difference. The plate's screw insert lips between two versions are having different location:

![alt text](images/Enclosure-Modification/mounting_plate_difference.png)

_Grey: Julius's version._

_Blue: KBM's version._

## 2.6 3D Printing Compatibility Improvement

\* *Note: These modifications apply to Julius's version only.

### 2.6.1 Over-all Size Optimize

The original design of main enclosure is oversized for most of regular 3D printers, making it hard to be widely manufactured. Current solution is to reduce the total dimension by shortening the battery rain shield and the front cable outlet.

|Original / KBM's Version|Julius's Version|
|-|-|
|![](images/Enclosure-Modification/total_enclosure_length_old.jpg)<br>34.739 cm|![](images/Enclosure-Modification/total_enclosure_length_julius.jpg)<br>31.416 cm|

This modification is also effective to the battery PCB cover part with shortened rain shield:

![](images/Enclosure-Modification/total_enclosure_length_detail_julius.jpg)

_Highlighted display of battery PCB cover._

### 2.6.2 Antenna Mount Optimize

The outer shape of antenna mount has been improved to prevent junky 3D printing overhang, also preventing any rain drops to concentrate around the antenna base.

|Original / KBM's Version|Julius's Version|
|-|-|
|![](images/Enclosure-Modification/antenna_mount_old.jpg)|![](images/Enclosure-Modification/antenna_mount_julius.jpg)|

# Results and Deliverables 

Two versions of new models sets, including: Lid, Main enclosure, Front PCB cover and Module mounting plate. All models are ready to be 3D printed.

For ideal 3D printing quality, the slicing orientation should be set to upward facing. Enabling raft or support structures for the main enclosure during the printing is strongly recommended to prevent print failure or dimmensional inaccuracies.

For the waterproof liquid silicone application, please refer to the silicone supplier's instructions and perform the operation on a leveled surface.

# Remarks

**(End of content)**