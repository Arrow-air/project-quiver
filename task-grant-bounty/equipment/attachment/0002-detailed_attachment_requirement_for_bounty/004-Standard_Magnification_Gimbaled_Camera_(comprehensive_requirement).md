# Comprehensive Requirement
### Standard Magnification Gimbaled Camera
Version: 14.05.25-1 Boar

## General Objective Description:

A camera module with two sensors, it contains a normal main lens and a high magnification lens, both are fixed focus. 
Instead of controlling a single complex optical zooming lens, this camera can just switch between two different zooming via some kind of digital video switching mechanism. 
The camera module can be attach or detach from a gimbal stablizer via certain standard mounting base and connector between them.

## Optional Functions:
- OF-1: May include on-ground wireless imagery download functions.
- OF-2: May include point tracking, fight heading following, or locking functions.
- OF-3: May include built-in camera pose record, GNSS trigger record or track record function.

## Architecture & Boundary:
- AB-1: Shall accept 12~60V DC power supply with anti-spark design.
- AB-2: Must connect to aircraft's video transmitting system
- AB-3: Must have the ability to switch the video transmitting feed between two sensors.
- AB-4: Shall paired with 3 axis gimbal with vibration canceling design.
- AB-5: May include on-ground companion software for video encoding configuration.
- AB-6: Shall support H.264 and MJPEG encodeing for balanced image quality and latency.

## Performance:
- P-1: Image sensors shall have diagonal size greater ≥ 1/2 inch and refresh rate ≥ 30 FPS.
- P-2: May select global shutter sensor for components.
- P-3: Main lens shall have focus length around 24mm (focus length are defined with 35mm equivalent focal length).
- P-4: Magnified lens may have focus length ≥ 85mm (focus length are defined with 35mm equivalent focal length).
- P-5: Shall include photo capture, video recording, SD card storage, and
- P-6: Must have dust and water splash proof ablility.

## Manufacturing & Maintenece Process Technology:
- M-1: The structure parts must design with materials with a thermal softening temperature higher than 110 degress Celsius.

## Safety:
- S-1: Must include over temperature protection mechanism.
- S-2: Must include at least passive heatsink design.
- S-3: Must include power line noise filering mechanism.

## Revision:
- 14.05.25-1 Boar: EDITING
