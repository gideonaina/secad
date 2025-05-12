import json
import os

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image


from knowledge_retrieval.diagram_analysis.diagram_analysis_crew import DiagramAnalysisCrew
from knowledge_retrieval.threat_analysis.threat_analysis_crew import ThreatAnalysisCrew
from knowledge_retrieval.models import ThreatAnalysisContext
from ui.utils import get_llm_model, check_file_type

KEY_PREFIX = "threat_analysis"


def get_tab(data, selected_model, model_provider):

    temp_slider = st.session_state.get('model_temp')

    # Initialize app_input in the session state if it doesn't exist
    if 'app_input' not in st.session_state:
        st.session_state['app_input'] = ''
    
    # Only do file analysis for OpenAI models.
    if model_provider and selected_model in data["sidebar"]["open_api"]["connection"]["model_selection"]["options"]:
        uploaded_file = st.file_uploader("Upload architecture diagram", key=f"{KEY_PREFIX}_uploader", type=data["sidebar"]["open_api"]["modal"]["upload_file_types"], help="Upload an image or a file containing mermaid diagram and saved as a .mmd")
        
        model_info = {
            'model_temp': temp_slider,
            'selected_model': selected_model,
            'model_provider': model_provider
        }
        llm_model = get_llm_model(model_info)

        if uploaded_file is not None:
            image_placeholder = st.empty()

            # Check if the uploaded file exist and its not the same as the previous one            
            if 'uploaded_file' not in st.session_state or st.session_state.uploaded_file != uploaded_file:
                # print(f"$$$${uploaded_file}$$$$ file url {uploaded_file._file_urls[2]}")
                st.session_state.uploaded_file = uploaded_file
                # analysis_output = None

                # # Check if the uploaded file is a mermaid diagram
                # if check_file_type(uploaded_file.name, "mmd"):
                #     with st.spinner("Agent analysing architecture diagram..."):
                #         try:
                #             mermaid_code = uploaded_file.read().decode("utf-8")
                #             render_mermaid_diagram(mermaid_code)
                #             st.session_state['mermaid_code'] = mermaid_code
                #             st.session_state['is_mermaid_diagram'] = True
                #             analysis_output = DiagramReview().run(llm_model, mermaid_code)
                #             st.session_state['analysis_output'] = analysis_output
                #         except Exception as e:
                #             st.error(f"Does not look like the file has a valid mermaid diagram - {e}")
                
                # else:
                #     with st.spinner("Agent analysing architecture..."):
                #         temp_dir = "/tmp"  # Specify your desired directory
                #         os.makedirs(temp_dir, exist_ok=True)
                #         file_path = os.path.join(temp_dir, uploaded_file.name)

                #         # TODO: use the uploaded_file._file_urls to get the file url or use the BytesIO directly.
                #         with open(file_path, "wb") as f:
                #             f.write(uploaded_file.getbuffer())
                        
                #         image = Image.open(uploaded_file)
                #         image_placeholder.image(image, caption="Uploaded Image")

                #         try:
                #             analysis_output = ImageReview().run(llm_model, file_path)
                #             st.session_state['analysis_output'] = analysis_output
                #             mermaid_code = ImageReview().run_mermaid(llm_model, file_path)
                #             st.session_state['mermaid_code'] = mermaid_code
                #             if not analysis_output:
                #                 st.error("Failed to analyze architecture.")
                #         except Exception as e:
                #             st.error("An unexpected error occurred while analyzing the image. Error {e}")

                if check_file_type(uploaded_file.name, "mmd"):
                    mermaid_code = uploaded_file.read().decode("utf-8")
                    render_mermaid_diagram(mermaid_code)
                    st.session_state['mermaid_code'] = mermaid_code
                    st.session_state['is_mermaid_diagram'] = True

                    try:
                        with st.spinner("Agent analysing architecture..."):
                            arch_analysis_output = DiagramAnalysisCrew().run_mermaid(llm_model, mermaid_code)
                            st.session_state['arch_analysis_output'] = arch_analysis_output
                    except Exception as e:
                        print(f"Mermaid analysis error: {e}")
                        st.error(f"An unexpected error occurred while analyzing the mermaid diagram. Error {e}")

                else:
                    temp_dir = st.session_state["TMP_FILE_PATH"] 
                    # os.makedirs(temp_dir, exist_ok=True)
                    file_path = os.path.join(temp_dir, uploaded_file.name)
                    
                    # TODO: use the uploaded_file._file_urls to get the file url or use the BytesIO directly.
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    image = Image.open(uploaded_file)
                    image_placeholder.image(image, caption="Uploaded Image")

                    try:
                        with st.spinner("Agent analysing architecture..."):
                            arch_analysis_output = DiagramAnalysisCrew().run_image(llm_model, file_path)
                            st.session_state['arch_analysis_output'] = arch_analysis_output
                    except Exception as e:
                        print(f"Image analysis error: {e}")
                        st.error(f"An unexpected error occurred while analyzing the image. Error {e}")

                
                if st.session_state.get('arch_analysis_output', None):
                    st.session_state['analysis_output'] = arch_analysis_output.system_information
                    st.session_state['mermaid_code'] = arch_analysis_output.mermaid_diagram

                    # # Check if the analysis output is a mermaid diagram
                    # if check_file_type(uploaded_file.name, "mmd"):
                    #     st.session_state['is_mermaid_diagram'] = True
                    #     render_mermaid_diagram(st.session_state.get('mermaid_code', ''))
                    # else:
                    #     image = Image.open(uploaded_file)
                    #     image_placeholder.image(image, caption="Uploaded Image")
            

            uploaded_file = st.session_state.get("uploaded_file", None)
            if check_file_type(uploaded_file.name, "mmd"):
                mermaid_code = st.session_state['mermaid_code']
                render_mermaid_diagram(mermaid_code)

            else:
                image = Image.open(st.session_state.get('uploaded_file'))
                image_placeholder.image(image, caption="Uploaded Image")
                mermaid_code = st.session_state['mermaid_code']
                render_mermaid_diagram(mermaid_code)

            if st.session_state.get('analysis_output', None):
                st.session_state['app_input'] = st.session_state.get('analysis_output')

                    
    # Use the get_input() function to get the application description
    # app_input = get_input(key=f"{KEY_PREFIX}_input")

    input_text = st.text_area(
        label="Describe the System Architecture",
        value=st.session_state.get('app_input', ''),
        placeholder="Enter your application details...",
        height=300,
        key=f"{KEY_PREFIX}_input",
        help="Please provide a detailed description of the application, including the purpose of the application, the technologies used, and any other relevant information.",
    )


    # Create a submit button for Threat Modeling
    threat_analysis_button = st.button(label="Analyze Threat", key=f"{KEY_PREFIX}_button")

    # If the Generate Threat Model button is clicked and the user has provided an application description
    if threat_analysis_button and st.session_state.get(f"{KEY_PREFIX}_input"):
        app_input = st.session_state[f"{KEY_PREFIX}_input"]  # Retrieve from session state
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

                context_info = ThreatAnalysisContext(
                    system_information=app_input, # st.session_state.get('analysis_output', None),
                    mermaid_diagram=st.session_state.get('mermaid_code', None)
                )
                
                if app_input and st.session_state.get('mermaid_code', None):
                    threat_analysis_output = ThreatAnalysisCrew().execute(llm_model, context_info)
                    st.session_state[f"{KEY_PREFIX}"] = threat_analysis_output
                else:
                    st.error("Please upload arch diagram to extract a valid application description and architecture diagram.")
            except Exception as e:
                print(f"Threat analysis error: {e}")
                st.error(f"Error generating threat model. Error: {e}")
    
    if st.session_state.get(f"{KEY_PREFIX}", None):
        # Convert the threat model JSON to Markdown
        # TODO: Convert this to use JsonParser from Pydantic or Langchain
        markdown_output =  json_to_threat_model_markdown(st.session_state.get(f"{KEY_PREFIX}"))

        # Display the threat model in Markdown
        st.markdown(markdown_output)

        st.download_button(
            label="Download Threat Model",
            data=markdown_output,  # Use the Markdown output
            file_name="threat_model.md",
            mime="text/markdown",
            key=f"{KEY_PREFIX}_download_button",
       )
        # If the submit button is clicked and the user has not provided an application description
        if threat_analysis_button and not st.session_state.get('app_input'):
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
        markdown_output += f"| TS.{idx+1} | {threat['threat_type']} | {threat['threat_scenario']} | {threat['impact']} |{threat['control']} |\n"
    
    return markdown_output

def render_mermaid_diagram(mermaid_code):
    # See information on the html conversion her - https://emersonbottero.github.io/mermaid-docs/config/usage.html

    user_code = st.text_area("Mermaid Code", value=mermaid_code, key=f"{KEY_PREFIX}_mermaid_box", height=300, )
    components.html(f"""
        <html>
        <head>
        <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true }});
        </script>
        <style>
      .scroll-container {{
        width: 100%;
        height: 100%;
        overflow: auto;
        border: 1px solid #ccc;
        padding: 10px;
        box-sizing: border-box;
        }}
    </style>
        </head>
        <body>
        <div class="scroll-container">
        <div class="mermaid">{user_code}</div>
        </div>
        </body>
        </html>
        """, scrolling=True, height=500)

# def get_input(key=""):
#     input_text = st.text_area(
#         label="Describe the System Architecture",
#         value=st.session_state.get('app_input', ''),
#         placeholder="Enter your application details...",
#         height=300,
#         key=f"{key}_app_desc",
#         help="Please provide a detailed description of the application, including the purpose of the application, the technologies used, and any other relevant information.",
#     )

#     st.session_state['app_input'] = input_text

#     return input_text
