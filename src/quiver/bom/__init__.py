"""Load and validate the Quiver bill of materials master data.

The BOM source of truth is the YAML files in bom/ at the repo root (see
bom/README.md for the schema and revision policy). This package parses
them into dataclasses and enforces the schema rules with precise
"file: id: message" errors. Rendering to the docs page and procurement
CSV lives in quiver.bom.render; the CLI is `python -m quiver.bom`.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent.parent.parent
BOM_DIR = REPO_ROOT / "bom"

_ID_RE = re.compile(r"^(\d{4}|(FAST|CONS|TOOL|HSUP)-\d{3}|HAR-\d{4})$")
_SOURCING = {"laser-cut", "3d-print", "cut-to-length", "cots", "pcb-assembly", "harness"}
_MAKE_SOURCING = {"laser-cut", "3d-print", "cut-to-length"}

_DATA_FILES = [
    "1000-airframe-structure.yaml",
    "2000-supporting-structure.yaml",
    "3000-equipment.yaml",
    "4000-harness.yaml",
    "fasteners.yaml",
    "consumables.yaml",
]


@dataclass
class Supplier:
    name: str
    part_number: str | None = None
    url: str | None = None
    note: str | None = None


@dataclass
class Item:
    id: str
    name: str
    qty: int | str  # int per vehicle, or "AR" for CONS/TOOL
    sourcing: str
    category: str
    material: str | None = None
    finish: str | None = None
    spec: str | None = None
    design_ref: str | None = None
    production_bom: str | None = None
    unit_cost_usd: float | None = None
    purchase_qty: int | None = None
    purchase_note: str | None = None
    included_in: str | None = None
    since: str | None = None
    notes: str | None = None
    suppliers: list[Supplier] = field(default_factory=list)


@dataclass
class Category:
    key: str
    name: str
    items: list[Item]


@dataclass
class Bom:
    meta: dict
    categories: list[Category]

    def items(self):
        for cat in self.categories:
            yield from cat.items

    def by_id(self) -> dict[str, Item]:
        return {item.id: item for item in self.items()}


class BomError(Exception):
    """Validation failure; message lists every violation found."""


def _parse_item(raw: dict, category: str, errors: list[str], where: str) -> Item:
    def err(msg: str) -> None:
        errors.append(f"{where}: {msg}")

    item_id = raw.get("id")
    if not isinstance(item_id, str) or not _ID_RE.match(item_id):
        err(f"id {item_id!r} is missing or not a quoted 4-digit / prefixed id")
        item_id = str(item_id)

    qty = raw.get("qty")
    if qty == "AR":
        if not item_id.startswith(("CONS-", "TOOL-")):
            err("qty 'AR' is only allowed for CONS-/TOOL- items")
    elif not isinstance(qty, int) or qty < 1:
        err(f"qty {qty!r} must be an integer >= 1 (or 'AR' for CONS/TOOL)")

    sourcing = raw.get("sourcing")
    if sourcing not in _SOURCING:
        err(f"sourcing {sourcing!r} not one of {sorted(_SOURCING)}")

    suppliers = []
    for i, s in enumerate(raw.get("suppliers") or []):
        if not s.get("name"):
            err(f"supplier #{i + 1} is missing a name")
        suppliers.append(Supplier(
            name=s.get("name", ""),
            part_number=str(s["part_number"]) if "part_number" in s else None,
            url=s.get("url"),
            note=s.get("note"),
        ))

    purchase = raw.get("purchase") or {}

    item = Item(
        id=item_id,
        name=raw.get("name") or "",
        qty=qty,
        sourcing=sourcing or "",
        category=category,
        material=raw.get("material"),
        finish=raw.get("finish"),
        spec=raw.get("spec"),
        design_ref=raw.get("design_ref"),
        production_bom=raw.get("production_bom"),
        unit_cost_usd=raw.get("unit_cost_usd"),
        purchase_qty=purchase.get("qty"),
        purchase_note=purchase.get("note"),
        included_in=raw.get("included_in"),
        since=raw.get("since"),
        notes=raw.get("notes"),
        suppliers=suppliers,
    )

    if not item.name:
        err("missing name")
    # Generic tools and TBC-marked draft items are exempt from the supplier
    # requirement; TBCs still surface via make_warnings.
    supplier_exempt = (
        item.included_in
        or item.id.startswith("TOOL-")
        or (item.notes and "TBC" in item.notes)
    )
    if item.sourcing == "cots" and not supplier_exempt:
        usable = [s for s in suppliers if s.part_number or s.url or s.note]
        if not usable:
            err("cots item needs a supplier with part_number, url, or note "
                "(or an included_in reference / TBC note)")
    if item.sourcing == "pcb-assembly" and not item.production_bom:
        err("pcb-assembly item needs a production_bom path")
    if item.sourcing in _MAKE_SOURCING and not item.material:
        err("make item needs a material")
    for path_field in ("design_ref", "production_bom"):
        rel = getattr(item, path_field)
        if rel and not (REPO_ROOT / rel).exists():
            err(f"{path_field} does not exist: {rel}")
    if item.unit_cost_usd is not None and not isinstance(item.unit_cost_usd, (int, float)):
        err(f"unit_cost_usd {item.unit_cost_usd!r} must be a number")
    if item.purchase_qty is not None and (not isinstance(item.purchase_qty, int) or item.purchase_qty < 1):
        err(f"purchase.qty {item.purchase_qty!r} must be an integer >= 1")

    return item


def load_bom(bom_dir: Path = BOM_DIR) -> Bom:
    """Parse and validate all BOM files. Raises BomError listing every issue."""
    errors: list[str] = []

    meta = yaml.safe_load((bom_dir / "meta.yaml").read_text())
    for required in ("revision", "config", "date", "title"):
        if required not in meta:
            errors.append(f"meta.yaml: missing {required}")

    categories = []
    for filename in _DATA_FILES:
        path = bom_dir / filename
        data = yaml.safe_load(path.read_text())
        key = data.get("category")
        if not isinstance(key, str):
            errors.append(f"{filename}: category must be a quoted string")
            key = str(key)
        items = [
            _parse_item(raw, key, errors, f"{filename}: {raw.get('id', f'item #{i + 1}')}")
            for i, raw in enumerate(data.get("items") or [])
        ]
        categories.append(Category(key=key, name=data.get("name", ""), items=items))

    seen: dict[str, str] = {}
    all_ids = set()
    for cat in categories:
        for item in cat.items:
            if item.id in seen:
                errors.append(f"duplicate id {item.id} (also in {seen[item.id]})")
            seen[item.id] = cat.name
            all_ids.add(item.id)
    for cat in categories:
        for item in cat.items:
            if item.included_in and item.included_in not in all_ids:
                errors.append(f"{item.id}: included_in {item.included_in!r} is not a known id")

    if errors:
        raise BomError("BOM validation failed:\n  " + "\n  ".join(errors))
    return Bom(meta=meta, categories=categories)


def make_warnings(bom: Bom) -> list[str]:
    """Non-fatal data-quality warnings (reported by the CLI, not errors)."""
    warnings = []
    for item in bom.items():
        if item.sourcing in _MAKE_SOURCING and not item.design_ref:
            warnings.append(f"{item.id} ({item.name}): make item without a design_ref")
        if item.notes and "TBC" in item.notes:
            warnings.append(f"{item.id} ({item.name}): marked TBC")
    return warnings
