from typing import Any

import requests


class CarbonCalculatorError(Exception):
    pass


class CarbonCalculator:
    def __init__(self):
        self.base_url = "https://api.websitecarbon.com/site"

    def get_carbon_footprint(self, url: str) -> dict[str, Any]:
        try:
            response = requests.get(self.base_url, params={"url": url})
            response_json = response.json()
        except Exception as e:
            raise CarbonCalculatorError from e
        return response_json
