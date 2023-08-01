from typing import Any

import requests


class CarbonCalculator:
    def __init__(self):
        self.base_url = "https://api.websitecarbon.com/site"

    def get_carbon_footprint(self, url: str) -> dict[str, Any]:
        response = requests.get(self.base_url, params={"url": url})
        return response.json()


carbon_service = CarbonCalculator()
