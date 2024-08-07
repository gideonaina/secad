import gradio as gr
import os
from knowledge_retrieval.kes_crew import KESCrew
import base64
from dotenv import load_dotenv
load_dotenv()

domain_option = ["General", "Product Security", "Security Testing"]
product_security_task = ["Security Review", "Threat Modeling", "Logging & Auditing Requirement"]
security_testing_task = ["Pentration Testing", "DAST"]
general_task = ["General"]

def process_file_base64(file):
    if file is None:
        return ""
    
    print(f"picture b4 encoding: {file}")
    # Read the file and convert to base64
    with open(file, "rb") as f:
        file_content = f.read()
        encoded_file = base64.b64encode(file_content).decode('utf-8')
    return encoded_file


def update_dropdown(selection):
    if selection == "Product Security":
        return gr.update(choices=product_security_task)
    elif selection == "Security Testing":
        return gr.update(choices=security_testing_task)
    else:
        return gr.update(choices=general_task)

# Define a function to process the final selection
def process_selection(domain, task, user_prompt, file_input):
    picture_base64 = process_file_base64(file_input)
    # print(f"Parameters are: Domain: {domain}")
    # print(f"picture post encoding: {picture_base64}")
    return KESCrew().run(domain=domain, task=task, prompt=user_prompt, base64_encoded_picture=picture_base64)
    # return ""

css = """ 
.small-file-upload input[type="file"] {
    height: 10px;
    padding: 5px;
}
"""

# Create the Gradio interface
with gr.Blocks(theme=gr.themes.Soft(), css=css) as demo:
    gr.Markdown("## KES")
    domain = gr.Dropdown(choices=domain_option, label="Select Domain", value=domain_option[0])
    task = gr.Dropdown(choices=general_task, label="Select Task", value=general_task[0])
    with gr.Row():
        with gr.Column():
            file_input = gr.File(label="Upload your image", elem_classes="small-file-upload")
            # background_info = gr.Textbox(lines=4, placeholder="Enter background information here...", label="Background Information")
            user_prompt = gr.Textbox(lines=15, placeholder="Enter some text here...", label="User Prompt")  # Text input
            submit_button = gr.Button("Submit")
        
        with gr.Column():
            # gr.Markdown("## Upload a File")
            # background_info = gr.Textbox(lines=4, placeholder="Enter background information here...", label="Background Information")
            output = gr.Textbox(label="Output", lines=40)

    # Update the second dropdown based on the first dropdown's value
    domain.change(fn=update_dropdown, inputs=domain, outputs=task)
    
    # Process the final selection
    # submit_button.click(fn=process_selection, inputs=[domain, task, background_info], outputs=output)
    submit_button.click(fn=process_selection, inputs=[domain, task, user_prompt, file_input], outputs=output)


gr.close_all()

# Launch the interface
port=os.getenv("GRADIO_PORT")
demo.launch(server_name="0.0.0.0", server_port=int(port))
