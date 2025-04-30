# Common Equipment (Ordinary things):

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
  - The IR sensor sensitivity shall be suitable for most types of common, industrial, and petrochemical gases (Ref: https://www.flir.com/instruments/optical-gas-imaging/what-gases-can-i-see-cooled-vs.-uncooled/).
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
  - Shall having on board machine vision computer (e.g. Raspberry Pi, Nvidia Jetson)  for imager processing and identification.
  - May sort targets by size, shape, visible colors, or signal difference.
  - May having special target early warning function.
  - Shall have raster-to-vector conversion function for survey data output.
  - Shall output standardized or universal data format (e.g.  KML / KMZ) for survey data archiving and exchanging (e.g. Google Earth, ArcGIS, QGIS, etc.).
