import os

import gradio as gr
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from knowledge_retrieval.main_crew import MainCrew
from ui.utils import convert_markdown

load_dotenv()

domain_option = ["General", "Product Security", "Security Testing"]
product_security_task = ["Security Requirements", "Threat Modeling"]
security_testing_task = ["Pentration Testing", "DAST"]
general_task = ["General"]


def update_dropdown(selection):
    if selection == "Product Security":
        return gr.update(choices=product_security_task)
    elif selection == "Security Testing":
        return gr.update(choices=security_testing_task)
    else:
        return gr.update(choices=general_task)

# Define a function to process the final selection
def process_selection(task, user_prompt, file_input, temp_slider):
    # model_info = {
    #     "model_provider": "OPENAPI",
    #     "model_name": os.getenv('OPENAI_MODEL_NAME'),
    #     "base_url": os.getenv('OPENAI_API_BASE'),
    #     "model_temp": temp_slider
    # }

    main_model = ChatOpenAI(
        model=os.getenv('OPENAI_MODEL_NAME'),
        base_url=os.getenv('OPENAI_API_BASE'),
        temperature=temp_slider
    )

    vision_model = ChatOpenAI(
        model=os.getenv('OPENAI_VISION_MODEL'),
        base_url=os.getenv('OPENAI_API_BASE'),
        temperature=temp_slider
    )
    
    return MainCrew().run(main_model=main_model, vision_model=vision_model, task=task, prompt=user_prompt, image_path=file_input)

css = """ 
    .small-file-upload input[type="file"] {
        height: 10px;
        padding: 5px;
    }
    .custom-button {
        background-color: #c1c7fc !important; 
        color: #696af4 !important;
    }
    .custom-button:hover {
        background-color: #e4ecfc !important;
    }
"""

# Create the Gradio interface
with gr.Blocks(theme=gr.themes.Soft(), css=css) as demo:
    gr.Markdown("## SECAD")
    temp_slider = gr.Slider(
            0, 1,
            value=0.05,
            step=0.01,
            interactive=True,
            label="Model Temperature",
        )
    domain = gr.Dropdown(choices=domain_option, label="Select Domain", value=domain_option[0])
    task = gr.Dropdown(choices=general_task, label="Select Task", value=general_task[0])
    with gr.Row():
        with gr.Column():
            file_input = gr.File(label="Upload your image", visible=True)
            # background_info = gr.Textbox(lines=4, placeholder="Enter background information here...", label="Background Information")
            user_prompt = gr.Textbox(lines=15, placeholder="Enter some text here...", label="User Prompt")  # Text input
            submit_button = gr.Button("Submit", elem_classes="custom-button")
        
        with gr.Column():
            # gr.Markdown("## Upload a File")
            # background_info = gr.Textbox(lines=4, placeholder="Enter background information here...", label="Background Information")
            pdf = gr.Textbox(value="pdf", visible=False)
            docx = gr.Textbox(value="docx", visible=False)
            # output = gr.Textbox(label="Output", lines=17)
            output = gr.Markdown(label="Output")
            export_doc_button = gr.Button("Export as .docx", elem_classes="custom-button")
            export_pdf_button = gr.Button("Export as .pdf", elem_classes="custom-button")

            download_output = gr.File(label="Download", visible=False)


    # Update the second dropdown based on the first dropdown's value
    domain.change(fn=update_dropdown, inputs=domain, outputs=task)
    
    # Process the final selection
    # submit_button.click(fn=process_selection, inputs=[domain, task, background_info], outputs=output)
    # print (f"file: {file_input}, prompt: {user_prompt}")
    if (file_input or user_prompt):
        submit_button.click(fn=process_selection, inputs=[task, user_prompt, file_input, temp_slider], outputs=output)

    # if (output):
    export_doc_button.click(fn=convert_markdown, inputs=[output], outputs=download_output)

    # if (output):
    export_pdf_button.click(fn=convert_markdown, inputs=[output], outputs=download_output )


gr.close_all()

# Launch the interface
port=os.getenv("GRADIO_PORT")
demo.launch(server_name="0.0.0.0", server_port=int(port))
