from textwrap import dedent

from crewai import Task

from knowledge_retrieval.models import ThreatAnalysisContext

TRUST_ZONE_RULES = dedent(
            """
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
            """)


class ThreatAnalysisTasks:

    def trust_boundary_identification_task(self, context_info: ThreatAnalysisContext, agent):
        system_description = context_info.system_information
        system_diagram =  context_info.mermaid_diagram
        return Task(description=dedent(f"""
            <task>
            Extract information about components, assets, 
            connection and communication protocol from this system information {system_description}
            and this mermaid diagram representation of its architecture {system_diagram}.
            </task>
                                           
            <description>.
            From the sytem information and diagram provided deduce the following information:
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
                {TRUST_ZONE_RULES}
            - Append the following trust zone rules to the end of the output
                {TRUST_ZONE_RULES}
            """
            ))
    
    def threat_scenario_creation_task(self, context_info: ThreatAnalysisContext, agent):
        system_description = context_info.system_information
        system_diagram =  context_info.mermaid_diagram
        trust_zone_analysis = context_info.trust_zone_analysis

        return Task(description=dedent(f"""
            <task>
                Generate detailed, realistic and relevant threat scenarios from the 
                following context information about the system:
                - System Information: {system_description}
                - Mermaid Representation of the System Diagram: {system_diagram}
                - Trust Zones: {trust_zone_analysis}
            </task>

                   
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

    def control_measure_task(self, context_info: ThreatAnalysisContext, agent):
        system_description = context_info.system_information
        system_diagram =  context_info.mermaid_diagram
        trust_zone_analysis = context_info.trust_zone_analysis
        threat_scenarios = context_info.threat_scenario

        return Task(description=dedent(f"""
            <task>
                Generate a list of well defined control or countermeasures from threat scenarios 
            </task>
                                       
                   
            <description>
                - Review the following information about the system:
                {system_description}
                
                - Review the following mermaid diagram representation of the system architecture:
                {system_diagram}

                - Review the following trust zones for each node:
                {trust_zone_analysis}

                - Review the following threat scenarios:
                {threat_scenarios}

                - Review the following organization controls and policies and incorporate the relevant ones into the countermeasures:
                {context_info.rag_context}

                - Using all the preceeding information, generate one or more countermeasure that can be implemented to mitigate the threat.
                  Annotate the control with a reference of Policy, Standard or framework that the requirement suggestion is coming from. 
                  For example PCI Requirement 5, NIST 800-53, OWASP etc.

                - The countermeasure should be well defined and should be able to mitigate the threat scenario.
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
    
    def __tip_section(self):
        return """
        Do not enclose the output in markdown syntax using ```markdown and ````.
        If you do your BEST WORK, I'll tip you $100!
        """
