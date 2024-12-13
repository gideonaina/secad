from textwrap import dedent

from crewai import Task


class ProductSecurityTask:

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
            """
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
            """
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
                business rules in the system.
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
            """
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
            Make sure to properly understanding the information above before providing the 
            following information for each threat scenario:
            - Threat Type: Generate the threat type.
            - Threat Scenario: detailed infromation about the threat scenario.
            - Control: Generate one or more countermeasure that can be implemented to mitigate the threat. Annotate the control with a reference of Policy, Standard or framework that the requirement suggestion is coming from. For example PCI Requirement 5 or NIST 800-53.
            - Potential Imapct: Provide information about potential impact of the threat scenario on the system.
            </description>
            
            <notes>
            {self.__tip_section()}
            </notes>
        """),
            agent=agent,
            # expected_output= dedent(
            # f"""
            # Document your final output as a markdown all under a section with heading:
            # # Controls
            # """
            # )
            expected_output= dedent(
            """
            Output this information as JSON. Ensure the JSON response is correctly formatted and does not 
            contain any additional text. Here is an example of the expected JSON response format:
                {
                    "threat_model": [
                        {
                        "threat_type": "Spoofing",
                        "threat_scenario": "Example Scenario 1",
                        "control": "control 1"
                        "impact": "Example Potential Impact 1"
                        },
                        {
                        "threat_type": "Tampering and Man-in-the-middle (MIM) attack.",
                        "threat_scenario": "Example Scenario 2",
                        "control": "control 2"
                        "impact": "Example Potential Impact 2"
                        }
                    ]
                }
            """
            ))
    
    def requirement_generation_task(self, system_description, agent):
        return Task(description=dedent(f"""
            <task>
                Given the context below: generate a list of well defined security requirement that needs to be met by the
                application to mitigate each threat scenario.
            </task>
                                       
            <context>
                {system_description}
            </context>
                   
            <description>
            The output should contain the following information:
            **Requirement**: This the security requirement for the threat scenario. 
            It should follow the following rules:
            * Requirements must have a coherent and extract 
            structure that includes at least:   
            * The entity in question must be clearly defined and prescribed. 
            Examples include but are not limited to 'the system', 'the user',
            'the administrator', 'the database', etc.
            * The mandate level of requirement based on RFC 2119. Examples 'MUST',
            'SHOULD', 'MAY' etc.
            * The action / expectation from the entity.
            * The system reference must be generic and not a specific vendor technology.
            * The requirements must be written in the following manner: The 
            Entity -> The Requirement Mandate Level -> The Requirement.
            * Annotate the requirement with a reference of Policy, Standard or framework that the requirement suggestion is coming from. For example OWASP top 10, PCI DSS Section 5.
            * An examples of well written requirement are:
            - The system MUST encrypt all data in transit to prevent sniffing and spoofing attacks.
            - The platform MUST block all executable files uploaded to it.
            
            **Details**: This should containe extra information that will provide context and 
            understanding for the requirement. For example, if a requirement requires all
            system to encrypt data in transit using TLS. The details will be: 
            'Encrypting data in transit ensures that the data remains protected from exposure during transmission'
            **Threat Scenario**: This the threat scenario for that the requirement is looking to mitigate.
            **Risk Score**: The is a Common Vulnerability Scoring System (CVSS) risk score for the threat
            based on your knowledge of the system.
            
            Output this information as JSON. Ensure the JSON response is correctly formatted and does not 
            contain any additional text. Here is an example of the expected JSON response format:
            {{
            "requirements": [
                {{
                "requirement": "The system MUST encrypt all data in transit to prevent sniffing and spoofing attacks",
                "details": "Encrypting data in transit ensures that the data remains protected from exposure during transmission.",
                "threat_scenario": "An attacker intercepts the communication between the client (e.g., an application or user) and the server by positioning themselves as a proxy (man-in-the-middle)",
                "risk_score": 6
                }},
                {{
                "requirement": "The platform MUST block all executable files uploaded to it.",
                "details": "Blocking executable file on the platform prevents remote code execution attack.",
                "threat_scenario": "An attacker uploads a malicious executable file disguised as a legitimate document or compressed archive to the platform. Due to insufficient validation, the platform accepts the file, allowing it to be stored or processed. Later, the malicious executable is either executed on the platform's servers or downloaded by unsuspecting users, potentially leading to system compromise or malware propagation.",
                "risk_score": 8
                }}
            ]
            }}
            </description>
            
            <notes>
            {self.__tip_section()}
            </notes>
        """),
            agent=agent,
            expected_output= dedent(
            """
            Output this information as JSON. Ensure the JSON response is correctly formatted and does not 
            contain any additional text. Here is an example of the expected JSON response format:
            {
            "requirements": [
                {
                "requirement": "The system MUST encrypt all data in transit to prevent sniffing and spoofing attacks",
                "details": "Encrypting data in transit ensures that the data remains protected from exposure during transmission.",
                "threat_scenario": "An attacker intercepts the communication between the client (e.g., an application or user) and the server by positioning themselves as a proxy (man-in-the-middle)",
                "risk_score": 6
                },
                {
                "requirement": "The platform MUST block all executable files uploaded to it.",
                "details": "Blocking executable file on the platform prevents remote code execution attack.",
                "threat_scenario": "An attacker uploads a malicious executable file disguised as a legitimate document or compressed archive to the platform. Due to insufficient validation, the platform accepts the file, allowing it to be stored or processed. Later, the malicious executable is either executed on the platform's servers or downloaded by unsuspecting users, potentially leading to system compromise or malware propagation.",
                "risk_score": 8
                }
            ]
            }
            """
            ))
    
    def requirement_refinement_task(self, written_requirement, generated_context, agent):
        return Task(description=dedent(f"""
            # Task Instruction
            Given the contextual information below, enrich these security requirements {written_requirement}. 

            ## Context
            {generated_context}
                   
            # Task Output
            The rewrriten output should contain the following information:
            **Requirement**: Rewrite the requirement to follow the following rules:
            * Requirements must have a coherent and extract 
            structure that includes at least:   
            * The entity in question must be clearly defined and prescribed. 
            Examples include but are not limited to 'the system', 'the user',
            'the administrator', 'the database', etc.
            * The mandate level of requirement based on RFC 2119. Examples 'MUST',
            'SHOULD', 'MAY' etc.
            * The action / expectation from the entity.
            * The system reference must be generic and not a specific vendor technology.
            * The requirements must be written in the following manner: The 
            Entity -> The Requirement Mandate Level -> The Requirement.
            * An examples of well written requirement are:
            - The system MUST encrypt all data in transit to prevent sniffing and spoofing attacks.
            - The platform MUST block all executable files uploaded to it.

            **Source**: Find a source for the requirement. The source is a reference to Policy, Standard or 
            Framework that the requirement suggestion came from. For example OWASP top 10, 
            PCI DSS Requirement 5, NIST 800-53.

            **Details**: This should contain extra information that will provide context and 
            understanding for the requirement. For example, if a requirement requires all
            system to encrypt data in transit using TLS. The details will be: 
            'Encrypting data in transit ensures that the data remains protected from exposure during transmission'
            **Threat Scenario**: This the threat scenario that the requirement is looking to mitigate.
            **Threat Story**: "This is narrative scenario that describes a potential cyber attack, outlining 
            the attacker's methods, the vulnerabilities they might exploit, and the potential consequences 
            for a victim organization."
            **Risk Score**: The is a Common Vulnerability Scoring System (CVSS) risk score for the threat
            based on your knowledge of the system.

            
            Output this information as JSON. Ensure the JSON response is correctly formatted and does not 
            contain any additional text. Here is an example of the expected JSON response format:
            {{
            "requirements": [
                {{
                "requirement": "The system MUST encrypt all data in transit to prevent sniffing and spoofing attacks",
                "source": "PCI DSS 4.0 Requirement 4",
                "details": "Encrypting data in transit ensures that the data remains protected from exposure during transmission.",
                "threat_scenario": "An attacker intercepts the communication between the client (e.g., an application or user) and the server by positioning themselves as a proxy (man-in-the-middle)",
                "threat_story": "As an attacker, I would like to leverage man-in-the-middle attacked to steal data transmitted between two parties or systems",
                "risk_score": 6
                }},
                {{
                "requirement": "The platform MUST block all executable files uploaded to it.",
                "source": "NIST 800-53",
                "details": "Blocking executable file on the platform prevents remote code execution attack.",
                "threat_scenario": "An attacker uploads a malicious executable file disguised as a legitimate document or compressed archive to the platform. Due to insufficient validation, the platform accepts the file, allowing it to be stored or processed. Later, the malicious executable is either executed on the platform's servers or downloaded by unsuspecting users, potentially leading to system compromise or malware propagation.",
                "threat_story": "As malicious outsider, I would like to to trick my victim into executing code containing malicious code.",
                "risk_score": 8
                }}
            ]
            }}
            
            <notes>
            {self.__tip_section()}
            </notes>
        """),
            agent=agent,
            expected_output= dedent(
            """
            Output this information as JSON. Ensure the JSON response is correctly formatted and does not 
            contain any additional text. Here is an example of the expected JSON response format:
            {
            "requirements": [
                {
                "requirement": "The system MUST encrypt all data in transit to prevent sniffing and spoofing attacks",
                "source": "PCI DSS 4.0 Requirement 4",
                "details": "Encrypting data in transit ensures that the data remains protected from exposure during transmission.",
                "threat_scenario": "An attacker intercepts the communication between the client (e.g., an application or user) and the server by positioning themselves as a proxy (man-in-the-middle)",
                "threat_story": "As an attacker, I would like to leverage man-in-the-middle attacked to steal data transmitted between two parties or systems",
                "risk_score": 6
                },
                {
                "requirement": "The platform MUST block all executable files uploaded to it.",
                "source": "NIST 800-53",
                "details": "Blocking executable file on the platform prevents remote code execution attack.",
                "threat_scenario": "An attacker uploads a malicious executable file disguised as a legitimate document or compressed archive to the platform. Due to insufficient validation, the platform accepts the file, allowing it to be stored or processed. Later, the malicious executable is either executed on the platform's servers or downloaded by unsuspecting users, potentially leading to system compromise or malware propagation.",
                "threat_story": "As malicious outsider, I would like to to trick my victim into executing code containing malicious code.",                
                "risk_score": 8
                }
            ]
            }
            """
            ))
    
    def __tip_section(self):
        return """
        Do not enclose the output in markdown syntax using ```markdown and ````.
        If you do your BEST WORK, I'll tip you $100!
        """
