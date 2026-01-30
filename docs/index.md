---
title: Project Quiver
description: Introduction to Project Quiver
---

# Project Quiver

![Project Quiver PT3](./images/quiver_wide-angle.jpg)

Project Quiver is an open-source, multi-purpose quadcopter platform designed for reliability, modularity, and adaptability. Developed by [Arrow Air](https://arrowair.com), Quiver provides a complete dev-kit drone that can be used as-is with our current attachment library for operations or as a foundation for custom modifications, attachments, and features.

The platform supports a maximum takeoff weight of 25 kg with 5-8 kg of payload capacity, three modular attachment interfaces, and a distributed electronics architecture built around custom PCBs. It runs ArduPilot firmware and is designed for straightforward assembly, maintenance, and field servicing.

## Key Capabilities

- **Modular payload system** -- Three quick-release attachment interfaces (bottom, left, and right) allow hot-swapping of mission equipment without disturbing the main electronics. Each interface includes a dedicated Attachment Interface PCB that provides regulated power and data lines (CAN, Ethernet) to the payload 
- **Dual GNSS with RTK** -- Centimeter-level positioning via Holybro DroneCAN H-RTK F9P or Here4, with a Mateksys M9N-G4-3100 backup module for redundancy
- **Radar altimeter** -- Nanoradar NRA15 for accurate altitude sensing and terrain following
- **Weatherproof enclosure** -- Sealed cockpit with rain canopies, drip-proof structures, and reverse-slope geometry for dust and water resistance
- **Distributed PCB architecture** -- Four custom boards (Battery, Main, Flight Controller, and Attachment Interface) that can be individually serviced or replaced
- **Companion computer support** -- Optional Raspberry Pi integration via Ethernet and CAN for computer vision, autonomy algorithms, data logging, and custom features
- **25-31 minute hover endurance** -- Powered by a Tattu 14S 30 Ah smart battery with four Hobbywing XRotor X6 Plus propulsion units

## Platform Overview

Quiver has been developed across three prototype iterations and a production dev-kit, each building on lessons from the previous:

| | PT1 | PT2 | PT3 | Dev-kit (Current) |
|---|---|---|---|---|
| Flight Controller | Pixhawk 6X | Mateksys H743 | Pix32 V6 | Pix32 V6 |
| PCB Strategy | Repurposed single board | Custom main PCB | Four custom PCBs | Updated connector layout and bus bar integration |
| Payload Interfaces | 1 | 1 | 3 | 3 |
| Structure | 3D printed + aluminum plates | Aluminum plates, tubes & rivets | Aluminum plates, tubes & rivets | Thinner aluminum for weight savings |
| Landing Gear | Fixed | Fixed | Fixed | Detachable |
| Obstacle Avoidance | Downward facing radar only | Downward facing radar only | Downward facing radar only | 360 LiDAR + forward-facing and downward-facing radar |
| Companion Computer | None | Optional Raspberry Pi | Optional Raspberry Pi with Ethernet | Optional Raspberry Pi with Ethernet |
| Communications | CAN, Serial, Analog | CAN, Serial, Analog | CAN, Serial, Analog, Ethernet | CAN, Serial, Analog, Ethernet |
| Power Management | Arduino contactor | SSR with pre-charge | Battery PCB with SOC, temp monitoring, & kill switch | Battery PCB with SOC, temp monitoring, & kill switch |
| Weatherproofing | No | No | No | Yes |

The airframe uses laser-cut aluminum plates and tubes for the primary structure, carbon fiber tubes for motor arms and landing gear, and 3D-printed components for enclosures and adapters. Motor arms fold for transport, bringing the platform down to a case-portable size.

All CAD files (Fusion 360 / STEP), KiCAD PCB designs, ArduPilot configurations, and assembly documentation are available in the [GitHub repository](https://github.com/Arrow-air/project-quiver).

## Current Status

PT3 is the current production design. The airframe, electronics, and harnessing are finalized, and the platform has been regularly tested in both the US and Germany. It is considered stable enough for developers and businesses to build on with some support.

The DAO has funded the build of 8 drones in the US and 4 in Germany to serve as dev-kits. These units can be loaned, sold, or given away to support ecosystem growth and further testing and refinement of the core platform. Assembly guides and documentation are complete, and the platform uses standard QGroundControl or Mission Planner for ground control.

## Roadmap

With the basic design nearing completion, direct platform development is shifting toward maintenance and support. The primary focus going forward is growing a community-driven attachment ecosystem around the platform. Quiver's three modular payload interfaces are designed to let developers build specialized mission equipment -- cameras, sensors, delivery mechanisms, sprayers, and tools we haven't imagined yet -- without needing to modify the core drone.

To kick-start that ecosystem, the project will use several incentive programs:

- **Dev-kit loans** -- Drones loaned to developers with promising attachment or integration ideas, so they can build and test without purchasing hardware upfront
- **Contests** -- Design challenges for specific attachment categories, with prizes for the best solutions
- **Grants and bounties** -- Funded tasks for building, testing, and documenting new attachments and features

On the platform side, the main remaining efforts are scaling up manufacturing through a network of community manufacturers and expanding onboard autonomy with stronger companion computer integration and improved obstacle avoidance.

## Getting Involved

The biggest near-term opportunity is attachment development -- designing, building, and testing new payloads that plug into Quiver's three modular interfaces. If you have an idea for a mission attachment, you can apply for a dev-kit loan, enter a contest, or pick up a grant or bounty.

Contributors are also welcome across the core platform: electronics, structural design, flight controller configuration, flight testing, and tooling. All work is coordinated through the GitHub repository, the Arrow Discord, and the [DAO forum](https://dao.arrowair.com).

For technical details on each prototype, see the [Engineering Reports](./Engineering-Reports/).
