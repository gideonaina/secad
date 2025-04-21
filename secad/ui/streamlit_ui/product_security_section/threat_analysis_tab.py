import json
import os

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image



from knowledge_retrieval.architecture_review_crew.image_review import ImageReview
from knowledge_retrieval.architecture_review_crew.diagram_review import DiagramReview
from knowledge_retrieval.threat_analysis.threat_analysis_crew import ThreatAnalysisCrew
from ui.utils import get_llm_model, check_file_type

KEY_PREFIX = "threat_analysis"


def get_tab(data, selected_model, model_provider):

    temp_slider = st.session_state.get('model_temp')

    # Initialize app_input in the session state if it doesn't exist
    if 'app_input' not in st.session_state:
        st.session_state['app_input'] = ''
    
    # Only do file analysis for OpenAI models.
    if model_provider and selected_model in data["sidebar"]["open_api"]["connection"]["model_selection"]["options"]:
        uploaded_file = st.file_uploader("Upload architecture diagram", key=f"{KEY_PREFIX}_uploader", type=data["sidebar"]["open_api"]["modal"]["upload_file_types"])
        
        model_info = {
            'model_temp': temp_slider,
            'selected_model': selected_model,
            'model_provider': model_provider
        }
        llm_model = get_llm_model(model_info)

        if uploaded_file is not None:

            # Check if the uploaded file exist and its not the same as the previous one            
            if 'uploaded_file' not in st.session_state or st.session_state.uploaded_file != uploaded_file:
                print(f"$$$${uploaded_file}$$$$ file url {uploaded_file._file_urls}")
                st.session_state.uploaded_file = uploaded_file
                analysis_output = None

                # Check if the uploaded file is a mermaid diagram
                if check_file_type(uploaded_file.name, "mmd"):
                    with st.spinner("Agent analysing architecture diagram..."):
                        try:
                            mermaid_code = uploaded_file.read().decode("utf-8")
                            render_mermaid_diagram(mermaid_code)
                            st.session_state['mermaid_code'] = mermaid_code
                            st.session_state['is_mermaid_diagram'] = True
                            analysis_output = DiagramReview().run(llm_model, mermaid_code)
                        except Exception as e:
                            st.error(f"Does not look like the file has a valid mermaid diagram - {e}")
                
                else:
                    with st.spinner("Agent analysing architecture..."):
                        temp_dir = "/tmp"  # Specify your desired directory
                        os.makedirs(temp_dir, exist_ok=True)
                        file_path = os.path.join(temp_dir, uploaded_file.name)

                        # TODO: use the ulpoaded_file._file_urls to get the file url or use the BytesIO directly.
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        image = Image.open(uploaded_file)
                        st.image(image, caption="Uploaded Image")

                        try:
                            analysis_output = ImageReview().run(llm_model, file_path)
                            mermaid_code = ImageReview().run_mermaid(llm_model, file_path)
                            st.session_state['mermaid_code'] = mermaid_code
                        except Exception as e:
                            st.error("An unexpected error occurred while analyzing the image. Error {e}")

                if analysis_output:
                    st.session_state.analysis_content = analysis_output
                    st.session_state['app_input'] = analysis_output
                else:
                    st.error("Failed to analyze architecture.")

                
                
                    
    # Use the get_input() function to get the application description
    app_input = get_input(key=f"{KEY_PREFIX}_input")

    # Display the mermaid diagram
    if st.session_state.get("analysis_content", None) and not bool (st.session_state.get('is_mermaid_diagram', False)):
        render_mermaid_diagram(st.session_state.get('mermaid_code', ''))


    # Update session state only if the text area content has changed
    if app_input != st.session_state.get(f"{KEY_PREFIX}_input", ''):
        st.session_state[f"{KEY_PREFIX}_input"] = app_input


    # Create a submit button for Threat Modelling
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
                
                threat_analysis_output = ThreatAnalysisCrew().execute(llm_model, system_information=app_input)
                st.session_state[f"{KEY_PREFIX}"] = threat_analysis_output
            except Exception as e:
                st.error(f"Error generating threat model. Error: {e}")

        # Convert the threat model JSON to Markdown
        markdown_output =  json_to_threat_model_markdown(threat_analysis_output)

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
        markdown_output += f"| R.{idx+1} | {threat['threat_type']} | {threat['threat_scenario']} | {threat['impact']} |{threat['control']} |\n"
    
    return markdown_output

def render_mermaid_diagram(mermaid_code):
    # See information on the html conversion her - https://emersonbottero.github.io/mermaid-docs/config/usage.html

    user_code = st.text_area("Mermaid Code", value=mermaid_code, key=f"{KEY_PREFIX}_mermaid_box", height=250)
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
        height: 400px;
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
        """, height=450)
    

def get_input(key=""):
    input_text = st.text_area(
        label="Describe the System Architecture",
        value=st.session_state.get('app_input', ''),
        placeholder="Enter your application details...",
        height=300,
        key=f"{key}_app_desc",
        help="Please provide a detailed description of the application, including the purpose of the application, the technologies used, and any other relevant information.",
    )

    st.session_state['app_input'] = input_text

    return input_text
