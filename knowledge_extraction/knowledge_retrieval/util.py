import os
import base64
from PIL import Image
import json

def remove_file(tmp_file):
    # Step 1: Delete the temp file if it exists
    if os.path.exists(tmp_file):
        os.remove(tmp_file)
        print(f"Deleted existing file: {tmp_file}")

def append_to_file(tmp_file, content):
    with open(tmp_file, "a") as file:
        file.write(content + '\n')
        print(f"Appended to file: {tmp_file}")

def read_file(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        raise f"Error: The file '{file_path}' was not found."
    except Exception as e:
        raise f"Error: {file_path}"
    
def image_parsing():
    pass

    # # Load the image file
    # image_path = 'path_to_your_architectural_diagram.png'
    # with open(image_path, 'rb') as image_file:
    #     image_data = image_file.read()

    # # Send the image to GPT-4-V for analysis and description
    # response = openai.ChatCompletion.create(
    #     model="gpt-4",  # or "gpt-4-vision" if a specific endpoint exists
    #     messages=[
    #         {"role": "system", "content": "You are an expert in software architecture."},
    #         {"role": "user", "content": "Please describe the content of this software architectural diagram."}
    #     ],
    #     files=[
    #         {"name": "architectural_diagram.png", "content": image_data}
    #     ]
    # )

    # # Output the description
    # print(response['choices'][0]['message']['content'])

def resize_image(image_path, max_width=200, max_height=200):
    image = Image.open(image_path)
    image.thumbnail((max_width, max_height))
    resized_path = image_path
    image.save(resized_path)
    print(f"resized_path - {resized_path}")
    return resized_path

def process_file_base64(file):
    if file is None:
        return ""
    
    print(f"picture b4 encoding: {file}")
    resized_file_path = resize_image(file)
    with open(resized_file_path, "rb") as f:
        file_content = f.read()
        encoded_file = base64.b64encode(file_content).decode('utf-8')
    return encoded_file

def json_to_security_requirement_table (security_requirements_json):
    try:
        security_requirements = json.loads(security_requirements_json)
    except json.JSONDecodeError as e:
        raise (f"JSON decoding error: {e}")

    markdown_output =  "| Reference | Requirement | Details     | Threat Scenario | Risk Score | Status |\n"
    markdown_output += "|-----------|-------------|-------------|-----------------|------------|--------|\n"
    try:
        # Access the list of threats under the "Risk Assessment" key
        requirements = security_requirements.get("requirements", [])
        for index, requirement in enumerate(requirements):
            # Check if threat is a dictionary
            if isinstance(requirement, dict):
                reference = f"R.{index+1}"
                req = requirement.get('requirement', '')
                details = requirement.get('details', '')
                threat_scenario = requirement.get('threat_scenario', '')
                risk_score = requirement.get('risk_score', '')
                status = requirement.get('status', '')

                markdown_output += f"| {reference} | {req} | {details} | {threat_scenario} | {risk_score} | {status} |\n"
            else:
                raise TypeError(f"Expected a dictionary, got {type(requirement)}")
    except Exception as e:
        # Print the error message and type for debugging
        # st.write(f"Error: {e}")
        raise f"Error: {e}"
    return markdown_output

