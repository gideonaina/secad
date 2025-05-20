from textwrap import dedent

from crewai import Agent, Task


class DiagramReview:

    def system_information_agent(self, vision_llm):
        return Agent(
            role='Software Architect',
            backstory=dedent(""" You are an expert in software architecture
                        with expertise in understanding the details of a software 
                        by looking at the system software architectural diagram.
                        """),
            goal=dedent("""Properly Analyze the software architectural diagram,
                        break it down into its components, connections between 
                        components and communication protocols. This information 
                        will be used as input into a threat modeling task.
                        """),
            verbose=True,
            allow_delegation=False,
            llm = vision_llm
    )

    def architecture_diagram_analysis_task(self, mmd_diagram, agent) -> Task:

        return Task(description=dedent(f"""
            <task>
            Extract information about components, assets, 
            connection and communication protocol from the diagram
            </task>
                                    
                                    
            Provide detailed description of the the architectural diagram
            in this mermaid diagram {mmd_diagram}
            Extract the following information from the task:
            - Detailed system description
            - System Functionality
            - Components and Communication Protocols
            - Data Flow Direction

        """),
            agent=agent,
            expected_output= dedent(
            """
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
    
    def run(self, vision_llm, mmd_diagram):
        diagram_agent = self.system_information_agent(vision_llm)
        diagram_analysis_task = self.architecture_diagram_analysis_task(mmd_diagram, diagram_agent)
        output = diagram_analysis_task.execute_sync()
        return output

    

