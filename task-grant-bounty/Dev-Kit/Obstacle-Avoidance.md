# Obstacle Avoidance System Overview

# Status

`Author: ZeynepB`

`Status: Valid`

`Revision History: v1.1 (2026-08-29) — QGB-02 testing roadmap, Texas Baseline candidate, S2L dropout notes`

`Replacement Log: None`

`Reference: [QGB-02](https://github.com/Arrow-air/project-quiver/issues/203), [OA Testing Roadmap](../../flight-test/OA/testing-roadmap.md)` 

# Project Description

This information note describes the current obstacle avoidance (OA) architecture implemented on Project Quiver, including sensor configuration, software integration, algorithm selection, and baseline parameterization. The system is under active development and tuning; values and behaviors described here represent the current validated state at the time of writing.

# Methodology

Project Quiver employs a multi-sensor proximity architecture to support obstacle detection and avoidance across varying environmental conditions. Sensor data is fused through ArduPilot's proximity database and fed into the BendyRuler obstacle avoidance framework. The current parameter set was derived from field tuning in Germany and is validated primarily for low-speed operations in cluttered environments.

ArduPilot integration for the RPLidar S2L required a custom firmware build, as the sensor is not natively supported upstream. All avoidance behavior described here assumes operation on the Quiver-custom ArduPilot firmware.

## Sensors Used for Obstacle Avoidance

### RPLidar S2L — 360° Top-Mounted LiDAR
- **Coverage:** 360° horizontal field of view
- **Effective range:** up to ~18 m
- **Primary role:** Horizontal obstacle detection and short-range avoidance
- **Usage:** Primary input to the proximity database used by the BendyRuler algorithm

The top-mounted RPLidar S2L provides high-resolution, near-field spatial awareness and serves as the primary proximity sensor for obstacle avoidance in tree-dense or cluttered environments. Its omnidirectional coverage enables continuous monitoring of lateral and rear sectors during both manual and autonomous flight.

### NanoRadar MR82 — Forward-Facing Radar
- **Coverage:** Forward sector
- **Effective range:** up to ~30 m
- **Primary role:** Forward obstacle detection under degraded visual conditions
- **Usage:** Supplemental forward obstacle awareness

The forward-facing radar extends obstacle detection capability beyond LiDAR limits, particularly in conditions where optical or laser-based sensing may degrade (e.g., rain, dust, partial occlusion). Radar data contributes primarily to early forward detection during higher-speed flight.

### Altitude Sensing (Barometer + Rangefinder)
- **Primary role:** Vertical position estimation
- **Usage:** Low-altitude navigation, terrain clearance, and landing support

Altitude information is derived from a combination of barometric pressure sensing and range-based measurements. While not directly part of horizontal obstacle avoidance, accurate altitude estimation is critical when avoidance commands introduce vertical motion or when operating close to terrain.

## Software Integration and ArduPilot Modifications

At the time of integration, the RPLidar S2L is not natively supported by upstream ArduPilot. To enable full functionality, Project Quiver operates on a custom ArduPilot firmware build incorporating an in-house developed extension.

This extension is implemented as a targeted patch applied on top of the latest stable ArduPilot release, adding native support for the RPLidar S2L driver and registering it within the ArduPilot proximity sensor framework.

Key characteristics of the integration include:
- Based on the latest stable ArduPilot branch at the time of implementation
- Changes limited to sensor driver support and proximity interface integration
- No modification to core navigation, control, or obstacle avoidance algorithms
- Full compatibility with existing ArduPilot proximity handling and BendyRuler logic

**ArduPilot Pull Request:**
https://github.com/ArduPilot/ardupilot/pull/31663

All obstacle avoidance behavior described in this document assumes operation on the Quiver-custom ArduPilot firmware incorporating this patch. Behavior observed on unmodified upstream ArduPilot builds is not representative of the Dev-Kit configuration and is not supported for operational use.

The patch is maintained as a minimal overlay to simplify rebasing as ArduPilot evolves and to facilitate eventual upstream inclusion if accepted.

# Results and Deliverables

## Obstacle Avoidance Algorithm Configuration

Project Quiver currently utilizes the ArduPilot BendyRuler obstacle avoidance framework. BendyRuler evaluates candidate motion vectors and constrains vehicle movement based on obstacle data stored in a proximity database populated by onboard sensors.

### Obstacle Avoidance Mode
- `OA_TYPE = 1` — Enables proximity-based obstacle avoidance using supported sensors.

### Proximity Database Configuration

The proximity database aggregates obstacle detections over time and space, forming the basis for avoidance decisions.

| Parameter | Value | Description |
|--------|------|------------|
| `OA_DB_SIZE` | 100 | Maximum number of stored obstacle points |
| `OA_DB_QUEUE_SIZE` | 80 | Queue depth for incoming proximity data |
| `OA_DB_EXPIRE` | 3 s | Time after which unused obstacle points expire |
| `OA_DB_OUTPUT` | 3 | Output mode for obstacle data |
| `OA_DB_BEAM_WIDTH` | 10° | Angular width used for obstacle representation |
| `OA_DB_RADIUS_MIN` | 0.2 m | Minimum obstacle radius |
| `OA_DB_DIST_MAX` | 10 m | Maximum distance considered for obstacle storage |
| `OA_DB_ALT_MIN` | 0 m | Minimum altitude threshold for obstacle consideration |

This configuration emphasizes near-field obstacle awareness, consistent with low-altitude operations in cluttered environments. Restricting the maximum database distance reduces the influence of distant detections that are unlikely to affect immediate trajectory planning.

### BendyRuler Motion Constraints

| Parameter | Value | Description |
|--------|------|------------|
| `OA_BR_TYPE` | 1 | Enables BendyRuler avoidance method |
| `OA_BR_LOOKAHEAD` | 12 m | Forward projection distance for candidate paths |
| `OA_BR_CONT_RATIO` | 1.2 | Continuity weighting for path selection |
| `OA_BR_CONT_ANGLE` | 60° | Maximum allowed directional change |
| `OA_OPTIONS` | 1 | Enables basic obstacle avoidance features |

The selected lookahead distance represents a balance between reaction time and environmental density. Testing has shown that excessive lookahead values in cluttered environments may lead to delayed or overly aggressive avoidance behavior.

### Obstacle Margin Configuration

- `OA_MARGIN_MAX = 4 m`

The obstacle margin defines the minimum clearance maintained between the aircraft and detected obstacles. This value is intentionally set relatively low to allow escape and maneuverability within tree-dense environments where larger margins may prevent feasible path planning.

This margin setting is appropriate for:
- Low to moderate ground speeds
- Close-proximity navigation
- Controlled test environments with trained operators

For higher-speed autonomous missions, an increased margin may be required to account for vehicle inertia and braking distance, sensor latency and update rates, and accumulated navigation uncertainty. Dynamic margin scaling as a function of ground speed is under investigation as a future enhancement to expand the safe operational envelope.

## Parameter Baselines

Two parameter files are maintained for different operating environments:

| Baseline | File | Status | Environment |
|----------|------|--------|-------------|
| Germany | [`params-object-avoidance.param`](../../docs/Operations/firmware/parameters/params-object-avoidance.param) | Field-tuned (low-speed, tree-dense) | Cluttered / Germany site |
| Texas v1 | [`params-object-avoidance-texas-v1.param`](../../docs/Operations/firmware/parameters/params-object-avoidance-texas-v1.param) | **Candidate** — pending Phase 2 validation | Open field / Texas site |

See [OA-Texas-Baseline-v1.md](./OA-Texas-Baseline-v1.md) for the SITL exploration matrix and tuning rationale.

Validate any parameter file before upload:

```bash
python task-grant-bounty/Tools/OA-Analysis/compare_oa_params.py <path-to-param-file>
```

## Known Issue: S2L Flight Dropouts

The RPLidar S2L exhibits intermittent proximity data loss in flight that is not present on the ground. Symptoms, diagnostic steps, and log-analysis tooling are documented in [OA-S2L-Dropout-Investigation.md](./OA-S2L-Dropout-Investigation.md).

**Structured OA flight testing (Phases 1–4) is blocked until Phase 1 sensor checks pass without dropouts.**

## Flight Testing Status

A structured four-phase test roadmap is published in [`flight-test/OA/`](../../flight-test/OA/README.md), aligned with the [Arrow DAO forum roadmap](https://dao.arrowair.com/t/project-quiver-obstacle-avoidance-testing-roadmap/142).

| Phase | Focus | Status (2026-08-29) |
|-------|-------|---------------------|
| 1 | Sensor alignment, 360° yaw PRX check | Not started |
| 2 | Manual avoidance → Texas Baseline v1 validation | Not started |
| 3 | AUTO missions (≥ 95% success) | Not started |
| 4 | Germany tree-dense cross-validation | Not started |

SITL parameter exploration uses the environment documented in [SITL-Evaluation.md](./SITL-Evaluation.md). SITL informs parameter selection; it does not replace hardware validation.

## Recommended Operating Conditions

Until Texas Baseline v1 is flight-validated, use the Germany baseline with the following limits:

| Condition | Recommendation |
|-----------|----------------|
| Ground speed | ≤ 5 m/s in cluttered environments |
| Altitude | ≥ 5 m AGL for OA evaluation (reduce ground reflection) |
| Wind | Avoid OA AUTO missions above 8 m/s sustained |
| Payload | Verify PRX continuity with Brush-Bullet active before OA missions |
| Failsafe | SmartRTL for payload / dense-environment tests |

## Current Limitations and Development Status

- Obstacle avoidance performance is sensitive to ground speed, sensor update rate, and environmental density.
- The Germany parameter set is validated primarily for low-speed operations in cluttered environments.
- Texas Baseline v1 is a SITL-informed candidate; open-field flight validation is pending.
- High-speed avoidance behavior has not yet been fully characterized.
- Sensor fusion behavior between LiDAR and radar remains under evaluation.
- Vertical avoidance relies on altitude estimation and does not include independent vertical obstacle sensing.
- S2L in-flight dropouts remain under investigation (see above).

# Remarks

- OA log analysis tooling: [`task-grant-bounty/Tools/OA-Analysis/`](../Tools/OA-Analysis/information-note.md)
- Forum discussion: [Obstacle Avoidance Testing Roadmap](https://dao.arrowair.com/t/project-quiver-obstacle-avoidance-testing-roadmap/142)


