"""
Script to test the corrected daasstrikeprice endpoints.
"""

import json
from pathlib import Path

from gridstatus.isone_api.isone_api import ISONEAPI

# Create output directory
output_dir = Path("isone_api_examples")
output_dir.mkdir(exist_ok=True)

# Initialize API client
api = ISONEAPI()

# Corrected endpoints with 's' at the end
endpoints = [
    ("daasstrikeprices_current", "/daasstrikeprices/current"),
    ("daasstrikeprices_day", "/daasstrikeprices/day/20240101"),
    ("daasstrikeprices_info", "/daasstrikeprices/info"),
]

print("Testing corrected ISONE API strike price endpoints...")
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
        print(f"  ✗ Failed: {str(e)}")
        failed += 1

    print()

print("\n" + "=" * 60)
print(
    f"Summary: {successful} successful, {failed} failed out of {len(endpoints)} total",
)
print("=" * 60)
