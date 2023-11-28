import requests
from retry import retry
from typing import Any


class CarbonCalculatorError(Exception):
    pass


class CarbonCalculator:
    BASE_URL = "https://api.websitecarbon.com/site"
    TIMEOUT = 300  # 5 minutes timeout for the API request

    @retry(CarbonCalculatorError, tries=3, delay=2, backoff=2)
    def get_carbon_footprint(self, url: str) -> dict[str, Any]:
        if not url:
            raise ValueError("URL cannot be empty.")

        try:
            response = requests.get(
                self.BASE_URL, params={"url": url}, timeout=self.TIMEOUT
            )
            response.raise_for_status()
            response_json = response.json()
        except requests.RequestException as e:
            raise CarbonCalculatorError(
                f"Request to Carbon Calculator API failed: {str(e)}"
            ) from e
        except ValueError as e:
            # This will catch JSON decoding errors
            raise CarbonCalculatorError(
                f"Failed to decode API response: {str(e)}"
            ) from e
        return response_json
