# Status

`Valid`

# Project Description

The objective is to select an appropriate GNSS system for Project Quiver, ensuring it supports the development and operational goals of UAVs with minimal complexity. The system must balance cost-effectiveness, ease of integration, open-source compatibility, high reliability, and precision accuracy. Essential criteria also include robust documentation, compatibility with existing ecosystems (ArduPilot and PX4), and flexibility in antenna configurations.

# Methodology

## Constraints and Decision Criteria

-   **Open Source Ecosystem:** Priority given to open-source systems to mitigate the risk of vendor lock-in and enable community-supported troubleshooting.
    
-   **Documentation and Ease of Integration:** Systems with comprehensive documentation and standard interfaces are preferred to facilitate rapid development and efficient integration.
    
-   **Cost Efficiency:** The selected GNSS system should be cost-effective to avoid sunk cost fallacy and enable parallel experimentation.
    
-   **Accuracy and Reliability:** Systems must provide centimeter-level accuracy, reliability, and multi-band GNSS support (GPS, GLONASS, Galileo, BeiDou).
    
-   **Form Factor and Antenna Integration:** Consideration of compact systems suitable for UAV platforms, with either integrated antennas or flexible external antenna options.

## GNSS System Options

| GNSS Module                          | Key Features                                                               | Pros                                                                       | Cons                                             |
|--------------------------------------|----------------------------------------------------------------------------|----------------------------------------------------------------------------|--------------------------------------------------|
| **Holybro H-RTK F9P GNSS**           | Multi-band, RTK (ZED-F9P), supports GPS, GLONASS, Galileo, BeiDou          | High accuracy, robust support, open-source integration                     | Larger antenna footprint                         |
| **Holybro DroneCAN H-RTK F9P Rover** | Compact, DroneCAN interface, integrated helical antenna                    | UAV-optimized, simple DroneCAN integration                                 | Less antenna flexibility                         |
| **SparkFun GPS-RTK-SMA/GPS-RTK2**    | RTK, SMA connector, Arduino compatible, ZED-F9P chipset                    | Versatile antenna options, well-documented, cost-effective                 | External antenna complexity                      |
| **Drotek DP0601 RTK GNSS**           | ZED-F9P chipset, built-in SMA connector, multiple interfaces               | Reliable, versatile, excellent EMI protection, affordable                  | No CAN bus feature, external antenna complexity  |
| **Mateksys M9N-G4-3100**             | Compact, multi-constellation GNSS, non-RTK (u-blox M9N chipset)            | Extremely low cost, compact, open-source friendly                          | Lower accuracy, not RTK, reliability concerns    |
| **Systork Wren Mini**                | L1/L5 RTK, integrated antenna & magnetometer, DroneCAN protocol            | Compact, robust against EMI, PX4/ArduPilot integration                     | Limited interface options (DroneCAN/USB only)    |
| **3DR Mosaic-X5 CAN GPS**            | High-end RTK (Septentrio Mosaic-X5), integrated sensors, CAN protocol      | Exceptional precision, advanced EMI resistance, high update rate (100Hz)   | High cost, more complex integration              |

# Results and Deliverables

The team recommends the following GNSS selections:
        
   - Project Quiver PT3 will be designed in a way that **Holybro DroneCAN H-RTK F9P Rover** and **Systork Wren Mini**  may be integrated, these will be ordered first and tried, these will then also be experimented during the decentralized test campaign
   - These options provide reliability and precision for operational scalability.
   - **Mateksys M9N-G4-3100** will be used as secondary backup GNSS
   - Use test campaign to finalise combinations and selections.
       
# References

-   [Project Quiver - GNSS System Options](https://docs.google.com/presentation/d/18Xd6aV_LBQb4nk88YzbedioLXHt0NIIe_R7d0gYp22A/edit#slide=id.p)
    
-   Holybro GNSS Systems Documentation: [Holybro Website](https://holybro.com/collections/h-rtk-gps)
    
-   SparkFun RTK Documentation: [SparkFun RTK Kits](https://www.sparkfun.com)
    
-   Drotek GNSS Product Documentation: [Drotek GNSS](https://drotek.com)
    
-   Mateksys Product Page: [Mateksys GNSS Modules](https://www.mateksys.com)
    
-   Systork Wren Mini RTK GNSS Module: [Systork Product Page](https://www.systork.io)
    
-   3DR Mosaic-X5 Documentation: [3DR Mosaic-X5](https://store.3dr.com/mro-mosaic-x5-can-gps/)
