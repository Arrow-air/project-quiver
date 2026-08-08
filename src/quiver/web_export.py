"""Export per-subassembly GLB models for the docs-site 3D viewer.

Each BOM subcategory is exported as its own binary glTF file plus a
manifest.json describing the BOM tree. The website's QuiverModelViewer
component fetches the manifest and lazy-loads the GLBs, so visitors can
toggle subassemblies on and off. Mesh names inside each GLB carry the
part names (e.g. "3111-Motor") for hover identification.

Raw tessellated GLBs are large; if node is available the exporter pipes
each file through gltf-transform (weld, join primitives per mesh,
simplify, Draco) for a ~30x size reduction. The viewer requires the
Draco-compressed output, so install node before regenerating for real.

Usage:
    python -m quiver.web_export                  # -> docs/3D-Model/models/
    python -m quiver.web_export -o /tmp/models   # custom output dir
    python -m quiver.web_export --skip-optimize  # raw GLBs (debugging only)
"""

import argparse
import json
import shutil
import struct
import subprocess
import tempfile
from pathlib import Path

from build123d import export_gltf

# Tessellation: coarser than the CAD export, sized for web viewing.
_LINEAR_DEFLECTION = 1.0  # mm
_ANGULAR_DEFLECTION = 0.8  # rad

# gltf-transform pipeline: join per-face primitives so simplification and
# Draco work on whole meshes (vendor B-reps export thousands of tiny
# per-face primitives otherwise). --keep-meshes preserves mesh identity
# and names; simplify error is a fraction of the scene span.
_OPTIMIZE_STEPS = [
    ("weld", []),
    ("join", ["--keep-meshes"]),
    ("simplify", ["--ratio", "0.6", "--error", "0.001"]),
    ("draco", []),
]

# (category label, category BOM, subassembly label, BOM, module path)
_SUBASSEMBLIES = [
    ("Airframe Structure", 1000, "Plates", 1100, "quiver.airframe_structure.plates.assembly"),
    ("Airframe Structure", 1000, "Beams", 1200, "quiver.airframe_structure.beams.assembly"),
    ("Airframe Structure", 1000, "Landing Gear", 1300, "quiver.airframe_structure.landing_gear.assembly"),
    ("Airframe Structure", 1000, "Motor Arm", 1400, "quiver.airframe_structure.motor_arm.assembly"),
    ("Supporting Structure", 2000, "Attachment Interface", 2100, "quiver.supporting_structure.attachment_interface.assembly"),
    ("Supporting Structure", 2000, "Battery Slider", 2200, "quiver.supporting_structure.battery_slider.assembly"),
    ("Supporting Structure", 2000, "Equipment Mount", 2300, "quiver.supporting_structure.equipment_mount.assembly"),
    ("Supporting Structure", 2000, "Cockpit Enclosure", 2400, "quiver.supporting_structure.cockpit_enclosure.assembly"),
    ("Equipment", 3000, "Propulsion", 3100, "quiver.equipment.propulsion.assembly"),
    ("Equipment", 3000, "Peripheral", 3200, "quiver.equipment.peripheral.assembly"),
    ("Equipment", 3000, "PCB", 3300, "quiver.equipment.pcb.assembly"),
    ("Equipment", 3000, "Battery", 3400, "quiver.equipment.battery.assembly"),
    ("Harness", 4000, "Harness", 4000, "quiver.harness.assembly"),
]

_DEFAULT_OUTPUT = Path(__file__).parent.parent.parent / "docs" / "3D-Model" / "models"


def _slug(label: str) -> str:
    return label.lower().replace(" ", "_")


def _optimize(path: Path) -> bool:
    """Run the gltf-transform pipeline on a GLB in place. False if no node."""
    if shutil.which("npx") is None:
        return False
    current = path
    with tempfile.TemporaryDirectory() as tmp:
        for i, (cmd, flags) in enumerate(_OPTIMIZE_STEPS):
            out = Path(tmp) / f"step{i}.glb"
            subprocess.run(
                ["npx", "-y", "@gltf-transform/cli", cmd, str(current), str(out), *flags],
                check=True, capture_output=True,
            )
            current = out
        shutil.copyfile(current, path)
    return True


def _rename_nodes_from_meshes(path: Path) -> None:
    """Copy mesh names onto their glTF nodes, in place.

    OCC names nodes with XCAF label paths ("=>[0:1:1:3]") but names
    meshes after the parts ("3111-Motor"). three.js names scene objects
    after the NODE, so the viewer would show the label paths on hover.
    """
    raw = path.read_bytes()
    magic, version, _ = struct.unpack_from("<4sII", raw, 0)
    assert magic == b"glTF", path
    json_len, json_type = struct.unpack_from("<I4s", raw, 12)
    assert json_type == b"JSON", path
    gltf = json.loads(raw[20:20 + json_len])

    meshes = gltf.get("meshes", [])
    for node in gltf.get("nodes", []):
        mesh_name = meshes[node["mesh"]].get("name") if "mesh" in node else None
        if mesh_name:
            node["name"] = mesh_name

    body = json.dumps(gltf, separators=(",", ":")).encode()
    body += b" " * (-len(body) % 4)  # GLB chunks are 4-byte aligned
    rest = raw[20 + json_len:]
    out = struct.pack("<4sII", b"glTF", version, 20 + len(body) + len(rest))
    out += struct.pack("<I4s", len(body), b"JSON") + body + rest
    path.write_bytes(out)


def export_models(output_dir: Path, optimize: bool = True) -> dict:
    """Export all subassembly GLBs and return the manifest dict."""
    import importlib

    output_dir.mkdir(parents=True, exist_ok=True)
    categories: dict[str, dict] = {}
    optimized = True

    for cat_label, cat_bom, label, bom, module_path in _SUBASSEMBLIES:
        module = importlib.import_module(module_path)
        assembly = module.make_assembly()
        if assembly is None:
            print(f"skip {label}: no parts loaded")
            continue
        filename = f"{bom}_{_slug(label)}.glb"
        out = output_dir / filename
        export_gltf(
            assembly, str(out), binary=True,
            linear_deflection=_LINEAR_DEFLECTION,
            angular_deflection=_ANGULAR_DEFLECTION,
        )
        if optimize:
            optimized = _optimize(out) and optimized
        _rename_nodes_from_meshes(out)
        size = out.stat().st_size
        print(f"{filename}: {size / 1e6:.2f} MB")
        cat = categories.setdefault(cat_label, {"label": cat_label, "bom": cat_bom, "models": []})
        cat["models"].append({"label": label, "bom": bom, "file": filename, "bytes": size})

    if optimize and not optimized:
        print("WARNING: npx not found - GLBs are raw (huge, no Draco). "
            "Install node and re-run before committing.")

    manifest = {
        "generated_by": "python -m quiver.web_export",
        "units": "mm",
        "draco": optimize and optimized,
        "categories": list(categories.values()),
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export web GLB models")
    parser.add_argument("-o", "--output", type=Path, default=_DEFAULT_OUTPUT,
                        help="output directory (default: docs/3D-Model/models/)")
    parser.add_argument("--skip-optimize", action="store_true",
                        help="skip the gltf-transform pipeline (debugging only)")
    args = parser.parse_args()

    export_models(args.output, optimize=not args.skip_optimize)
    print(f"Manifest written to {args.output / 'manifest.json'}")
