#main.py

import base64
import requests
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
from github import Github
from collections import defaultdict
import re
import os
from dotenv import load_dotenv
import yaml
from ui.utils import get_model_provider
from product_security_section import threat_model_tab, security_review_tab

load_dotenv()

st.set_page_config(
    page_title="Security Advisor",
    page_icon=":bird:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# st.sidebar.image("logo.png")
st.sidebar.header("Security Advisor")

root_dir = Path(__file__).parent.parent
config_path = os.path.join(root_dir, "config/side_bar_definition.yml")

with open(config_path, "r") as file:
    data = yaml.safe_load(file)

with st.sidebar:
    st.markdown("---")
    st.markdown("## Model Configuration")

    model_provider = st.selectbox(
        "Select your preferred model provider:",
        data["sidebar"]["models"]["types"],
        key=data["sidebar"]["models"]["key"],
        help="Select the model provider you would like to use.",
    )

    print(f"********** model provider - {model_provider}")

    get_model_provider(model_provider, data)

    model_temp = st.slider(label="Model Temperature", min_value=0.0, max_value=1.0, value=0.05, step=0.05, key="model_temp")

# ------------------ Main App UI ------------------ #

# tab1, tab2 = st.tabs(["Threat Model", "Security Requirements"])
tab1, tab2 = st.tabs(["Threat Model", "Security Requirements"])
selected_model = st.session_state.get('selected_model', '')

with tab1:
    threat_model_tab.get_tab(data=data, model_provider=model_provider, selected_model=selected_model)

with tab2:
    security_review_tab.get_tab(data=data, model_provider=model_provider, selected_model=selected_model)