import json
import os

import streamlit as st

from knowledge_retrieval.image_review_crew.image_review import ImageReview
from knowledge_retrieval.product_security_crew.threat_model_crew import ThreatModelCrew
from ui.utils import get_input, get_llm_model


def get_tab(data, selected_model, model_provider):

    temp_slider = st.session_state.get('model_temp')

    # Initialize app_input in the session state if it doesn't exist
    if 'app_input' not in st.session_state:
        st.session_state['app_input'] = ''
    
    # Only do file analysis for OpenAI models.
    if model_provider and selected_model in data["sidebar"]["open_api"]["connection"]["model_selection"]["options"]:
        uploaded_file = st.file_uploader("Upload architecture diagram", type=data["sidebar"]["open_api"]["modal"]["upload_file_types"])
        
        model_info = {
            'model_temp': temp_slider,
            'selected_model': selected_model,
            'model_provider': model_provider
        }
        llm_model = get_llm_model(model_info)

        if uploaded_file is not None:
            if 'uploaded_file' not in st.session_state or st.session_state.uploaded_file != uploaded_file:
                print(f"$$$${uploaded_file}$$$$ file url {uploaded_file._file_urls}")

                st.session_state.uploaded_file = uploaded_file
                with st.spinner("Agent analysing image..."):
                    temp_dir = "/tmp"  # Specify your desired directory
                    os.makedirs(temp_dir, exist_ok=True)
                    file_path = os.path.join(temp_dir, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    try:
                        image_analysis_output = ImageReview().run(llm_model, file_path)
                        if image_analysis_output:
                            st.session_state.image_analysis_content = image_analysis_output
                            st.session_state['app_input'] = image_analysis_output
                        else:
                            st.error("Failed to analyze the image.")
                    except Exception as e:
                        st.error("An unexpected error occurred while analyzing the image. Error {e}")
                        print(f"Error: {e}")
                
                
                    
    # Use the get_input() function to get the application description and GitHub URL
    app_input = get_input()
    # Update session state only if the text area content has changed
    if app_input != st.session_state['app_input']:
        st.session_state['app_input'] = app_input


    # Create a submit button for Threat Modelling
    threat_model_submit_button = st.button(label="Generate Threat Model")

    # If the Generate Threat Model button is clicked and the user has provided an application description
    if threat_model_submit_button and st.session_state.get('app_input'):
        app_input = st.session_state['app_input']  # Retrieve from session state
        model_temp = st.session_state.get('model_temp')

        # Show a spinner while generating the threat model
        with st.spinner("Analysing potential threats..."):

            try:
                model_info = {
                    'model_temp': model_temp,
                    'selected_model': selected_model,
                    'model_provider': model_provider
                }
                llm_model = get_llm_model(model_info)
                
                threat_model_output = ThreatModelCrew().execute(llm_model, system_information=app_input)
                st.session_state['threat_model'] = threat_model_output
            except Exception as e:
                st.error(f"Error generating threat model. Error: {e}")

        # Convert the threat model JSON to Markdown
        markdown_output =  json_to_threat_model_markdown(threat_model_output)

        # Display the threat model in Markdown
        st.markdown(markdown_output)

        st.download_button(
            label="Download Threat Model",
            data=markdown_output,  # Use the Markdown output
            file_name="threat_model.md",
            mime="text/markdown",
       )
        # If the submit button is clicked and the user has not provided an application description
        if threat_model_submit_button and not st.session_state.get('app_input'):
            st.error("Please enter your application details before submitting.")
        
def json_to_threat_model_markdown(threat_model):

    try:
        threat_model_obj = json.loads(threat_model)
    except json.JSONDecodeError as e:
        raise (f"JSON decoding error: {e}")

    markdown_output = "## Threat Model\n\n"
    
    # Start the markdown table with headers
    markdown_output += "| Reference | Threat Scenario | Threat Type | Potential Impact | Control |\n"
    markdown_output += "|-----------|-----------------|-------------|------------------|---------|\n"
    
    # Fill the table rows with the threat model data
    threat_model_dict = threat_model_obj.get("threat_model", [])
    for idx, threat in enumerate(threat_model_dict):
        markdown_output += f"| R.{idx+1} | {threat['threat_type']} | {threat['threat_scenario']} | {threat['impact']} |{threat['control']} |\n"
    
    return markdown_output
