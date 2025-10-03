"""
Script to hit ISONE API endpoints and save example outputs.
"""

import json
from pathlib import Path

from gridstatus.isone_api.isone_api import ISONEAPI

# Create output directory
output_dir = Path("isone_api_examples")
output_dir.mkdir(exist_ok=True)

# Initialize API client
api = ISONEAPI()

# Endpoints to test
endpoints = [
    # Hourly Final Reserve Price
    ("hourlyfinalreserveprice", "/hourlyfinalreserveprice"),
    ("hourlyfinalreserveprice_current", "/hourlyfinalreserveprice/current"),
    (
        "hourlyfinalreserveprice_current_locationType_ZONE",
        "/hourlyfinalreserveprice/current/locationType/ZONE",
    ),
    (
        "hourlyfinalreserveprice_current_reserveZone_7000",
        "/hourlyfinalreserveprice/current/reserveZone/7000",
    ),
    ("hourlyfinalreserveprice_day_20251001", "/hourlyfinalreserveprice/day/20251001"),
    (
        "hourlyfinalreserveprice_day_20251001_reserveZone_7000",
        "/hourlyfinalreserveprice/day/20251001/reserveZone/7000",
    ),
    ("hourlyfinalreserveprice_info", "/hourlyfinalreserveprice/info"),
    # Realtime Hourly Operating Reserve
    ("realtimehourlyoperatingreserve", "/realtimehourlyoperatingreserve"),
    (
        "realtimehourlyoperatingreserve_current_all",
        "/realtimehourlyoperatingreserve/current/all",
    ),
    (
        "realtimehourlyoperatingreserve_current_location_4001",
        "/realtimehourlyoperatingreserve/current/location/4001",
    ),
    (
        "realtimehourlyoperatingreserve_current_locationType_ZONE",
        "/realtimehourlyoperatingreserve/current/locationType/ZONE",
    ),
    (
        "realtimehourlyoperatingreserve_day_20251001_location_4001",
        "/realtimehourlyoperatingreserve/day/20251001/location/4001",
    ),
    ("realtimehourlyoperatingreserve_info", "/realtimehourlyoperatingreserve/info"),
    # Hourly Prelim Reserve Price
    ("hourlyprelimreserveprice", "/hourlyprelimreserveprice"),
    ("hourlyprelimreserveprice_current", "/hourlyprelimreserveprice/current"),
    (
        "hourlyprelimreserveprice_current_locationType_ZONE",
        "/hourlyprelimreserveprice/current/locationType/ZONE",
    ),
    (
        "hourlyprelimreserveprice_current_reserveZone_7000",
        "/hourlyprelimreserveprice/current/reserveZone/7000",
    ),
    ("hourlyprelimreserveprice_day_20251001", "/hourlyprelimreserveprice/day/20251001"),
    (
        "hourlyprelimreserveprice_day_20251001_reserveZone_7000",
        "/hourlyprelimreserveprice/day/20251001/reserveZone/7000",
    ),
    ("hourlyprelimreserveprice_info", "/hourlyprelimreserveprice/info"),
    # Day-Ahead Hourly Operating Reserve
    ("dayaheadhourlyoperatingreserve", "/dayaheadhourlyoperatingreserve"),
    (
        "dayaheadhourlyoperatingreserve_current_all",
        "/dayaheadhourlyoperatingreserve/current/all",
    ),
    (
        "dayaheadhourlyoperatingreserve_current_location_4001",
        "/dayaheadhourlyoperatingreserve/current/location/4001",
    ),
    (
        "dayaheadhourlyoperatingreserve_current_locationType_ZONE",
        "/dayaheadhourlyoperatingreserve/current/locationType/ZONE",
    ),
    (
        "dayaheadhourlyoperatingreserve_day_20251001_location_4001",
        "/dayaheadhourlyoperatingreserve/day/20251001/location/4001",
    ),
    ("dayaheadhourlyoperatingreserve_info", "/dayaheadhourlyoperatingreserve/info"),
    # Day-Ahead Reserve Data
    ("daasreservedata_current", "/daasreservedata/current"),
    ("daasreservedata_day_20251001", "/daasreservedata/day/20251001"),
    ("daasreservedata_info", "/daasreservedata/info"),
    # Day-Ahead Strike Prices
    ("daasstrikeprices_current", "/daasstrikeprices/current"),
    ("daasstrikeprices_day_20251001", "/daasstrikeprices/day/20251001"),
    ("daasstrikeprices_info", "/daasstrikeprices/info"),
    # Five Minute RCP
    ("fiveminutercp", "/fiveminutercp"),
    ("fiveminutercp_type_ZONE_current", "/fiveminutercp/ZONE/current"),
    ("fiveminutercp_type_ZONE_day_20251003", "/fiveminutercp/ZONE/day/20251003"),
    ("fiveminutercp_type_ZONE_info", "/fiveminutercp/ZONE/info"),
    ("fiveminutercp_current", "/fiveminutercp/current"),
    ("fiveminutercp_day_20251003", "/fiveminutercp/day/20251003"),
    ("fiveminutercp_info", "/fiveminutercp/info"),
]

print(f"Testing {len(endpoints)} ISONE API endpoints...")
print(f"Output directory: {output_dir.absolute()}\n")

successful = 0
failed = 0

for name, endpoint in endpoints:
    try:
        print(f"Testing {name}: {endpoint}...")
        url = f"{api.base_url}{endpoint}"
        response = api.make_api_call(url, parse_json=True)

        # Save the response
        output_file = output_dir / f"{name}.json"
        with open(output_file, "w") as f:
            json.dump(response, f, indent=2)

        print(f"  ✓ Success - saved to {output_file}")
        successful += 1

    except Exception as e:
        print(f"  ✗ Failed: {e!s}")
        failed += 1

    print()

print("\n" + "=" * 60)
print(
    f"Summary: {successful} successful, {failed} failed out of {len(endpoints)} total",
)
print("=" * 60)
