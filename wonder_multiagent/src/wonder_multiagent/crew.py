from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import EXASearchTool
from wonder_multiagent.tools.job_evaluation_tool import JobEvaluationTool
from wonder_multiagent.tools.job_match_tool import JobMatchTool
from wonder_multiagent.tools.resume_read_tool import ResumeReadTool

# Instantiate tools
exa_search_tool = EXASearchTool()
resume_read_tool = ResumeReadTool()
job_match_tool = JobMatchTool()
job_evaluation_tool = JobEvaluationTool()


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
    def resume_reader(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_reader"],
            tools=[resume_read_tool],
            verbose=True,
        )

    @agent
    def matcher(self) -> Agent:
        return Agent(
            config=self.agents_config["job_matcher"],
            tools=[job_match_tool],
            verbose=True,
        )

    @agent
    def quality_control_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["quality_control_specialist"],
            tools=[job_evaluation_tool],
            verbose=True,
        )

    # Define tasks
    @task
    def job_finding_task(self) -> Task:
        return Task(config=self.tasks_config["job_finding_task"])

    @task
    def resume_reading_task(self) -> Task:
        return Task(config=self.tasks_config["resume_reading_task"])

    @task
    def job_matching_task(self) -> Task:
        return Task(config=self.tasks_config["job_matching_task"])

    @task
    def job_quality_control_task(self) -> Task:
        return Task(config=self.tasks_config["job_quality_control_task"])

    @crew
    def crew(self) -> Crew:
        """Creates the WonderMultiagent crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
