"""Top-level Quiver drone assembly.

Composes BOM categories (airframe structure, supporting structure,
equipment) into the complete drone. Run this file directly to export
the full assembly or view it in ocp-vscode.

Usage:
    python -m quiver.assembly              # export full assembly STEP
    python -m quiver.assembly --show       # open in ocp-vscode viewer
"""

import argparse
from pathlib import Path

from build123d import Compound, export_step

from quiver.gps import DEFAULT_PRIMARY_GPS, PRIMARY_GPS_OPTIONS, validate_primary_gps

from quiver.airframe_structure.assembly import make_assembly as airframe_structure
from quiver.supporting_structure.assembly import make_assembly as supporting_structure
from quiver.equipment.assembly import make_assembly as equipment
from quiver.harness.assembly import make_assembly as harness

EXPORT_DIR = Path(__file__).parent.parent / "export"


def make_assembly(primary_gps: str = DEFAULT_PRIMARY_GPS) -> Compound | None:
    """Build the complete Quiver drone assembly."""
    validate_primary_gps(primary_gps)
    subassemblies = [
        airframe_structure(),
        supporting_structure(primary_gps=primary_gps),
        equipment(primary_gps=primary_gps),
        harness(),
    ]
    children = [s for s in subassemblies if s is not None]
    if not children:
        return None
    return Compound(children=children, label="Quiver Drone")


def export(output: Path | None = None, primary_gps: str = DEFAULT_PRIMARY_GPS) -> Path:
    """Export the full assembly as a STEP file."""
    assembly = make_assembly(primary_gps=primary_gps)
    if assembly is None:
        raise RuntimeError(
            "No STEP files found in any subassembly. "
            "Export parts from Fusion 360 and place them in the "
            "appropriate steps/ directories."
        )
    EXPORT_DIR.mkdir(exist_ok=True)
    out = output or EXPORT_DIR / "quiver_assembly.step"
    export_step(assembly, str(out))
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quiver drone assembly")
    parser.add_argument("--show", action="store_true", help="Open in ocp-vscode viewer")
    parser.add_argument("-o", "--output", type=Path, help="Output STEP file path")
    parser.add_argument(
        "--gps", choices=PRIMARY_GPS_OPTIONS, default=DEFAULT_PRIMARY_GPS,
        help="Primary GPS receiver and matching mount (default: here4)",
    )
    args = parser.parse_args()

    if args.show:
        from ocp_vscode import show

        assembly = make_assembly(primary_gps=args.gps)
        if assembly is None:
            print("No parts loaded. Add STEP files to subassembly steps/ directories.")
        else:
            show(assembly, deviation=0.5, angular_tolerance=0.5)
    else:
        out = export(args.output, primary_gps=args.gps)
        print(f"Exported assembly to {out}")
