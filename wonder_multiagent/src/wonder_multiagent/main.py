#!/usr/bin/env python
import sys
import warnings

from wonder_multiagent.crew import WonderMultiagent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

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

filepath_to_resume = "./tools/resume.jpeg"


def run():
    """
    Run the crew.
    """
    inputs = {
        "user_preferences": user_preferences,
        "filepath_to_resume": filepath_to_resume,
    }
    WonderMultiagent().crew().kickoff(inputs=inputs)


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
