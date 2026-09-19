"""Supported primary GPS choices; neither option changes the backup GPS."""

PRIMARY_GPS_OPTIONS = ("here4", "holybro-f9p")
DEFAULT_PRIMARY_GPS = "here4"

# Retain the existing F9P base placement pending physical stack-up review.
F9P_MOUNT_DZ = -11.95
# Vendor case local -Y face is its mounting surface, at Y=-10 mm.
# Rotate X +90 degrees, match the three mounting holes, then seat on
# the base's native Z=81.6 mm top face (plus its assembly correction).
F9P_RECEIVER_POSITION = (0.0, -3.125, 81.6 + F9P_MOUNT_DZ + 10.0)


def validate_primary_gps(primary_gps: str) -> None:
    if primary_gps not in PRIMARY_GPS_OPTIONS:
        raise ValueError(f"Unknown primary GPS {primary_gps!r}; choose {PRIMARY_GPS_OPTIONS}")
