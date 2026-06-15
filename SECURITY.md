# Security Policy

## Reporting a vulnerability

If you find a vulnerability that could be exploited remotely or through
crafted input — please do not open a public issue. Instead:

1. Use GitHub's
   [private vulnerability reporting](https://github.com/Arrow-air/project-quiver/security/advisories/new)
   for this repository, or
2. Contact the maintainers privately on the
   [Arrow Discord](https://discord.gg/arrow).

## Scope

In scope (privately, via the channels above):

- Companion computer software, the Quiver SDK, and tooling in this
  repository (e.g. log analyzers parsing untrusted flight logs)
- Telemetry, RF, and network interfaces (Ethernet, CAN, MAVLink
  configurations) where a remote party could influence the aircraft
- Firmware configurations that expose remotely abusable behavior

Not in scope — use the regular
[issue tracker](https://github.com/Arrow-air/project-quiver/issues):

- Mechanical/CAD design issues, documentation errors, and other defects
  that require physical access to matter
