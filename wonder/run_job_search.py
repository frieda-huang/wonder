import json
import os
import pprint
from dataclasses import dataclass
from typing import Optional

from anthropic import APIResponse
from anthropic.types.beta import BetaContentBlockParam, BetaMessage, BetaMessageParam
from dotenv import load_dotenv
from wonder.computer_use_demo.loop import sampling_loop
from wonder.computer_use_demo.tools import ToolResult

load_dotenv()

final_response: Optional[APIResponse[BetaMessage]] = None


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
    global final_response
    final_response = response
    pprint.pprint(response)


async def run_claude(
    instruction: str, config: Config
) -> Optional[APIResponse[BetaMessage]]:
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

    return final_response


def extract_json_from_text(text: str):
    import anthropic

    client = anthropic.Anthropic()

    prompt = f"""
    Please extract all JSON objects from the following text and return them as a list of JSON objects:

    {text}

    Provide only the JSON objects without any additional text or explanations.
    """

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        temperature=0,
        system=prompt,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    return message.content[0].text


def create_instruction(user_preferences: dict, number_of_jobs_to_search: int) -> str:
    user_preferences_json = json.dumps(user_preferences, indent=4)

    instruction = f"""
    You have a user’s job search preferences for a tech position. The preferences are as follows:

    {user_preferences_json}

    Instructions:
        1.	Analyze the user’s preferences (location, role_type, and aspirations) to understand their experience and goals.
        2.	Based on this analysis, find the top {number_of_jobs_to_search} job listings that best match all specified preferences by searching on https://www.workatastartup.com and https://wellfound.com/jobs.
        
    Please output **only** the job results in the following JSON array format. Do not add any additional text, explanations, or comments:
    [
        {{
            "location": "City or region where the job is located",
            "role_name": "Title of the job role",
            "company_name": "Name of the hiring company",
            "description": "Brief summary or description of the company",
            "experience_level": "Level of experience required (e.g., Entry, Mid, Senior)",
            "required_skills": ["List", "of", "required", "skills"],
            "category": ["List", "of", "industries or sectors related to the job (e.g., Enterprise Software, Fintech, Health Tech, Education Tech, E-commerce)"],
            "link_to_website": "Direct link to the company's website",
            "link_to_job": "Direct link to the job posting"
        }},
    ]
    """
    return instruction
