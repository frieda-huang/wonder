import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class URLValidatorToolInput(BaseModel):
    url: str = Field(
        ..., description="An URL to a website, be it a company website or job posting"
    )


class URLValidatorTool(BaseTool):
    """Detect any of broken links"""

    def _run(self, url: str) -> bool:
        try:
            result = requests.get(url, timeout=1)
            return result.status_code == 200
        except (requests.ConnectionError, requests.Timeout, requests.RequestException):
            return False
