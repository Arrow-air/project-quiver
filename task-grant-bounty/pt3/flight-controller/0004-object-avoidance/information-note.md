# Status  

`Valid`


# Project Description

-   **Project:**  Quiver PT3 — Object-Avoidance (OA) sensor suite for a 25 kg quadcopter (Pix32 v6, ArduPilot)
    
-   **Use modes:**  Manual (Loiter/PosHold)  and  automated missions (AUTO with OA)
    
-   **Architecture:**  **360° LiDAR (top) + forward mmWave radar (nose)**  to compensate LiDAR’s weather/light dependency with radar’s all-weather performance
    
-   **Bus plan:**  **Nanoradar MR82 on CAN**  (same vendor protocol already in PT3; CAN bus otherwise busy) and  **RPLIDAR S2L on Serial (UART)**
    
   
# Methodology

-   Considered all ArduPilot-supported options provided below (https://ardupilot.org/copter/docs/common-rangefinder-landingpage.html) :

**Unidirectional Rangefinders**

Ainstein US-D1 Radar Altimeter; Ainstein LR-D1 Radar Altimeter; Attollo Engineering Wasp200; Avionics Anonymous DroneCAN LiDAR Interface; Benewake TF02 / TF03 / TF-Luna; Benewake TFmini / TFmini Plus; Garmin Lidar-Lite; GY-US42 Sonar; Hexsoon 24G Radar; Hondex Sonar; HC-SR04 Sonar; JAE JRE-30; JSN-SR04T Sonar; LeddarTech Leddar One; LeddarTech LeddarVu8; LightWare SF10 / SF11 LiDAR; LightWare SF20 / LW20 LiDAR; LightWare SF02 LiDAR; Maxbotix I²C Sonar; Maxbotix Analog Sonar; Nanoradar NRA24; Nooploop TOF-Sense P; Nooploop TOF-Sense F; ST VL53L0X / VL53L1X LiDAR; TeraRanger One/EVO Rangefinders; TeraRanger NEO; Underwater Sonar.

**Omnidirectional / Proximity Rangefinders**

Hexsoon 77G mmWave Radar; LDRobot LD-06 TOF; LightWare SF40/C (360°); LightWare SF45/B (350°); Nanoradar MR72 (112°); RPLidar A2/C1/S1 (360° Laser/TOF LiDAR); TerraRanger Tower / Tower EVO (360°); Cygbot D1 (120°).
    
-   Screening criteria: outdoor range, horizontal/vertical FOV, interface fit (CAN/UART), ArduPilot maturity, power/weight, availability, cost.
    
-   Basis of selection (safe-side, low-risk integration):
    
    -   **Nanoradar MR82 (forward, CAN):**  very wide azimuth with ~14° vertical to catch over/under obstacles; mmWave resilience in sun/dust/rain; protocol already used on PT3 → straightforward CAN integration
        
    -   **RPLIDAR S2L 18 m (top, Serial):**  DTOF 360° coverage with practical 18 m outdoor range; mature ArduPilot “Lidar360” path; Serial keeps CAN congestion low
        

# Results and Deliverables

  

## **Final Selection — Technical Specs**

  

**Forward sensor — Nanoradar MR82 (mmWave radar, CAN)**

-   **Band / type:**  80 GHz FMCW radar
    
-   **Range:**  ~**0.2–40 m**  (short-range beam), ~**0.2–80 m**  (mid-range beam)
    
-   **Field of view:**  **112° × 13.2°** (short) / **32° × 14°** (mid)
    
-   **Outputs:**  distance, speed, angle (up to  **64**  targets)
    
-   **Interfaces:**  **CAN** / UART (**using CAN** on PT3)
    
-   **Supply / power:**  **5–28 V**, ~**2.5 W**
    
-   **Ingress / temp:**  **IP66**, −40 °C…+70 °C (oper.)
    
-   **Form factor / mass:** ~**97 × 57 × 16.5 mm**, ~**92 g**
    

**360° surround — RPLIDAR S2L (DTOF LiDAR, UART)**

-   **Range radius:**  up to  **18 m**  (shorter on dark/low-reflectivity targets)
    
-   **Scan:**  **360°**, ~**10 Hz**  rotation,  **~0.12°**  angular resolution,  **~32 kHz**  sampling
    
-   **Accuracy / resolution:** ~**±30 mm** / **13 mm** (typ.)
    
-   **Interface / baud:**  **TTL UART**, **1 Mbps** (**using Serial** on PT3)
    
-   **Supply / power:**  **5 V**, ~**0.4 A** (~2 W)
    
-   **Protection / laser:**  **IP65**, Class-1 laser
    
-   **Form factor / mass:** ~**77 × 77 × 38.5 mm**, ~**190 g**
    

# Remarks

  
- **Useful Links**

	-   https://ardupilot.org/copter/docs/common-rangefinder-setup.html
	- https://ardupilot.org/copter/docs/common-rplidar-a2.html
	- https://ardupilot.org/copter/docs/common-rangefinder-mr72.html

-   **Speed note:**  Forward speed is  **TBD**  and will be finalized after flight tests; selection is sized conservatively



