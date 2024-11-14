import asyncio
import os
import pprint
from dataclasses import dataclass

from anthropic import APIResponse
from anthropic.types.beta import BetaContentBlockParam, BetaMessage, BetaMessageParam
from computer_use_demo.loop import sampling_loop
from computer_use_demo.tools import ToolResult
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    provider: str = "anthropic"
    model: str = "claude-3-5-sonnet-20241022"
    api_key: str = os.getenv("ANTHROPIC_API_KEY")
    max_tokens: int = 4096
    recent_images: int = 10
    verbose: bool = False


DEFAULT_CONFIG = Config()


def output_callback(content_block: BetaContentBlockParam):
    pprint.pprint(content_block)


def tool_output_callback(result: ToolResult, tool_id: str):
    if result.base64_image:
        return
    else:
        pprint.pprint(result)


def api_response_callback(response: APIResponse[BetaMessage]):
    pprint.pprint(response)


async def run_claude(instruction: str, config: Config) -> None:
    messages: list[BetaMessageParam] = [
        {
            "role": "user",
            "content": instruction,
        }
    ]

    messages = await sampling_loop(
        model=config.model,
        provider=config.provider,
        system_prompt_suffix="",
        messages=messages,
        output_callback=output_callback,
        tool_output_callback=tool_output_callback,
        api_response_callback=api_response_callback,
        api_key=config.api_key,
        only_n_most_recent_images=config.recent_images,
        max_tokens=config.max_tokens,
    )


def main():
    NUMBER_OF_JOBS = 10
    instruction = f"""
    You have a user’s job search preferences for a tech position. The preferences contain:
        - location: a string specifying the city or region.
        - resume: a PDF document encoded in base64, under "base64_data", representing the user’s experience and skills.
        - role type: a list of strings indicating preferred roles, which include:
            - AI & Machine Learning
            - Full Stack
            - Backend
            - Frontend
            - Data Science
            - System & Infrastructure
        - aspirations: a string describing the user’s career goals or ideal job role.

    Example:
    {{
        "message": "File and data processed successfully",
        "filename": "resume.pdf",
        "location": "San Francisco",
        "role_type": [
            "AI & Machine Learning",
            "Full Stack",
            "System & Infrastructure"
        ],
        "aspirations": "I’m looking for an AI engineer role at a San Francisco startup 
                        focused on large language models, machine learning, RAG, and Python.",
        "base64_data": "RESUME DATA"
    }}

    Instructions:
        1.	Use the pdf_reader tool to parse the "base64_data" field for the resume.
        2.	Analyze the resume content alongside the user’s preferences (location, roleType, and aspirations) to understand their experience and goals.
        3.	Based on this analysis, find the top {NUMBER_OF_JOBS} job listings that best match all specified preferences.
    """
    asyncio.run(run_claude(instruction, DEFAULT_CONFIG))


if __name__ == "__main__":
    main()
