#!/usr/bin/env python3
"""Generate human-readable Quiver BOM docs from the canonical CSV."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import OrderedDict
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CSV = REPO_ROOT / "docs" / "bom" / "quiver-pt1-bom.csv"
DEFAULT_MARKDOWN = REPO_ROOT / "docs" / "bom" / "bill-of-materials.md"

REQUIRED_COLUMNS = [
    "ID",
    "System",
    "Name",
    "Supplier",
    "Link",
    "Unit Cost",
    "Quantity",
    "Cost",
    "Order Details",
    "Notes",
]


@dataclass(frozen=True)
class BomRow:
    item_id: str
    system: str
    name: str
    supplier: str
    link: str
    unit_cost: str
    quantity: str
    cost: str
    order_details: str
    notes: str


def parse_money(value: str) -> Decimal | None:
    cleaned = re.sub(r"[^0-9.\-]", "", value or "")
    if not cleaned:
        return None
    try:
        return Decimal(cleaned)
    except InvalidOperation:
        return None


def format_money(value: Decimal) -> str:
    return f"${value:,.2f}"


def display(value: str) -> str:
    value = (value or "").strip()
    return value if value else "—"


def escape_md(value: str) -> str:
    return display(value).replace("|", r"\|")


def supplier_cell(row: BomRow) -> str:
    supplier = display(row.supplier)
    link = (row.link or "").strip()
    if supplier == "—":
        return "—"
    if link.startswith(("http://", "https://")):
        return f"[{escape_md(supplier)}]({link})"
    if link and link.casefold() != supplier.casefold():
        return f"{escape_md(supplier)} ({escape_md(link)})"
    return escape_md(supplier)


def read_bom(csv_path: Path) -> list[BomRow]:
    with csv_path.open(newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        missing = [column for column in REQUIRED_COLUMNS if column not in (reader.fieldnames or [])]
        if missing:
            raise SystemExit(f"Missing required BOM columns: {', '.join(missing)}")
        rows = []
        for row in reader:
            has_item_identity = any((row[column] or "").strip() for column in ("ID", "System", "Name"))
            if not any((value or "").strip() for value in row.values()) or not has_item_identity:
                continue
            rows.append(
                BomRow(
                    item_id=(row["ID"] or "").strip(),
                    system=(row["System"] or "Uncategorized").strip() or "Uncategorized",
                    name=(row["Name"] or "").strip(),
                    supplier=(row["Supplier"] or "").strip(),
                    link=(row["Link"] or "").strip(),
                    unit_cost=(row["Unit Cost"] or "").strip(),
                    quantity=(row["Quantity"] or "").strip(),
                    cost=(row["Cost"] or "").strip(),
                    order_details=(row["Order Details"] or "").strip(),
                    notes=(row["Notes"] or "").strip(),
                )
            )
    return rows


def grouped_rows(rows: list[BomRow]) -> OrderedDict[str, list[BomRow]]:
    grouped: OrderedDict[str, list[BomRow]] = OrderedDict()
    for row in rows:
        grouped.setdefault(row.system, []).append(row)
    return grouped


def row_cost(row: BomRow) -> Decimal | None:
    explicit_cost = parse_money(row.cost)
    if explicit_cost is not None:
        return explicit_cost

    unit_cost = parse_money(row.unit_cost)
    quantity = parse_money(row.quantity)
    if unit_cost is None or quantity is None:
        return None
    return unit_cost * quantity


def render_markdown(rows: list[BomRow], csv_path: Path) -> str:
    grouped = grouped_rows(rows)
    total_cost = sum((cost for row in rows if (cost := row_cost(row)) is not None), Decimal("0"))
    relative_csv = csv_path.relative_to(DEFAULT_MARKDOWN.parent).as_posix()

    lines: list[str] = [
        "---",
        "title: Bill of Materials",
        "description: Complete bill of materials for the Quiver dev-kit build",
        "sidebar_position: 2",
        "---",
        "",
        "<!-- GENERATED FILE: edit docs/bom/quiver-pt1-bom.csv, then run tools/bom/generate_bom_docs.py -->",
        "",
        "# Bill of Materials",
        "",
        "Complete bill of materials for building a Quiver dev-kit. This list covers structural, harness, avionics, propulsion, equipment, and shop-supply components.",
        "",
        f"**Estimated total cost: {format_money(total_cost)}**",
        "",
        ":::tip Canonical source",
        f"The canonical BOM source is [`{csv_path.relative_to(REPO_ROOT).as_posix()}`]({relative_csv}). This markdown page is generated from that CSV for easier browsing in the docs site.",
        ":::",
        "",
        ":::note Spreadsheet workflows",
        "Google Sheets or other spreadsheet tools can still be used as import/export views, but GitHub is the source of truth. Proposed BOM changes should update the CSV in a pull request so review history, releases, and manufacturer packets stay reproducible.",
        ":::",
        "",
        ":::note Manufacturing references",
        'Items marked "See Manufacturing Guide, Assembly Section" reference the Quiver manufacturing guide for detailed specs, tolerances, and assembly instructions.',
        ":::",
        "",
        "---",
        "",
    ]

    for system, system_rows in grouped.items():
        lines.extend(
            [
                f"## {escape_md(system)}",
                "",
                "| ID | Name | Unit Cost | Qty | Total | Supplier | Order Details | Notes |",
                "|----|------|-----------|-----|-------|----------|---------------|-------|",
            ]
        )
        for row in system_rows:
            total = row.cost or (format_money(cost) if (cost := row_cost(row)) is not None else "")
            lines.append(
                "| "
                + " | ".join(
                    [
                        escape_md(row.item_id),
                        escape_md(row.name),
                        escape_md(row.unit_cost),
                        escape_md(row.quantity),
                        escape_md(total),
                        supplier_cell(row),
                        escape_md(row.order_details),
                        escape_md(row.notes),
                    ]
                )
                + " |"
            )
        lines.extend(["", "---", ""])

    lines.extend(
        [
            "## Cost Summary",
            "",
            "| System | Estimated Cost |",
            "|--------|----------------|",
        ]
    )

    for system, system_rows in grouped.items():
        system_total = sum((cost for row in system_rows if (cost := row_cost(row)) is not None), Decimal("0"))
        lines.append(f"| {escape_md(system)} | {format_money(system_total)} |")

    lines.extend([f"| **Total** | **{format_money(total_cost)}** |", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV, help="Canonical BOM CSV path")
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN, help="Generated markdown output path")
    parser.add_argument("--check", action="store_true", help="Fail if generated markdown is stale")
    args = parser.parse_args()

    rows = read_bom(args.csv)
    rendered = render_markdown(rows, args.csv)

    if args.check:
        existing = args.markdown.read_text(encoding="utf-8") if args.markdown.exists() else ""
        if existing != rendered:
            print(
                f"{args.markdown.relative_to(REPO_ROOT)} is stale. "
                f"Run tools/bom/generate_bom_docs.py and commit the result.",
                file=sys.stderr,
            )
            return 1
        return 0

    args.markdown.write_text(rendered, encoding="utf-8")
    print(f"Generated {args.markdown.relative_to(REPO_ROOT)} from {args.csv.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
