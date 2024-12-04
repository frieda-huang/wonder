#!/usr/bin/env python
import json
import os
import sys
import warnings
from datetime import datetime
from pathlib import Path

import agentops
from wonder_multiagent.crew import WonderMultiagent
from wonder_multiagent.memory import client

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"), default_tags=["job-search"])


# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

user_preferences = {
    "location": "SF and Silicon Valley",
    "role_type": "AI Full-Stack Software Engineer",
    "aspirations": (
        "I am seeking an entry-level software engineering role focused on LLMs, AI, Agents, "
        "and RAG, using Python, TypeScript, and Next.js. I prefer opportunities in SF and "
        "Silicon Valley."
    ),
}

filepath_to_resume = str(Path(__file__).parent / "tools" / "resume.jpeg")
date = datetime.today().strftime("%Y-%m-%d")


def run():
    """
    Run the crew.
    """
    inputs = {
        "user_preferences": user_preferences,
        "date": date,
        "num_jobs": 10,
        "filepath_to_resume": filepath_to_resume,
    }
    # Add user preferences to long-term memory
    client.add(json.dumps(user_preferences), user_id="friedahuang")
    crew_output = WonderMultiagent().crew().kickoff(inputs=inputs)
    if crew_output.json_dict:
        print(f"JSON Output: {json.dumps(crew_output.json_dict, indent=2)}")
    print(f"Token Usage: {crew_output.token_usage}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "user_preferences": user_preferences,
        "filepath_to_resume": filepath_to_resume,
    }
    try:
        WonderMultiagent().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        WonderMultiagent().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {"topic": "AI LLMs"}
    try:
        WonderMultiagent().crew().test(
            n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
