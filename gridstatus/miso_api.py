import os

import requests

# Called load, generation, and interchange on MISO
LOAD_API_TYPE = "load"
PRICING_API_TYPE = "pricing"

BASE_API_URL = "https://apim.misoenergy.org/"
BASE_PRICING_API_URL = f"{BASE_API_URL}/pricing/v1"
BASE_LOAD_API_URL = f"{BASE_API_URL}/lgi/v1"

REAL_TIME_LMP_EXPOST_ENDPOINT = BASE_PRICING_API_URL + "/real-time/{date}/lmp-expost"


class MisoAPI:
    def __init__(self, load_subscription_key, pricing_subscription_key):
        self.load_subscription_key = load_subscription_key or os.getenv(
            "MISO_LOAD_SUBSCRIPTION_KEY",
        )
        self.pricing_subscription_key = pricing_subscription_key or os.getenv(
            "MISO_PRICING_SUBSCRIPTION_KEY",
        )

    def headers(self, api_type):
        return {
            "Cache-Control": "no-cache",
            "Ocp-Apim-Subscription-Key": self.load_subscription_key
            if api_type == LOAD_API_TYPE
            else self.pricing_subscription_key,
        }

    def lmp_real_time_expost(self, date, end=None, verbose=False, preliminary=True):
        """Get MISO LMP Real Time Ex Post data"""
        return self._get(
            "https://api.misoenergy.org/MISORTWDData/api/ExPostLMPRealTime",
            date,
            end,
            verbose,
            api_type=PRICING_API_TYPE,
        )

    def hit_miso_api(self, url, verbose):
        last_page = False
        response = requests.get(url, headers=self.headers())
        if verbose:
            print(response)
        return response
