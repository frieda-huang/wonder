import base64
from typing import List

from fastapi import FastAPI, File, Form, UploadFile

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

    return {
        "message": "File and data processed successfully",
        "filename": resume.filename,
        "location": location,
        "role_type": role_type,
        "aspirations": aspirations,
        "base64_data": base64_encoded_data,
    }


@app.get("/")
def root():
    return {"status": "success"}
