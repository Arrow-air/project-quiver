"""RAM Ball Base adapter for Quiver attachment interface.

A 3D-printable adapter that bolts to the existing metal attachment
interface plate and provides a RAM ball mount.

Mounting: 4x M3 screws into the corner hole pattern on the interface plate.

Variants:
    B Size: 1" (25.4mm) ball, up to 2 lbs
    C Size: 1.5" (38.1mm) ball, up to 4 lbs
"""

from pathlib import Path

from build123d import (
    Align,
    BuildPart,
    BuildSketch,
    Circle,
    Cylinder,
    Cone,
    Location,
    Locations,
    Mode,
    Part,
    Plane,
    Sphere,
    extrude,
    fillet,
    export_step,
    export_stl,
    Compound,
    RectangleRounded,
)

_DIR = Path(__file__).parent

# === RAM Ball Sizes ===
BALL_SIZES = {
    "B": 25.4,   # 1 inch, up to 2 lbs
    "C": 38.1,   # 1.5 inch, up to 4 lbs
}

# === Mounting Hole Pattern (corner holes on interface plate) ===
# 38mm x 38mm pattern
MOUNT_HOLES_CENTERED = [
    (19, 19),
    (19, -19),
    (-19, -19),
    (-19, 19),
]

# === Adapter Geometry ===
BASE_SIZE = 50.0         # mm (square)
BASE_THICKNESS = 6.0     # mm
CORNER_RADIUS = 5.0      # mm

M3_CLEARANCE = 3.4       # mm
M3_HEAD_DIA = 6.0        # mm
M3_HEAD_DEPTH = 3.5      # mm

NECK_HEIGHT = 12.0       # mm


def make_ram_ball_adapter(ball_size: str = "B") -> Part:
    """Create a RAM ball adapter plate."""
    if ball_size not in BALL_SIZES:
        raise ValueError(f"Invalid ball size: {ball_size}. Use 'B' or 'C'.")

    ball_d = BALL_SIZES[ball_size]
    neck_base_d = ball_d * 0.75
    neck_top_d = ball_d * 0.5
    overlap = 3.0  # mm overlap for solid fusion
    
    # Build base plate (XY plane, Z up)
    with BuildPart() as base:
        with BuildSketch(Plane.XY):
            RectangleRounded(BASE_SIZE, BASE_SIZE, CORNER_RADIUS)
        extrude(amount=BASE_THICKNESS)
        
        # Screw holes (from top, through plate)
        with BuildSketch(Plane.XY.offset(BASE_THICKNESS)):
            for hx, hy in MOUNT_HOLES_CENTERED:
                with Locations((hx, hy)):
                    Circle(M3_CLEARANCE / 2)
        extrude(amount=-BASE_THICKNESS, mode=Mode.SUBTRACT)
        
        # Counterbores
        with BuildSketch(Plane.XY.offset(BASE_THICKNESS)):
            for hx, hy in MOUNT_HOLES_CENTERED:
                with Locations((hx, hy)):
                    Circle(M3_HEAD_DIA / 2)
        extrude(amount=-M3_HEAD_DEPTH, mode=Mode.SUBTRACT)
    
    # Build neck + ball (Z vertical)
    # Use wider flared base and collar for reinforcement
    neck_flare_d = neck_base_d * 1.8  # Much wider at base
    ball_collar_d = ball_d * 0.7      # Collar around ball base
    
    with BuildPart() as neck:
        # Large flared base section
        Cone(
            bottom_radius=neck_flare_d / 2,
            top_radius=neck_base_d / 2,
            height=6.0,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        
        # Main tapered neck (continuous taper from base to ball)
        with Locations((0, 0, 6.0)):
            Cone(
                bottom_radius=neck_base_d / 2,
                top_radius=ball_collar_d / 2,
                height=NECK_HEIGHT + overlap - 6.0,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            )
        
        # Ball collar cylinder
        collar_z = NECK_HEIGHT + overlap
        with Locations((0, 0, collar_z)):
            Cylinder(
                radius=ball_collar_d / 2,
                height=4.0,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            )
        
        # Ball (embedded into collar)
        ball_z = collar_z + ball_d / 2 - 2
        with Locations((0, 0, ball_z)):
            Sphere(radius=ball_d / 2)
    
    # Position neck so it overlaps into the base plate
    neck_positioned = neck.part.moved(Location((0, 0, BASE_THICKNESS - overlap)))
    
    # Fuse into single solid
    result = base.part.fuse(neck_positioned)
    
    result.label = f"RAM Ball Adapter ({ball_size})"
    return result


def make_assembly(ball_size: str = "B") -> Compound | None:
    """Build the RAM ball adapter assembly for visualization."""
    adapter = make_ram_ball_adapter(ball_size)
    return Compound(children=[adapter], label=f"RAM Ball Adapter ({ball_size})")


def export_all():
    """Export both B and C size models as STEP and STL."""
    steps_dir = _DIR / "steps"
    steps_dir.mkdir(exist_ok=True)

    for size in ["B", "C"]:
        print(f"\n=== Generating {size} Size ===")
        model = make_ram_ball_adapter(size)

        bb = model.bounding_box()
        print(f"  Dimensions: {bb.max.X - bb.min.X:.1f} x "
              f"{bb.max.Y - bb.min.Y:.1f} x "
              f"{bb.max.Z - bb.min.Z:.1f} mm")
        print(f"  Solids: {len(list(model.solids()))}")

        # Export
        step_path = steps_dir / f"ram_ball_adapter_{size.lower()}.step"
        export_step(model, str(step_path))
        print(f"  Exported: {step_path.name}")

        stl_path = steps_dir / f"ram_ball_adapter_{size.lower()}.stl"
        export_stl(model, str(stl_path))
        print(f"  Exported: {stl_path.name}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate RAM Ball Adapter")
    parser.add_argument("--size", choices=["B", "C", "both"], default="both")
    args = parser.parse_args()

    if args.size == "both":
        export_all()
    else:
        model = make_ram_ball_adapter(args.size)
        steps_dir = _DIR / "steps"
        steps_dir.mkdir(exist_ok=True)
        export_step(model, str(steps_dir / f"ram_ball_adapter_{args.size.lower()}.step"))
        export_stl(model, str(steps_dir / f"ram_ball_adapter_{args.size.lower()}.stl"))
        print(f"Exported {args.size} size")
