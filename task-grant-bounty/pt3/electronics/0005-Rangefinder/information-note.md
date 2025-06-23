# Status  

`Valid`

`Revision History: None`

`Replacement Log: None`

`Reference: None`

# Project Description

Project Quiver is a multirotor UAV platform with a maximum takeoff weight (MTOW) of 25 kg, using the Pix32 v6 flight controller and running ArduPilot firmware. One of the mission-critical requirements for this UAV is robust low-altitude awareness, including:

- Precision landing  
- Terrain following  
- Obstacle avoidance  

The sensors selected must be resilient across varying surface types and lighting conditions, while maintaining ArduPilot compatibility and low integration complexity.

---

# Methodology

A detailed evaluation was conducted to identify reliable altitude sensors compatible with ArduPilot for two primary purposes:

1. Landing and terrain hold (downward sensor) 
2. Vertical or directional ranging (for obstacle awareness or terrain profiling)

## Selection Criteria:

- Operational range (≥ 40 m preferred)  
- Compatibility with Pix32 v6 (UART / CAN / I²C)  
- Resistance to environmental interference (sunlight, water, dust)  
- Integration ease with ArduPilot  
- Weight and power requirements suitable for a 25 kg-class drone  
- Availability and support/documentation  

Multiple radar altimeters and LiDAR sensors were benchmarked, focusing on field-proven use cases in UAV platforms of similar scale.

---

# Results and Deliverables

## Selected Sensors

#### 1. Ainstein US-D1 Radar Altimeter

- **Type**: mmWave radar (77–79 GHz)  
- **Interface**: CAN / UART  
- **Range**: 0.5 m – 50 m  
- **Use Case**: Landing and terrain following  

**Pros:**
- Robust against dust, snow, grass, and sunlight  
- Weather-independent performance  
- Natively supported in ArduPilot via CAN or serial  
- Industrial build quality  

**Cons:**
- Lower spatial resolution compared to LiDAR  
- Slightly heavier than miniaturized LiDARs  

---

#### 2. Benewake TF03-180 LiDAR

- **Type**: TOF-based LiDAR  
- **Interface**: UART / CAN  
- **Range**: Up to 180 m  
- **Use Case**: Terrain profiling, vertical ranging, fast altitude hold  

**Pros:**
- Long detection range  
- IP67-rated enclosure for outdoor use  
- High refresh rate (up to 1 kHz)  
- Supported in ArduPilot with simple configuration  

**Cons:**
- Affected by sunlight and surface reflectivity  
- Narrow field of view  

---

## Evaluated Alternatives

| Sensor                 | Type            | Pros                                       | Cons                                         |
|------------------------|------------------|--------------------------------------------|----------------------------------------------|
| LightWare SF11/C       | LiDAR            | High resolution, proven, ArduPilot native  | Sensitive to reflectivity; more expensive     |
| LightWare SF45/B       | Scanning LiDAR   | 350° FOV, great for obstacle detection     | Not ideal as a dedicated altimeter           |
| TeraRanger Evo/Tower   | TOF array        | Modular, wide detection                    | Limited range and outdoor reliability        |
| Benewake TFmini Plus   | LiDAR            | Lightweight, low-cost                      | Short range (~12 m), weak outdoor performance |
| NanoRadar MR72         | 77 GHz radar     | All-weather detection                      | No ArduPilot native support; low vertical res |

---

# References

1. [Ainstein US-D1 Datasheet & Integration Guide](https://ainstein.ai)  
2. [Benewake TF03 Wiki](https://en.benewake.com/TF03/index.html)  
3. [LightWare LiDAR Documentation](https://lightwarelidar.com)  
4. [ArduPilot Rangefinder Setup](https://ardupilot.org/copter/docs/common-rangefinder-landingpage.html)  
5. [NanoRadar MR72 Overview](http://en.nanoradar.cn)  
