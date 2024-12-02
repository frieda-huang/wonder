from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from wonder_multiagent.tools.resume_read_util import claude_vision


class ResumeReadToolInput(BaseModel):
    filepath_to_resume: str = Field(
        ..., description="Provide a filepath to access the resume"
    )


class ResumeReadTool(BaseTool):
    name: str = "Resume Read Tool"
    description: str = "Parse resume and extract key details about a job seeker"
    args_schema: type[BaseModel] = ResumeReadToolInput

    def _run(self, filepath_to_resume: str):
        return claude_vision(filepath=filepath_to_resume)
