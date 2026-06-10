"""Shrink a vendor STEP file by dropping tiny solids — BEFORE first commit.

Vendor exports (especially KiCad PCB assemblies) carry hundreds of tiny
SMD component solids that bloat the file and are filtered out at load
time anyway (see quiver.common.load_step extract_solids). Run new vendor
files through this tool before committing them.

Do NOT run it on files already committed: git keeps the old blob in
history forever, so rewriting an existing file grows the repository for
every future clone. Measured on the existing fleet (June 2026), retrofit
savings were 0-13% — not worth the pack growth.

The tool only replaces the file if the re-imported result still matches
what the assembly code would have produced at runtime:

    reference = original file loaded with --runtime-min-volume filtering
                (use the min_solid_volume the assembly code passes for
                this file; 0 for files loaded unfiltered)
    candidate = original filtered at --min-volume, exported, re-imported

The file is replaced only when candidate center-of-mass and bounding box
match the reference within --tolerance (mm). Center-of-mass matters
because assembly modules position parts via part.center().

Usage:
    python src/tools/simplify_step.py FILE --min-volume 50
    python src/tools/simplify_step.py FILE --min-volume 1 --runtime-min-volume 0
"""

import argparse
import sys
import tempfile
from pathlib import Path

from build123d import export_step, import_step

sys.path.insert(0, str(Path(__file__).parent.parent))
from quiver.common import _flatten_solids  # noqa: E402


def _stats(compound):
    bb = compound.bounding_box()
    c = compound.center()
    return {
        "solids": len(compound.solids()),
        "center": (c.X, c.Y, c.Z),
        "bbox": (bb.min.X, bb.min.Y, bb.min.Z, bb.max.X, bb.max.Y, bb.max.Z),
    }


def _max_delta(a: tuple, b: tuple) -> float:
    return max(abs(x - y) for x, y in zip(a, b))


def simplify(path: Path, min_volume: float, runtime_min_volume: float, tolerance: float) -> bool:
    original_size = path.stat().st_size
    raw = import_step(str(path))

    reference = _flatten_solids(raw, min_volume=runtime_min_volume)
    ref = _stats(reference)

    filtered = _flatten_solids(raw, min_volume=min_volume)
    with tempfile.NamedTemporaryFile(suffix=".step", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    # Parametric curves are redundant (consumers recompute them) and
    # roughly double STEP file size.
    export_step(filtered, str(tmp_path), write_pcurves=False)

    candidate = _flatten_solids(import_step(str(tmp_path)), min_volume=0.0)
    new_stats = _stats(candidate)

    center_delta = _max_delta(ref["center"], new_stats["center"])
    bbox_delta = _max_delta(ref["bbox"], new_stats["bbox"])
    new_size = tmp_path.stat().st_size

    print(f"{path.name}:")
    print(f"  solids   {ref['solids']} -> {new_stats['solids']}")
    print(f"  center delta {center_delta:.4f} mm, bbox delta {bbox_delta:.4f} mm")
    print(f"  size     {original_size / 1e6:.1f} MB -> {new_size / 1e6:.1f} MB")

    if center_delta > tolerance or bbox_delta > tolerance:
        print(f"  SKIPPED: deltas exceed tolerance ({tolerance} mm), file unchanged")
        tmp_path.unlink()
        return False
    if new_size >= original_size:
        print("  SKIPPED: no size reduction, file unchanged")
        tmp_path.unlink()
        return False

    tmp_path.replace(path)
    print("  replaced")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("file", type=Path, help="STEP file to simplify in place")
    parser.add_argument("--min-volume", type=float, required=True,
                        help="drop solids with bounding-box volume below this (mm³)")
    parser.add_argument("--runtime-min-volume", type=float, default=None,
                        help="min_solid_volume the assembly code uses for this file "
                             "(defaults to --min-volume)")
    parser.add_argument("--tolerance", type=float, default=0.1,
                        help="max allowed center/bbox shift in mm (default 0.1)")
    args = parser.parse_args()

    runtime = args.min_volume if args.runtime_min_volume is None else args.runtime_min_volume
    ok = simplify(args.file, args.min_volume, runtime, args.tolerance)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
