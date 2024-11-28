from langchain_community.chat_models import ChatOpenAI
import base64
from crewai import Agent, Task
from textwrap import dedent
from crewai_tools import VisionTool

class ImageReview:
    # def get_architectural_diagram_info(self, image_path):
    #     image_path = 'path_to_your_architectural_diagram.png'

    #     with open(image_path, 'rb') as image_file:
    #         image_data = image_file.read()

    #     # Send the image to GPT-4-V for analysis and description
    #     response = openai.ChatCompletion.create(
    #         model="gpt-4",  # or "gpt-4-vision" if a specific endpoint exists
    #         messages=[
    #             {"role": "system", "content": "You are an expert in software architecture."},
    #             {"role": "user", "content": "Please describe the content of this software architectural diagram."}
    #         ],
    #         files=[
    #             {"name": "architectural_diagram.png", "content": image_data}
    #         ]
    #     )

    def get_architectural_diagram_description(model: ChatOpenAI, image ):
        # Step 1: Set up your OpenAI API key
 

        # Step 2: Define the prompt template
        # prompt_template = """
        # You are an expert in software architecture. 
        # Please describe the content of the following software architectural diagram: {image_description}.
        # """

        # # Step 3: Create a LangChain prompt
        # prompt = PromptTemplate(input_variables=["image_description"], template=prompt_template)

        # # Step 4: Initialize the ChatOpenAI model
        # llm = ChatOpenAI(model_name="gpt-4")  # Specify the model as gpt-3.5-turbo or gpt-4

        # # Step 5: Create an LLMChain
        # chain = LLMChain(llm=llm, prompt=prompt)

        # # Step 6: Process the image (use OCR or image captioning to get the description)
        # # This part is a placeholder; use OCR/image captioning library as needed
        # image_description = "Extracted description of the architectural diagram"

        # # Step 7: Run the chain with the image description
        # result = chain.run({"image_description": image_description})

        # # Step 8: Output the result
        # print(result)
        pass

    def encode_image(uploaded_file):
        return base64.b64encode(uploaded_file.read()).decode('utf-8')

    def system_information_agent(self, vision_llm):
        # prompt_template = """
        #                 You are an expert in software architecture
        #                 with expertise in understanding the details of a software 
        #                 by looking at the system software architectural diagram. {image_description}.
        # """
        # prompt = PromptTemplate(input_variables=["image_description"], template=prompt_template)
        return Agent(
            role='Software Architect',
            backstory=dedent(f""" You are an expert in software architecture
                        with expertise in understanding the details of a software 
                        by looking at the system software architectural diagram.
                        """),
            goal=dedent(f"""Properly Analyze the software architectural diagram,
                        break it down into its components, connections between 
                        components and communication protocols. This information 
                        will be used as input into a threat modeling task.
                        """),
            verbose=True,
            # allow_delegation=True,
            tools=[VisionTool()],
            llm = vision_llm
    )

    def architecture_image_analysis_task(self, image_path, agent) -> Task:
        # image_content = util.read_file(image_path)
        # image_content = Image.open(image_path)

        return Task(description=dedent(f"""
            <task>
            Extract information about components, assets, 
            connection and communication protocol from the diagram
            </task>
                                    
                                    
            Provide detailed description of the the architectural diagram
            in this image {image_path}
            Extract the following information from the task:
            - Detailed system description
            - System Functionality
            - Components and Communication Protocols
            - Data Flow Direction

        """),
            agent=agent,
            expected_output= dedent(
            f"""
            Your final answer must be a detailed report about the system.
            Document your final output as a markdown containing the following sections and heading
            - Detailed system description and it general function. The heading of this section 
            should be `System Description`
            - A list of all the components in the diagram. Each listed component should have 
            the following details under it: The function of the component, the technology 
            (for example data base, object store, User interface, API), and the list of other components
            it connects to or that connnects to it. The heading of this section 
            should be `System Components`
            - For each link or connection in the diagram, provide the following details about the pair of connected
            components: If there is source and destination, denote it with an arrow, -> otherwise
            denote it with a hypen -, the communication protocols between both component and the type 
            of data, asset or information that flows through that connection. The heading of this section 
            should be `Assets and Data Flow`
            """
            )
        )
    
    def run(self, vision_llm, image_path):
        image_agent = self.system_information_agent(vision_llm)
        image_analysis_task = self.architecture_image_analysis_task(image_path, image_agent)
        output = image_analysis_task.execute_sync()
        return output
    

