import json
import subprocess
from enum import StrEnum
from typing import Any


class LighthouseCategories(StrEnum):
    ACCESSIBILITY = "accessibility"
    BEST_PRACTICES = "best-practices"

class LighthouseError(Exception):
    pass

class AccessibilityError(Exception):
    pass

class BestPracticesError(Exception):
    pass

class LighthouseWrapper:
    def get_accessibility(self, url: str) -> dict[str, Any]:
        try:
            result = self.get_categories(url=url, categories=[LighthouseCategories.ACCESSIBILITY])
        except LighthouseError as e:
            raise AccessibilityError from e
        return result['accessibility']

    def get_best_practices(self, url:str) -> dict[str, Any]:
        try:
            result = self.get_categories(url=url, categories=[LighthouseCategories.BEST_PRACTICES])
        except LighthouseError as e:
            raise BestPracticesError from e
        return result['best-practices']

    def get_categories(self, url: str, categories: list[LighthouseCategories]) -> dict[str, Any]:
        try:
            lighthouse_process = subprocess.run(
                " ".join(
                    [
                        "lighthouse",
                        url,
                        '--chrome-flags="--no-sandbox --headless --disable-dev-shm-usage"',
                        f"--only-categories={','.join(categories)}",
                        "--output=json",
                        "--disable-full-page-screenshot",
                        "--no-enable-error-reporting",
                        "--quiet",
                    ]
                ),
                stdout=subprocess.PIPE,
                shell=True,
            )
            lighthouse_response = json.loads(lighthouse_process.stdout)
            result = lighthouse_response["categories"]
        except Exception as e:
            raise LighthouseError from e
        return result
