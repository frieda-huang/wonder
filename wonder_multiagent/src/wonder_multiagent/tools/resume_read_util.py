import base64

from anthropic import Anthropic

client = Anthropic()
MODEL_NAME = "claude-3-opus-20240229"

resume_read_tool = {
    "name": "resume_parser",
    "description": "Processes an image of a job resume to extract detailed career information, such as contact details, summary, education, skills, work experience, and projects.",
    "input_schema": {
        "type": "object",
        "properties": {
            "contact_information": {
                "type": "string",
                "description": "Job seeker's email address, phone number, or other contact details.",
            },
            "professional_summary": {
                "type": "string",
                "description": "A brief summary of the job seeker's professional background and goals.",
            },
            "education": {
                "type": "string",
                "description": "Details of the job seeker's educational background, including degrees and institutions.",
            },
            "skills": {
                "type": "string",
                "description": "A list of key skills relevant to the job seeker's profession.",
            },
            "work_experience": {
                "type": "string",
                "description": "Details of past work experiences, including job titles, companies, and durations.",
            },
            "projects": {
                "type": "string",
                "description": "Descriptions of notable projects the job seeker has worked on, showcasing relevant accomplishments.",
            },
        },
        "required": [
            "contact_information",
            "professional_summary",
            "education",
            "skills",
            "work_experience",
        ],
    },
}


def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as image_file:
        binary_data = image_file.read()
        base_64_encoded_data = base64.b64encode(binary_data)
        base64_string = base_64_encoded_data.decode("utf-8")
        return base64_string


def claude_vision(filepath: str):
    message_list = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": get_base64_encoded_image(filepath),
                    },
                },
                {
                    "type": "text",
                    "text": "Please extract the key information from this resume image.",
                },
            ],
        }
    ]

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=4096,
        messages=message_list,
        tools=[resume_read_tool],
    )

    if response.stop_reason == "tool_use":
        last_content_block = response.content[-1]
        if last_content_block.type == "tool_use":
            tool_name = last_content_block.name
            tool_inputs = last_content_block.input
            print(f"=======Claude Wants To Call The {tool_name} Tool=======")
            print(tool_inputs)

    else:
        print("No tool was called. This shouldn't happen!")

    return tool_inputs
