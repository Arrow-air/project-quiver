# Status  

`Valid`


# Project Description

The objective is to select a flight controller that supports ongoing development with minimal complexity while preserving the option for high-reliability upgrades. Constraints include cost, integration effort, and the need for standard compute and communication interfaces. Future-proofing and access to advanced features such as redundant IMUs or Ethernet were also considered in the selection process.



# Methodology

## Constraints and Decision Criteria

- **Cost Awareness**: Priority given to low-cost options during prototyping phase. It is also possible to support several flight controllers in varying prices, which will allow customers to select the best flight controller according to their needs 
- **Modularity**: Preference for controllers compatible with current and future PCB layouts.  
- **Sensor Quality and Loop Frequency**: Higher-grade sensors and faster control loops favored.  
- **Compute Distribution**: Systems that handle mission logic on the FCU, with optional companion computer for compute-heavy tasks.  
- **Processor Consistency**: Most FCUs under consideration share the same STM32H7-class processor.  
- **Ethernet Requirement**: It'll be used for peripherals. 


## Flight Controller Options

| Flight Controller     | Key Features                                              | Pros                                                      | Cons                                                  |
|-----------------------|-----------------------------------------------------------|-----------------------------------------------------------|-------------------------------------------------------|
| Pixhawk 6X / 6X Pro   | Expanded IO, Pro has better sensors & loop performance    | Robust, extensible, familiar system                       | Higher cost, Pro version significantly more expensive |
| CubePilot+       | Redundant FCs and more IMUs                               | Feature-rich, aerospace-grade                             | ~$200 more expensive than 6X Pro                      |
| uAvionix George       | Manned aircraft-grade with FAA cert-ready architecture   | Extensive integration potential                           | Overkill for current unmanned use                     |
| Auterion Skynode      | Full-stack system with CC and LTE                         | Plug-and-play, high-end                                    | Overkill for current needs, less transparency         |
| Mateksys H743-SLIM V3 | Minimalistic, low-cost, ArduPilot compatible              | Extremely cheap, small form factor                        | Manual wiring required, reliability concerns          |
| Pix32 V6              | Modular design, no onboard Ethernet                      | Affordable, flexible PCB integration                      | Requires adapter for Ethernet, breakout board needed  |


# Results and Deliverables

The team recommends the following course of action:

1. **Short-term**: Use **Pix32 V6** during prototyping due to its cost-efficiency and ease of integration with custom PCBs.
   - Breakout board is simpler than alternatives.
   - Ethernet not natively available but can be added via serial-to-Ethernet adapter (e.g., [DroneNet](https://ardupilot.org/copter/docs/common-botblox-dronenet.html#common-botblox-dronenet)).

2. **Long-term**: Update PCB design for compatibility with **Pixhawk 6X** or **Cube Orange+** to enable use of redundant sensors, more robust compute, and better loop performance.
   - Pixhawk 6X Pro and Cube Orange+ provide access to additional IMUs and higher control frequency (150 Hz vs 100 Hz).
   - Algorithms run identically across supported STM32H7 platforms, allowing code continuity.


# References

- [Project Quiver - Flight Control Options (prepared by 21stCenturyAlex](https://docs.google.com/presentation/d/1L3D2KNSmWAnT7PEegutxZOMr4_4M_DaEUc1flgLqVl8/edit?slide=id.g22905c65f43_0_11#slide=id.g22905c65f43_0_11)  
- [Pix32 V6 Product Page](https://holybro.com/products/pix32-v6?variant=43020083527869)  
- [BotBlox DroneNet Adapter](https://ardupilot.org/copter/docs/common-botblox-dronenet.html#common-botblox-dronenet)  
- [Meeting Notes from 25/05/08](https://github.com/Arrow-air/project-quiver/wiki/05-2025)  


---
