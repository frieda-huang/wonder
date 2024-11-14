import base64
from typing import List

from fastapi import FastAPI, File, Form, UploadFile
from wonder.run_job_search import run_claude, DEFAULT_CONFIG, create_instruction
import json

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
        "resume_filename": resume.filename,
        "location": location,
        "role_type": role_type,
        "aspirations": aspirations,
        "resume_base64_data": base64_encoded_data,
    }

    instruction = create_instruction(user_preferences, number_of_jobs_to_search=3)
    result = await run_claude(instruction, DEFAULT_CONFIG)

    data = result.text
    print(data)

    re = json.loads(data)
    inner_data = json.loads(re["content"])
    print(inner_data)


@app.get("/")
def root():
    return {"status": "success"}
