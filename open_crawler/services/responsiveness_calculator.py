import os
from typing import Any

import requests


class ResponsivenessCalculatorError(Exception):
    pass


class ResponsivenessCalculator:
    def __init__(self):
        self.base_url = "https://content-searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run"
        self._api_key = os.environ["GOOGLE_API_KEY"]

    def get_responsiveness(self, url: str) -> dict[str, Any]:
        try:
            response = requests.post(self.base_url, data={"url": url}, params={"key": self._api_key, "alt": "json"})
            response_json = response.json()
        except Exception as e:
            raise ResponsivenessCalculatorError from e
        return response_json
