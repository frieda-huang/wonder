# Based on https://github.com/HackerNews/API?tab=readme-ov-file

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from typing import List, Optional

import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

base_url = "https://hacker-news.firebaseio.com/v0"
jobstories = f"{base_url}/jobstories.json"


class JobPost(BaseModel):
    by: str
    id: int
    score: int
    time: datetime
    title: str
    type: str
    text: Optional[str] = None
    url: Optional[str] = None


class HNScrapeToolInput(BaseModel):
    last_n: int = Field(
        ..., description="The number of days to look back from the current date."
    )


class HNScrapeTool(BaseTool):
    name: str = "Hacker News Scrape Tool"
    description: str = "Scrape the latest software engineering jobs from Hacker News"

    def fetch_job_post(self, job_id: str):
        url = f"{base_url}/item/{job_id}.json"
        response = requests.get(url=url)
        return response.json()

    def _run(self, last_n: int) -> List[JobPost]:
        """Retrieve job listings posted within the past n days."""
        n_days_ago = datetime.now() - timedelta(days=last_n)
        response = requests.get(url=jobstories)
        job_ids = response.json()

        with ThreadPoolExecutor() as executor:
            job_posts = list(executor.map(self.fetch_job_post, job_ids))

        job_posts = [
            JobPost(**job_post)
            for job_post in job_posts
            if datetime.fromtimestamp(job_post["time"]) > n_days_ago
        ]

        return job_posts
