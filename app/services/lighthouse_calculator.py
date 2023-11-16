import json
import subprocess
from typing import Any


class LighthouseError(Exception):
    pass


class LighthouseCalculator:
    def get_lighthouse(self, url: str) -> dict[str, Any]:
        try:
            lighthouse_process = subprocess.run(
                " ".join(
                    [
                        "lighthouse",
                        url,
                        '--chrome-flags="--no-sandbox --headless --disable-dev-shm-usage"',
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
            result = lighthouse_response
        except Exception as e:
            raise LighthouseError from e
        return result
