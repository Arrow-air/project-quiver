# Status

Valid

# Project Description

This list is to showcase the drone attachments that may be used for Project Quiver to stimulate R&D and market expansion in mission equipment subject.

# Methodology

Most of the attachments in this list are mixed or came from the drone application scenarios that are currently common used in the world or under third-party R&D.

# Results and Deliverables

The following content is the list with application scenario classification:

## Common Equipment (Ordinary things):

### UAV Integrated Logistic:
- Universal Cargo Container:
  - Can be fixed into attachment interface, or can be released and deployed.
  - Optimized shape and direction for aerodynamic or space utilization. 
  - May have control interface or auxiliary storage unit for goods exchange.
  - May be transportable and stackable manually without aircraft.

### General UAV Remote Sensing:
- Standard FPV Camera
  - Must connect to video transmitting system with video quality greater than 720p and 45 FPS.
  - Must not be gimbaled, and must be fixed toward certain flight direction.
  - Shall not crop the video feed image or modify the timing, for ensure the direct attitude feedback to pilot.
  - Shall canceling the vibration from aircraft by certain designs.

- Standard Magnification Gimbaled Camera:
  - Must connect to video transmitting system with image sensors format larger than 1/2 inch and 30 FPS.
  - Must have the ability to switch the video transmitting feed between two sensors.
  - Main sensor may have ≈24mm focus length, magnified sensor may have focus length ≥85mm (focus length are defined with 35mm equivalent focal length).
  - Shall paired with 3 axis gimbal with vibration canceling design.

- Advanced IR Optical Gas Imagining Camera:
  - Must connect to video transmitting system.
  - The IR sensor sensitivity shall be suitable for most types of common, industrial, and petrochemical gases [(Reference)](https://www.flir.com/instruments/optical-gas-imaging/what-gases-can-i-see-cooled-vs.-uncooled/).
  - The lens shall have ≈50mm focus length in order to be universal in most applications (focus length is defined with 35mm equivalent focal length).
  - The Sensor refresh rate shall greater than 25 FPS.
  - Shall paired with 3 axis gimbal with vibration canceling design.

- Standard Geiger-Mueller Counter:
  - Shall design for close-ground and close-water radioactive sensing applications.
  - The sensor shall have protection against background noise such as cosmic rays in case of high precision applications.
  - Shall paired with distancing or avoidance equipment to protect the aircraft away from dangerous radiation area.
  - Shall have two or more sensors for data cross-reference.
  - Must have high level shock and vibration protection for the sensor.

- Multispectral Imagery System: (Survey moisture conditions on vegetation area, provide visual reference for further operations. Can be use for agricultural maintenance, forestry, even shallow groundwater detection.)
  - Sensors must contain RGB and NIR spectrum, with synchronous shutter design.
  - RGB sensor feed may connect to video transmitting system for better mission control.
  - Must have additional sunlight sensor on the top to capture the signal strength baseline.
  - May paired with down facing 3 axis gimbal to increase sensor pose accuracy.

- Ground Target Machine Vision System: (Recognize and sort ground targets, can be use as ranch animal counting, predator detection or any target area identification.)
  - Shall connect to other camera or sensor system to acquire camera frames.
  - Shall having on board machine vision computer (e.g. Raspberry Pi, Nvidia Jetson)  for image processing and identification.
  - May sort targets by size, shape, visible colors, or signal difference.
  - May having special target early warning function.
  - Shall have raster-to-vector conversion function for survey data output.
  - Shall output standardized or universal data format (e.g.  KML / KMZ) for survey data archiving and exchanging (e.g. Google Earth, ArcGIS, QGIS, etc.).
    
### UAV Interactive Device Series:
- General Airborne Speaker:
  - Shall be directional and loud enough to inform any living entities with distance ≥200m.
  - May broadcast the sound signal from live voice transmitting, pre-record and TTS system.
  - May having multiple speakers to amplify the sound pressure.

- High Capacity Flood Light:
  - Shall have same maximum brightness as modern LED train light. 
  - The light spot shall cover a horizontal range of 45~60 degrees.
  - May have functions of flashing and breathing effect.
  - May use 4000~4500K of color temperature.

- General Fishing Equipment:
  - Shall have buoy or water body landing system.
  - Shall have remote manual controlled fishing gear.
  - Shall have down view camera paired with 3-axis gimbal to compensate the waves on the water body.
  - Shall have emergency release or cutoff design.
  - The system must be waterproof for at least storm condition.

- Multi-Purpose Robotic Arm System:
  - Could grab, drag, push most kind of small solid objects.
  - Shall have minimize interference to the aircraft's center of gravity.
  - Shall have multiple joints with foldable structural design.
  - Shall could be mount on different side of the aircraft.
  - Shall have safety switch and emergency detach function, to prevent accidental release and aircraft trapping.

- Tethering Drone Converter System: (Convert the aircraft into a fix point hovering drone with constant ground power supply.)
  - Must provide stable AC voltage and current to the aircraft, and convert to stable DC power supply by the aircraft on-board system.
  - Must have on-board backup power system for emergency landing in case of any main power malfunction.
  - Must have wear protections for the tether and cable.
  - May have additional cable or pipeline to transport any other required signal or substance through the tether.
  - May have tension adjusting mechanism for the tether.

- Airborne Electrical Warfare System: (On-board anti-UAV jamming signal emitter, *Could be lots of issues for practical uses.)
  - Shall emit jamming signal in ISM and GNSS RF channels for common target engagement.
  - Shall have SDR controlled frequency band defining, noise signal generating and signal amplifying.
  - Shall use directional PCB panel emitter antenna for better targeting.
  - Must have standing wave protection design for emitter aircraft (e.g. emitter antenna distancing pylon).
  - Shall have 915Mhz / 1.2Ghz backup frequency or SDR controlled frequency hopping for secondary telemetry and flight control.
  - May optimize emitter aircraft's telemetry data packet to protect the bandwidth and link budget.
  - May have GNSS receiver shielding and aerospace grade inertial navigation system for emitter aircraft.

### Advanced Flight Assistance Series:
- Arrow Airframe Parachute System (AAPS):
  - Shall have 100% reliability.
  - Shall design as an energy release or pressure-launched ballistic parachute.
  - May provide a maintenance-free advantage.
  - Shall provide 20 meters of minimum operating altitude limit.

- Passive Propeller Defense System: (Provide protections from horizontal to diagonally downward terrain collision and dangerous object incursion.)
  - Shall have ability to prevent ground flying objects and slow projectiles to reach the propeller)
  - Shall use lightweight or composite materials for the structure.
  - Shall minimize aerodynamic and vibration interference to the aircraft.
  - Shall have impact shock absorbing design.
  - Must not be frangible.

- Mechanical Comm-Link Extension System: (On-board and ground based antenna tracker)
  - The aircraft and ground system must have matching basic functions and antenna layout.
  - Shall use directional PCB panel antenna.
  - Antenna must paired with high reliability 2 axis gimbal.
  - May use slip rings gimbal connectors to increase the reliability for complex flight missions.
  - May have two pairs of gimbaled antennas for fail safe and backup.

### UAV Geophysics Sensors: [(Reference)](https://fasttimesonline.co/the-future-of-drone-geophysics/)
- Low Altitude Magneto Field Anomaly Sensor
  - Shall design with zero or minimal ferrite components to prevent sensor interference.
  - Shall pair with extension pylon or certain distancing equipment to prevent sensor interference from aircraft body.
  - Sensor shall use multi-axis magnetic compass with certain multi-axis fusion algorithm to output the readable survey data such as heatmap.
  - Sensor assembly should maintain a stable heading and attitude during flight to ensure the continuity of survey data.

- Compact Synthetic Aperture Radar:
  - Shall design with high precise GNSS, IMU and PPS timing integration.
  - Shall have an acceptable antenna size for matching aircraft dimension limit.
  - TBD... (Frequency, Resolution, etc.)

- General Aerial LiDAR Scanning Device: (Scanning the ground while aircraft continues flying).
  - Shall design with high precise GNSS, IMU and PPS timing integration.
  - Sensor shall be mounted on the location that cover as many ground directions as possible.
  - May pair with fixed heading 3 axis gimbal to increase sensor pose accuracy and repeatability.
  - Ideal detecting range must greater than 80~120m.
  - Sensor must have ≥32 laser channels @ ≥20Hz, with accuracy greater than 1cm @ 100m.

- Sentinel LiDAR Mapping System: (LiDAR scanner mounted on the top of the aircraft, and ready to perform stationary full-dome high precision 3d scanning while landed.)
  - Shall design with high precise GNSS integration.
  - May integrate with off-shelf compact commercial 3D scanning stations (e.g. Leica BLK ARC, BLK360).
  - Scanning station must be mounted on the top of the aircraft with full coverage to full-dome directions, and the lower side coverage shall be as high as possible.
  - May pair with 3 axis gimbal to provide artificial ground leveling.
  - Shall have the ability of real world RGB colored point cloud output.

- Aerial Water Body Sampling System:
  - Shall be deploy, retrieve, transport by aircraft to collect certain amount of surface water for further examination.
  - May perform in-flight water sample examination with integrated testers or sensors.
  - Shall design to reduce close-water operation risks for the aircraft.

# Remarks
- This list may be updated from time to time.
