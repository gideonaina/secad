#main.py

import os
from pathlib import Path

import streamlit as st
import yaml
from dotenv import load_dotenv
from product_security_section import security_review_tab, threat_model_tab, threat_analysis_tab

from ui.utils import get_model_provider
from rag_management.data_prep import save_as_embedding

load_dotenv()
root_dir = Path(__file__).parent.parent
icon_path = os.path.join(root_dir, "assets/secad-icon.png")
os.makedirs(os.path.join(root_dir, "tmp"), exist_ok=True)
TMP_FILE_PATH = os.path.join(root_dir, "tmp")
st.session_state["TMP_FILE_PATH"] = TMP_FILE_PATH

st.set_page_config(
    page_title="Security Advisor",
    page_icon=icon_path,
    layout="wide",
    initial_sidebar_state="expanded",
)

logo_path = os.path.join(root_dir, "assets/logo.png")
# st.sidebar.image(image=logo_path)

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

    st.markdown("---")
    st.markdown("## RAG Configuration")
    is_rag_used_value = False
    is_rag_used = st.toggle("Update RAG", value=is_rag_used_value, key="use_rag", help="Use to specify if a RAG should be used for the current workflow")
    if is_rag_used:
        st.selectbox(
            "Select the collection to use", data["sidebar"]["rag"]["collections"],
            key="rag_selection", help="Select the collection to use",
    )
        uploaded_doc = st.file_uploader("Upload Document to add to RAG", key="rag_uploader", type=["pdf"], help="Upload a document to add to the RAG")
        
        if uploaded_doc is not None:
            with st.spinner("Saving to RAG ..."):
                result = save_as_embedding(uploaded_doc, st.session_state.rag_selection)
                st.info(result["message"])


# tab1  = st.tabs(["Threat Model"])[0]
tab1, tab2 = st.tabs(["Threat Model", "Control - Threat Model"])
selected_model = st.session_state.get('selected_model', '')

with tab1:
    threat_analysis_tab.get_tab(data=data, model_provider=model_provider, selected_model=selected_model)

with tab2:
    threat_model_tab.get_tab(data=data, model_provider=model_provider, selected_model=selected_model)

# with tab3:
#     security_review_tab.get_tab(data=data, model_provider=model_provider, selected_model=selected_model)

# with tab3:
#     requirement_refinement_tab.get_tab(data=data, model_provider=model_provider, selected_model=selected_model)