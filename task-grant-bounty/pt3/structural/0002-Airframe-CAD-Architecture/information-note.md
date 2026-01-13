
# Airframe CAD Architecture 

# Status

`Valid`

`Revision History: None`

`Replacement Log: None`

# Project Description

This information note covers the CAD model and structural architecture of the PT3 airframe. Compared to earlier prototypes, PT3 introduces weight optimizations, multiple features for ease of maintenance, and additional quick-release attachment interfaces.

# Methodology

The airframe was designed using Fusion 360 and evaluated through mechanical reasoning supported by past prototype failures and FEA insights. The structural system was broken into subassemblies to improve manufacturability and repairability. Each component was evaluated based on the following criteria:

- Weight-to-strength efficiency
- Ease of manufacturing/sourcing
- Compatibility with standard fasteners and tools
- Ease of maintenance

# Results and Deliverables

## CAD Model

Due to its file size, the CAD geometry is provided in Google Drive Arrow Teamspace. 

[Project Quiver PT3 CAD Model](https://drive.google.com/file/d/1uqtE9orY-Ni_axPZA7jhgISjftXAoFyP/view?usp=drive_link)

## Part List

|	Category	|	Subcategory	|	Component Family	|	Component	|
|-------|------------------|-----------------------------|----------------------|
|	1000 - Airframe Structure	|	1100 - Plates	|	-	|	1101 - Upper Plate	|
|	1000 - Airframe Structure	|	1100 - Plates	|	-	|	1102 - Mid Plate	|
|	1000 - Airframe Structure	|	1100 - Plates	|	-	|	1103 - Lower Plate	|
|	1000 - Airframe Structure	|	1200 - Beams	|	1210 - Cockpit Support	|	1211 - CW Long	|
|	1000 - Airframe Structure	|	1200 - Beams	|	1210 - Cockpit Support	|	1212 - CCW Back	|
|	1000 - Airframe Structure	|	1200 - Beams	|	1210 - Cockpit Support	|	1213 - CCW Front	|
|	1000 - Airframe Structure	|	1200 - Beams	|	1220 - Battery Walls	|	1221 - Right Wall	|
|	1000 - Airframe Structure	|	1200 - Beams	|	1220 - Battery Walls	|	1222 - Left Wall	|
|	1000 - Airframe Structure	|	1300 - Landing Gear	|	1310 - Vertical Tubes	|	1311 - FR	|
|	1000 - Airframe Structure	|	1300 - Landing Gear	|	1310 - Vertical Tubes	|	1312 - FL	|
|	1000 - Airframe Structure	|	1300 - Landing Gear	|	1310 - Vertical Tubes	|	1313 - BR	|
|	1000 - Airframe Structure	|	1300 - Landing Gear	|	1310 - Vertical Tubes	|	1314 - BL	|
|	1000 - Airframe Structure	|	1300 - Landing Gear	|	1320 - Horizontal Tubes	|	1321 - Right	|
|	1000 - Airframe Structure	|	1300 - Landing Gear	|	1320 - Horizontal Tubes	|	1322 - Left	|
|	1000 - Airframe Structure	|	1300 - Landing Gear	|	1330 - Main Adapter	|	1331 - FR	|
|	1000 - Airframe Structure	|	1300 - Landing Gear	|	1330 - Main Adapter	|	1332 - FL	|
|	1000 - Airframe Structure	|	1300 - Landing Gear	|	1330 - Main Adapter	|	1333 - BR	|
|	1000 - Airframe Structure	|	1300 - Landing Gear	|	1330 - Main Adapter	|	1334 - BL	|
|	1000 - Airframe Structure	|	1300 - Landing Gear	|	1340 - Tube Joint	|	1341 - FR	|
|	1000 - Airframe Structure	|	1300 - Landing Gear	|	1340 - Tube Joint	|	1342 - FL	|
|	1000 - Airframe Structure	|	1300 - Landing Gear	|	1340 - Tube Joint	|	1343 - BR	|
|	1000 - Airframe Structure	|	1300 - Landing Gear	|	1340 - Tube Joint	|	1344 - BL	|
|	1000 - Airframe Structure	|	1300 - Landing Gear	|	1350 - Foam	|	1351 - FR	|
|	1000 - Airframe Structure	|	1300 - Landing Gear	|	1350 - Foam	|	1352 - FL	|
|	1000 - Airframe Structure	|	1300 - Landing Gear	|	1350 - Foam	|	1353 - BR	|
|	1000 - Airframe Structure	|	1300 - Landing Gear	|	1350 - Foam	|	1354 - BL	|
|	1000 - Airframe Structure	|	1400 - Motor Arm	|	1410 - FR	|	1411 - Foldable Connector	|
|	1000 - Airframe Structure	|	1400 - Motor Arm	|	1410 - FR	|	1412 - Arm	|
|	1000 - Airframe Structure	|	1400 - Motor Arm	|	1420 - FL	|	1421 - Foldable Connector	|
|	1000 - Airframe Structure	|	1400 - Motor Arm	|	1420 - FL	|	1422 - Arm	|
|	1000 - Airframe Structure	|	1400 - Motor Arm	|	1430 - BR	|	1431 - Foldable Connector	|
|	1000 - Airframe Structure	|	1400 - Motor Arm	|	1430 - BR	|	1432 - Arm	|
|	1000 - Airframe Structure	|	1400 - Motor Arm	|	1440 - BL	|	1441 - Foldable Connector	|
|	1000 - Airframe Structure	|	1400 - Motor Arm	|	1440 - BL	|	1442 - Arm	|
|	2000 - Supporting Structure	|	2100 - Attachment Interface	|	2110 - Right	|	2111 - Spacer	|
|	2000 - Supporting Structure	|	2100 - Attachment Interface	|	2110 - Right	|	2112 - Interface	|
|	2000 - Supporting Structure	|	2100 - Attachment Interface	|	2120 - Left	|	2121 - Spacer	|
|	2000 - Supporting Structure	|	2100 - Attachment Interface	|	2120 - Left	|	2122 - Interface	|
|	2000 - Supporting Structure	|	2100 - Attachment Interface	|	2130 - Bottom	|	2131 - Spacer	|
|	2000 - Supporting Structure	|	2100 - Attachment Interface	|	2130 - Bottom	|	2132 - Interface	|
|	2000 - Supporting Structure	|	2200 - Battery Slider	|	-	|	2201 - Right	|
|	2000 - Supporting Structure	|	2200 - Battery Slider	|	-	|	2202 - Left	|
|	2000 - Supporting Structure	|	2300 - Equipment Mount	|	2310 - PCB	|	2311 - Main PCB Mount	|
|	2000 - Supporting Structure	|	2300 - Equipment Mount	|	2310 - PCB	|	2312 - BC PCB Mount	|
|	2000 - Supporting Structure	|	2300 - Equipment Mount	|	2320 - Camera	|	2321 - Camera Mount	|
|	2000 - Supporting Structure	|	2300 - Equipment Mount	|	2330 - AltitudeSensor	|	2331 - Altitude Sensor Mount	|
|	2000 - Supporting Structure	|	2300 - Equipment Mount	|	2340 - GNSS	|	2341 - GNSS Mount	|
|	2000 - Supporting Structure	|	2400 - Cockpit Enclosure	|	2410 - Enclosure	|	2411 - Main Enclosure	|
|	2000 - Supporting Structure	|	2400 - Cockpit Enclosure	|	2410 - Enclosure	|	2412 - Top Cap	|
|	2000 - Supporting Structure	|	2400 - Cockpit Enclosure	|	2420 - Anchor	|	2421 - FR	|
|	2000 - Supporting Structure	|	2400 - Cockpit Enclosure	|	2420 - Anchor	|	2422 - FL	|
|	2000 - Supporting Structure	|	2400 - Cockpit Enclosure	|	2420 - Anchor	|	2423 - BR	|
|	2000 - Supporting Structure	|	2400 - Cockpit Enclosure	|	2420 - Anchor	|	2424 - BL	|
|	2000 - Supporting Structure	|	2400 - Cockpit Enclosure	|	2430 - Hinge	|	2431 - Right	|
|	2000 - Supporting Structure	|	2400 - Cockpit Enclosure	|	2430 - Hinge	|	2432 - Left	|
|	2000 - Supporting Structure	|	2400 - Cockpit Enclosure	|	2440 - Clip	|	2441 - Right	|
|	2000 - Supporting Structure	|	2400 - Cockpit Enclosure	|	2440 - Clip	|	2442 - Left	|
|	3000 - Equipment	|	3100 - Propulsion System	|	3110 - FR	|	3111 - Motor	|
|	3000 - Equipment	|	3100 - Propulsion System	|	3110 - FR	|	3112 - Propeller	|
|	3000 - Equipment	|	3100 - Propulsion System	|	3120 - FL	|	3121 - Motor	|
|	3000 - Equipment	|	3100 - Propulsion System	|	3120 - FL	|	3122 - Propeller	|
|	3000 - Equipment	|	3100 - Propulsion System	|	3130 - BR	|	3131 - Motor	|
|	3000 - Equipment	|	3100 - Propulsion System	|	3130 - BR	|	3132 - Propeller	|
|	3000 - Equipment	|	3100 - Propulsion System	|	3140 - BL	|	3141 - Motor	|
|	3000 - Equipment	|	3100 - Propulsion System	|	3140 - BL	|	3142 - Propeller	|
|	3000 - Equipment	|	3200 - Peripheral	|	3210 - LiDAR	|	3211 - LiDAR	|
|	3000 - Equipment	|	3200 - Peripheral	|	3220 - Radar Altimeter	|	3221 - Radar Altimeter	|
|	3000 - Equipment	|	3200 - Peripheral	|	3230 - Front Telemetry Antenna	|	3231 - Front Telemetry Antenna	|
|	3000 - Equipment	|	3200 - Peripheral	|	3240 - Rear Telemetry Antenna	|	3241 - Rear Telemetry Antenna	|
|	3000 - Equipment	|	3200 - Peripheral	|	3250 - GNSS Wren Mini	|	3251 - GNSS Wren Mini	|
|	3000 - Equipment	|	3200 - Peripheral	|	3260 - Power Switch	|	3261 - Power Switch	|
|	3000 - Equipment	|	3200 - Peripheral	|	3270 - Camera	|	3271 - Camera	|
|	3000 - Equipment	|	3200 - Peripheral	|	3280 - Telemetry	|	3281 - Telemetry	|
|	3000 - Equipment	|	3300 - PCB	|	3310 - Main PCB	|	3311 - Main PCB	|
|	3000 - Equipment	|	3300 - PCB	|	3320 - BC PCB	|	3321 - BC PCB	|
|	3000 - Equipment	|	3300 - PCB	|	3330 - Attachment PCB	|	3331 - Right Attachment PCB	|
|	3000 - Equipment	|	3300 - PCB	|	3330 - Attachment PCB	|	3332 - Left Attachment PCB	|
|	3000 - Equipment	|	3300 - PCB	|	3330 - Attachment PCB	|	3333 - Bottom Attachment PCB	|
|	3000 - Equipment	|	3400 - Battery	|	3410 - Battery	|	3411 - Battery	|

# Remarks
