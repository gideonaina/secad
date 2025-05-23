import json

import streamlit as st

from knowledge_retrieval.product_security_crew.security_requirement_crew import (
    SecurityRequirementCrew,
)
from ui.utils import get_llm_model


def get_tab(data, selected_model, model_provider):
    st.markdown("""
A security requirement is a specific, measurable, and enforceable condition or guideline that defines how an application, system,
or process must operate to ensure its security.
""")
    st.markdown("""---""")

    model_temp = st.session_state.get('model_temp')
    security_requirement_submit_button = st.button(label="Generate Security Requirement")
    if security_requirement_submit_button:
        # Check if threat_model data exists
        tm = st.session_state.get('threat_model', 'NON')
        print(f"Threat model state - {tm}")
        if 'threat_model' in st.session_state and st.session_state['threat_model']:
            with st.spinner("Generating Security Requirements..."):

                try:
                    model_info = {
                        'model_temp': model_temp,
                        'selected_model': selected_model,
                        'model_provider': model_provider
                    }
                    llm_model = get_llm_model(model_info)
                    threat_model = st.session_state.get('threat_model')
                    app_input = st.session_state.get('app_input')

                    system_information = f"""
                    ## System Information
                    {app_input}

                    ## Threat Model
                    {threat_model}
                    """
                    security_requirements = SecurityRequirementCrew().execute(llm_model, system_information=system_information)
                    st.session_state['security_requirements'] = security_requirements

                except Exception as e:
                    st.error(f"Error generating security requirements. Error: {e}")
                    security_requirements = []

                security_requirements_markdown = json_to_security_requirement_table(security_requirements)
                st.markdown(security_requirements_markdown)
                
            st.download_button(
                label="Download Security Requirements",
                data=security_requirements_markdown,
                file_name="security_requirements.md",
                mime="text/markdown",
            )
        else:
            st.error("Please generate a threat model first before requesting Security Requirements.")

        
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
