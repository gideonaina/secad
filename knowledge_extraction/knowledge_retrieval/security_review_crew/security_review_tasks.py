from crewai import Task
from textwrap import dedent
from knowledge_retrieval import util
from PIL import Image


class SecurityReviewTasks():

    def architecture_image_analysis_task(self, image_path, agent):
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
            
            <notes>
            {self.__tip_section()}
            </notes>

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

    def anaylsis_task(self, system_description, agent):
        return Task(description=dedent(f"""
            <task>
            Extract information about components, assets, 
            connection and communication protocol from system information.
            </task>
                                    
            <systemInformation>
                {system_description}
            </systemInformation>
                                    
            <description>
            Analyze the software system description or software 
            architectural diagram provided within the 
            systemInformation XML tag. Breakdown its components, 
            extract information that would be useful for threat
            modeling.
            The task will involve gathering the following 
            information:
                - Examine software system description or software architectural diagram.
                - Extract components and description.
                - Identify connection between componenent and the protocol for communication.
                - Get a list of important asset that need to be protected and their detailed description.
                - Based on diagram or description, identify security objectives and provide explanation 
                of each that can be used to generate threat scenarios.
            </description>
            
            <notes>
            {self.__tip_section()}
            </notes>

        """),
            agent=agent,
            expected_output= dedent(
            f"""
            Your final answer must be a detailed report about the system.
            Document your final output as a markdown containing the following sections and heading
            - Data Dictionary: This information is a comprehensive and structured reference that 
            defines and describes all the data elements relevant to the system
            - Conponents: This is information about each component, the components they are connected to and the protocol 
            used for communication or connection between them.
            - Security Objectives: This are objectives and goals for security for this system
            """
            )

        )
  
    def trust_boundary_identification_task(self, system_description, agent):
        return Task(description=dedent(f"""
            <task>
            Extract information about componenets, assets, 
            connection and communication protocol from system information.
            </task>
                                       
            <systemInformation>
                {system_description}
            </systemInformation>
                   
            <description>.
           Read the following from the system information provided as systemInformation xml tag::
            - Read System Information and output from the previous task.
            - Read system information, data dictionary and security objectives.
            - Generate trust zones for each node based on the rules of the trust
            stated in the output format below.
            - Capture the trust zones in a list against each node.
            </description>
            
            <notes>
            {self.__tip_section()}
            </notes>

        """),
            agent=agent,
            expected_output= dedent(
            f"""
            Document your final output as a markdown all in a section with heading
            Trust Boundaries.
            Your final output must be a detailed and formated as a readable markdown.
            It should have the following information in readable markdown format only:
            - Capture components with names
            - Capture the trust zone against each node based on the following rules
                * Mark 0 for output control entities. For example: Users are not in 
                control of the system, they are marked 0
                * Mark 1 for boundary entities. These are components of the system
                accessed throught external communication.
                * Mark 2 and 3 for data pass through entities. These are entities 
                that have data pass through them but do not process any critical data.
                * Mark 4 and 5 for Business rule processing entities. These are 
                components that process data based on some business rules. They 
                are typically non-critical business rules being processed.
                * Mark 6 and 7 for critical business business rule processing entities.
                They are components that are parsing or processing critical or sensitive
                business rukes in the system.
                * Mark 8 or 9 for components where data hits the disk. These are components
                that store information related to the system like databases, object store.
            """
            ))
    
    def threat_scenario_creation_task(self, system_description, agent):
        return Task(description=dedent(f"""
            <task>
                Generate a detailed, realistic and relevant threat scenarios.
            </task>
                                       
            <systemInformation>
                {system_description}
            </systemInformation>

                   
            <description>
           Read the following from both the system information provided as systemInformation xml tag:
            - Read System Information and output from the previous task.
            - Read system information, data dictionary and security objectives.
            - Study the trust zones for each node 
            Make sure to properly understanding the information above before performing the following tasks:
            - Generate realistic threat scenarios.
            </description>
            
            <notes>
            {self.__tip_section()}
            </notes>

        """),
            agent=agent,
            expected_output= dedent(
            f"""
            Document your final output as a markdown all under a section with heading:
            # Threat Scenarios
            - Each scenario must be captured in the following format "<Threat Actor> can
            perform <Attack Vector> to achieve <Attack Outcome>. For each variable in
            the angle bracket, try to identify  the specific Threat Actor, Attack Vector
            and Attack Outcome.
            - The severity of each scenario generated must be classified with as "High",
            "Medium", "Low" using the CVSS scoring metric system.
            """
            ))

    def control_measure_task(self, system_description, agent):
        return Task(description=dedent(f"""
            <task>
                Generate a list of well defined control or countermeasures for each threat scenario.
            </task>
                                       
            <systemInformation>
                {system_description}
            </systemInformation>
                   
            <description>
           Read the following from the system information provided as systemInformation xml 
           tag that contains a list of threat scenarios:
            Make sure to properly understanding the information above before performing the following tasks:
            - For each threat scenarios generate one of more countermeasure.
            - Provide information that will help implement the countermeasure.
            </description>
            
            <notes>
            {self.__tip_section()}
            </notes>

        """),
            agent=agent,
            expected_output= dedent(
            f"""
            Document your final output as a markdown all under a section with heading:
            # Controls
            """
            ))
    
    def __tip_section(self):
        return """
        Do not enclose the output in markdown syntax using ```markdown and ````.
        If you do your BEST WORK, I'll tip you $100!
        """