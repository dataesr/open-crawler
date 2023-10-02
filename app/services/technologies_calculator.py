import json
import subprocess
from typing import Any


class TechnologiesError(Exception):
    pass


class TechnologiesCalculator:
    def get_technologies(self, url: str) -> list[dict[str, Any]]:
        try:
            technologies_process = subprocess.run(
                " ".join(
                    [
                        "node",
                        "/wappalyzer/src/drivers/npm/cli.js",
                        url,
                    ]
                ),
                stdout=subprocess.PIPE,
                shell=True,
            )
            technologies_response = json.loads(technologies_process.stdout)
            result = technologies_response["technologies"]
            result = self._be_agnostic(result)
        except Exception as e:
            raise TechnologiesError from e
        return result

    def _be_agnostic(
        self, result: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        return [res for res in result if res["confidence"] == 100]
