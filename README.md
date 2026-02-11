# Project Quiver

![Project Quiver PT3](docs/images/quiver_wide-angle.jpg)

**An open-source, modular quadcopter platform for developers and operators.**

Project Quiver is a 25 kg MTOW drone with 5-8 kg payload capacity, three hot-swappable attachment interfaces, and a distributed electronics architecture. Built for reliability, field serviceability, and customization.

Developed by [Arrow Air](https://arrowair.com) and released under the CERN Open Hardware Licence.

## Key Features

- **Modular payload system** — Three quick-release interfaces (bottom, left, right) for mission equipment
- **Dual GNSS with RTK** — Centimeter-level positioning with backup redundancy
- **Distributed PCB architecture** — Four custom boards that can be individually serviced
- **25-31 min hover endurance** — Tattu 14S 30Ah smart battery with Hobbywing X6 Plus propulsion
- **ArduPilot firmware** — Standard QGroundControl/Mission Planner compatibility
- **Weatherproof design** — Sealed cockpit with rain canopies and drip-proof geometry

## Documentation

📖 **[Full Documentation](https://arrowair.com/docs/quiver)** — Platform overview, capabilities, and roadmap

The `docs/` folder is hosted on the [Arrow website](https://arrowair.com/docs/quiver).

| Resource | Description |
|----------|-------------|
| [Assembly Guides](https://arrowair.com/docs/quiver/pt3-assembly-guides) | Step-by-step build instructions |
| [Engineering Reports](https://arrowair.com/docs/quiver/Engineering-Reports) | Technical details for each prototype |

## Repository Structure

```
project-quiver/
├── docs/                    # Documentation (hosted at arrowair.com/docs/quiver)
├── src/
│   ├── quiver/              # CAD assembly — build123d Python package
│   ├── pcb/                 # KiCad PCB designs (4 custom boards)
│   ├── printing/            # 3D print profiles and settings
│   └── manufacturing/       # DXFs and cut sheets for CNC/laser
├── flight-test/             # Historical flight test logs
└── task-grant-bounty/       # Bounty and grant task specifications
```

### CAD Assembly

The CAD source is a [build123d](https://github.com/gumyr/build123d) Python package that composes STEP files into the full drone assembly. This enables programmatic CAD generation and version-controlled mechanical design. See [`src/quiver/`](src/quiver/) for details.

## Getting Started

**Want to build one?** Start with the [Assembly Guides](https://arrowair.com/docs/quiver/pt3-assembly-guides).

**Want to develop attachments?** Check out:
- [Possible Attachment List](task-grant-bounty/equipment/attachment/0001-possible_attachment_list/information-note.md)
- [Priority Attachment Requirements](task-grant-bounty/equipment/attachment/0002-detailed_attachment_requirement_for_bounty/information-note.md)

**Want a dev-kit?** Dev-kit drones are available for loan to developers with promising projects. Join the [Arrow Discord](https://discord.gg/arrow) to learn more.

## Contributing

We welcome contributions across:
- **Attachments** — Design new payloads for the modular interfaces
- **Electronics** — PCB improvements and new sensor integrations  
- **Mechanical** — Structural design and manufacturing optimization
- **Software** — ArduPilot configs, companion computer features, tooling
- **Documentation** — Guides, tutorials, and translations

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Community

- **Discord** — [discord.gg/arrow](https://discord.gg/arrow)
- **DAO Forum** — [dao.arrowair.com](https://dao.arrowair.com)
- **Flight Tracking** — [project-flight-tracking.vercel.app](https://project-flight-tracking.vercel.app/)

## License

[CERN Open Hardware Licence Version 2 - Strongly Reciprocal (CERN-OHL-S)](LICENSE)
