"""Tests for the BOM master data and its agreement with the CAD assembly.

The BOM is a quality reference for manufacturers; these tests keep it
honest: the schema always validates, the committed generated outputs are
never stale, and every part in the CAD assembly is covered by a BOM line
item with a sufficient quantity.
"""

import re
from collections import Counter

import pytest

from quiver.bom import load_bom
from quiver.bom.render import render

# CAD leaf parts whose labels intentionally carry no BOM id. Keep small:
# anything new landing here should instead get a BOM-numbered label.
UNLABELED_ALLOWLIST: set[str] = set()

_BOM_LABEL = re.compile(r"^(\d{4})[-_]")


@pytest.fixture(scope="session")
def bom():
    return load_bom()


def test_bom_validates(bom):
    assert sum(1 for _ in bom.items()) > 100


def test_generated_outputs_are_fresh(bom):
    for path, content in render(bom).items():
        assert path.exists(), f"{path} missing — run `python -m quiver.bom render`"
        assert path.read_text() == content, (
            f"{path} is stale — run `python -m quiver.bom render`"
        )


def _cad_id_counts(assembly) -> tuple[Counter, list[str]]:
    """Count BOM-id-prefixed nodes; don't descend into them (their children
    are internal solids). Returns (id counts, unlabeled leaf labels)."""
    counts: Counter = Counter()
    unlabeled: list[str] = []

    def walk(node):
        label = node.label or ""
        match = _BOM_LABEL.match(label)
        if match:
            counts[match.group(1)] += 1
            return
        children = list(getattr(node, "children", []))
        if not children:
            if label:
                unlabeled.append(label)
            return
        for child in children:
            walk(child)

    walk(assembly)
    return counts, unlabeled


def test_every_cad_part_has_a_bom_entry(assembly, bom):
    cad_counts, unlabeled = _cad_id_counts(assembly)

    stray = set(unlabeled) - UNLABELED_ALLOWLIST
    assert not stray, (
        f"CAD leaf parts without BOM-id labels: {sorted(stray)} — label them "
        "with a BOM id or add to the allowlist with justification"
    )

    by_id = bom.by_id()
    problems = []
    for cad_id, count in sorted(cad_counts.items()):
        item = by_id.get(cad_id)
        if item is None:
            problems.append(f"{cad_id}: in CAD ({count}x) but missing from the BOM")
        elif isinstance(item.qty, int) and item.qty < count:
            problems.append(
                f"{cad_id} ({item.name}): BOM qty {item.qty} < {count} CAD instances"
            )
    assert not problems, "BOM does not cover the CAD assembly:\n  " + "\n  ".join(problems)


def test_bom_ids_not_in_cad_are_intentional(assembly, bom):
    """4-digit BOM items absent from CAD must say why (a note or TBC)."""
    cad_counts, _ = _cad_id_counts(assembly)
    silent = [
        f"{item.id} ({item.name})"
        for item in bom.items()
        if item.id.isdigit() and item.id not in cad_counts and not item.notes
    ]
    assert not silent, (
        "BOM items missing from CAD need a notes field explaining why:\n  "
        + "\n  ".join(silent)
    )
