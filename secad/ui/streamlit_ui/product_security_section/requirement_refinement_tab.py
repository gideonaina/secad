import json
import os

import streamlit as st

from knowledge_retrieval.product_security_crew.requirement_refinement_crew import RequirementRefinementCrew
from ui.utils import get_input, get_llm_model


# def get_tab(data, selected_model, model_provider):

#     temp_slider = st.session_state.get('model_temp')

#     # Initialize app_input in the session state if it doesn't exist
#     if 'app_input' not in st.session_state:
#         st.session_state['app_input'] = ''
    
#     # Only do file analysis for OpenAI models.
#     if model_provider and selected_model in data["sidebar"]["open_api"]["connection"]["model_selection"]["options"]:
#         uploaded_file = st.file_uploader("Upload architecture diagram", type=data["sidebar"]["open_api"]["modal"]["upload_file_types"])
        
#         model_info = {
#             'model_temp': temp_slider,
#             'selected_model': selected_model,
#             'model_provider': model_provider
#         }
#         llm_model = get_llm_model(model_info)

#         # if uploaded_file is not None:
#         #     if 'uploaded_file' not in st.session_state or st.session_state.uploaded_file != uploaded_file:
#         #         print(f"$$$${uploaded_file}$$$$ file url {uploaded_file._file_urls}")

#         #         st.session_state.uploaded_file = uploaded_file
#         #         with st.spinner("Agent analysing image..."):
#         #             temp_dir = "/tmp"  # Specify your desired directory
#         #             os.makedirs(temp_dir, exist_ok=True)
#         #             file_path = os.path.join(temp_dir, uploaded_file.name)
#         #             with open(file_path, "wb") as f:
#         #                 f.write(uploaded_file.getbuffer())

#         #             try:
#         #                 image_analysis_output = ImageReview().run(llm_model, file_path)
#         #                 if image_analysis_output:
#         #                     st.session_state.image_analysis_content = image_analysis_output
#         #                     st.session_state['app_input'] = image_analysis_output
#         #                 else:
#         #                     st.error("Failed to analyze the image.")
#         #             except Exception as e:
#         #                 st.error("An unexpected error occurred while analyzing the image. Error {e}")
#         #                 print(f"Error: {e}")
                
                
                    
#     # Use the get_input() function to get the application description and GitHub URL
#     # app_input = get_input()
#     # Update session state only if the text area content has changed
#     if app_input != st.session_state['app_input']:
#         st.session_state['app_input'] = app_input


#     # Create a submit button for Threat Modelling
#     refine_button = st.button(label="Refine Requirements")

#     # If the Generate Threat Model button is clicked and the user has provided an application description
#     if refine_button and st.session_state.get('app_input'):
#         app_input = st.session_state['app_input']  # Retrieve from session state
#         model_temp = st.session_state.get('model_temp')

#         # Show a spinner while generating the threat model
#         with st.spinner("Refining Requirements..."):

#             try:
#                 model_info = {
#                     'model_temp': model_temp,
#                     'selected_model': selected_model,
#                     'model_provider': model_provider
#                 }
#                 llm_model = get_llm_model(model_info)
                
#                 threat_model_output = ThreatModelCrew().execute(llm_model, system_information=app_input)
#                 st.session_state['threat_model'] = threat_model_output
#             except Exception as e:
#                 st.error(f"Error generating threat model. Error: {e}")

#         # Convert the threat model JSON to Markdown
#         markdown_output =  json_to_threat_model_markdown(threat_model_output)

#         # Display the threat model in Markdown
#         st.markdown(markdown_output)

#         st.download_button(
#             label="Download Threat Model",
#             data=markdown_output,  # Use the Markdown output
#             file_name="threat_model.md",
#             mime="text/markdown",
#        )
#         # If the submit button is clicked and the user has not provided an application description
#         if refine_button and not st.session_state.get('app_input'):
#             st.error("Please enter your application details before submitting.")
        
def get_tab(data, selected_model, model_provider):
    # st.markdown("""---""")

    model_temp = st.session_state.get('model_temp')
    input_text = st.text_area(
        label="Add some contextual requirements.",
        placeholder="Add Security Requirements...",
        height=300,
        key="refine_app_desc",
        help="Add some requirements you have written to provide additional context"    )

    # st.session_state['app_input'] = input_text
    refine_requirement_submit_button = st.button(label="Refine Requirements")
    if refine_requirement_submit_button:
        # Check if threat_model data exists
        # tm = st.session_state.get('threat_model', 'NON')
        # print(f"Threat model state - {tm}")
        if 'security_requirements' in st.session_state and st.session_state['security_requirements']:
            with st.spinner("Refining Security Requirements..."):

                try:
                    model_info = {
                        'model_temp': model_temp,
                        'selected_model': selected_model,
                        'model_provider': model_provider
                    }
                    llm_model = get_llm_model(model_info)
                    threat_model = st.session_state.get('threat_model')
                    app_input = st.session_state.get('app_input')
                    gen_security_requirements = st.session_state.get('security_requirements')

                    system_information = f"""
                    ## System Information
                    {app_input}

                    ## Threat Model
                    {threat_model}

                    """
                    refined_requirements = RequirementRefinementCrew().execute(main_model=llm_model, generated_context=system_information, written_context=input_text)
                    st.session_state['refined_requirements'] = refined_requirements

                except Exception as e:
                    st.error(f"Error refining security requirements. Error: {e}")
                    refined_requirements = []

                refined_requirements_markdown = json_to_refined_security_requirement_table(refined_requirements)
                st.markdown(refined_requirements_markdown)
                
            st.download_button(
                label="Download Refined Security Requirements",
                data=refined_requirements_markdown,
                file_name="refined_security_requirements.md",
                mime="text/markdown",
            )
        else:
            st.error("Please generate a security requirement first before requesting Refined Security Requirements.")

def json_to_refined_security_requirement_table(refined_security_requirements_json):
    try:
        security_requirements = json.loads(refined_security_requirements_json)
    except json.JSONDecodeError as e:
        raise (f"JSON decoding error: {e}")

    markdown_output =  "| Reference | Requirement | Source      | Details     | Threat Scenario | Threat Story | Risk Score | Status |\n"
    markdown_output += "|-----------|-------------|-------------|-------------|-----------------|---------------|-----------|-------|\n"
    try:
        requirements = security_requirements.get("requirements", [])
        for index, requirement in enumerate(requirements):
            if isinstance(requirement, dict):
                reference = f"R.{index+1}"
                source=requirement.get('source', '')
                req = requirement.get('requirement', '')
                details = requirement.get('details', '')
                threat_scenario = requirement.get('threat_scenario', '')
                threat_story = requirement.get('threat_story', '')
                risk_score = requirement.get('risk_score', '')
                status = requirement.get('status', '')

                markdown_output += f"| {reference} | {req} | {source} | {details} | {threat_scenario} | {threat_story} | {risk_score} | {status} |\n"
            else:
                raise TypeError(f"Expected a dictionary, got {type(requirement)}")
    except Exception as e:
        raise f"Error: {e}"
    return markdown_output

