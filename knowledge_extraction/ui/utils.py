import base64
from PIL import Image
import json
import requests
import streamlit as st
import base64
import re
from github import Github
from collections import defaultdict



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
        requirements = security_requirements.get("requirements", [])
        for index, requirement in enumerate(requirements):
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
        raise f"Error: {e}"
    return markdown_output


def get_model_provider(model_provider, config_data):

  if model_provider == "OpenAI API":
      # st.session_state['openai_api_key'] = openai_api_key
      # Add model selection input field to the sidebar
    selected_model = st.selectbox(
          "Select the model you would like to use:",
          config_data["sidebar"]["open_api"]["connection"]["model_selection"]["options"],
          key="selected_model",
          # help="GPT-4o and GPT-4o mini are OpenAI's latest models and are recommended."
      )

    if model_provider == "Ollama":
        # Make a request to the Ollama API to get the list of available models
        try:
            response = requests.get("http://localhost:11434/api/tags")
            response.raise_for_status() # Raise an exception for 4xx/5xx status codes
        except requests.exceptions.RequestException as e:
            st.error("Ollama endpoint not found, please select a different model provider.")
            response = None
        
        if response:
            data = response.json()
            available_models = [model["name"] for model in data["models"]]
            # Add model selection input field to the sidebar
            selected_model = st.selectbox(
                "Select the model you would like to use:",
                available_models,
                key="selected_model",
            )


def get_input(key=""):
    # github_url = st.text_input(
    #     label="Enter GitHub repository URL (optional)",
    #     placeholder="https://github.com/owner/repo",
    #     key=f"{key}_github_url",
    #     help="Enter the URL of the GitHub repository you want to analyze.",
    # )

    # if github_url and github_url != st.session_state.get('last_analyzed_url', ''):
    #     if 'github_api_key' not in st.session_state or not st.session_state['github_api_key']:
    #         st.warning("Please enter a GitHub API key to analyze the repository.")
    #     else:
    #         with st.spinner('Analyzing GitHub repository...'):
    #             system_description = analyze_github_repo(github_url)
    #             st.session_state['github_analysis'] = system_description
    #             st.session_state['last_analyzed_url'] = github_url
    #             st.session_state['app_input'] = system_description + "\n\n" + st.session_state.get('app_input', '')

    input_text = st.text_area(
        label="Describe the application to be modelled",
        value=st.session_state.get('app_input', ''),
        placeholder="Enter your application details...",
        height=300,
        key=f"{key}_app_desc",
        help="Please provide a detailed description of the application, including the purpose of the application, the technologies used, and any other relevant information.",
    )

    st.session_state['app_input'] = input_text

    return input_text


def analyze_github_repo(repo_url):
    # Extract owner and repo name from URL
    parts = repo_url.split('/')
    owner = parts[-2]
    repo_name = parts[-1]

    # Initialize PyGithub
    g = Github(st.session_state.get('github_api_key', ''))

    # Get the repository
    repo = g.get_repo(f"{owner}/{repo_name}")

    # Get the default branch
    default_branch = repo.default_branch

    # Get the tree of the default branch
    tree = repo.get_git_tree(default_branch, recursive=True)

    # Analyze files
    file_summaries = defaultdict(list)
    total_chars = 0
    char_limit = 100000  # Adjust this based on your model's token limit
    readme_content = ""

    for file in tree.tree:
        if file.path.lower() == 'readme.md':
            content = repo.get_contents(file.path, ref=default_branch)
            readme_content = base64.b64decode(content.content).decode()
        elif file.type == "blob" and file.path.endswith(('.py', '.js', '.ts', '.html', '.css', '.java', '.go', '.rb')):
            content = repo.get_contents(file.path, ref=default_branch)
            decoded_content = base64.b64decode(content.content).decode()
            
            # Summarize the file content
            summary = summarize_file(file.path, decoded_content)
            file_summaries[file.path.split('.')[-1]].append(summary)
            
            total_chars += len(summary)
            if total_chars > char_limit:
                break

    # Compile the analysis into a system description
    system_description = f"Repository: {repo_url}\n\n"
    
    if readme_content:
        system_description += "README.md Content:\n"
        # Truncate README if it's too long
        if len(readme_content) > 5000:
            system_description += readme_content[:5000] + "...\n(README truncated due to length)\n\n"
        else:
            system_description += readme_content + "\n\n"

    for file_type, summaries in file_summaries.items():
        system_description += f"{file_type.upper()} Files:\n"
        for summary in summaries:
            system_description += summary + "\n"
        system_description += "\n"

    return system_description

def summarize_file(file_path, content):
    # Extract important parts of the file
    imports = re.findall(r'^import .*|^from .* import .*', content, re.MULTILINE)
    functions = re.findall(r'def .*\(.*\):', content)
    classes = re.findall(r'class .*:', content)

    summary = f"File: {file_path}\n"
    if imports:
        summary += "Imports:\n" + "\n".join(imports[:5]) + "\n"  # Limit to first 5 imports
    if functions:
        summary += "Functions:\n" + "\n".join(functions[:5]) + "\n"  # Limit to first 5 functions
    if classes:
        summary += "Classes:\n" + "\n".join(classes[:5]) + "\n"  # Limit to first 5 classes

    return summary
