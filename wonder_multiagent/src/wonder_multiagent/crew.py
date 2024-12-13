from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import EXASearchTool, WebsiteSearchTool
from wonder_multiagent.tools.resume_read_tool import ResumeReadTool
from wonder_multiagent.tools.url_validator_tool import URLValidatorTool

# Instantiate tools
exa_search_tool = EXASearchTool()
resume_read_tool = ResumeReadTool()
url_validator_tool = URLValidatorTool()
website_scrape_tool = WebsiteSearchTool()


@CrewBase
class WonderMultiagent:
    """WonderMultiagent crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # Create agents
    @agent
    def job_finder(self) -> Agent:
        return Agent(
            config=self.agents_config["job_finder"],
            tools=[exa_search_tool],
            verbose=True,
        )

    @agent
    def website_scraper(self) -> Agent:
        return Agent(
            config=self.agents_config["website_scraper"],
            tools=[website_scrape_tool],
            verbose=True,
        )

    @agent
    def resume_reader(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_reader"],
            tools=[resume_read_tool],
            verbose=True,
        )

    @agent
    def matcher(self) -> Agent:
        return Agent(
            config=self.agents_config["matcher"],
            verbose=True,
        )

    @agent
    def quality_control_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["quality_control_specialist"],
            tools=[url_validator_tool],
            verbose=True,
        )

    # Define tasks
    @task
    def job_finding_task(self) -> Task:
        return Task(config=self.tasks_config["job_finding_task"])

    @task
    def website_scrape_task(self) -> Task:
        return Task(
            config=self.tasks_config["website_scrape_task"],
            context=[self.job_finding_task()],
        )

    @task
    def resume_reading_task(self) -> Task:
        return Task(config=self.tasks_config["resume_reading_task"])

    @task
    def job_matching_task(self) -> Task:
        return Task(
            config=self.tasks_config["job_matching_task"],
            context=[self.resume_reading_task(), self.website_scrape_task()],
        )

    @task
    def job_quality_control_task(self) -> Task:
        return Task(
            config=self.tasks_config["job_quality_control_task"],
            context=[self.job_matching_task()],
            output_file="output/jobs.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the WonderMultiagent crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            memory=True,
            memory_config={"provider": "mem0", "config": {"user_id": "friedahuang"}},
        )
