# Fusion v148 mechanical sync — draft review

Source: `Quiver_PT3_Drone_Assembly` v148, saved July 30, 2026 at 17:55:10 UTC.
Compared with repository main `ef316bc9f4e9e001dd5421f8070e54f3180f1600`.
The read-only export was taken September 18, 2026; the Fusion design was not saved
or modified. This is a review snapshot, **not a manufacturing release**.

## Scope

| Part | Change from repository STEP | Fusion reference |
| --- | --- | --- |
| 2311 main PCB adapter | Threaded inserts and screws replace snap-in pins; updated rubber spacers | `New_Main_PCB_Adapter_0226_2`, v4 |
| 2313 battery-PCB cover | Envelope depth 44.09 → 27.35 mm; solid volume −10.94% | `UPDATED_2313 - BCPCBCover.f3d`, v1 |
| 2321 sensor mount | Same envelope; detail geometry changes, volume +0.79% | In-document component |
| 2411 enclosure | Envelope 330.19 × 347.39 × 93.00 → 330.19 × 319.25 × 91.00 mm | `UPDATED_2411-MainEnclosure`, v3 |
| 2412 top cap | Envelope 306.60 × 306.66 × 50.31 → 319.20 × 309.16 × 54.85 mm | `UPDATED_2412-TopCap.f3d`, v1 |
| 2341 PPP/beacon mount | Old bracket replaced by the 79.19 × 79.19 × 8.00 mm mounting board | `2340-PPP, Beacon_mounting_board_v3`, v12 |
| 3200 peripherals, 3310 main PCB | Eight parts moved to their Fusion occurrence placement (see below) | `3000-Equipment` occurrences |

![Before and after printable bodies](assets/fusion-v148-comparison.png)

Dimensions are axis-aligned CAD envelopes, not manufacturing tolerances. Volume
changes are geometric measurements, not weight estimates. Plates, compared cockpit
beams, battery slider, and attachment spacers match the existing STEP geometry and
are intentionally unchanged. GPS changes are separate.

## PPP/beacon mount: replacement, not an addition

The first draft of this PR added the mounting board as a new part (2342) next to
the old 2341 bracket, because both are visible in the Fusion master. That was
wrong. As placed in v148 the two parts overlap by about 990 mm³, and the
relocated PPP adapter overlaps the old bracket, so they cannot both be built.
The published `2341.stl` and Step 22 of the Manufacturing Guide already show the
board as part 2341 (the STL matches the board within 0.008% volume); only the
2341 STEP source was stale. The board STEP now replaces it, and the 2342 part,
BOM line, and duplicate STL are gone. The old bracket in the Fusion master
looks like a leftover that should be hidden or deleted there.

## Equipment placement (review follow-up, October 2026)

Erick's review flagged three peripherals. A check of every 3200 part against the
v148 occurrences found four more, mostly side effects of the parts this PR
updates, and the main PCB floated above the new adapter. Each correction
reproduces the Fusion occurrence transform; after the move, repository and
Fusion geometry agree to within 0.06 mm.

| BOM (Fusion) | Part | Was | Now |
| --- | --- | --- | --- |
| 3260 (3231) | Push button | Right (+X) side, 2 mm high, inside the new 2411 wall | Left (−X) side of the front face, clear of the enclosure |
| 3280 (3223) | SIYI HM30 air unit | Component frame, not rotated | Rotated 180° about Z |
| 3290 (3212) | Nanoradar MR82 | Component frame: upside down, tilted 5°, into the 2321 mount | Rotated 180°, tilt removed, clear of the mount |
| 3210 (3211) | RPLidar S2L | 4 mm low, inside the new 2412 top cap | Seated in the top-cap slot |
| 3201 (3271) | PPP adapter | Old bracket position | On the 2341 board (37 mm move) |
| 3202 (3261) | Remote ID beacon | Old bracket position | On the 2341 board (17 mm move) |
| 3220 (3213) | NRA15 radar altimeter | 5 mm off in X | Fusion position |
| 3310 (3310) | Main PCB | 7.4 mm above the adapter | Resting on the adapter, where its screws reach |

The repository BOM numbers differ from the Fusion component numbers in this
subassembly; the first column lists both. Antennas and camera already matched.
A regression test now checks the world bounds and center of mass of all ten
peripherals and the main PCB board against the recorded Fusion placements.

## Placement and hardware

The adapter's native export requires a **−7.85 mm Z translation**, measured from
the Fusion occurrence, replacing the old +13.15 mm correction. The other five
updated bodies already contain their world placement. Independent source bounds,
occurrences, linked versions, and file hashes are recorded in
[the provenance manifest](../src/quiver/fusion-mechanical-provenance.json).
Regression tests compare printable-body world bounds with those measurements.

The adapter STEP contains 34 solids, including 12 screws, 16 inserts, and five
rubber spacers. Only its largest solid is the printable adapter. The existing BOM
and Step 6 already describe 16 short inserts (FAST-024) and five rubber spacers
(FAST-033); the 12 modeled screws are part of the existing FAST-014 allocation,
not 12 additional purchases. Hardware names in the source model disagree on
insert length; they are not procurement authority. The BOM specifications remain
unchanged pending physical confirmation.

## Print files and review gates

The repository is a mixed snapshot: several existing, watertight manufacturing
STLs already have the revised envelopes even though their STEP sources were old.
The existing 2311, 2313, 2321, 2341, 2411, and 2412 STLs are therefore **not overwritten**.
All six meshes pass closed-surface and consistent-winding checks.
Against the source Fusion body measurements, their volume differences are below
0.08% and their maximum bound differences are below 0.014 mm. Recorded results
and file hashes are in [print mesh checks](print-mesh-checks.json). These checks
support retaining the existing files; they do not prove exact surface equivalence
or physical fit.

- **Correction: the existing 2321 STL is not established to be stale.** Its volume
  is approximately 63,337 mm³; Fusion records 63,327 mm³ and the valid imported
  STEP solid measures 63,332 mm³. The earlier 62,450 mm³ figure came from the
  defective generated mesh, not the STEP solid. The STEP-to-STL exporter skipped
  geometry; that trial was discarded. Keep the existing watertight STL. A direct
  Fusion export remains the preferred way to establish exact revision provenance,
  but these measurements are not evidence that the existing print file is wrong.
- Confirm revision provenance for retained meshes with the revised sources before a new
  print release. They remain the existing manufacturing files, not newly validated
  exports from this PR.
- Confirm adapter insert lengths and physical stack-up against the current build.
- Review enclosure/hinge/latch fit and sensor clearance; the automated tests check
  source placement and assembly integrity, not every physical interface.

## Validation

With Python 3.12 and `src/constraints.txt` installed:

```bash
PYTHONPATH=src python -m pytest src/tests/ -q
PYTHONPATH=src python -m quiver.bom render --check
PYTHONPATH=src python -m quiver.assembly -o /tmp/quiver-mechanical.step
```

The full-assembly count changes from 1,242 to 1,260 solids: +18 in the adapter
assembly. The outer drone envelope is unchanged.
