# Based on Exa API https://docs.exa.ai/reference/search#body-use-autoprompt

import os
from typing import List, Literal, Optional, TypeAlias

from crewai.tools import BaseTool
from dotenv import load_dotenv
from exa_py import Exa
from pydantic import BaseModel, Field

load_dotenv()

CategoryType: TypeAlias = Literal["company", "tweet"]


class ExaSearchToolInput(BaseModel):
    query: str = Field(..., description="The query string")
    category: CategoryType = Field(..., description="A data category to focus on")
    num_results: int = Field(..., description="Number of search results to return")
    include_domains: List[str] = Field(
        default=[
            "https://www.ycombinator.com/jobs",
            "https://wellfound.com/jobs",
            "https://x.com/jobs",
        ],
        description="List of domains to include in the search. If specified, results will only come from these domains",
    )
    start_crawl_date: str = Field(
        ...,
        description="Crawl date refers to the date that Exa discovered a link. Results will include links that were crawled after this date",
    )


class ExaSearchTool(BaseTool):
    name: str = "Exa Search Tool"
    description: str = "Retrieve most relevant job listings"
    args_schema: type[BaseModel] = ExaSearchToolInput

    def _run(
        self,
        query: str,
        category: CategoryType,
        num_results: int,
        start_crawl_date: str,
        include_domains: Optional[List[str]] = None,
    ):
        exa_api_key = os.getenv("EXA_API_KEY")
        if not exa_api_key:
            raise ValueError("EXA_API_KEY is not set")

        exa = Exa(exa_api_key)
        response = exa.search_and_contents(
            query,
            type="neural",
            use_autoprompt=True,
            category=category,
            num_results=num_results,
            start_crawl_date=start_crawl_date,
            include_domains=include_domains,
            highlights=True,
        )

        parsedResult = "".join(
            [
                f"<Title id={idx}>{eachResult.title}</Title>"
                f"<URL id={idx}>{eachResult.url}</URL>"
                f'<Highlight id={idx}>{"".join(eachResult.highlights)}</Highlight>'
                for (idx, eachResult) in enumerate(response.results)
            ]
        )

        return parsedResult
