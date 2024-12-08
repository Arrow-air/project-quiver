# Status  

`Valid`

# Project Description

This study aims to determine the center of gravity (CG) and moment of inertia matrix for PT1 both without payload and with various payload weights and sizes. Additionally, it seeks to establish a straightforward method for calculating the updated CG and moment of inertia matrix when adding an additional mass, particularly payloads. Accurate determination of these parameters is crucial for evaluating stability, maneuverability, and for developing a simulation model to analyze the drone's performance under different configurations.

# Methodology 
The center of gravity and moment of inertia matrix are obtained through the design of the aircraft on Onshape.

The addition of a new mass to the system will affect the center of gravity and the moment of inertia matrix of the drone. The calculation of the modified parameters involve three  main steps:

1. Determine the New CG 
 - Calculate the weighted average of the original CG and the position of the added mass.
2. Adjust the Original Moment of Inertia:
- Shift the original moment of inertia matrix to the new CG using the parallel axis theorem.
3. Add the Effect of the New Mass:
- Provide the moment of inertia of the new mass or treat it as a point load to compute its contribution to the moment of inertia relative to the new CG.
- Combine this with the adjusted original moment of inertia matrix to get the updated values.

This process will be implemented using an Octave script to make them repeatable and efficient.

Fasteners, cables, connectors, and other small components are not included in the aircraft model and therefore do not contribute to the moment of inertia matrix. Including them would require waiting for a complete design freeze, which would significantly delay progress. As their contribution is negligible compared to the overall aircraft, this assumption is reasonable at this stage.

# Results and Deliverables
The payload weight and center of gravity completely depend on the attachment used on the aircraft. In this section, the parameters for the base configuration (with 1 x Tattu Gen 3.0 14S 28ah battery) with no attachment will be provided, as well as various sample cases which will be most likely to be utilized in the short term. If other cases are required, the [Octave script](./cg_I.m) is provided with this document to be used creating the parameters. 

**Reference Frame**
* All data provided in this section complies with the following reference frame.
* Origin: At the center of thrust.
* Axes:
  * X: Backward direction.
  * Y: Right
  * Z: Upward

**Moment of Inertia Matrix Definition**

|   |   |   |
| -- | -- | -- |
| I<sub>xx</sub> | I<sub>xy</sub> | I<sub>xz</sub> |
| I<sub>xy</sub> | I<sub>yy</sub> | I<sub>yz</sub>  |
| I<sub>xz</sub>  | I<sub>yz</sub>  | I<sub>zz</sub>  |

### **Case 1**
* Base configuration with no payload
* Weight: 18 kg
* CG location: [0	0	3.36] cm

| I: | [g x cm<sup>2</sup>]  |   |
| -- | -- | -- |
| 1.24E+07 | 793.57 | -39876 |
| 793.57 | 1.225E+07 | -349.24 |
| -39876 | -349.24 | 2.17E+07 |

### **Case 2**
* Base configuration with brush bullet dispenser
  * 4 kg @ [0, 0, -20] cm
* Weight: 22 kg
* CG location: [0	0	-0.89] cm

|	I:	|	[g x cm<sup>2</sup>]	|		|
|	--	|	--	|	--	|
|	1.42E+07	|	793.57	|	-39876	|
|	793.57	|	1.40E+07	|	-349.24	|
|	-39876	|	-349.24	|	2.17E+07	|

### **Case 3**
* Using Tattu Gen 3.0 14S 25ah with no payload
* Weight: 18 kg
* CG location: [-1.16	0	-0.89] cm

|	I:	|	[g x cm<sup>2</sup>]	|		|
|	--	|	--	|	--	|
|	1.24E+07	|	739.95	|	3.71E+04	|
|	739.95	|	1.22E+07	|	-344.74	|
|	3.71E+04	|	-344.74	|	2.17E+07	|

### **Case 4**
* Using Tattu Gen 3.0 14S 25ah with brush bullet dispenser
  * 4 kg @ [0, 0, -20] cm
* Weight: 22 kg
* CG location: [-0.95	0	-0.89] cm

|	I:	|	[g x cm<sup>2</sup>]	|		|
|	--	|	--	|	--	|
|	1.42E+07	|	739.95	|	1.26E+05	|
|	739.95	|	1.40E+07	|	-344.74	|
|	1.26E+05	|	-344.74	|	2.17E+07	|

# Remarks
- The parameters provided here are for preliminary studies only, mainly due to lack of accurate CAD models of each part on the aircraft.
- Due to the assumption stated in methodology and possible mismatches between the design and real model, more accurate parameters can be obtained from the real flight test data.
