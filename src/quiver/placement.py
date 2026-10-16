"""Recorded world poses of every placed part (checked by tests/test_placement.py).

part-poses.json holds one record per part instance: world bounds, the
volume-weighted centroid and reference vertices. The records were frozen
from the Fusion 360 v148 master when it was retired; after moving a part
on purpose, re-record it:

    python -m quiver.placement check           # compare the build with the records
    python -m quiver.placement record KEY ...  # re-record parts by key or label

Records of the GNSS receiver and mount carry the receiver option they
belong to (``primary_gps``); pass ``--gps holybro-f9p`` to check or record
that build (default: here4).
"""

import argparse
import json
import re
import sys
import zlib
from collections import defaultdict
from datetime import date
from pathlib import Path

import numpy as np

from quiver.gps import DEFAULT_PRIMARY_GPS, PRIMARY_GPS_OPTIONS

POSES_PATH = Path(__file__).parent / "part-poses.json"
_BOM_LABEL = re.compile(r"^(\d{4})[-_]")
PROBES = 16


def part_instances(assembly) -> dict[str, list]:
    """BOM-labelled part instances by label (a part's children are its own solids)."""
    out = defaultdict(list)

    def walk(node):
        if _BOM_LABEL.match(node.label or ""):
            out[node.label].append(node)
            return
        for child in node.children:
            walk(child)

    walk(assembly)
    return dict(out)


def centroid(shape) -> tuple[float, float, float]:
    """Volume-weighted centroid of the solids. Compound.center() weights by
    signed volume, so inverted solids in vendor STEPs would skew it."""
    solids = shape.solids()
    weights = [abs(solid.volume) for solid in solids]
    centers = [tuple(solid.center()) for solid in solids]
    total = sum(weights)
    return tuple(sum(w * c[axis] for w, c in zip(weights, centers)) / total for axis in range(3))


def probe_vertices(part, key: str, count: int = PROBES) -> list[list[float]]:
    """Reference vertices: half spread out (farthest-point), half seeded random,
    so asymmetric details are sampled too."""
    v = np.unique(np.round(np.array([tuple(p) for p in part.vertices()]), 6), axis=0)
    if len(v) <= count:
        return v.round(4).tolist()
    c = np.array(centroid(part))
    picked = [int(np.argmax(np.linalg.norm(v - c, axis=1)))]
    d = np.linalg.norm(v - v[picked[0]], axis=1)
    while len(picked) < count // 2:
        i = int(np.argmax(d))
        picked.append(i)
        d = np.minimum(d, np.linalg.norm(v - v[i], axis=1))
    taken = set(picked)
    rng = np.random.default_rng(zlib.crc32(key.encode()))
    picked += [int(i) for i in rng.permutation(len(v)) if int(i) not in taken][: count - len(picked)]
    return v[picked].round(4).tolist()


def measure(part, key: str) -> dict:
    box = part.bounding_box()
    return {
        "centroid_mm": [round(x, 4) for x in centroid(part)],
        "bounds_mm": [[round(x, 4) for x in box.min], [round(x, 4) for x in box.max]],
        "probes_mm": probe_vertices(part, key),
    }


def records_for(records: list[dict], assembly) -> list[dict]:
    """The records that apply to this build: a record tagged with a receiver
    option (``primary_gps``) applies only to that option's build."""
    gps = getattr(assembly, "primary_gps", DEFAULT_PRIMARY_GPS)
    return [r for r in records if r.get("primary_gps") in (None, gps)]


def match(records: list[dict], instances: dict[str, list]) -> list[tuple[dict, object]]:
    """Pair each record with the built instance of its label nearest its centroid."""
    pairs, used = [], set()
    for record in records:
        options = [p for p in instances.get(record["label"], []) if id(p) not in used]
        if not options:
            pairs.append((record, None))
            continue
        want = np.array(record["centroid_mm"])
        part = min(options, key=lambda p: np.linalg.norm(np.array(centroid(p)) - want))
        used.add(id(part))
        pairs.append((record, part))
    return pairs


def deviation(record: dict, part) -> float:
    """Largest distance from a recorded probe to the nearest built vertex (mm)."""
    v = np.array([tuple(p) for p in part.vertices()])
    return max(float(np.linalg.norm(v - np.array(p), axis=1).min()) for p in record["probes_mm"])


def dump(data: dict) -> str:
    """JSON with one record field per line and short numeric lists inline."""
    f = lambda v: json.dumps(v, ensure_ascii=False)  # noqa: E731
    head = [f"  {f(k)}: {f(v)}," for k, v in data.items() if k != "parts"]
    parts = []
    for r in data["parts"]:
        fields = [f"      {f(k)}: {f(v)}" for k, v in r.items() if k != "probes_mm"]
        probes = ",\n".join(f"        {f(p)}" for p in r["probes_mm"])
        parts.append("    {\n" + ",\n".join(fields) + ',\n      "probes_mm": [\n' + probes + "\n      ]\n    }")
    return "{\n" + "\n".join(head) + '\n  "parts": [\n' + ",\n".join(parts) + "\n  ]\n}\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="python -m quiver.placement", description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check", help="compare the built assembly with part-poses.json")
    rec = sub.add_parser("record", help="re-record parts (by key or label) from the current build")
    rec.add_argument("names", nargs="+")
    rec.add_argument(
        "--gps-only", action="store_true",
        help="new records apply only to the --gps receiver option",
    )
    for cmd in sub.choices.values():
        cmd.add_argument(
            "--gps", choices=PRIMARY_GPS_OPTIONS, default=DEFAULT_PRIMARY_GPS,
            help="primary GPS receiver option to build",
        )
    args = parser.parse_args(argv)

    from quiver.assembly import make_assembly

    data = json.loads(POSES_PATH.read_text())
    assembly = make_assembly(primary_gps=args.gps)
    instances = part_instances(assembly)
    active = records_for(data["parts"], assembly)
    pairs = match(active, instances)
    if args.cmd == "check":
        bad = 0
        for record, part in pairs:
            dev = float("inf") if part is None else deviation(record, part)
            if dev >= 0.01:
                bad += 1
                print(f"{record['key']}: probe off by {dev:.3f} mm")
        counted = defaultdict(int)
        for record in active:
            counted[record["label"]] += 1
        for label, parts in instances.items():
            if len(parts) != counted.get(label, 0):
                bad += 1
                print(f"{label}: {len(parts)} built, {counted.get(label, 0)} recorded")
        print("all parts match their records" if not bad else f"{bad} mismatches")
        return 1 if bad else 0

    wanted = set(args.names)
    source = f"re-recorded from the build {date.today().isoformat()}"
    for record, part in pairs:
        if record["key"] in wanted or record["label"] in wanted:
            if part is None:
                print(f"{record['key']}: not in the build", file=sys.stderr)
                return 1
            record.update(measure(part, record["key"]))
            record["source"] = source
            record.pop("fusion_occurrence", None)
            record.pop("fusion_max_dev_mm", None)
            print(f"re-recorded {record['key']}")
    # New instances of a named label get new records.
    matched = {id(part) for _, part in pairs if part is not None}
    for label in sorted(wanted & set(instances)):
        for n, part in enumerate(p for p in instances[label] if id(p) not in matched):
            key = f"{label}#{n}"
            tag = {"primary_gps": args.gps} if args.gps_only else {}
            data["parts"].append({"key": key, "label": label, **tag, "source": source, **measure(part, key)})
            print(f"recorded new {key}")
    POSES_PATH.write_text(dump(data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
