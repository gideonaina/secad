from textwrap import dedent

from crewai import Task



class DiagramAnalysisTasks:

    def image_architecture_diagram_analysis_task(self, image_path, agent) -> Task:
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
    

    def mermaid_architecture_diagram_analysis_task(self, mmd_diagram, agent) -> Task:

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
    

    def architecture_image_analysis_as_mermaid_task(self, image_path, agent) -> Task:

        return Task(description=dedent(f"""
            <task>
                Draw a mermaid diagram representation of the architecture.
            </task>
                                           
            Redraw as mermaid diagram the architectural diagram in this image {image_path}.
            The mermaid diagram should be a proper representation of the system architecture.
            Make sure to include all the components and connections in the diagram.

        """),
            agent=agent,
            expected_output= dedent(
            """
            Your final answer must and ONLY a valid mermaid code without any other text.
            Don't include any other text or explanation. DO NOT include
            "```mermaid" or "```" or any other text. Just include the mermaid code starting "graph TD"
            An example of a valid format is below (without the "):
            "
                graph TD
                A[Component A] -->|Protocol| B[Component B]
                A --> C[Component C]
                B --> D[Component D]
            "
            Make sure to use the correct syntax for mermaid diagrams.
            """
            )
        )
    
    
    def mermaid_diagram_validation_task(self, mermaid_graph, agent) -> Task:

        return Task(description=dedent(f"""
            <task>
                Check the following mermaid diagram and validate that will render without errors.
            </task>
                                           
            - Validate the following mermaid diagram {mermaid_graph}.
            - Check if it will render without errors.
            - ONLY correct any errors in the diagram (if any) and provide a valid mermaid diagram.

        """),
            agent=agent,
            expected_output= dedent(
            """
            Your final answer must and ONLY a valid mermaid code without any other text.
            Don't include any other text or explanation. DO NOT include
            "```mermaid" or "```" or any other text. Just include the mermaid code starting "graph TD"
            An example of a valid format is below (without the "):
            "
                graph TD
                A[Component A] -->|Protocol| B[Component B]
                A --> C[Component C]
                B --> D[Component D]
            "
            Make sure to use the correct syntax for mermaid diagrams.
            """
            )
        )
    
    

    

