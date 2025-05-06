
# Status  

`Valid`



# Project Description

This Python script anonymizes GPS-related location data from ArduPilot `.log` files. These `.log` files are typically converted from `.bin` format using Mission Planner or APM Planner.

The purpose of this script is to preserve flight behavior and telemetry data while protecting sensitive location information such as latitude and longitude — making the logs safe to share or publish.


# Methodology

The script processes ArduPilot `.log` files line by line and zeroes out specific fields that may contain location data. It specifically targets:

| Message | Fields Zeroed            |
|---------|--------------------------|
| GPS     | `Lat`, `Lng`      |
| AHR2    | `Lat`, `Lng`             |
| EAHR    | `Lat`, `Lng` |
| POS     | `Lat`, `Lng`             |
| TERR    | `Lat`, `Lng`             |
| ORGN    | `Lat`, `Lng`             |

Each field index was manually verified using the actual message structure (via `FMT` lines) in a sample `.log` file. The script ensures Mission Planner compatibility after anonymization.

# Results and Deliverables

-  `anonymize_gps_log.py`: Python script for log anonymization
-  `README.md`: This documentation
-  Compatible with:
  -- Mission Planner
  -- APM Planner

## How to Use
 1. Convert `.bin` to `.log`
Use **Mission Planner**:
**Dataflash Logs → Convert .Bin to .Log**

 2. Save your `.log` file in the same folder as the script:
Example: `00000072.log`

3. Make sure this is added at the bottom of the script:
``anonymize_gps_log("00000072.log", "anonymized_output.log")``
You can change the input and output file names according to your needs.

4.  Run the script:
``python anonymize_gps_log.py ``


# Remarks
-   No external dependencies required — runs on plain Python 3.
-   Designed for  .log  files (not  .bin).
-   You can extend this script to include additional messages like  CAM,  TRIG, or  GPS2.
-   Contributions and feedback are welcome!
