import os
import json
import streamlit as st
from langchain_openai import ChatOpenAI
from ui.utils import get_input
from knowledge_retrieval.utils import get_llm_model
from knowledge_retrieval.image_review_crew.image_review import ImageReview
from knowledge_retrieval.product_security_crew.threat_model_crew import ThreatModelCrew

def get_tab(data, selected_model, model_provider):
    # st.markdown("Upload an architctural diagram to get")
    # st.markdown("""---""")
    
    # Two column layout for the main app content
    # col1, col2 = st.columns([1, 1])

    temp_slider = st.session_state.get('model_temp')


    # Initialize app_input in the session state if it doesn't exist
    if 'app_input' not in st.session_state:
        st.session_state['app_input'] = ''
    

    # If model provider is OpenAI API and the model is gpt-4-turbo or gpt-4o
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
                with st.spinner("Analysing image..."):
                    # def encode_image(uploaded_file):
                    #     return base64.b64encode(uploaded_file.read()).decode('utf-8')

                    # base64_image = encode_image(uploaded_file)
                    temp_dir = "/tmp"  # Specify your desired directory
                    os.makedirs(temp_dir, exist_ok=True)
                    file_path = os.path.join(temp_dir, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    try:
                        image_analysis_output = ImageReview().run(llm_model, file_path)
                        if image_analysis_output:
                            # image_analysis_content = image_analysis_output['choices'][0]['message']['content']
                            st.session_state.image_analysis_content = image_analysis_output
                            # Update app_input session state
                            st.session_state['app_input'] = image_analysis_output
                        else:
                            st.error("Failed to analyze the image.")
                    except Exception as e:
                        st.error("An unexpected error occurred while analyzing the image.")
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

        # get_model_provider(model_provider)
        # ThreatModelingCrew.run_v2(image_path=uploaded_file, model_temp=model_temp, system_information=app_input)
        

        # Show a spinner while generating the threat model
        with st.spinner("Analysing potential threats..."):
            max_retries = 1
            retry_count = 0

            while retry_count < max_retries:
                try:
                    model_info = {
                        'model_temp': model_temp,
                        'selected_model': selected_model,
                        'model_provider': model_provider
                    }
                    print("**************** BEFORE MODEL RUN IN SPINNER LOOP")
                    llm_model = get_llm_model(model_info)
                    
                    #  def run_v2(self, system_information, image_path, model_info):
                    threat_model_output = ThreatModelCrew().execute(llm_model, system_information=app_input)
                    st.session_state['threat_model'] = threat_model_output
                    break  # Exit the loop if successful
                except Exception as e:
                    retry_count += 1
                    if retry_count == max_retries:
                        st.error(f"Error generating threat model after {max_retries} attempts: {e}")
                        threat_model_output = []
                    else:
                        st.warning(f"Error generating threat model. Retrying attempt {retry_count+1}/{max_retries}...")

        # Convert the threat model JSON to Markdown
        markdown_output =  json_to_threat_model_markdown(threat_model_output)

        # Display the threat model in Markdown
        st.markdown(markdown_output)

        # Add a button to allow the user to download the output as a Markdown file
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
    print (f"*********THREAT MODEL {threat_model}")

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
