"""Receiver/mount selection and measured interface geometry."""

import pytest
from build123d import GeomType
from OCP.BRepAdaptor import BRepAdaptor_Surface

from quiver.assembly import make_assembly


def find(node, prefix):
    if node.label.startswith(prefix):
        return node
    for child in node.children:
        found = find(child, prefix)
        if found is not None:
            return found
    return None


def test_receiver_selects_matching_mount(assembly):
    receiver = find(assembly, "3250_")
    here4 = receiver.label == "3250_gnss_here4"
    assert (find(assembly, "2333_") is not None) == here4
    assert (find(assembly, "2331_") is not None) == (not here4)
    assert find(assembly, "2332_") is None
    assert find(assembly, "3250_gnss_wren") is None


def test_receiver_position(assembly):
    receiver = find(assembly, "3250_")
    box = receiver.bounding_box()
    if receiver.label == "3250_gnss_here4":
        # Independent Fusion world bounds, mm.
        assert tuple(box.min) == pytest.approx((-33.9, -33.89738, 79.65), abs=0.02)
        assert tuple(box.max) == pytest.approx((33.9, 33.89738, 95.25), abs=0.02)
    else:
        # Vendor case seats on the existing F9P base's upper face.
        mount = find(assembly, "2331_")
        assert box.min.Z == pytest.approx(mount.bounding_box().max.Z, abs=0.02)
        assert box.max.Z - box.min.Z == pytest.approx(21.0, abs=0.02)


def _vertical_holes(part, radius, z_min, z_max):
    axes = set()
    for face in part.faces():
        if face.geom_type != GeomType.CYLINDER:
            continue
        surface = BRepAdaptor_Surface(face.wrapped).Cylinder()
        box = face.bounding_box()
        if (abs(surface.Radius() - radius) < 0.001
                and abs(surface.Axis().Direction().Z()) > 0.999
                and box.min.Z >= z_min - 0.01 and box.max.Z <= z_max + 0.01):
            point = surface.Axis().Location()
            axes.add((round(point.X(), 3), round(point.Y(), 3)))
    return axes


def test_f9p_mounting_pattern(assembly):
    receiver = find(assembly, "3250_")
    if receiver.label != "3250_gnss_holybro_neo_f9p":
        return
    mount = find(assembly, "2331_")
    # Three mount bores: radius 1.3 mm; receiver insert seats: radius 1.6 mm.
    expected = {(0.0, 9.375), (-10.825, -9.375), (10.825, -9.375)}
    assert expected <= _vertical_holes(mount, 1.3, 63.95, 69.65)
    assert expected <= _vertical_holes(receiver, 1.6, 69.65, 74.65)


def test_retired_or_unknown_gps_rejected():
    with pytest.raises(ValueError, match="Unknown primary GPS"):
        make_assembly(primary_gps="wren-mini")
