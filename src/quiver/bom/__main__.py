"""CLI for the Quiver BOM: validate the master data, render the outputs.

Usage:
    python -m quiver.bom validate          # schema + cross-checks, exit 1 on error
    python -m quiver.bom render            # write docs/Manufacturing/BOM.md + quiver-bom.csv
    python -m quiver.bom render --check    # exit 1 if committed outputs are stale
"""

import argparse
import sys

from quiver.bom import BomError, load_bom, make_warnings
from quiver.bom.render import render


def main() -> int:
    parser = argparse.ArgumentParser(description="Quiver BOM tooling")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate", help="validate bom/*.yaml")
    render_p = sub.add_parser("render", help="generate docs outputs")
    render_p.add_argument("--check", action="store_true",
                          help="verify committed outputs are current instead of writing")
    args = parser.parse_args()

    try:
        bom = load_bom()
    except BomError as exc:
        print(exc, file=sys.stderr)
        return 1

    for warning in make_warnings(bom):
        print(f"warning: {warning}", file=sys.stderr)

    if args.command == "validate":
        print(f"OK: {sum(1 for _ in bom.items())} items, "
              f"revision {bom.meta['revision']} ({bom.meta.get('status', 'final')})")
        return 0

    outputs = render(bom)
    if args.check:
        stale = [str(p) for p, content in outputs.items()
                 if not p.exists() or p.read_text() != content]
        if stale:
            print("stale generated BOM outputs (run `python -m quiver.bom render`):\n  "
                  + "\n  ".join(stale), file=sys.stderr)
            return 1
        print("generated BOM outputs are current")
        return 0

    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
