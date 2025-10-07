"""
Script to check if interval=0x returns the same status code as interval=x
for hourly MISO API endpoints.

Tests intervals 1-9 with both formats (0x and x) for date 2025-10-04.
Outputs results to a CSV file.
"""

import os
import time

import requests

from gridstatus.miso_api import (
    BASE_PRICING_URL,
    CERTIFICATES_CHAIN_FILE,
    EX_ANTE,
    EX_POST,
    FINAL_STRING,
    HOURLY_RESOLUTION,
    PRELIMINARY_STRING,
)

# Get API key from environment
PRICING_API_KEY = os.getenv("MISO_API_PRICING_SUBSCRIPTION_KEY", "")

if not PRICING_API_KEY:
    print("WARNING: MISO_API_PRICING_SUBSCRIPTION_KEY not set in environment")
    print("Requests may fail without valid API key")

# Split API keys for rotation
API_KEYS = [key.strip() for key in PRICING_API_KEY.split(",") if key.strip()]
current_key_index = 0

DATE_PRELIM = "2025-10-05"
DATE_FINAL = "2025-10-03"
DATE_DAY_AHEAD = "2025-10-03"

# Define hourly endpoints to test
HOURLY_ENDPOINTS = {
    "LMP Day Ahead Ex Ante": {
        "url_template": f"{BASE_PRICING_URL}/day-ahead/{DATE_DAY_AHEAD}/lmp-{EX_ANTE}",
        "interval_param": "interval",
    },
    "LMP Day Ahead Ex Post": {
        "url_template": f"{BASE_PRICING_URL}/day-ahead/{DATE_DAY_AHEAD}/lmp-{EX_POST}",
        "interval_param": "interval",
    },
    "LMP Real Time Hourly Ex Post Prelim": {
        "url_template": f"{BASE_PRICING_URL}/real-time/{DATE_PRELIM}/lmp-{EX_POST}",
        "interval_param": "interval",
        "extra_params": {
            "preliminaryFinal": PRELIMINARY_STRING,
            "timeResolution": HOURLY_RESOLUTION,
        },
    },
    "LMP Real Time Hourly Ex Post Final": {
        "url_template": f"{BASE_PRICING_URL}/real-time/{DATE_FINAL}/lmp-{EX_POST}",
        "interval_param": "interval",
        "extra_params": {
            "preliminaryFinal": FINAL_STRING,
            "timeResolution": HOURLY_RESOLUTION,
        },
    },
    "AS MCP Day Ahead Ex Ante": {
        "url_template": f"{BASE_PRICING_URL}/day-ahead/{DATE_DAY_AHEAD}/asm-{EX_ANTE}",
        "interval_param": "interval",
    },
    "AS MCP Day Ahead Ex Post": {
        "url_template": f"{BASE_PRICING_URL}/day-ahead/{DATE_DAY_AHEAD}/asm-{EX_POST}",
        "interval_param": "interval",
    },
    "AS MCP Real Time Hourly Ex Post Prelim": {
        "url_template": f"{BASE_PRICING_URL}/real-time/{DATE_PRELIM}/asm-{EX_POST}",
        "interval_param": "interval",
        "extra_params": {
            "preliminaryFinal": PRELIMINARY_STRING,
            "timeResolution": HOURLY_RESOLUTION,
        },
    },
    "AS MCP Real Time Hourly Ex Post Final": {
        "url_template": f"{BASE_PRICING_URL}/real-time/{DATE_FINAL}/asm-{EX_POST}",
        "interval_param": "interval",
        "extra_params": {
            "preliminaryFinal": FINAL_STRING,
            "timeResolution": HOURLY_RESOLUTION,
        },
    },
}


def get_next_api_key():
    """Get the next API key in rotation."""
    global current_key_index
    if not API_KEYS:
        return ""
    key = API_KEYS[current_key_index]
    current_key_index = (current_key_index + 1) % len(API_KEYS)
    return key


def test_interval_format(endpoint_config: dict, interval_num: int):
    """Test both interval=0x and interval=x formats for a given interval number."""
    url = endpoint_config["url_template"]

    # Format interval numbers
    interval_x = str(interval_num)  # e.g., "1", "2", etc.
    interval_0x = "0" + str(interval_num)  # e.g., "01", "02", etc.

    # Build params
    params_x = {endpoint_config["interval_param"]: interval_x}
    params_0x = {endpoint_config["interval_param"]: interval_0x}

    # Add extra params if they exist
    if "extra_params" in endpoint_config:
        params_x.update(endpoint_config["extra_params"])
        params_0x.update(endpoint_config["extra_params"])

    # Make requests with rotating API keys
    headers_x = {
        "Ocp-Apim-Subscription-Key": get_next_api_key(),
        "Cache-Control": "no-cache",
    }
    response_x = None
    content_x = None
    try:
        response_x = requests.get(
            url,
            params=params_x,
            headers=headers_x,
            verify=CERTIFICATES_CHAIN_FILE,
            timeout=10,
        )
        status_x = response_x.status_code
        content_x = response_x.content
    except Exception as e:
        status_x = f"Error: {e}"
        content_x = None

    # Sleep to avoid rate limits
    time.sleep(1.5)

    headers_0x = {
        "Ocp-Apim-Subscription-Key": get_next_api_key(),
        "Cache-Control": "no-cache",
    }
    response_0x = None
    content_0x = None
    try:
        response_0x = requests.get(
            url,
            params=params_0x,
            headers=headers_0x,
            verify=CERTIFICATES_CHAIN_FILE,
            timeout=10,
        )
        status_0x = response_0x.status_code
        content_0x = response_0x.content
    except Exception as e:
        status_0x = f"Error: {e}"
        content_0x = None

    # Sleep to avoid rate limits
    time.sleep(1.5)

    # Check if both status code and content match
    match = (status_x == status_0x) and (content_x == content_0x)

    return interval_x, status_x, interval_0x, status_0x, match


def main():
    import csv

    output_file = "miso_interval_test_results.csv"

    print("Testing MISO API hourly endpoints")
    print(f"  Day Ahead: {DATE_DAY_AHEAD}")
    print(f"  Prelim: {DATE_PRELIM}")
    print(f"  Final: {DATE_FINAL}")
    print(f"Writing results to {output_file}")
    print()
    print(
        f"{'Endpoint':<45} {'Interval':<10} {'0x Status':<12} {'x Status':<12} {'Match':<10}",
    )
    print("=" * 90)

    # Open CSV file and write header
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "endpoint",
                "interval",
                "interval_0x_status_code",
                "interval_x_status_code",
                "match",
            ],
        )
        writer.writeheader()

        for endpoint_name, endpoint_config in HOURLY_ENDPOINTS.items():
            for i in range(1, 10):
                interval_x, status_x, _, status_0x, match = test_interval_format(
                    endpoint_config,
                    i,
                )

                result = {
                    "endpoint": endpoint_name,
                    "interval": interval_x,
                    "interval_0x_status_code": status_0x,
                    "interval_x_status_code": status_x,
                    "match": match,
                }

                # Write to CSV immediately
                writer.writerow(result)
                f.flush()  # Ensure it's written to disk

                # Print result
                print(
                    f"{endpoint_name:<45} {interval_x:<10} {str(status_0x):<12} {str(status_x):<12} {str(match):<10}",
                )

    print()
    print(f"Results written to {output_file}")


if __name__ == "__main__":
    main()
