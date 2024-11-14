import base64
import json
from typing import List

from fastapi import FastAPI, File, Form, UploadFile
from wonder.run_job_search import (
    DEFAULT_CONFIG,
    create_instruction,
    extract_json_from_text,
    run_claude,
)

app = FastAPI()


@app.post("/submit-preferences")
async def submit_preferences(
    resume: UploadFile = File(...),
    location: str = Form(...),
    role_type: List[str] = Form(...),
    aspirations: str = Form(...),
):
    file_data = await resume.read()
    base64_encoded_data = base64.b64encode(file_data).decode("utf-8")

    user_preferences = {
        "location": location,
        "role_type": role_type,
        "aspirations": aspirations,
    }

    instruction = create_instruction(user_preferences, number_of_jobs_to_search=1)
    claude_response = await run_claude(instruction, DEFAULT_CONFIG)

    # Extract json objects from claude response
    data = claude_response.text
    json_data = json.loads(data)
    text = json_data["content"][0]["text"]
    jobs = json.loads(extract_json_from_text(text))
    return jobs


@app.get("/")
def root():
    return {"status": "success"}
