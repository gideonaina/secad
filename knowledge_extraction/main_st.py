#main.py

import base64
import requests
import streamlit as st
import streamlit.components.v1 as components
from github import Github
from collections import defaultdict
import re
import os
from dotenv import load_dotenv
import yaml
from ui.streamlit_ui.utils import get_model_provider
from ui.streamlit_ui import threat_model_tab, security_review_tab


# def load_env_variables():
#     # Try to load from .env file
#     if os.path.exists('.env'):
#         load_dotenv('.env')
    
#     # Load GitHub API key from environment variable
#     github_api_key = os.getenv('GITHUB_API_KEY')
#     if github_api_key:
#         st.session_state['github_api_key'] = github_api_key

#     # Load other API keys if needed
#     openai_api_key = os.getenv('OPENAI_API_KEY')
#     if openai_api_key:
#         st.session_state['openai_api_key'] = openai_api_key

#     azure_api_key = os.getenv('AZURE_API_KEY')
#     if azure_api_key:
#         st.session_state['azure_api_key'] = azure_api_key

#     azure_api_endpoint = os.getenv('AZURE_API_ENDPOINT')
#     if azure_api_endpoint:
#         st.session_state['azure_api_endpoint'] = azure_api_endpoint

#     azure_deployment_name = os.getenv('AZURE_DEPLOYMENT_NAME')
#     if azure_deployment_name:
#         st.session_state['azure_deployment_name'] = azure_deployment_name

#     google_api_key = os.getenv('GOOGLE_API_KEY')
#     if google_api_key:
#         st.session_state['google_api_key'] = google_api_key

#     mistral_api_key = os.getenv('MISTRAL_API_KEY')
#     if mistral_api_key:
#         st.session_state['mistral_api_key'] = mistral_api_key

# # Call this function at the start of your app
# load_env_variables()

# ------------------ Streamlit UI Configuration ------------------ #

st.set_page_config(
    page_title="Security Advisor",
    page_icon=":bird:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------ Sidebar ------------------ #

# st.sidebar.image("logo.png")
st.sidebar.header("Security Advisor")

# Add instructions on how to use the app to the sidebar
# st.sidebar.header("How to use STRIDE GPT")

with open("knowledge_extraction/config/side_bar_definition.yml", "r") as file:
    data = yaml.safe_load(file)

with st.sidebar:
    # Add model selection input field to the sidebar
    model_provider = st.selectbox(
        "Select your preferred model provider:",
        data["sidebar"]["models"]["types"],
        key=data["sidebar"]["models"]["key"],
        # help="Select the model provider you would like to use. This will determine the models available for selection.",
    )

    get_model_provider(model_provider, data)

    model_temp = st.slider(label="Model Temperature", min_value=0.0, max_value=1.0, value=0.05, step=0.05, key="model_temp")
    # st.session_state['model_temp'] = model_temp

# ------------------ Main App UI ------------------ #

# tab1, tab2 = st.tabs(["Threat Model", "Security Requirements"])
tab1, tab2 = st.tabs(["Threat Model", "Security Requirements"])
selected_model = st.session_state.get('selected_model', '')

with tab1:
    threat_model_tab.get_tab(data=data, model_provider=model_provider, selected_model=selected_model)

with tab2:
    security_review_tab.get_tab(data=data, model_provider=model_provider, selected_model=selected_model)