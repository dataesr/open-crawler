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
        response = None
        try:
            response = requests.post(
                self.base_url,
                data={"url": url},
                params={"key": self._api_key, "alt": "json"},
            )
            response.raise_for_status()
        except requests.HTTPError as e:
            error_msg = None
            if response:
                error_msg = response.json().get("error", {}).get("message", "")
            raise ResponsivenessCalculatorError(
                error_msg or "Unknown error"
            ) from e
        except Exception as e:
            raise ResponsivenessCalculatorError from e
        return response.json()
