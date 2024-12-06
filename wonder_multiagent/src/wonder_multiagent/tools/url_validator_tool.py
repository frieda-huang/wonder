import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class URLValidatorToolInput(BaseModel):
    url: str = Field(
        ..., description="An URL to a website, be it a company website or job posting"
    )


class URLValidatorTool(BaseTool):
    name: str = "URL Validator Tool"
    description: str = "Detect any broken links on job listings"
    args_schema: type[BaseModel] = URLValidatorToolInput

    def _run(self, url: str) -> str:
        try:
            result = requests.get(url, timeout=3, allow_redirects=True)
            if result.status_code == 200:
                return f"URL is valid (status: 200)"
            else:
                return f"URL potentially invalid (status: {result.status_code})"
        except Exception as e:
            return f"URL invalid (error: {str(e)})"
