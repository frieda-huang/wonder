import asyncio
import os
from dataclasses import dataclass

from anthropic import APIResponse
from anthropic.types.beta import BetaContentBlockParam, BetaMessage, BetaMessageParam
from computer_use_demo.loop import sampling_loop
from computer_use_demo.tools import ToolResult
from dotenv import load_dotenv
from loguru import logger

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
    logger.debug(content_block)


def tool_output_callback(result: ToolResult, tool_id: str):
    print(result, tool_id)


def api_response_callback(response: APIResponse[BetaMessage]):
    logger.debug(response)


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
    instruction = "Find top colleges in Boston."
    asyncio.run(run_claude(instruction, DEFAULT_CONFIG))


if __name__ == "__main__":
    main()
