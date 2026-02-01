"""Top-level Quiver drone assembly.

Composes all subassemblies into the complete drone. Run this file
directly to export the full assembly or view it in ocp-vscode.

Usage:
    python -m quiver.assembly              # export full assembly STEP
    python -m quiver.assembly --show       # open in ocp-vscode viewer
"""

import argparse
from pathlib import Path

from build123d import Compound, export_step

from quiver.frame.assembly import make_assembly as frame
from quiver.arms.assembly import make_assembly as arms
from quiver.landing_gear.assembly import make_assembly as landing_gear
from quiver.enclosure.assembly import make_assembly as enclosure
from quiver.electronics.assembly import make_assembly as electronics
from quiver.attachments.interfaces.assembly import make_assembly as attachments

EXPORT_DIR = Path(__file__).parent.parent / "export"


def make_assembly() -> Compound | None:
    """Build the complete Quiver drone assembly."""
    subassemblies = [
        frame(),
        arms(),
        landing_gear(),
        enclosure(),
        electronics(),
        attachments(),
    ]
    children = [s for s in subassemblies if s is not None]
    if not children:
        return None
    return Compound(children=children)


def export(output: Path | None = None) -> Path:
    """Export the full assembly as a STEP file."""
    assembly = make_assembly()
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
    args = parser.parse_args()

    if args.show:
        from ocp_vscode import show

        assembly = make_assembly()
        if assembly is None:
            print("No parts loaded. Add STEP files to subassembly steps/ directories.")
        else:
            show(assembly)
    else:
        out = export(args.output)
        print(f"Exported assembly to {out}")
