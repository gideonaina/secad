#main.py

import os
from pathlib import Path

import streamlit as st
import yaml
from dotenv import load_dotenv
from product_security_section import security_review_tab, threat_model_tab, requirement_refinement_tab

from ui.utils import get_model_provider

load_dotenv()
root_dir = Path(__file__).parent.parent
icon_path = os.path.join(root_dir, "assets/secad-icon.png")

st.set_page_config(
    page_title="Security Advisor",
    page_icon=icon_path,
    layout="wide",
    initial_sidebar_state="expanded",
)

logo_path = os.path.join(root_dir, "assets/logo.png")
st.sidebar.image(image=logo_path)

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

    get_model_provider(model_provider, data)
    model_temp = st.slider(label="Model Temperature", min_value=0.0, max_value=1.0, value=0.05, step=0.05, key="model_temp")

tab1, tab2, tab3 = st.tabs(["Threat Model", "Security Requirements", "Requirement Refinement"])
selected_model = st.session_state.get('selected_model', '')

with tab1:
    threat_model_tab.get_tab(data=data, model_provider=model_provider, selected_model=selected_model)

with tab2:
    security_review_tab.get_tab(data=data, model_provider=model_provider, selected_model=selected_model)

with tab3:
    requirement_refinement_tab.get_tab(data=data, model_provider=model_provider, selected_model=selected_model)